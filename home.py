import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

maternal_model = pickle.load(open("model/finalized_maternal_model.sav",'rb'))
fetal_model = pickle.load(open("model/fetal_health_classifier.sav",'rb'))

# sidebar for navigation
with st.sidebar:
    st.title("MedPredict")
    st.write("Welcome to the MedPredict")
    st.write(" Choose an option from the menu below to get started:")

    selected = option_menu('MedPredict',
                          
                          ['About us',
                            'Pregnancy Risk Prediction',
                           'Fetal Health Prediction',
                           'Dashboard'],
                          icons=['chat-square-text','hospital','capsule-pill','clipboard-data'],
                          default_index=0)
    if (selected == 'About us'):
    
    st.title("Welcome to MedPredict")
    st.write("At MedPredict, our mission is to revolutionize healthcare by offering innovative solutions through predictive analysis. "
         "Our platform is specifically designed to address the intricate aspects of maternal and fetal health, providing accurate "
         "predictions and proactive risk management.")
    
    col1, col2= st.columns(2)
    with col1:
        # Section 1: Pregnancy Risk Prediction
        st.header("1. Pregnancy Risk Prediction")
        st.write("Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, "
                "body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of "
                "potential risks during pregnancy.")
        # Add an image for Pregnancy Risk Prediction
        st.image("graphics/pregnancy_risk_image.jpg", caption="Pregnancy Risk Prediction", use_column_width=True)
    with col2:
        # Section 2: Fetal Health Prediction
        st.header("2. Fetal Health Prediction")
        st.write("Fetal Health Prediction is a crucial aspect of our system. We leverage cutting-edge technology to assess the "
                "health status of the fetus. Through a comprehensive analysis of factors such as ultrasound data, maternal health, "
                "and genetic factors, we deliver insights into the well-being of the unborn child.")
        # Add an image for Fetal Health Prediction
        st.image("graphics/fetal_health_image.jpg", caption="Fetal Health Prediction", use_column_width=True)

    # Section 3: Dashboard
    st.header("3. Dashboard")
    st.write("Our Dashboard provides a user-friendly interface for monitoring and managing health data. It offers a holistic "
            "view of predictive analyses, allowing healthcare professionals and users to make informed decisions. The Dashboard "
            "is designed for ease of use and accessibility.")
    
    # Closing note
    st.write("Thank you for choosing E-Doctor. We are committed to advancing healthcare through technology and predictive analytics. "
            "Feel free to explore our features and take advantage of the insights we provide.")

def classify_pregnancy_risk(age, diastolic_bp, bs, body_temp, heart_rate):
    """Manually classify pregnancy risk based on predefined ranges."""
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

def classify_fetal_health(values):
    """Manually classify fetal health based on predefined thresholds."""
    normal_range = {
        'Baseline Value': (110, 160),
        'Accelerations': (0.0, 0.02),
        'Fetal Movement': (0.0, 0.5),
        'Uterine Contractions': (0.0, 0.015),
        'Light Decelerations': (0.0, 0.02),
        'Severe Decelerations': (0.0, 0.005),
        'Prolongued Decelerations': (0.0, 0.005),
        'Abnormal Short Term Variability': (0.0, 0.01),
        'Mean Short Term Variability': (5, 7),
        'Percentage of Abnormal Long Term Variability': (0, 40),
        'Mean Long Term Variability': (10, 25),
        'Histogram Width': (50, 70),
        'Histogram Min': (60, 80),
        'Histogram Max': (120, 160),
        'Histogram Peaks': (2, 6),
        'Histogram Zeroes': (0, 5),
        'Histogram Mode': (120, 140),
        'Histogram Mean': (120, 140),
        'Histogram Median': (120, 140),
        'Histogram Variance': (0, 20),
        'Histogram Tendency': (-1, 1)
    }
    
    abnormal_count = sum(1 for key, val in zip(normal_range.keys(), values) if not (val >= normal_range[key][0] and val <= normal_range[key][1]))
    
    if abnormal_count >= 6:
        return "Pathological"
    elif abnormal_count >= 3:
        return "Suspect"
    else:
        return "Normal"

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
    
if selected == 'Fetal Health Prediction':
    st.title('Fetal Health Prediction')
    
    input_fields = ['Baseline Value', 'Accelerations', 'Fetal Movement', 'Uterine Contractions',
                    'Light Decelerations', 'Severe Decelerations', 'Prolongued Decelerations',
                    'Abnormal Short Term Variability', 'Mean Short Term Variability',
                    'Percentage of Abnormal Long Term Variability', 'Mean Long Term Variability',
                    'Histogram Width', 'Histogram Min', 'Histogram Max', 'Histogram Peaks',
                    'Histogram Zeroes', 'Histogram Mode', 'Histogram Mean', 'Histogram Median',
                    'Histogram Variance', 'Histogram Tendency']
    
    user_inputs = [st.number_input(label, value=0.0) for label in input_fields]
    
    if st.button('Predict Fetal Health'):
        health_status = classify_fetal_health(user_inputs)
        st.write("Fetal Health Status:", health_status)
        
        if (selected == "Dashboard"):
    api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
    api_endpoint = api_endpoint= f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
    st.header("Dashboard")
    content = "Our interactive dashboard offers a comprehensive visual representation of maternal health achievements across diverse regions. The featured chart provides insights into the performance of each region concerning institutional deliveries compared to their assessed needs. It serves as a dynamic tool for assessing healthcare effectiveness, allowing users to quickly gauge the success of maternal health initiatives."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

    dashboard = MaternalHealthDashboard(api_endpoint)
    dashboard.create_bubble_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_bubble_chart_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

    dashboard.create_pie_chart()
    with st.expander("Show More"):
    # Display a portion of the data
        content = dashboard.get_pie_graph_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

