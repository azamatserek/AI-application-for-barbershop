import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def predict(features):
    return int(model.predict([features])[0])
