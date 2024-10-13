import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")


st.sidebar.title("Split Panel")

st.title("Split-panel Map")

st.subheader("Can show comparison between different metrics or timeline")



#bus services from our model
options = [11, 21, 33, 57, 110, 858]
st.selectbox('Select bus service', options)

st.subheader("E.g: Compare 2017 vs 2024 difference")
m1 = leafmap.Map()
m1.split_map(left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020")
m1.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
m1.to_streamlit(height=700)

st.subheader("E.g: Compare Bus routes and passenger volume")
m2 = leafmap.Map()
m2.split_map(left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020")
m2.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
m2.to_streamlit(height=700)