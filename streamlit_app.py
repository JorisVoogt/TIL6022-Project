import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# To run this streamlit application, run in a terminal: streamlit run streamlit_app.py

# Streamlit cheat sheet:
# https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

# Sets sidebar for streamlit page
sidebar = st.sidebar
sidebar.title('European road safety')
sidebar.write("""
This application shows data about roads in European countries 
and analyses their safety with regards to the countries GDP. 
""")

# Read in prepared data set, rename a column and extract the different years
df = pd.read_csv("Data/pg_GDP_map.csv")
df = df.rename(columns={"pg_GDP": "index"})
years = df.year.unique()

# Calculate max value for continuous colour range
max_pg_gdp = df['index'].max()

# Get year from user and apply to dataset
given_year = st.select_slider('Select year to visualise:', years)
st.write('You selected the year ' + str(given_year))
df_new = df.query('year=='+str(given_year))
customdata = df_new['country']

# Create choropleth figure
fig = px.choropleth(df_new,
                    # Iso-alpha-3 codes to signify which country
                    locations="iso_alpha",
                    color="index",
                    hover_name="country",
                    # Gray represents countries with no available data.
                    color_continuous_scale=[[0, 'gray'], [0.01, 'gray'], [0.01, 'blue'], [1, 'red']],
                    projection='miller',
                    range_color=(0,max_pg_gdp),
                    scope='europe'
                    )

# Sets hover data
fig.update_traces(customdata=customdata,
                  hovertemplate=np.select([df_new["index"] == 0],
                                          ["<b>Country: </b> %{customdata}<br><br>No data available"],
                                          "<b>Country: </b>%{customdata}<br><br><b>Index value: </b>%{z}"))

# Gets value for the entire EU
numb = df_new.query('country=="EU"')["index"]

# Set title and EU index
fig.update_layout(title="<b>Volume of passengers relative to GDP in " + str(given_year)
                        + " (2015 base year)</b><br>EU index: " + str(numb.tolist()[0]),
                  coloraxis_colorbar=dict(x=0,
                                          y=0.5)
                  )

# Set figure size
fig.update_layout(width=1000,
                  height=600)

# Shows figure on streamlit page
st.plotly_chart(fig)
