import pandas as pd
import streamlit as st

# Set page name
st.set_page_config(
    page_title='Data',
    page_icon=':bar_chart:',
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: white;'>Data</h1>", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>Here, you can look through the data used in this mini
project.</p>""", unsafe_allow_html=True)

# Read in safety and expenditures dataframes
df_saf = pd.read_csv('streamlit/data/app_data/road_safety.csv')
df_exp = pd.read_csv('streamlit/data/app_data/road_expenditures.csv')

# Create data selection
data = st.sidebar.selectbox('Select dataset:', ['Road Safety', 'Road Expenditures'])

# Show chosen dataframe
if data == 'Road Safety':
    st.dataframe(df_saf)

if data == 'Road Expenditures':
    st.dataframe(df_exp)
