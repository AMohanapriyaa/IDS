import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load('model.pkl')

# Preprocessing function
def preprocess_input(int_features):
    # One-hot for feature[0]
    if int_features[0] == 0:
        f_features = [0, 0, 0] + int_features[1:]
    elif int_features[0] == 1:
        f_features = [1, 0, 0] + int_features[1:]
    elif int_features[0] == 2:
        f_features = [0, 1, 0] + int_features[1:]
    else:
        f_features = [0, 0, 1] + int_features[1:]

    # One-hot for feature[6] (was originally feature index 6, now at 9 after first one-hot)
    if f_features[6] == 0:
        fn_features = f_features[:6] + [0, 0] + f_features[7:]
    elif f_features[6] == 1:
        fn_features = f_features[:6] + [1, 0] + f_features[7:]
    else:
        fn_features = f_features[:6] + [0, 1] + f_features[7:]

    return np.array(fn_features)

# UI
st.title("Intrusion Detection System")

# Collect inputs
protocol = st.selectbox("Protocol Type", [0, 1, 2], format_func=lambda x: ['tcp', 'udp', 'icmp'][x])
features = [protocol]
for i in range(1, 10):
    features.append(st.number_input(f"Feature {i}", step=0.01))

if st.button("Predict"):
    input_array = preprocess_input(features)
    prediction = model.predict([input_array])[0]
    labels = ['Normal', 'DOS', 'PROBE', 'R2L', 'U2R']
    st.success(f"Prediction: {labels[prediction]}")
