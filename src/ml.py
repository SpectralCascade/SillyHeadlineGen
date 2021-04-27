import nlp
import soupScraping as scrape
import csv
import sys
import textblob # used for sentiment analysis

# Machine learning class for training basic classification
class Learner:
    # Takes an array of possible classification values e.g. ["Yes", "No"] and
    # a dictionary training dataset that has a "data" key, with the value being a column-major 2D array.
    # containing training data, as well as a "answers" key, with the value as an array of classification results
    # TODO: enumeration? The "enumeration" array enumerates non-numeric values in the dataset by column.
    # e.g. dictionary/JSON input
    # {
    #     "enumeration" : [{"Low": 0, "Medium": 0.5, "High": 1}, {"Quiet": 0, "Busy": 1}],
    #     "data" : [["High", "Low", "Medium"], ["Busy", "Quiet", "Quiet"]],
    #     "answers" : ["No", "Yes", "Yes"]
    # }
    def __init__(self, training_dataset):
        # The training data set
        self.dataset = training_dataset
        self.model = dict()
        self.classes = dict()
    
    # Takes a list of data and returns the probabilities for each classification
    def classify(self, data):
        value = dict()
        for key in self.classes:
            value[key] = self.classes[key]
            for i in range(0, len(data)):
                if key in self.model and i < len(self.model[key]) and data[i] in self.model[key][i]:
                    value[key] = value[key] * self.model[key][i][data[i]]
                else:
                    value[key] = 0
        return value
    
    # Runs the machine learning logic over the training dataset and builds a probability model.
    # This uses the Naive Bayes algorithm, based on discrete variables (multinomial distribution).
    def train(self):
        self.classes = dict() # Probabilities of classifiers
        self.model = dict()
        bayes = self.model # Variable probabilities given classifiers
        total = 0 # Total rows in the dataset
        for answer in self.dataset["answers"]:
            if (answer not in self.classes):
                self.classes[answer] = 0
            self.classes[answer] += 1
            total += 1
        #print(str(classes))
        # Compute classification probabilities
        for key in self.classes:
            self.classes[key] = self.classes[key] / total
        # Now compute the probability of each variable given independant classifiers
        dataset = self.dataset["data"]
        # Iterate over field
        count = len(dataset)
        inc = 1 / total
        #print(count)
        for col in range(0, count):
            # Iterate over field variables
            for row in range(0, total):
                # Make sure the classifier is added
                #print("Checking classifier: " + self.dataset["answers"][row])
                if self.dataset["answers"][row] not in bayes:
                    bayes[self.dataset["answers"][row]] = []
                    for i in range(0, count):
                        bayes[self.dataset["answers"][row]].append(dict())
                # Increment conditional probability for given discrete variable value
                # Structure is Classifier (dict) -> Columns/Fields (list) -> Discrete variable (dict) -> Probability (real number)
                if dataset[col][row] not in bayes[self.dataset["answers"][row]][col]:
                    bayes[self.dataset["answers"][row]][col][dataset[col][row]] = 0
                bayes[self.dataset["answers"][row]][col][dataset[col][row]] += inc
        #print(bayes)    

# Set of profanity words
profanity = set()
# Set of adjectives that are exclusive to the parody headlines training data
exclusive_real_adjectives = set()

is_parody = "Not realistic"
not_parody = "Realistic"

# Converts headline into machine learning format
# Takes the raw string and NLP extracted data
def headlineToTrainingEntry(headline):
    output = [0, 0, 0, 0] # sentiment, subjectivity, uncommon adjective, profanity
    
    # Extract useful information using NLP
    data = nlp.GetHeadlineNLP().nlp_extract(headline)
    
    # Sentiment analysis
    sentiment = textblob.TextBlob(headline).sentiment
    output[0] = int(round(sentiment.polarity))
    output[1] = int(round(sentiment.subjectivity))
    
    # These entity counts are very rigid, non useful measures of "parody or not"
    # While the probabilistic relationship may hold between a particular pair of websites or headline styles,
    # the whole point of parody headlines is that they have the *form* of real article headlines,
    # but context and juxtaposition should differentiate them
    # For instance, the seemingly random use of profanity in a parody headline vs usage in a quote or subject name in a real news headline.
    for adj in data["adjectives"]:
        if adj not in exclusive_real_adjectives:
            # This does rely on having a large training set, but it's more accurate than checking for any adjective
            output[2] = 1
            break
    for noun in data["nouns"]:
        if (noun.lower() in profanity):
            output[3] = 1
            break
    # Make sure data is all strings
    for i in range(len(output)):
        output[i] = str(output[i])
    return output

# Takes list of headlines and list of yes/no parody or not, returns trained learner
def trainLearner(headlines, parodyOrNot):
    sentiment = []
    subjectivity = []
    adjectives = []
    profanities = []

    for i in range(len(headlines)):
        data = headlineToTrainingEntry(headlines[i])
        sentiment.append(data[0])
        subjectivity.append(data[1])
        adjectives.append(data[2])
        profanities.append(data[3])
    
    learner = Learner({"data" : [sentiment, subjectivity, adjectives, profanities], "answers" : parodyOrNot})
    #print(learner.dataset)
    learner.train()
    return learner

def demo(headline):
    # Modified from https://github.com/RobertJGabriel/Google-profanity-words/blob/master/list.txt on 25/04/2021
    with open('data/profanity.csv', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            profanity.add(row[0])
    
    # Data obtained from 10000 article headlines in The Guardian
    with open('data/exclusive_real_adjectives.csv', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            exclusive_real_adjectives.add(row[0])
        #print(exclusive_real_adjectives[0])
        #input()

    scrape_limit = 100

    # Scrape a bunch of headlines for the training set
    # Always get parody headlines first
    headlines = scrape.dailymashScrape(scrape_limit)
    total_parody = len(headlines)
    
    headlines = headlines + scrape.guardianScrape(scrape_limit)
    total_real = len(headlines) - total_parody
    
    #print("Headlines: " + str(headlines))
    print("Scraped " + str(len(headlines)) + " headlines out of limit " + str(scrape_limit * 2))
 
    to_predict = headlineToTrainingEntry(headline)
    
    learner = trainLearner(headlines, [is_parody] * total_parody + [not_parody] * total_real)
    #print(learner.dataset)
    
    print("Input data: " + str(to_predict))
    print("Prediction model: " + str(learner.model))
    predictionModel = learner.model
    data = learner.classify(to_predict)
    best_score = 0
    best = "\"Unknown\""
    for v in data:
        if data[v] > best_score:
            best_score = data[v]
            best = v
    print(data)
    print("Determined best match to be " + best + " with a score of " + str(best_score))

    return {"Input Headline" : headline, "Prediction Model" : predictionModel, "Outcome Probabilities" : data, "Result" : best}

if (__name__ == "__main__"):
    if (len(sys.argv) > 1):
        demo(sys.argv[1])
    else:
        demo("'Impossible to know' which senior Royal was worried about how dark baby would be")
