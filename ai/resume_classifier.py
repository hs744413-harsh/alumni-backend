import joblib

# load ML components
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


def classify_resume(text):

    X = vectorizer.transform([text])

    prediction = model.predict(X)

    category = label_encoder.inverse_transform(prediction)[0]

    return category