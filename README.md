# Air Quality Forecasting with Flask

## Abstract

This project presents an **Air Quality Forecasting System**, leveraging Flask and advanced machine learning techniques. By utilizing extensive historical air quality data and meteorological parameters, the system delivers accurate predictions of the **Air Quality Index (AQI)** for any chosen city and date. The user-friendly web interface allows users to select their city, date, and preferred prediction model, enhancing interaction and accessibility. This tool serves policymakers, environmentalists, and the public, fostering informed decision-making to combat air pollution.

## Introduction

As urbanization, industrialization, and environmental concerns rise, air quality has become a critical issue impacting public health and sustainability. This project introduces an advanced **Air Quality Forecasting System**, built with Flask and sophisticated machine learning models, aimed at delivering precise AQI forecasts tailored to specific cities and dates. By utilizing historical air quality data and meteorological parameters, the system applies diverse machine learning algorithms—such as Linear Regression, Random Forest Regression, and XGBoost—to generate highly accurate AQI predictions.

Key parameters influencing air quality dynamics, including PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, and Xylene, are integrated into the forecasting models. This integration provides stakeholders with comprehensive information on air quality variations and health risks, enabling informed decisions and targeted interventions. The intuitive web interface further enhances user engagement, allowing seamless selection of cities, dates, and prediction models.


## Data Preprocessing

### Dataset Description

The **"Air Quality Data in India (2015 - 2020)"** dataset offers a detailed overview of air quality metrics and AQI measurements from various stations and cities in India. It includes hourly and daily records, facilitating in-depth analysis of air quality trends over five years. The dataset covers key pollutant measurements and AQI categorizations across multiple cities, sourced from Kaggle and the Central Pollution Control Board.

### Handling Missing Values

To ensure data integrity, missing values were addressed using visualization techniques. Numerical columns related to pollutants were filled using mean imputation based on city and year. The ‘Date’ column was converted to datetime format, and missing values were appropriately handled to maintain dataset consistency.

### Feature Selection

Using **Mutual Information (MI)** scores, the most relevant features for predicting AQI were selected. This method identifies features with strong dependencies on the target variable, ensuring the model focuses on the most informative data.

## Methodology

### Models Used

Several machine learning models were employed for air quality prediction:

- **Linear Regression**: Provides insights into linear relationships between pollutants and AQI.
- **Random Forest**: Captures complex non-linear interactions among features, robust against outliers.
- **XGBoost**: Excels in structured data handling, optimizing performance through gradient boosting.
- **LightGBM**: Known for its speed and efficiency, suitable for large-scale datasets.
- **Artificial Neural Networks (ANN)**: Learns intricate patterns from diverse input data, ideal for non-linear AQI modeling.

### Flask Application

The Flask web application serves as the user interface for AQI prediction. It consists of several routes:

1. **/** (Index Route): Renders the main page with a dropdown for unique cities.
2. **/get-dates**: Accepts a city and returns available dates for selection.
3. **/predict**: Accepts user inputs, fetches relevant data, and predicts the AQI using the selected model. The results are rendered on a result page, displaying AQI value, category, and pollutant concentrations.

### Web Pages

- **index.html**: The landing page allows users to select city, date, and model type for prediction.
- **result.html**: Displays prediction results, AQI levels, and health implications, enhancing user understanding.

  ![image](https://github.com/user-attachments/assets/01a18257-c461-4ddc-88e5-ab37fa660756)
  
  ![image](https://github.com/user-attachments/assets/76f22711-c02e-46cf-b571-f7b7be48a952)



## Model Evaluation

Model performance was evaluated based on prediction accuracy and reliability, ensuring that the system delivers actionable insights for air quality management.

![image](https://github.com/user-attachments/assets/6c5aa721-1c5f-4b06-b51e-a9e3591fc1d1)


By providing accurate AQI forecasts and comprehensive air quality data, this project aims to support stakeholders in making informed decisions and fostering healthier communities in the face of air pollution challenges.
