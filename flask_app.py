from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load reference data
reference_data = pd.read_csv('datasets\clean_category_data.csv')


# Load linear regression model
#linear_model = joblib.load('linear_reg_model.pkl')

# Load random forest model
# random_forest_model = joblib.load('random_forest_reg.pkl')

@app.route('/')
def index():
    cities = reference_data['City'].unique().tolist()
    return render_template('index.html', cities=cities)

@app.route('/get_dates', methods=['POST'])
def get_dates():
    city = request.json['city']
    dates = reference_data.loc[reference_data['City'] == city, 'Date'].unique().tolist()
    return jsonify(dates)


# Modify the 'predict_air_quality' route in flask_app.py

@app.route('/predict', methods=['POST'])
def predict_air_quality():
    city = request.form['city']
    date = request.form['date']
    model_type = request.form['model']  # Get selected model type

    # Fetch data for selected city and date
    data = reference_data[(reference_data['City'] == city) & (reference_data['Date'] == date)]
    print("Data DataFrame:", data)  # Debugging print statement
    
    # Extract features
    features = data[['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3']]
    #poll_category = data[['PM2.5_category','PM10_category','NO2_category','CO_category','SO2_category']]

    # Get pollutant concentrations
    pollutants = list(features.columns)
    #poll_category = list(poll_category.columns)
    concentrations = features.values.tolist()
    flattened_concentrations = [val for sublist in concentrations for val in sublist]
    pollutant_concentrations = dict(zip(pollutants, flattened_concentrations))

    if model_type == 'random_forest':
        model = joblib.load('random_forest_reg.pkl')
    elif model_type == 'XGBoost':
        model = joblib.load('xgboost_reg.pkl')
    elif model_type == 'lightBGM':
        model = joblib.load('lgb_reg.pkl')
    else:
        return "Invalid model selection."

    # Predict AQI
    result = model.predict(features)
    predict_air_quality_index = round(result[0], 2)

    # Map AQI to category
    category_mapping = {
        (0, 50): "Good",
        (51, 100): "Satisfactory",
        (101, 200): "Moderate",
        (201, 300): "Poor",
        (301, 400): "Very Poor",
        (401, float('inf')): "Severe"
    }
    
    # Iterate through the category_mapping dictionary
    predicted_category = None
    for range_, category in category_mapping.items():
        if predict_air_quality_index <= range_[1]:
            predicted_category = category
            break

    # If predicted_category is still None, the value is out of range
    if predicted_category is None:
        predicted_category = "Undefined"

    # Fetch health implications for categories 3 to 6 of each pollutant
    health_implications = {
        'PM2.5': {
            "Average": " Pneumonia and bronchitis.",
            "Poor": " Difficulty in breathing, chest tightness, coughing, worsening of cardiovascular conditions, heart attacks, strokes.",
            "Very Poor": "Acute respiratory distress, increased risk of hospital admissions, exacerbation of chronic health conditions.",
            "Severe": "Acute respiratory distress syndrome (ARDS), cardiac events, potential life-threatening consequences."
        },
        'PM10': {
            "Average": "coughing, throat irritation, and shortness of breath.",
            "Poor": "Reduced lung function. Greater susceptibility to respiratory infections such as bronchitis and pneumonia.",
            "Very Poor": "Exacerbation of asthma and COPD. Increased risk of respiratory infections.",
            "Severe": "Severe respiratory distress, with symptoms becoming widespread and potentially life-threatening."
        },
        'CO': {
            "Average": "Headaches, dizziness, and nausea.",
            "Poor": "Headaches, dizziness, and nausea become more common. Chest pain and reduced exercise tolerance.",
            "Very Poor": "Extreme headaches, dizziness, and nausea are expected. Chest pain and potential cardiac arrhythmias.",
            "Severe": "Life-threatening symptoms such as loss of consciousness, seizures, and coma may occur rapidly."
        },
        'NO2': {
            "Average": "Worsening of asthma, decreased lung function and other respiratory conditions.",
            "Poor": "Coughing, wheezing, and shortness of breath may occur in the general population.",
            "Very Poor": "Severe coughing, wheezing, and shortness of breath, are expected. Risk of respiratory infections due to reduced lung function and compromised immune response.",
            "Severe": "Chest pain, palpitations, and other cardiovascular symptoms. Permanent lung damage and increased risk of cardiovascular events."
        },
        'SO2': {
            "Average": "Worsening of asthma, increased frequency of coughing, chest tightness, and difficulty breathing.",
            "Poor": "Severe coughing, wheezing, shortness of breath, and chest discomfort.",
            "Very Poor": "Severe coughing fits, difficulty breathing even at rest, audible wheezing and tightness in the chest.",
            "Severe": "Acute respiratory distress syndrome (ARDS), respiratory failure, severe bronchospasm, suffocation, and death."
        },
        'O3': {
            "Average": "Increased asthma symptoms, more frequent coughing, chest tightness, and slight difficulty in breathing.",
            "Poor": "Severe coughing, wheezing, moderate difficulty breathing, and discomfort in the chest.",
            "Very Poor": "Severe coughing fits, difficulty breathing even at rest, audible wheezing, and noticeable chest tightness.",
            "Severe": "Conditions such as acute respiratory distress syndrome (ARDS), respiratory failure, and suffocation may occur."
        }
    }
    
    # Pass health implications to the result.html template
    pollutant_health_implications = {}
    for pollutant, categories in health_implications.items():
        pollutant_category = data.get(f"{pollutant}_category")
        print(f"Pollutant: {pollutant}, Category: {pollutant_category}")  # Debugging print statement
        if pollutant_category is not None:
            pollutant_health_implications[pollutant] = categories.get(pollutant_category.iloc[0], "")  # Get health implications if category is 3 to 6
            print(f"Added health implication for {pollutant}")  # Debugging print statement

    print("Health implications:", pollutant_health_implications)  # Debugging print statement

    return render_template('result.html', city=city, date=date, data=data, pollutant_concentrations=pollutant_concentrations,pollutant_category=pollutant_category, AQI=predict_air_quality_index, category=predicted_category, health_implications=pollutant_health_implications)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
