import joblib
import numpy as np

class SymptomModel:
    def __init__(self):
        self.vectorizer = None
        self.mlb = None
        self.model = None
        self.load_model()
    
    def load_model(self):
        try:
            self.vectorizer = joblib.load('vectorizer.joblib')
            self.mlb = joblib.load('multilabel_binarizer.joblib')
            self.model = joblib.load('symptom_classifier.joblib')
            print("✅ Model loaded successfully!")
            print(f"✅ Available conditions: {list(self.mlb.classes_)}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise Exception("Model files not found. Please run training script first.")
    
    def predict_conditions(self, symptoms_text):
        try:
            # Transform input
            X = self.vectorizer.transform([symptoms_text.lower()])
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)[0]
            
            # Debug: Show top probabilities
            top_indices = np.argsort(probabilities)[-5:][::-1]
            print(f"DEBUG - Input: '{symptoms_text}'")
            for idx in top_indices:
                if probabilities[idx] > 0.01:
                    print(f"  {self.mlb.classes_[idx]}: {probabilities[idx]:.3f}")
            
            # Get conditions with probability > 2%
            condition_probs = []
            for i, prob in enumerate(probabilities):
                if prob > 0.02:  # Very low threshold to catch something
                    condition_probs.append({
                        'name': self.mlb.classes_[i],
                        'probability': float(prob)
                    })
            
            # Sort by probability
            condition_probs.sort(key=lambda x: x['probability'], reverse=True)
            
            # If no conditions found, return at least the top one
            if not condition_probs and len(probabilities) > 0:
                top_idx = np.argmax(probabilities)
                if probabilities[top_idx] > 0.01:
                    condition_probs.append({
                        'name': self.mlb.classes_[top_idx],
                        'probability': float(probabilities[top_idx])
                    })
            
            return condition_probs[:5]  # Return top 5
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return []
    
    def get_next_steps(self, conditions):
        next_steps = [
            "Monitor your symptoms and note any changes",
            "Stay hydrated and get plenty of rest"
        ]
        
        if not conditions:
            next_steps.append("If symptoms persist, consult a healthcare professional")
            return next_steps
        
        condition_names = [cond['name'].lower() for cond in conditions]
        
        # General advice based on conditions
        if any(name in ['fever', 'influenza', 'viral infection'] for name in condition_names):
            next_steps.append("Monitor your temperature regularly")
            next_steps.append("Consider over-the-counter fever reducers if needed")
        
        if any(name in ['muscle', 'strain', 'arthritis', 'pain'] for name in condition_names):
            next_steps.append("Apply ice or heat to affected area")
            next_steps.append("Avoid strenuous activities")
        
        if any(name in ['cold', 'cough', 'respiratory'] for name in condition_names):
            next_steps.append("Use a humidifier to ease breathing")
            next_steps.append("Get plenty of rest")
        
        if any(cond['probability'] > 0.3 for cond in conditions):
            next_steps.append("Consider scheduling a doctor's appointment")
        
        return next_steps