#Libraries
import pickle

#Import model and generate prediction function
with open("data/model.bin", "rb") as f:
    dv, model = pickle.load(f)
f.close()

def generate_prediction(result):
    
    #Turn the client into a feature matrix
    X = dv.transform(result)

    #Determine probability that result generates an alert
    probability = model.predict_proba(X)[0,1]

    return probability


