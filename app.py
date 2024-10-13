import streamlit as st

# Streamlit app layout
st.title("Bus and MRT Route Analysis Dashboard")

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

# Explanation about our solution
st.subheader("Explanation about how our proposed solution works")
st.markdown(
    """
    Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum
    """
)

# Create a form to hold the slider and checkbox components
with st.form(key='my_form'):
    # Slider for overlap percentage threshold
    threshold = st.slider('Select overlap % threshold for service change recommendation', 0.0, 1.0, 0.7)

    # Checkboxes for Regions
    regions_selected = st.multiselect(
        'Select the regions to analyse',
        ['Central Region', 'North Region', 'North-East Region', 'East Region', 'West Region'],
        default=['Central Region']
    )

    other_factors = st.slider('Select value for other factors', 0.0, 1.0, 0.7)
    
    # Add a submit button
    submit_button = st.form_submit_button(label='Submit')

# Handle form submission
if submit_button:
    # The app will only run this block after the form is submitted
    st.write('threshold Value: ', threshold)
    st.write('regions_selected Value: ', regions_selected)
    st.write('other factors Value: ', other_factors)




