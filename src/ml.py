import nlp
import soupScraping as scrape

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

# Converts headline into machine learning format
def headlineToTrainingEntry(headline):
    output = [0, 0] # people, gpe
    # Perform NLP on headline
    data = nlp.GetHeadlineNLP().nlp_extract(headline)
    for ent in data["entities"]:
        if (data["entities"][ent] == "PERSON"):
            output[0] += 1
        elif (data["entities"][ent] == "GPE"):
            output[1] += 1
    # Make sure data is all strings
    for i in range(len(output)):
        output[i] = str(output[i])
    return output

# Takes list of headlines and list of yes/no parody or not, returns trained learner
def trainLearner(headlines, parodyOrNot):
    gpe = [];
    people = [];
    
    for headline in headlines:
        data = headlineToTrainingEntry(headline);
        people.append(data[0])
        gpe.append(data[1])
    
    learner = Learner({"data" : [people, gpe], "answers" : parodyOrNot})
    #learner = Learner({"data" : [people, gpe], "answers" : ["Yes"] * 10 + ["No"] * 10})
    print(learner.dataset)
    learner.train()
    return learner

def demo(headline):
    # Scrape a bunch of headlines for the training set
    headlines = scrape.dailymashScrape(10)
    
    # Some random headlines from the BBC
    headlines = headlines + ["Greta Thunberg becomes 'bunny hugger' on Twitter",
        "Covid-19: MP claims 'outrage' at dropped charge for 150-guest funeral",
        "Convicted Post Office workers have names cleared",
        "Covid: India on UK travel red list as Covid crisis grows",
        "UK's coronavirus infection levels continue to fall",
        "Desperation as Indian hospitals buckle under Covid",
        "Brexit: UK-EU talks on Northern Ireland 'to intensify'",
        "US joins race to find stricken Indonesia submarine",
        "Putin opponent Navalny ends hunger strike in Russian jail",
        "Malaria vaccine hailed as potential breakthrough"]
    
    print("Headlines: " + str(headlines))
    
    #headline = "A minuscule jewel-studded thong: five things to buy now the contactless limit is £100"
    to_predict = headlineToTrainingEntry(headline)
    
    learner = trainLearner(headlines, ["Yes"] * 10 + ["No"] * 10)
    
    print("Input data: " + str(to_predict))
    print("Prediction model: " + str(learner.model))
    data = learner.classify(to_predict)
    best_score = 0
    best = "\"Unknown\""
    for v in data:
        if data[v] > best_score:
            best_score = data[v]
            best = v
    print(data)
    print("Determined best match to be " + best + " with a score of " + str(best_score))

if (__name__ == "__main__"):
    demo("A minuscule jewel-studded thong: five things to buy now the contactless limit is £100")
