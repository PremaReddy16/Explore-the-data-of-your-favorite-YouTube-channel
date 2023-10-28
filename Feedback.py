import streamlit as st

def app():

    st.select_slider(
    'Select the Level',
    options= ['Practice More', 'Excellent', 'Awesome', 'Outstanding'])

    st.text_area('Comments:' )
    st.write('# :orange[Thanks for your valuable time😊]')