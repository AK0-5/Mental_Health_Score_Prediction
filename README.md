# Mental Health Score Prediction
A machine learning web app that predicts a student's Mental Health Score (0–10) based on their lifestyle, academic, and social media habits.

## 📖 About
Student Wellbeing Lab lets users input their daily habits — sleep, study time, physical activity, stress level, and social media usage — and returns a predicted mental health score displayed on an interactive gauge.

The project has two parts:

FastAPI backend — serves the trained ML model
Streamlit frontend — a clean dark-themed dashboard

## 📂 Project Structure
text

├── app.py                     # Streamlit frontend

├── main.py                    # FastAPI backend

├── Mental_Health_Model.pkl    # Trained scikit-learn model

├── config.toml                # Streamlit theme config

├── requirements.txt           # Dependencies

└── README.md

## 🛠 Tech Stack
- Model: scikit-learn (Random Forest in a Pipeline)
- Backend: FastAPI + Pydantic
- Frontend: Streamlit + Plotly
- Other: pandas, numpy, joblib

Run Locally
1. Clone & install
bash
git clone https://github.com/<your-username>/student-wellbeing-lab.git
cd student-wellbeing-lab

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

2. Start the API
bash
##### uvicorn main:app --reload --port 8000
API docs available at: http://localhost:8000/docs

3. Start the app
bash
##### streamlit run app.py
Then in the sidebar, set the API URL to http://localhost:8000 and click Check API connection.

## 🔌 API
POST /predict
Request:

json
{
-  "age": 21,
-  "gender": "Female",
-  "country": "India",
-  "academic_level": "Undergraduate",
-  "most_used_platform": "Instagram",
-  "purpose_of_use": "Entertainment",
-  "avg_daily_usage_hours": 4.5,
-  "daily_unlocks": 120,
-  "study_hours": 3.0,
-  "physical_activity_hours": 1.5,
-  "sleep_hours_per_night": 6.5,
-  "stress_level": "Medium"
}

Response:

json

{ 
  "predicted_mental_health_score": 7   
}

## 📦 Requirements
- streamlit
- fastapi
- uvicorn
- scikit-learn
- joblib
- pandas
- numpy
- pydantic
- requests
