from flask import Flask, request, jsonify
from flask_cors import CORS
from model import SymptomModel

app = Flask(__name__)
CORS(app)

# Initialize the model
print("🔄 Loading symptom checker model...")
try:
    symptom_model = SymptomModel()
    print("✅ Symptom Checker is ready!")
except Exception as e:
    print(f"❌ Failed to initialize model: {e}")
    symptom_model = None

@app.route('/')
def home():
    return jsonify({
        "message": "Symptom Checker API is running!",
        "model_loaded": symptom_model is not None,
        "status": "healthy"
    })

@app.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    try:
        if not symptom_model:
            return jsonify({
                "error": "Symptom model is not available. Please try again later."
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        symptoms = data.get('symptoms', '').strip()
        if not symptoms:
            return jsonify({"error": "Please describe your symptoms"}), 400
        
        print(f"📥 Received symptoms: '{symptoms}'")
        
        # Predict conditions
        conditions = symptom_model.predict_conditions(symptoms)
        
        # Get next steps
        next_steps = symptom_model.get_next_steps(conditions)
        
        response = {
            "symptoms": symptoms,
            "conditions": conditions,
            "next_steps": next_steps,
            "timestamp": "2024-01-01"  # Simple timestamp
        }
        
        print(f"📤 Sending response with {len(conditions)} conditions")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "conditions": [],
            "next_steps": ["Please try again or consult a healthcare professional"]
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "running",
        "model_loaded": symptom_model is not None,
        "service": "symptom-checker"
    })

if __name__ == '__main__':
    print("🚀 Starting Symptom Checker API...")
    print("📍 Server will be available at: http://127.0.0.1:5000")
    print("📍 Frontend should connect to: http://127.0.0.1:5000/analyze-symptoms")
    app.run(debug=True, host='0.0.0.0', port=5000)