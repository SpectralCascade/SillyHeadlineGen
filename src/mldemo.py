import ml

if (__name__ == "__main__"):
    learner = ml.Learner({"data" : [["High", "Low", "Medium", "Low", "High", "Low"], ["Busy", "Quiet", "Quiet", "Busy", "Quiet", "Busy"]], "answers" : ["No", "Yes", "Yes", "No", "No", "Yes"]})
    print(learner.dataset)
    learner.train()
    to_predict = ["High", "Quiet"]
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
    while (True):
        pass
