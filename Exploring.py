import streamlit as st
import numpy as np
import pandas as pd

def app():

    st.title('Youtube Channel Explorer')
    st.write('_This is a web app to store, explore and visualize the data of your favorite youtube channels_')
    data=pd.DataFrame(np.random.randn(50, 2), columns=['x','y'])
    st.area_chart(data)
