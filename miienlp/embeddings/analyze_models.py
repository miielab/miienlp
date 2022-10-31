import os
from gensim.models import word2vec
import gensim
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords
import numpy as np


def load_model(model_path):
    '''
    Loads in the model located at model_path
    '''
    return gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


def group_domain_similarity(group, domain, model):
    '''
    Calculate cosine similarity between a bundled group and domain word for a given model
    '''
    if group in model.vocab and domain in model.vocab:
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
    #gender_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])
    gender_centeredness_df = pd.DataFrame(columns = ['Model', 'Domain', 'Gender Centeredness'])
    #race_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])
    race_centeredness_df = pd.DataFrame(columns = ['Model', 'Domain', 'Race Centeredness'])
    race_gender_domain_df = pd.DataFrame(columns = ['Model', 'Group', 'Domain', 'Cosine Similarity'])    
    #top_n_df = pd.DataFrame(columns = ['Model', 'Category', 'Word', 'Similarity'])

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

def run_analysis2(model_dir_list, groups, domains, race=False, race_gender=False, gender=False):
    '''
    '''
    gender_centeredness_df = pd.DataFrame(columns = ['model', 'model_id', 'domain', 'gender_centeredness'])
    race_centeredness_df = pd.DataFrame(columns = ['model', 'model_id', 'domain', 'race_centeredness'])
    race_gender_domain_df = pd.DataFrame(columns = ['model', 'model_id', 'group', 'domain', 'cosine_similarity']) 

    for model_type, model_path in model_dir_list.items():
        models = os.listdir(model_path)
        print(len(models))
        for model in models:
            model_bin = load_model(os.path.join(model_path, model))
            model_id = model.split('_')[-1].split('.')[0]
            # calculate race and gender cosine similarity
            if race_gender: 
                for group in groups:
                    for domain in domains:
                        g2d_sim = group_domain_similarity(group, domain, model_bin)
                        if g2d_sim:
                            race_gender_domain_df = race_gender_domain_df.append({'model':model_type, 'model_id':model_id, 'group':group, 'domain':domain, 'cosine_similarity':g2d_sim}, ignore_index=True)
            #print(race_gender_domain_df)
            # calculate race centeredness
            if race:
                for domain in domains:
                    white_sim = group_domain_similarity("white_famous", domain, model_bin)
                    black_sim = group_domain_similarity("black_famous", domain, model_bin)    
                    if white_sim and black_sim:
                        race_centeredness = black_sim - white_sim
                        race_centeredness_df = race_centeredness_df.append({'model': model_type, 'model_id':model_id, 'domain': domain, 'race_centeredness': race_centeredness}, ignore_index=True)
            # calculate gender centeredness
            if gender: 
                for domain in domains:
                    female_sim = group_domain_similarity("female_famous", domain, model_bin)
                    male_sim = group_domain_similarity("male_famous", domain, model_bin)
                    if female_sim and male_sim:
                        gender_centeredness = female_sim - male_sim
                        gender_centeredness_df = gender_centeredness_df.append({'model': model_type, 'model_id':model_id, 'domain': domain, 'gender_centeredness': gender_centeredness}, ignore_index=True)
    #race_gender_domain_df.to_csv("race_gender_domain.csv", index = False)
    gender_centeredness_df.to_csv("gender_centeredness.csv", index = False)
    #race_centeredness_df.to_csv("race_centeredness.csv", index = False)

if __name__ == '__main__':
    groups = ["black_female", "black_male", "white_female", "white_male"]
    #genders = ["male_famous", "female_famous"]
    #races = ["white_famous", "black_famous"]
    domains = ["business", "power", "family", "struggle", "sports", "struggle", "performance_arts"]
    # model_dir_list = {'Bundled Diversity': '/project2/adukia/miie/text_analysis/models/simulation/bundled_race_gender/diversity/',
    #                   'Bundled Mainstream': '/project2/adukia/miie/text_analysis/models/simulation/bundled_race_gender/mainstream/'}
    #model_dir_list = {'Bundled Race Diversity': '/project2/adukia/miie/text_analysis/models/simulation/bundled_race/diversity/',
    #                'Bundled Race Mainstream': '/project2/adukia/miie/text_analysis/models/simulation/bundled_race/mainstream/'}
    model_dir_list = {'Bundled Gender Diversity': '/project2/adukia/miie/text_analysis/models/simulation/bundled_gender/diversity/',
                    'Bundled Gender Mainstream': '/project2/adukia/miie/text_analysis/models/simulation/bundled_gender/mainstream/'}
    run_analysis2(model_dir_list, groups, domains, gender=True)






