import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

class ImprovedSymptomClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.mlb = MultiLabelBinarizer()
        self.model = None
    
    def create_enhanced_data(self):
        data = {
            'symptoms': [
                # Original symptoms
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
                
                # NEW: Added leg and muscle related symptoms
                'leg pain muscle cramps',
                'leg pain swelling redness',
                'leg pain after exercise workout',
                'leg pain cramping walking',
                'muscle pain soreness stiffness',
                'joint pain knee hip leg',
                'leg pain numbness tingling',
                'leg pain varicose veins swelling',
                'muscle strain pain movement',
                'leg pain injury trauma',
                'growing pains legs children',
                'sciatica leg pain back pain',
                'arthritis joint pain leg',
                'tendonitis leg pain inflammation'
            ],
            'conditions': [
                # Original conditions
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
                
                # NEW: Conditions for leg pain
                ['muscle cramps'],
                ['inflammation'],
                ['muscle strain'],
                ['peripheral artery disease'],
                ['muscle soreness'],
                ['osteoarthritis'],
                ['nerve compression'],
                ['venous insufficiency'],
                ['muscle injury'],
                ['trauma'],
                ['growing pains'],
                ['sciatica'],
                ['arthritis'],
                ['tendonitis']
            ]
        }
        return pd.DataFrame(data)
    
    def train(self):
        df = self.create_enhanced_data()
        X = self.vectorizer.fit_transform(df['symptoms'])
        y = self.mlb.fit_transform(df['conditions'])
        
        self.model = OneVsRestClassifier(LogisticRegression(max_iter=1000))
        self.model.fit(X, y)
        
        # Save the improved model
        joblib.dump(self.vectorizer, 'vectorizer.joblib')
        joblib.dump(self.mlb, 'multilabel_binarizer.joblib')
        joblib.dump(self.model, 'symptom_classifier.joblib')
        
        print("Improved model training completed!")
        print(f"Trained on {len(df)} samples")
        print("Conditions available:", list(self.mlb.classes_))

if __name__ == '__main__':
    classifier = ImprovedSymptomClassifier()
    classifier.train()