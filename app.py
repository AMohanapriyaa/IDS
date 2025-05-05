import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load("model.pkl")

# One-hot encoding preprocessing (updated for binary classification)
def preprocess_input(inputs):
    protocol = int(inputs[0])
    service = int(inputs[7])

    # One-hot encode protocol type (tcp=0, udp=1, icmp=2)
    proto_encoded = [0, 0, 0]
    if protocol in [0, 1, 2]:
        proto_encoded[protocol] = 1

    # One-hot encode service type (0, 1, 2) => 2 bits
    service_encoded = [0, 0]
    if service == 1:
        service_encoded = [1, 0]
    elif service == 2:
        service_encoded = [0, 1]

    # Numerical features (excluding protocol/service)
    numerical = inputs[1:7] + inputs[8:]

    # Final feature vector
    final_input = proto_encoded + numerical[:6] + service_encoded + numerical[6:]
    return np.array(final_input)

# Streamlit UI
st.set_page_config(page_title="Network Intrusion Detection", layout="centered")
st.title("🔐 AI-Powered Intrusion Detection System")
st.markdown("Check if your device might be **at risk** while connecting to a network.")

# Input UI
protocol_map = {"tcp": 0, "udp": 1, "icmp": 2}
protocol = st.selectbox("Protocol Type", list(protocol_map.keys()))
f1 = st.number_input("Feature 1 (e.g. duration)")
f2 = st.number_input("Feature 2")
f3 = st.number_input("Feature 3")
f4 = st.number_input("Feature 4")
f5 = st.number_input("Feature 5")
f6 = st.number_input("Feature 6")
service = st.selectbox("Service Type (Feature 7)", [0, 1, 2])
f8 = st.number_input("Feature 8")
f9 = st.number_input("Feature 9")

# Predict Button
if st.button("🔍 Analyze Network Connection"):
    input_list = [
        protocol_map[protocol], f1, f2, f3, f4, f5, f6, service, f8, f9
    ]
    final_input = preprocess_input(input_list)
    prediction = model.predict([final_input])[0]

    if prediction == 1:
        st.error("🚨 WARNING: Suspicious activity detected! Your phone **might be at risk** if you connect to this network.")
    else:
        st.success("✅ All clear. This network connection looks safe.")

    st.write(f"Raw Prediction: {'Anomaly' if prediction == 1 else 'Normal'}")
