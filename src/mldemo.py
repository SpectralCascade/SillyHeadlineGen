import ml

if (__name__ == "__main__"):
    learner = ml.Learner({"data" : [["High", "Busy"], ["Low", "Quiet"], ["Medium", "Quiet"]], "answers" : ["No", "Yes", "Yes"]})
    learner.train()
    while (True):
        pass
