import csv
import json
import zipfile
import os.path
from names_dataset import NameDatasetV1

# NLP
import spacy
from spacy.pipeline import merge_entities

def GetHeadlineNLP():
    return HeadlineNLP().instance

class HeadlineNLP:
    instance = None
    
    # Initialise the singleton instance
    def __init__(self):
        if (HeadlineNLP.instance == None):
            # Kinda-singleton
            HeadlineNLP.instance = self
            print("Initialising HeadlineNLP...")
            
            # Load NLP
            self.nlp = spacy.load("en_core_web_sm")
            # This makes sure entities such as person names are joined together properly
            self.nlp.add_pipe("merge_entities")
            
            # Dictionary of entity types to proper nouns
            # Note, PERSON is not included because the names database is a little more complex
            self.database = {"GPE" : set()}
            
            # Initialise the name database
            self.name_db = NameDatasetV1()
            
            # Setup entity database
            with open('data/world-cities.csv', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    self.database["GPE"].add(row[0])
            
            # Country names database is so big it has to be compressed for git
            with zipfile.ZipFile('data/all_countries_dict.zip', 'r') as zipObj:
                zipObj.extractall()
            
            with open('all_countries_dict.json', encoding='utf-8') as json_file:
                loaded = json.load(json_file)
                for key in loaded:
                    self.database["GPE"].add(key)
            print ("HeadlineNLP initialised!")

    # For entities which aren't identified by spaCy, some additional processing is needed.
    def determine_subject_type(self, subject):
        for key in self.database:
            if (subject in self.database[key]):
                return key
            if (key == "PERSON"):
                splitted = subject.split(" ");
                if (self.name_db.search_first_name(splitted[0]) or self.name_db.search_last_name(splitted[0]) or (len(splitted) > 1 and (self.name_db.search_first_name(splitted[-1])  or self.name_db.search_last_name(splitted[-1])))):
                    # Must be a person's name
                    return "PERSON"
        return "UNKNOWN"

    # Debug logs info about the entities and tokens in an NLP document
    def nlp_analyse(self, doc):
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
    
    # Extracts entities and verbs from a headline into a dictionary
    def nlp_extract(self, headline):
        data = dict()
        data["entities"] = dict()
        data["verbs"] = []
        entities = data["entities"]
        verbs = data["verbs"]

        # Use spaCy to extract entities and verbs
        doc = self.nlp(headline)
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
                entities[key] = self.determine_subject_type(key)
        
        return data

print(GetHeadlineNLP().nlp_extract("John Smith: \'I was sacked in Exeter :('"))
