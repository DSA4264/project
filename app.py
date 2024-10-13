import streamlit as st
import streamlit_folium as st_folium

from main import sg_map

st.title("Streamlit baseline")

st.header("Map")

st.write("This currently presents a map of Singapore with MRT station and their exits")

st_folium.folium_static(sg_map)