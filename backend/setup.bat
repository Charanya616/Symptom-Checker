@echo off
echo Setting up Symptom Checker Backend...

:: Check if we're in the right directory
if exist "app.py" (
    echo Found app.py - good to go!
) else (
    echo Please make sure you're in the backend directory with all the Python files
    pause
    exit
)

:: Create virtual environment
echo Step 1: Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Step 2: Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Step 3: Installing dependencies...
pip install flask==2.3.3 flask-cors==4.0.0 scikit-learn==1.3.0 pandas==2.0.3 numpy==1.24.3 joblib==1.3.2 nltk==3.8.1

:: Train the model
echo Step 4: Training the model...
python train_model.py

:: Start the server
echo Step 5: Starting Flask server...
echo Server will start at http://127.0.0.1:5000
echo Keep this window open and open frontend/index.html in your browser
python app.py

pause