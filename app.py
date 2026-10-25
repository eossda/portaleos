import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Network Monitoring", page_icon="📡", layout="wide")

st.title("📡 Network Status & Traffic Monitoring")
st.markdown("Pemantauan *real-time* status perangkat site, latensi ICMP, dan grafik Cacti NMS.")

# Simulasi Data Status Perangkat Site
data_status = pd.DataFrame({
    "Site Name": ["Site Regional A", "Site Regional B", "Site Regional C", "Site Regional D"],
    "IP Address": ["10.60.10.1", "10.60.20.1", "10.60.30.1", "10.60.40.1"],
    "Vendor": ["Cisco", "Huawei", "MikroTik", "FortiGate"],
    "Status": ["UP", "UP", "DOWN", "UP"],
    "Latency (ms)": [12.4, 18.1, 0.0, 8.5]
})

# Filter Status di Sidebar
st.sidebar.subheader("Filter Monitoring")
status_filter = st.sidebar.multiselect("Pilih Status", options=data_status["Status"].unique(), default=["UP", "DOWN"])
filtered_data = data_status[data_status["Status"].isin(status_filter)]

# Tampilkan Metrik Ringkasan
col1, col2, col3 = st.columns(3)
col1.metric("Total Perangkat", len(data_status))
col2.metric("Perangkat UP", len(data_status[data_status["Status"] == "UP"]))
col3.metric("Perangkat DOWN", len(data_status[data_status["Status"] == "DOWN"]), delta="-1", delta_color="inverse")

st.divider()

# Layout Kolom: Tabel Status & Grafik Latensi
col_table, col_chart = st.columns([1.2, 1])

with col_table:
    st.subheader("📋 Status Perangkat Site")
    st.dataframe(filtered_data, use_container_width=True)

with col_chart:
    st.subheader("📈 Grafik Latensi Rata-rata")
    fig = px.bar(filtered_data, x="Site Name", y="Latency (ms)", color="Status", 
                 color_discrete_map={"UP": "#2ecc71", "DOWN": "#e74c3c"})
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Integrasi Grafik Cacti NMS
st.subheader("🌐 Cacti NMS Traffic Integration")
st.markdown("Menampilkan grafik trafik WAN uplink dari server Cacti NMS pusat.")
# Contoh penyematan gambar/grafik dari Cacti URL (pastikan otentikasi aman atau di dalam jaringan lokal)
cacti_graph_url = "http://your-cacti-server/graph_image.php?local_graph_id=46&rra_id=all"
st.image(cacti_graph_url, caption="Cacti WAN Uplink Traffic - 24 Hours", use_container_width=True)