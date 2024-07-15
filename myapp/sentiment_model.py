import joblib
import os
import re
import string

# Load the joblib model, vectorizer, and label encoder
model_path = os.path.join(os.path.dirname(__file__), 'sentiment_model.joblib')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'tfidf_vectorizer.joblib')
label_encoder_path = os.path.join(os.path.dirname(__file__), 'label_encoder.joblib')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(label_encoder_path)

def preprocess_text(text, vectorizer):
    # Preprocessing text: removing HTML tags, punctuation, digits, and stopwords
    text = re.sub("<.*?>", '', text)
    text = text.translate(str.maketrans('', '', string.digits))
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return vectorizer.transform([text])  # Ensure this returns the transformed text directly

def analyze_sentiment(text):
    try:
        # Ensure the input is processed and transformed correctly
        vectorized_text = preprocess_text(text, vectorizer)
        prediction = model.predict(vectorized_text)[0]
        decoded_prediction = label_encoder.inverse_transform([prediction])[0]
        return decoded_prediction
    except Exception as e:
        # Handle any exceptions that occur during sentiment analysis
        # Log the error for debugging purposes
        print(f"Error during sentiment analysis: {e}")
        return "Unknown"  # Return a default value or handle the error appropriately
