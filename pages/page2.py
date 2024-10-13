import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


st.sidebar.title("Output")

st.title("Recommendations")

# Sample data for demonstration (replace with real data)
bus_data = pd.DataFrame({
    'route_id': [1, 2],
    'stop_id': [101, 102],
    'latitude': [1.3521, 1.3551],
    'longitude': [103.8198, 103.8259],
})

mrt_data = pd.DataFrame({
    'station_id': [201, 202],
    'station_name': ['Station 1', 'Station 2'],
    'latitude': [1.3521, 1.3601],
    'longitude': [103.8198, 103.8310],
})

passenger_volume = pd.DataFrame({
    'route_id': [1, 2, 201, 202],
    'transport_type': ['bus', 'bus', 'mrt', 'mrt'],
    'passenger_volume': [500, 600, 1500, 1200],
})


# Table of routes for review
def routes_for_review_table(bus_data, passenger_volume):
    # Dummy calculation of overlap ratio (replace with actual analysis)
    overlap_ratios = [0.85, 0.65]  # Example data
    recommendations = ["Reduce Frequency", "Cancel Route"]

    bus_data['overlap_ratio'] = overlap_ratios
    bus_data['recommendation'] = recommendations

    st.table(bus_data[['route_id', 'overlap_ratio', 'recommendation']])

routes_for_review_table(bus_data, passenger_volume)