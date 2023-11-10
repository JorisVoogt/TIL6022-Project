import streamlit as st
import plotly.express as px
import pandas as pd

# Set page name
st.set_page_config(
    page_title='Home',
    page_icon=':house_with_garden:',
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: white;'>Home Page</h1>", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>This mini project tries to answer the following question:
<br>
<b>Is there a correlation between road safety (number of injuries & deaths) and road infrastructure expenditures?</b>
</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>We hypothesize that more money spend on road infrastructure 
should reduce the number of injuries & deaths. In order to answer this question and test our hypothesis, we analyze the 
amount of road injuries & deaths and road infrastructure expenditures for different countries. Finally, we use scatter 
plots to see if there is a correlation.</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>Below, you can play around with the data which will be 
analyzed on the subsequent pages. Pick a year to visualize the data on the globes.</p>""", unsafe_allow_html=True)

# Read in dataframes
df_saf = pd.read_csv('data/streamlit/road_safety.csv')
df_exp = pd.read_csv('data/streamlit/road_expenditures.csv')

# Create year selection
year = st.select_slider('Select year:', df_saf['Year'].unique())

# Set total road expenditures percentage
df_exp['Total_Perc'] = df_exp['Perc_Maintenance'] + df_exp['Perc_Investments']

# Set chosen year in data
df_saf_year = df_saf[df_saf['Year'] == year]
df_exp_year = df_exp[df_exp['Year'] == year]

# Get max amount of injuries and percentage expenditures for a chosen year
max_injuries = df_saf_year['Injuries_passenger_kilometres'].max()
max_expenditures = df_exp_year['Total_Perc'].max()

# Set columns
col1, col2 = st.columns([0.5, 0.5], gap='large')

with col1:
    st.header('Injuries & deaths per 1B passenger km')

    # Create world plot injuries
    fig_world_saf = px.choropleth(df_saf_year,
                                  locations='COUNTRY',
                                  color='Injuries_passenger_kilometres',
                                  hover_name='Country',
                                  color_continuous_scale='Viridis',
                                  projection='orthographic',
                                  range_color=(0, max_injuries),
                                  hover_data=['Country', 'Injuries_passenger_kilometres']
                                  )

    fig_world_saf.update_layout(title='Road injuries & deaths per 1B passenger km',
                                height=500,
                                width=500,
                                coloraxis_colorbar_title='',
                                geo=dict(bgcolor='rgba(0,0,0,0)')
                                )

    fig_world_saf.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>'
                                              '<b>Injuries & deaths per 1B passenger km:</b> %{customdata[1]:,.0f}')

    st.plotly_chart(fig_world_saf, use_container_width=True)

with col2:
    st.header('Road infrastructure expenditures')

    # Create world plot expenditures
    fig_world_exp = px.choropleth(df_exp_year,
                                  locations='Location',
                                  color='Total_Perc',
                                  #hover_name='Country',
                                  color_continuous_scale='Viridis',
                                  projection='orthographic',
                                  range_color=(0, max_expenditures),
                                  hover_data=['Country', 'Total_Perc']
                                  )

    fig_world_exp.update_layout(title='Percentage of total expenditures spend on road infrastructure',
                                height=500,
                                width=500,
                                coloraxis_colorbar_title='',
                                geo=dict(bgcolor='rgba(0,0,0,0)')
                                )\

    fig_world_exp.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>'
                                              '<b>Percentage of total expenditures:</b> %{customdata[1]:,.2f}')

    st.plotly_chart(fig_world_exp, use_container_width=True)
