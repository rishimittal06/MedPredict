import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import plotly.express as px
import requests

# Load models
maternal_model = pickle.load(open("finalized_maternal_model.sav", 'rb'))
fetal_model = pickle.load(open("fetal_health_classifier.sav", 'rb'))

# Sidebar for navigation
with st.sidebar:
    st.title("MedPredict")
    st.write("Welcome to MedPredict")
    st.write("Choose an option from the menu below to get started:")

    selected = option_menu('MedPredict',
                           ['About us', 'Pregnancy Risk Prediction', 'Fetal Health Prediction'],
                           icons=['chat-square-text', 'hospital', 'capsule-pill', 'clipboard-data'],
                           default_index=0)

# About Us Section
if selected == 'About us':
    st.title("Welcome to MedPredict")
    st.write("At MedPredict, our mission is to revolutionize healthcare by offering innovative solutions through predictive analysis. "
             "Our platform is specifically designed to address the intricate aspects of maternal and fetal health, providing accurate "
             "predictions and proactive risk management.")

    col1, col2 = st.columns(2)
    with col1:
        st.header("1. Pregnancy Risk Prediction")
        st.write("Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, "
                 "body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of "
                 "potential risks during pregnancy.")
        st.image("graphics/pregnancy_risk_image.jpg", caption="Pregnancy Risk Prediction", use_column_width=True)
    
    with col2:
        st.header("2. Fetal Health Prediction")
        st.write("Fetal Health Prediction is a crucial aspect of our system. We leverage cutting-edge technology to assess the "
                 "health status of the fetus. Through a comprehensive analysis of factors such as ultrasound data, maternal health, "
                 "and genetic factors, we deliver insights into the well-being of the unborn child.")
        st.image("graphics/fetal_health_image.jpg", caption="Fetal Health Prediction", use_column_width=True)
    
   

# Function to classify pregnancy risk
def classify_pregnancy_risk(age, diastolic_bp, bs, body_temp, heart_rate):
    risk_score = 0
    if age < 18 or age > 35:
        risk_score += 1
    if diastolic_bp < 60 or diastolic_bp > 90:
        risk_score += 1
    if bs < 3.5 or bs > 7.8:
        risk_score += 1
    if body_temp < 36 or body_temp > 38:
        risk_score += 1
    if heart_rate < 60 or heart_rate > 100:
        risk_score += 1

    if risk_score >= 3:
        return "High Risk"
    elif risk_score == 2:
        return "Medium Risk"
    else:
        return "Low Risk"

# Pregnancy Risk Prediction Page
if selected == 'Pregnancy Risk Prediction':
    st.title('Pregnancy Risk Prediction')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input('Age', min_value=10, max_value=100, step=1)
    with col2:
        diastolic_bp = st.number_input('Diastolic BP (mmHg)', min_value=30, max_value=200, step=1)
    with col3:
        bs = st.number_input('Blood Sugar (mmol/L)', min_value=0.0, max_value=20.0, step=0.1)
    with col1:
        body_temp = st.number_input('Body Temperature (°C)', min_value=30.0, max_value=45.0, step=0.1)
    with col2:
        heart_rate = st.number_input('Heart Rate (bpm)', min_value=40, max_value=200, step=1)
    
    if st.button('Predict Pregnancy Risk'):
        risk = classify_pregnancy_risk(age, diastolic_bp, bs, body_temp, heart_rate)
        st.write("Risk Level:", risk)

