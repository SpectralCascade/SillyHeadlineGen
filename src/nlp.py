import csv
import json
import zipfile
import os.path
from names_dataset import NameDatasetV1

# NLP
import spacy
from spacy.pipeline import merge_entities
nlp = spacy.load("en_core_web_sm")
# This makes sure entities such as person names are joined together properly
nlp.add_pipe("merge_entities")

def determine_subject_type(subject):
    splitted = subject.split(" ");

    # First check if it's a name or not
    name_database = NameDatasetV1()
    if (name_database.search_first_name(splitted[0]) or name_database.search_last_name(splitted[0]) or (len(splitted) > 1 and (name_database.search_first_name(splitted[-1])  or name_database.search_last_name(splitted[-1])))):
        # Must be a person
        return "PERSON"
    else:
        with open('data/world-cities.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                if (subject == row[0]):
                    # Is a city!
                    return "GPE"
        
        # Check the big database - needs extraction first
        #if (not os.path.isfile("all_countries_dict.json")):
            #print("First time use, extracting country names database...")
        with zipfile.ZipFile('data/all_countries_dict.zip', 'r') as zipObj:
            zipObj.extractall()
        
        with open('all_countries_dict.json', encoding='utf-8') as json_file:
            loaded = json.load(json_file)
            if (subject in loaded):
                # Is a country!
                return "GPE"
                    
        return "UNKNOWN"

def nlp_analyse(doc):
    print("Entities:")
    for ent in doc.ents:
        print(ent.text + " => " + ent.label_ + " (" + spacy.explain(ent.label_) + ")")
    print("\nTokens:")
    spans = []
    
    for token in doc:
        pos = spacy.explain(token.pos_)
        dep = spacy.explain(token.dep_)
        if (pos == None):
            pos = "unknown"
        if (dep == None):
            dep = "unknown"
        print(token.text + " | " + token.pos_ + " (" + pos + ") | " + token.dep_ + " (" + dep + ")" + " | Head: " + token.head.text + " | Children: \"" + str([t.text for t in token.children]) + "\"")
    

def nlp_extract(headline):
    data = dict()
    data["entities"] = dict()
    data["verbs"] = []
    entities = data["entities"]
    verbs = data["verbs"]

    # Use  spaCy to extract entities and verbs
    doc = nlp(headline)
    for token in doc:
        # Is this a verb?
        if token.pos_ == "VERB":
            verbs.append(token.text)
        # Is this a proper noun (if so, it's probably an entity we care about).
        if token.pos_ == "PROPN":
            entities[token.text] = "UNKNOWN"
    # Catch any entities that were missed by the proper noun check and assign type label
    for ent in doc.ents:
        entities[ent.text] = ent.label_
        
    # Now go over entities with unknown types and try and determine them
    for key in entities:
        if (entities[key] == "UNKNOWN"):
            entities[key] = determine_subject_type(key)
    
    return data

print(nlp_extract("John Smith: \'I was sacked in Exeter :('"))
