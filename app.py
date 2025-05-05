# streamlit_app.py
import streamlit as st
import numpy as np
import joblib

model = joblib.load('model.pkl')

def preprocess_input(int_features):
    if int_features[0]==0:
        f_features = [0,0,0]+int_features[1:]
    elif int_features[0]==1:
        f_features = [1,0,0]+int_features[1:]
    elif int_features[0]==2:
        f_features = [0,1,0]+int_features[1:]
    else:
        f_features = [0,0,1]+int_features[1:]

    if f_features[6]==0:
        fn_features = f_features[:6]+[0,0]+f_features[7:]
    elif f_features[6]==1:
        fn_features = f_features[:6]+[1,0]+f_features[7:]
    else:
        fn_features = f_features[:6]+[0,1]+f_features[7:]

    return np.array(fn_features)

st.title("Intrusion Detection System")

# Create input fields
input_values = []
input_values.append(st.selectbox("Protocol Type", [0, 1, 2], format_func=lambda x: ['tcp', 'udp', 'icmp'][x]))
for i in range(1, 10):  # Replace with actual feature names if available
    input_values.append(st.number_input(f"Feature {i}", step=0.01))

if st.button("Predict"):
    features = preprocess_input(input_values)
    prediction = model.predict([features])[0]

    labels = ['Normal', 'DOS', 'PROBE', 'R2L', 'U2R']
    st.success(f"Prediction: {labels[prediction]}")
