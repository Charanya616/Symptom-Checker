import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

class SymptomClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.mlb = MultiLabelBinarizer()
        self.model = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and remove stopwords
        tokens = text.split()
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)
    
    def create_sample_data(self):
        """Create sample medical data for training"""
        data = {
            'symptoms': [
                'headache fever body aches chills',
                'cough sore throat runny nose congestion',
                'nausea vomiting diarrhea stomach pain',
                'chest pain shortness of breath dizziness',
                'rash itching redness swelling',
                'fatigue weakness dizziness pale skin',
                'joint pain stiffness swelling redness',
                'abdominal pain bloating gas indigestion',
                'sneezing itchy eyes runny nose congestion',
                'back pain stiffness limited movement',
                'sore throat fever swollen glands',
                'headache sensitivity to light sound',
                'fever cough difficulty breathing',
                'muscle pain fatigue headache',
                'blurred vision headache nausea',
                'ear pain fever hearing loss',
                'frequent urination thirst fatigue',
                'weight loss increased appetite palpitations',
                'wheezing coughing chest tightness',
                'memory loss confusion difficulty concentrating'
            ],
            'conditions': [
                ['flu'],
                ['common cold'],
                ['gastroenteritis'],
                ['heart problems'],
                ['allergic reaction'],
                ['anemia'],
                ['arthritis'],
                ['indigestion'],
                ['allergies'],
                ['back strain'],
                ['strep throat'],
                ['migraine'],
                ['pneumonia'],
                ['viral infection'],
                ['migraine'],
                ['ear infection'],
                ['diabetes'],
                ['hyperthyroidism'],
                ['asthma'],
                ['cognitive issues']
            ]
        }
        return pd.DataFrame(data)
    
    def train(self):
        # Create or load your dataset
        df = self.create_sample_data()
        
        # Preprocess symptoms
        df['processed_symptoms'] = df['symptoms'].apply(self.preprocess_text)
        
        # Prepare features and labels
        X = self.vectorizer.fit_transform(df['processed_symptoms'])
        y = self.mlb.fit_transform(df['conditions'])
        
        # Train model
        self.model = OneVsRestClassifier(LogisticRegression(max_iter=1000))
        self.model.fit(X, y)
        
        # Save model and vectorizer
        joblib.dump(self.vectorizer, 'vectorizer.joblib')
        joblib.dump(self.mlb, 'multilabel_binarizer.joblib')
        joblib.dump(self.model, 'symptom_classifier.joblib')
        
        print("Model training completed!")
        print(f"Trained on {len(df)} samples")
        print(f"Number of conditions: {len(self.mlb.classes_)}")
        
    def predict(self, symptoms_text):
        # Preprocess input
        processed_text = self.preprocess_text(symptoms_text)
        
        # Transform using saved vectorizer
        X = self.vectorizer.transform([processed_text])
        
        # Predict probabilities
        probabilities = self.model.predict_proba(X)[0]
        
        # Get top predictions
        condition_probs = []
        for i, prob in enumerate(probabilities):
            if prob > 0.1:  # Threshold for considering a condition
                condition_probs.append({
                    'name': self.mlb.classes_[i],
                    'probability': float(prob)
                })
        
        # Sort by probability
        condition_probs.sort(key=lambda x: x['probability'], reverse=True)
        
        return condition_probs[:3]  # Return top 3 conditions

if __name__ == '__main__':
    classifier = SymptomClassifier()
    classifier.train()