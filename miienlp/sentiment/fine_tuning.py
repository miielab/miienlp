# model imports
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification, pipeline
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import AdamW, get_linear_schedule_with_warmup
import torch.nn.functional as F

# other imports
import os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import pickle
from sklearn.metrics import accuracy_score, roc_curve, auc
import pickle5 as pickle5
from utils import *

class Preprocess(object):
    """
    Tokenizes the data and encodes sequences using the BERT tokenizer
    """
    def __init__(self, tokenizer_name, data, labels):
        self.tokenizer_name = tokenizer_name
        self.data = data
        self.labels = labels

    def initialize_tokenizer(self):
        """
        Initializes BERT tokenizer
        """
        return AutoTokenizer.from_pretrained(self.tokenizer_name)

    def tokenize_and_encode(self):
        """
        Perform required preprocessing steps for pretrained BERT.
        @param    data (np.array): Array of texts to be processed.
        @return   input_ids (torch.Tensor): Tensor of token ids to be fed to a model.
        @return   attention_masks (torch.Tensor): Tensor of indices specifying which
                    tokens should be attended to by the model.
        """
        # Create empty lists to store outputs
        input_ids = []
        attention_masks = []
        tokenizer = self.initialize_tokenizer()
        for sent in self.data:
            encoded_sent = tokenizer.encode_plus(
                text=text_preprocessing(sent),  # Preprocess sentence
                add_special_tokens=True,        # Add `[CLS]` and `[SEP]`
                max_length=max_len,             # Max length to truncate/pad
                pad_to_max_length=True,         # Pad sentence to max length
                #return_tensors='pt',           # Return PyTorch tensor
                return_attention_mask=True      # Return attention mask
                )
            # Add the outputs to the lists
            input_ids.append(encoded_sent.get('input_ids'))
            attention_masks.append(encoded_sent.get('attention_mask'))

        # Convert lists to tensors
        input_ids = torch.tensor(input_ids)
        attention_masks = torch.tensor(attention_masks)
        return input_ids, attention_masks
    
    def create_data_loader(self, inputs, masks, labels):
        """
        """
        data_tensor = TensorDataset(train_inputs, masks, labels)
        sampler = RandomSampler(data_tensor)
        dataloader = DataLoader(data_tensor, sampler=sampler, batch_size=batch_size)
        return dataloader

    def reformat_sentiment_lbls(self):
        """
        Decreasing the values of the labels by 1 so they are between 0 and 4 instead of 1 and 5
        and converts data type to tensors
        """
        return torch.tensor(self.labels - 1, dtype=torch.long)

    def preprocess(self):
        """
        Preprocess input sentences and labels
        """
        inputs, masks = self.tokenize_and_encode()
        labels = self.reformat_sentiment_lbls()
        dataloader = self.create_data_loader(inputs, masks, labels)
        return dataloader

class BertClassifier(nn.Module):
    """
    Bert Model for Classification Tasks
    """
    def __init__(self, freeze_bert=False):
        """
        @param    bert: a BertModel object
        @param    classifier: a torch.nn.Module classifier
        @param    freeze_bert (bool): Set `False` to fine-tune the BERT model
        """
        super(BertClassifier, self).__init__(model_type)
        # Specify hidden size of BERT, hidden size of our classifier, and number of labels
        D_in, H, D_out = 768, 64, 5
        self.model_type = model_type

        # Instantiate BERT model
        self.bert = AutoModel.from_pretrained(self.model_type)
  
        self.classifier = nn.Sequential(
            nn.Linear(D_in, H),
            nn.ReLU(),
            nn.Linear(H, D_out),
            nn.Softmax()
        )
        # Freeze the BERT model
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False
        
    def forward(self, input_ids, attention_mask):
        """
        Feed input to BERT and the classifier to compute logits.
        @param    input_ids (torch.Tensor): an input tensor with shape (batch_size,
                      max_length)
        @param    attention_mask (torch.Tensor): a tensor that hold attention mask
                      information with shape (batch_size, max_length)
        @return   logits (torch.Tensor): an output tensor with shape (batch_size,
                      num_labels)
        """
        # Feed input to BERT
        outputs = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask)
        
        # Extract the last hidden state of the token `[CLS]` for classification task
        # last_hidden_state_cls = outputs[0][:][0][:]
        last_hidden_state_cls = outputs[0][:, 0, :]

        # Feed input to classifier to compute logits
        logits = self.classifier(last_hidden_state_cls)

        return logits

    
