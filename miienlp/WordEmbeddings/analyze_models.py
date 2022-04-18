import os
from gensim.models import word2vec
import gensim
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords
import numpy as np

# GROUPS AND DOMAINS
race_genders = ["black_female", "black_male", "white_female", "white_male"]
genders = ["male_famous", "female_famous"]
races = ["white_famous", "black_famous"]
domains = ["business", "power", "family", "struggle", "sports", "struggle", "performance_arts"]
stop_words = set(stopwords.words('english'))

# DATA
mainstream_full_gender = "/project2/adukia/miie/text_analysis/models/word2vec/mainstream/full_bundled_gender/model_0.bin"
diversity_full_gender = "/project2/adukia/miie/text_analysis/models/word2vec/diversity/full_bundled_gender/model_0.bin"
mainstream_full_race = "/project2/adukia/miie/text_analysis/models/word2vec/mainstream/full_bundled_race/model_0.bin"
diversity_full_race = "/project2/adukia/miie/text_analysis/models/word2vec/diversity/full_bundled_race/model_0.bin"
mainstream_full_race_gender = "/project2/adukia/miie/text_analysis/models/word2vec/mainstream/full_bundled_race_gender/model_0.bin"
diversity_full_race_gender = "/project2/adukia/miie/text_analysis/models/word2vec/diversity/full_bundled_race_gender/model_0.bin"


# LOAD MODELS
mainstream_full_gender_model = gensim.models.KeyedVectors.load_word2vec_format(mainstream_full_gender, binary=True)
diversity_full_gender_model = gensim.models.KeyedVectors.load_word2vec_format(diversity_full_gender, binary=True)
mainstream_full_race_model = gensim.models.KeyedVectors.load_word2vec_format(mainstream_full_race, binary=True)
diversity_full_race_model = gensim.models.KeyedVectors.load_word2vec_format(diversity_full_race, binary=True)
mainstream_full_race_gender_model = gensim.models.KeyedVectors.load_word2vec_format(mainstream_full_race_gender, binary=True)
diversity_full_race_gender_model = gensim.models.KeyedVectors.load_word2vec_format(diversity_full_race_gender, binary=True)

models = {"Mainstream Full Gender": mainstream_full_gender_model, "Diversity Full Gender": diversity_full_gender_model, 
          "Diversity Full Race Gender": diversity_full_race_gender_model, "Mainstream Full Race Gender": mainstream_full_race_gender_model,
          "Mainstream Full Race": mainstream_full_race_model, "Diversity Full Race": diversity_full_race_model}

#models = {"Mainstream Full Race Gender": mainstream_full_race_gender_model, "Diversity Full Race Gender": diversity_full_race_gender_model}

def group_domain_similarity(group, domain, model):
    '''
    Calculate cosine similarity between a bundled group and domain word for a given model
    '''
    if group in model.vocab and domain in model.vocab:
        #print(cosine_similarity(model[group], model[domain]))
        V1 = model[group]
        V2 = model[domain]
        sim = cosine_similarity([V1], [V2])[0][0]
    else:
        sim = None
    return sim


def top_n_similar(category, model, n = 50):
    '''
    Calculate the top 50 most similar words to a given category (ie. female) and remove stopwords
    '''
    top = pd.DataFrame(columns = ['Model', 'Category', 'Word', 'Similarity'])
    if category in models[model].vocab:
        top_n = models[model].most_similar(category, topn=n)
        for word in top_n:
            if word[0] not in stop_words:
                top = top.append({'Model':model, 'Category': category, 'Word': word[0], 'Similarity': word[1]}, ignore_index=True)
    return top

def run_analysis():
    '''
    Create gender, race_gender, and top_n data frames
    '''
    gender_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])
    gender_centeredness_df = pd.DataFrame(columns = ['Model', 'Domain', 'Gender Centeredness'])
    race_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])
    race_centeredness_df = pd.DataFrame(columns = ['Model', 'Domain', 'Race Centeredness'])
    race_gender_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])    
    top_n_df = pd.DataFrame(columns = ['Model', 'Category', 'Word', 'Similarity'])
    for model in models:
        if model == "Mainstream Full Gender" or model == "Diversity Full Gender":
            for domain in domains:
                female_sim = group_domain_similarity("female_famous", domain, models[model])
                male_sim = group_domain_similarity("male_famous", domain, models[model])
                if female_sim and male_sim:
                    gender_centeredness = female_sim - male_sim
                    gender_centeredness_df = gender_centeredness_df.append({'Model': model, 'Domain': domain, 'Gender Centeredness': gender_centeredness}, ignore_index=True)
                if female_sim:
                    gender_domain_df = gender_domain_df.append({'Model': model, 'Group': "female", 'Domain': domain, 'Cosine Similarity': female_sim}, ignore_index=True)
                if male_sim:
                    gender_domain_df = gender_domain_df.append({'Model': model, 'Group': "male", 'Domain': domain, 'Cosine Similarity': male_sim}, ignore_index=True)
               
        elif model == "Mainstream Full Race Gender" or model == "Diversity Full Race Gender":
            for race_gender in race_genders:
                for domain in domains:
                    sim = group_domain_similarity(race_gender, domain, models[model])
                    if sim:
                        race_gender_domain_df = race_gender_domain_df.append({'Model': model, 'Group': race_gender, 'Domain': domain, 'Cosine Similarity': sim}, ignore_index=True)
        elif model == "Mainstream Full Race" or model == "Diversity Full Race":
            for domain in domains:
                white_sim = group_domain_similarity("white_famous", domain, models[model])
                black_sim = group_domain_similarity("black_famous", domain, models[model])
                if white_sim and black_sim:
                    race_centeredness = black_sim - white_sim
                    race_centeredness_df = race_centeredness_df.append({'Model': model, 'Domain': domain, 'Race Centeredness': race_centeredness}, ignore_index=True)
                if white_sim:
                    race_domain_df = race_domain_df.append({'Model': model, 'Group': "white_famous", 'Domain': domain, 'Cosine Similarity': white_sim}, ignore_index=True)
                if black_sim:
                    race_domain_df = race_domain_df.append({'Model': model, 'Group': "black_famous", 'Domain': domain, 'Cosine Similarity': black_sim}, ignore_index=True)
        #for group in race_genders + genders + domains + races:
        for group in race_genders + domains:
            top_n = top_n_similar(group, model)
            if not top_n.empty:
                top_n_df = top_n_df.append(top_n, ignore_index = True)
    
    #gender_domain_df.to_csv("gender_domain.csv", index = False)
    race_gender_domain_df.to_csv("race_gender_domain.csv", index = False)
    gender_centeredness_df.to_csv("gender_centeredness.csv", index = False)
    race_centeredness_df.to_csv("race_centeredness.csv", index = False)
    #race_domain_df.to_csv("race_domain.csv", index = False)
    # top_n_df.to_csv("top_n.csv", index = False)

if __name__ == '__main__':
    run_analysis()






