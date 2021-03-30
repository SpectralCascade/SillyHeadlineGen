
# Machine learning class for training basic classification
class Learner:
    # Takes an array of possible classification values e.g. ["Yes", "No"] and
    # a dictionary training dataset that has a "data" key, with the value as an array of arrays
    # containing training data, as well as a "answers" key, with the value as an array of classification results
    # e.g. dictionary/JSON input
    # {
    #     "data" : [["High", "Busy"], ["Low", "Quiet"], ["Medium", "Quiet"]],
    #     "answers" : ["No", "Yes", "Yes"]
    # }
    def __init__(self, training_dataset):
        # The training data set
        self.dataset = training_dataset
    
    # Runs the machine learning logic over the training dataset and builds a decision model.
    def train(self):
        classes = dict();
        total = 0;
        for answer in self.dataset["answers"]:
            if (answer not in classes):
                classes[answer] = 0
            classes[answer] += 1
            total += 1
        print(str(classes))

