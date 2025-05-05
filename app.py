import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load("model.pkl")

# One-hot encoding preprocessing
def preprocess_input(inputs):
    protocol = int(inputs[0])
    service = int(inputs[7])

    # One-hot encode protocol type (3 values)
    proto_encoded = [0, 0, 0]
    if protocol in [0, 1, 2]:
        proto_encoded[protocol] = 1

    # One-hot encode service type (3 values assumed)
    service_encoded = [0, 0]
    if service == 1:
        service_encoded = [1, 0]
    elif service == 2:
        service_encoded = [0, 1]

    # Build final input array
    # Drop protocol and service from original input
    numerical = inputs[1:7] + inputs[8:]
    final_input = proto_encoded + numerical[:6] + service_encoded + numerical[6:]
    return np.array(final_input)

# Streamlit UI
st.title("Intrusion Detection System")

protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
protocol = st.selectbox("Protocol Type", list(protocol_map.keys()))
f1 = st.number_input("Feature 1")
f2 = st.number_input("Feature 2")
f3 = st.number_input("Feature 3")
f4 = st.number_input("Feature 4")
f5 = st.number_input("Feature 5")
f6 = st.number_input("Feature 6")
service = st.selectbox("Service Type (Feature 7)", [0, 1, 2])
f8 = st.number_input("Feature 8")
f9 = st.number_input("Feature 9")

if st.button("Predict"):
    input_list = [
        protocol_map[protocol], f1, f2, f3, f4, f5, f6, service, f8, f9
    ]
    final_input = preprocess_input(input_list)
    prediction = model.predict([final_input])[0]
    classes = ["Normal", "DOS", "PROBE", "R2L", "U2R"]
    st.success(f"Prediction: {classes[prediction]}")