# Fetal Health Prediction Page
def classify_fetal_risk(baseline_value, accelerations, fetal_movement, uterine_contractions,
                         light_decelerations, severe_decelerations, prolongued_decelerations,
                         abnormal_short_term_variability, mean_short_term_variability,
                         percentage_abnormal_long_term_variability, mean_long_term_variability,
                         histogram_width, histogram_min, histogram_max, histogram_peaks,
                         histogram_zeroes, histogram_mode, histogram_mean, histogram_median,
                         histogram_variance, histogram_tendency):

    risk_score = 0

    # Criteria for high risk
    if baseline_value < 110 or baseline_value > 160:
        risk_score += 1
    if accelerations < 0.002:
        risk_score += 1
    if fetal_movement < 0.2:
        risk_score += 1
    if uterine_contractions > 0.01:
        risk_score += 1
    if light_decelerations > 0.05:
        risk_score += 1
    if severe_decelerations > 0:
        risk_score += 1
    if prolongued_decelerations > 0:
        risk_score += 1
    if abnormal_short_term_variability > 0:
        risk_score += 1
    if mean_short_term_variability < 3:
        risk_score += 1
    if percentage_abnormal_long_term_variability > 60:
        risk_score += 1
    if mean_long_term_variability < 10:
        risk_score += 1

    # Histogram-based checks
    if histogram_width < 10 or histogram_width > 60:
        risk_score += 1
    if histogram_min < 60 or histogram_max > 160:
        risk_score += 1
    if histogram_peaks < 2:
        risk_score += 1
    if histogram_zeroes > 2:
        risk_score += 1
    if histogram_mode < 70 or histogram_mode > 150:
        risk_score += 1
    if histogram_mean < 80 or histogram_mean > 140:
        risk_score += 1
    if histogram_median < 80 or histogram_median > 140:
        risk_score += 1
    if histogram_variance > 10:
        risk_score += 1
    if abs(histogram_tendency) > 1:
        risk_score += 1

    # Assign risk level
    if risk_score >= 6:
        return "Pathological Risk"
    elif risk_score >= 3:
        return "Medium Risk"
    else:
        return "Low Risk"


if selected == 'Fetal Health Prediction':
    st.title('Fetal Health Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        baseline_value = st.number_input('Baseline Value', min_value=50, max_value=200, step=1)
        accelerations = st.number_input('Accelerations', min_value=0.0, max_value=1.0, step=0.001)
        fetal_movement = st.number_input('Fetal Movement', min_value=0.0, max_value=2.0, step=0.1)
        uterine_contractions = st.number_input('Uterine Contractions', min_value=0.0, max_value=1.0, step=0.001)
        light_decelerations = st.number_input('Light Decelerations', min_value=0.0, max_value=1.0, step=0.001)
        histogram_zeroes = st.number_input('Histogram Zeroes', min_value=0, max_value=10, step=1)
        histogram_mean = st.number_input('Histogram Mean', min_value=50, max_value=200, step=1)
    
    with col2:
        severe_decelerations = st.number_input('Severe Decelerations', min_value=0.0, max_value=1.0, step=0.001)
        prolongued_decelerations = st.number_input('Prolongued Decelerations', min_value=0.0, max_value=1.0, step=0.001)
        abnormal_short_term_variability = st.number_input('Abnormal Short Term Variability', min_value=0, max_value=10, step=1)
        mean_short_term_variability = st.number_input('Mean Short Term Variability', min_value=0, max_value=10, step=1)
        percentage_abnormal_long_term_variability = st.number_input('Percentage of Abnormal Long Term Variability', min_value=0, max_value=100, step=1)
        histogram_tendency = st.number_input('Histogram Tendency', min_value=-5, max_value=5, step=1)
        histogram_median = st.number_input('Histogram Median', min_value=50, max_value=200, step=1)
    
    with col3:
        mean_long_term_variability = st.number_input('Mean Long Term Variability', min_value=0, max_value=50, step=1)
        histogram_width = st.number_input('Histogram Width', min_value=0, max_value=100, step=1)
        histogram_min = st.number_input('Histogram Min', min_value=50, max_value=200, step=1)
        histogram_max = st.number_input('Histogram Max', min_value=50, max_value=200, step=1)
        histogram_peaks = st.number_input('Histogram Peaks', min_value=0, max_value=10, step=1)
        histogram_variance = st.number_input('Histogram Variance', min_value=0, max_value=50, step=1)
        histogram_mode = st.number_input('Histogram Mode', min_value=50, max_value=200, step=1)
        
        

    if st.button('Predict Fetal Health'):
        risk = classify_fetal_risk(
            baseline_value, accelerations, fetal_movement, uterine_contractions,
            light_decelerations, severe_decelerations, prolongued_decelerations,
            abnormal_short_term_variability, mean_short_term_variability,
            percentage_abnormal_long_term_variability, mean_long_term_variability,
            histogram_width, histogram_min, histogram_max, histogram_peaks,
            histogram_zeroes, histogram_mode, histogram_mean, histogram_median,
            histogram_variance, histogram_tendency
        )
        st.write("Fetal Health Risk Level:", risk)
