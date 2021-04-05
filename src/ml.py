
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