class FineTuneBert(object):
    """
    Fine tunes BERT model
    """
    def __init__(self, device, epochs):
        self.device = device
        self.train_data_loader = train_data_loader
        self.epochs = epochs

    def initialize_model(self):
        """
        Initialize the Bert Classifier, the optimizer and the learning rate scheduler.
        """
        # Instantiate Bert Classifier
        bert_classifier = BertClassifier(freeze_bert=False)

        # Tell PyTorch to run the model on GPU
        bert_classifier.to(self.device)

        # Create the optimizer
        optimizer = AdamW(bert_classifier.parameters(),
                        lr=5e-5,    # Default learning rate
                        eps=1e-8    # Default epsilon value
                        )

        # Total number of training steps
        total_steps = len(self.train_dataloader) * self.epochs

        # Set up the learning rate scheduler
        scheduler = get_linear_schedule_with_warmup(optimizer,
                                                    num_warmup_steps=0, # Default value
                                                    num_training_steps=total_steps)
        return bert_classifier, optimizer, scheduler

    def train(self):
        """
        Trains (fine-tunes) the BERT model
        """
        print("Start training...\n")
        for epoch_i in range(epochs):
            # =======================================
            #               Training
            # =======================================
            # Print the header of the result table
            print(f"{'Epoch':^7} | {'Batch':^7} | {'Train Loss':^12} | {'Val Loss':^10} | {'Val Acc':^9} | {'Elapsed':^9}")
            print("-"*70)

            # Measure the elapsed time of each epoch
            t0_epoch, t0_batch = time.time(), time.time()

            # Reset tracking variables at the beginning of each epoch
            total_loss, batch_loss, batch_counts = 0, 0, 0

            # Put the model into the training mode
            model.train()

            # For each batch of training data...
            for step, batch in enumerate(train_dataloader):
                batch_counts +=1
                # Load batch to GPU
                b_input_ids, b_attn_mask, b_labels = tuple(t.to(device) for t in batch)

                # Zero out any previously calculated gradients
                model.zero_grad()

                # Perform a forward pass. This will return logits.
                logits = model.forward(b_input_ids, b_attn_mask)

                # Compute loss and accumulate the loss values
                loss = loss_fn(logits, b_labels)
                
                batch_loss += loss.item()
                total_loss += loss.item()

                # Perform a backward pass to calculate gradients
                loss.backward()

                # Clip the norm of the gradients to 1.0 to prevent "exploding gradients"
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

                # Update parameters and the learning rate
                optimizer.step()
                scheduler.step()

                # Print the loss values and time elapsed for every 20 batches
                if (step % 20 == 0 and step != 0) or (step == len(train_dataloader) - 1):
                    # Calculate time elapsed for 20 batches
                    time_elapsed = time.time() - t0_batch

                    # Print training results
                    print(f"{epoch_i + 1:^7} | {step:^7} | {batch_loss / batch_counts:^12.6f} | {'-':^10} | {'-':^9} | {time_elapsed:^9.2f}")

                    # Reset batch tracking variables
                    batch_loss, batch_counts = 0, 0
                    t0_batch = time.time()

            # Calculate the average loss over the entire training data
            avg_train_loss = total_loss / len(train_dataloader)

            print("-"*70)
            # =======================================
            #               Evaluation
            # =======================================
            if evaluation == True:
                # After the completion of each training epoch, measure the model's performance
                # on our validation set.
                val_loss, val_accuracy = evaluate(model, val_dataloader)

                # Print performance over the entire training data
                time_elapsed = time.time() - t0_epoch
                
                print(f"{epoch_i + 1:^7} | {'-':^7} | {avg_train_loss:^12.6f} | {val_loss:^10.6f} | {val_accuracy:^9.2f} | {time_elapsed:^9.2f}")
                print("-"*70)
            print("\n")
        
        print("Training complete!")
        return model

    def evaluate(self):
        """After the completion of each training epoch, measure the model's performance
        on our validation set.
        """
        # Put the model into the evaluation mode. The dropout layers are disabled during
        # the test time.
        model.eval()

        # Tracking variables
        val_accuracy = []
        val_loss = []

        # For each batch in our validation set...
        for batch in val_dataloader:
            # Load batch to GPU
            b_input_ids, b_attn_mask, b_labels = tuple(t.to(device) for t in batch)

            # Compute logits
            with torch.no_grad():
                logits = model(b_input_ids, b_attn_mask)

            # Compute loss
            loss = loss_fn(logits, b_labels)
            val_loss.append(loss.item())

            # Get the predictions
            preds = torch.argmax(logits, dim=1).flatten()

            # Calculate the accuracy rate
            accuracy = (preds == b_labels).cpu().numpy().mean() * 100
            val_accuracy.append(accuracy)

        # Compute the average accuracy and loss over the validation set.
        val_loss = np.mean(val_loss)
        val_accuracy = np.mean(val_accuracy)

        return val_loss, val_accuracy

    def save_model(self):
        """
        Saves BERT model as pkl file
        """
        with open(self.model_path, 'wb') as out_path:
            pickle.dump(self.model, out_path, pickle.HIGHEST_PROTOCOL)