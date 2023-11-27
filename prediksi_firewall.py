import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler, StandardScaler
# Load model 

firewall_model = 'best_random_forest_model.pkl'  
with open(firewall_model, 'rb') as file:
    loaded_rf_model = pickle.load(file)
zscore_scaler ='normalized_ZScore.pkl'
with open(zscore_scaler, 'rb') as file:
    loaded_zscore_scaler = pickle.load(file)
minmax_scaler ='normalized_minmax.pkl'
with open(minmax_scaler, 'rb') as file: 
    loaded_minmax_scaler = pickle.load(file)
st.title("Data Mining Prediksi Firewall")
st.write("Klasifikasi menggunakan Decision Tree")
st.write("## Dataset: https://archive.ics.uci.edu/dataset/542/internet+firewall+datas")
# Fungsi untuk mereset nilai input
def reset_input():
    st.sidebar.number_input("Source Port", value=0, key='source_port')
    st.sidebar.number_input("Destination Port", value=0, key='destination_port')
    st.sidebar.number_input("NAT Source", value=0, key='nat_source_port')
    st.sidebar.number_input("NAT Destination", value=0, key='nat_destination_port')
    st.sidebar.number_input("Bytes", value=0, key='bytes')
    st.sidebar.number_input("Bytes Sent", value=0, key='bytes_sent')
    st.sidebar.number_input("Bytes Received", value=0, key='bytes_received')
    st.sidebar.number_input("Packets", value=0, key='packets')
    st.sidebar.number_input("Elapsed Time (Sec)", value=0, key='elapsed_time')
    st.sidebar.number_input("Packets Sent", value=0, key='pkts_sent')
    st.sidebar.number_input("Packets received", value=0, key='pkts_received')
# best_preprocessing = "Z-Score"
# Input pengguna
st.sidebar.header("Input Pengguna")
reset_input_button = st.sidebar.button("Reset Input")
if reset_input_button:
    reset_input()

# Load konfigurasi terbaik
source_port = st.number_input("Source Port")
destination_port = st.number_input("Destination Port")
nat_source_port = st.number_input("NAT Source Port")
nat_destination_port = st.number_input("NAT Destination Port")
bytes = st.number_input("Bytes")
bytes_sent = st.number_input("Bytes Sent")
bytes_received = st.number_input("Bytes Received")
packets = st.number_input("Packets")
elapsed_time = st.number_input("Elapsed Time (sec)")
pkts_sent = st.number_input("Packets Sent")
pkts_received = st.number_input("Packets received")

# Menggabungkan input pengguna menjadi DataFrame
user_input = pd.DataFrame({
    'Source Port': [source_port],
    'Destination Port': [destination_port],
    'NAT Source Port': [nat_source_port],
    'NAT Destination Port': [nat_destination_port],
    'Bytes': [bytes],
    'Bytes Sent': [bytes_sent],
    'Bytes Received': [bytes_received],
    'Packets': [packets],
    'Elapsed Time (sec)': [elapsed_time],
    'pkts_sent': [pkts_sent],
    'pkts_received': [pkts_received],
})
first_tree = loaded_rf_model.estimators_[0]
feature_names = user_input.columns
st.sidebar.write("Nama-nama fitur pada data pelatihan:",feature_names)
predict_button = st.button("Prediksi")
if predict_button:
    for col in user_input.columns:
        try:
            user_input[col] = user_input[col].astype(float)
        except ValueError as e:
            st.error(f"Error converting column {col} to float: {e}")

    user_input_zscore = loaded_zscore_scaler.transform(user_input)
    user_input_minmax = loaded_minmax_scaler.transform(user_input)

    prediction_zscore = loaded_rf_model.predict(user_input_zscore)
    prediction_minmax = loaded_rf_model.predict(user_input_minmax)
    # Menampilkan hasil prediksi
    st.subheader("Prediction (Z-Score):")
    st.write(prediction_zscore[0])
    st.subheader("Prediction (MinMax):")
    st.write(prediction_minmax[0])
