import pandas as pd
import re
from nltk import stopwords

def load_data(path):
    """
    Loads data from a given path
    """
    df = pd.read_csv(path)
    return df.drop(['Unnamed: 0'], axis=1)

def text_preproccessing(s):
    """
    Preprocesses a given sentence (s): 
    - Lowercase the sentence
    - Change "'t" to "not"
    - Remove "@name"
    - Isolate and remove punctuations except "?"
    - Remove other special characters
    - Remove stop words except "not" and "can"
    - Remove trailing whitespace
    """
    s = s.lower()
    s = re.sub(r"\'t", " not", s) # Change 't to 'not'
    s = re.sub(r'(@.*?)[\s]', ' ', s) # Remove @name
    s = re.sub(r'([\'\"\.\(\)\!\?\\\/\,])', r' \1 ', s) # Isolate and remove punctuations except '?'
    s = re.sub(r'[^\w\s\?]', ' ', s)
    s = re.sub(r'([\;\:\|•«\n])', ' ', s) # Remove some special characters
    # Remove stopwords except 'not' and 'can'
    s = " ".join([word for word in s.split()
                  if word not in stopwords
                  or word in ['not', 'can']])
    # Remove trailing whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def determine_core_type():
    """
    Determines whether your machine has a GPU or CPU
    If GPU is available, connect and display the name, else use CPU
    """
    if torch.cuda.is_available():       
        device = torch.device("cuda")
        print(f'There are {torch.cuda.device_count()} GPU(s) available.')
        print('Device name:', torch.cuda.get_device_name(0))
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device("cpu")
    return device


def determine_max_sent_len(train_df, val_df, test_df):
    """
    Finds max sentence length that will be used in the tokenizer
    """
    return max(train_df.sentence.map(len).max(),\
            val_df.sentence.map(len).max(),\
            test_df.sentence.map(len).max())


