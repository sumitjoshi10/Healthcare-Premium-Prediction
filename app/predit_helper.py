import pandas as pd
from joblib import load

model_young = load(r'app/artifacts/model_young_lr.joblib')
model_rest = load(r'app/artifacts/model_rest_xgb.joblib')


def calculate_total_risk_score(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    # Split the medical history into potential two parts and convert to lowercase
    diseases = medical_history.lower().split(" & ")

    # Calculate the total risk score by summing the risk scores for each part
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)  # Default to 0 if disease not found

    return total_risk_score

def preprocess_input(input_dict):
    
    df = pd.DataFrame(input_dict,columns=input_dict.keys(),index=[0])
    
    df['insurance_plan'] = df['insurance_plan'].map({'Bronze':1,'Silver':2, 'Gold':3})
    
    
    df['total_risk_score'] = df['medical_history'].apply(calculate_total_risk_score)
    
    df.drop('medical_history', axis='columns', inplace=True)
    
    return df
    
def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])
