import csv
import zipfile
from names_dataset import NameDatasetV1

# NLP
import spacy
nlp = spacy.load("en_core_web_sm")
import json

# object and subject constants
OBJECT_DEPS = {"dobj", "dative", "attr", "oprd"}
SUBJECT_DEPS = {"nsubj", "nsubjpass", "csubj", "agent", "expl"}
# tags that define wether the word is wh-
WH_WORDS = {"WP", "WP$", "WRB"}

#import pandas as pd
#import numpy as np
#from mlxtend.frequent_patterns import apriori, association_rules
#from mlxtend.preprocessing import TransactionEncoder

def determine_subject_type(subject):
    #splitted = subject.split(" ");

    # First check if it's a name or not
    #name_database = NameDatasetV1()
    #if (name_database.search_first_name(splitted[0]) or name_database.search_last_name(splitted[0]) or (len(splitted) > 1 and (name_database.search_first_name(splitted[-1])  or name_database.search_last_name(splitted[-1])))):
    #    # Must be a person
    #    return "person"
    #else:
    #subject = subject.lower()
    
    with open('data/world-cities.csv', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if (subject == row[0]):
                # Is a city!
                return "city"
    
    # Check the big database - needs extraction first
    with zipfile.ZipFile('data/all_countries_dict.zip', 'r') as zipObj:
        zipObj.extractall()
    
    with open('all_countries_dict.json', encoding='utf-8') as json_file:
        loaded = json.load(json_file)
        if (subject in loaded):
            # Is a place!
            return "place"
                
    return "unknown"

def nlp_extract(headline):
    # First use spacy to extract SVO
    # https://github.com/Dimev/Spacy-SVO-extraction/blob/master/main.py
    subjects = []
    objects = []
    verbs = []
    doc = nlp(headline)
    for token in doc:
        # is this a verb?
        if token.pos_ == "VERB":
            verbs.append(token.text)
        # is this the object?
        if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
            objects.append(token.text)
        # is this the subject?
        if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
            subjects.append(token.text)

    for subject in subjects:
        print("Found subject " + subject)
        #for word in subject:
        print(determine_subject_type(subject))

nlp_extract("Denmark suspends use of Oxford-AZ Covid jab")
