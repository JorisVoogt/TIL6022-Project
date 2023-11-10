import pandas as pd
import streamlit as st
import plotly.express as px

# Set page name
st.set_page_config(
    page_title='Correlation Research',
    page_icon=':microscope:',
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: white;'>Relation road safety & expenditures</h1>",
            unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>Here we analyse the relationship between road safety and 
road expenditures.<br> Our hypothesis is that higher road expenditures increase the road safety.</p>""",
            unsafe_allow_html=True)

# Read in road safety and expenditures files
df_safety = pd.read_csv('data/streamlit/road_safety.csv')
df_expend = pd.read_csv('data/streamlit/road_expenditures.csv')

# Concatenate required columns
df = pd.concat([df_safety['Year'],
                df_safety['Country'],
                df_safety['Population'],
                df_safety['Injuries_passenger_kilometres'],
                df_safety['Percentage_inj_pk_pop'],
                df_expend['Perc_Maintenance'],
                df_expend['Perc_Investments'],
                df_expend['Maintenance'],
                df_expend['Investments']
                ], axis=1)

# Sum total percentages road expenditures
df['Perc_Cost_Sum'] = df['Perc_Maintenance'] + df['Perc_Investments']
df['Cost_Sum'] = df['Maintenance'] + df['Investments']

st.markdown("""<p style='text-align: center; color: white;'>As our data only contains expenditures in local currencies,
we cannot simply compare countries to one another. Therefore, we first look if there is a correlation between road
expenditures and safety for individual countries. By picking a country from the sidebar, you can see its road
expenditures versus its injury & death ratio per 1B passenger kilometres over the time period 1995-2021 below.</p>""",
            unsafe_allow_html=True)

# Create country selection
country = st.sidebar.selectbox('Select country:', df['Country'].unique())

# Create dataframe for the selected country
df_country = df[df['Country'] == country]

# Scatter plot between costs and injuries per passenger kilometre
fig_sr = px.scatter(df_country,
                    x='Cost_Sum',
                    y='Injuries_passenger_kilometres',
                    color='Year',
                    color_continuous_scale='Viridis',
                    hover_data=['Country', 'Year']
                    )

fig_sr.update_layout(title='Correlation road expenditures and injuries/deaths for ' + country,
                     xaxis_title='Road expenditures (local currency)',
                     yaxis_title='Injuries/deaths per 1B passenger km'
                     )

fig_sr.update_traces(hovertemplate='<b>Country:</b> %{customdata[0]}<br>'
                                   '<b>Year:</b> %{customdata[1]}<br>'
                                   '<b>Road expenditures:</b> %{x:,.0f}<br>'
                                   '<b>Injuries/deaths per 1B passenger km:</b> %{y:,.0f}'
                                   '<extra></extra>')

# Setting x-axis to logarithmic scale
fig_sr.update_xaxes(type='log')

st.plotly_chart(fig_sr, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>Overall, there seems to be a correlation between road
expenditures and safety. However, some notable countries for which this is not true are: Japan, Türkiye and New Zealand.
In the case of Japan, we see that overtime, they spent less on roads, yet still had less injuries & deaths overall. 
New Zealand on the other hand spends more money over the years but does not seem to bring down the casualty number.
Finally, Türkiye seems to be a complete outlier as it not only spends more money on road infrastructure over the years,
but the injuries & deaths also increase. This could point to an expansion in road infrastructure and more people making
use of it.</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>We already found some counterexamples to our hypothesis.
In order to actually compare countries, we can make use of the percentage of government expenditures that is spend on
road infrastructure as seen in Road Infrastructure Expenditures. Furthermore, we notice that with the exception of
Türkiye, later years correlate with a lower injury/death rate. This can also be seen in Road Safety, where over the
years, the highest injuries & deaths ratio shows a decline.</p>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------------------------

st.markdown("""<p style='text-align: center; color: white;'>Below, we plot the percentage of government expenditures
spent on road infrastructure against the percentage of the population that is injured/killed per 1B passenger
kilometres.</p>""", unsafe_allow_html=True)

# Scatter plot to check correlation between percentage road expenditures and percentage road casualties
# relative to passenger kilometres and population.
fig_sc = px.scatter(df,
                    x='Perc_Cost_Sum',
                    y='Percentage_inj_pk_pop',
                    color='Country',
                    color_discrete_sequence=px.colors.qualitative.Alphabet,
                    hover_data=['Country', 'Year', 'Population']
                    )

fig_sc.update_layout(title='Correlation road expenditures and injuries/deaths',
                     xaxis_title='Percentage road expenditures',
                     yaxis_title='Percentage injuries/deaths'
                     )

fig_sc.update_traces(hovertemplate='<b>Country:</b> %{customdata[0]}<br>'
                                   '<b>Year:</b> %{customdata[1]}<br>'
                                   '<b>Population:</b> %{customdata[2]:,.0f}<br>'
                                   '<b>Percentage road expenditures:</b> %{x:,.1f}<br>'
                                   '<b>Percentage injury/death:</b> %{y:,.5f}<br>'
                                   '<extra></extra>')

fig_sc.update_xaxes(type='log')
fig_sc.update_yaxes(type='log')

st.plotly_chart(fig_sc, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>As we saw in Road Infrastructure Expenditures, the 
majority of the countries spend between 1% and 10% of their total expenditures on road infrastructure. However,
this scatter plot suggests there is no correlation between the percentage of expenditures spend on road infrastructure
and the amount of injuries & deaths. A good example here is Croatia who spends by far the most relatively speaking, yet
still has more relative injuries & deaths compared to Belgium who spends the least of its budget on road infrastructure.
</p>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------------------------

st.markdown("""<p style='text-align: center; color: white;'>Below, individual countries can be picked. Here, we compare
the correlations of percentage of total expenditures to total road expenditures, where the correlation of total road 
expenditures is the same as the one plotted at the top of this page.</p>""", unsafe_allow_html=True)

col1, col2 = st.columns([0.5, 0.5], gap='large')

with col1:
    st.header('Percentage of total expenditures')

    # Scatter plot to check correlation between percentage road expenditures and percentage road casualties
    # relative to passenger kilometres.
    fig_sc = px.scatter(df_country,
                        x='Perc_Cost_Sum',
                        y='Injuries_passenger_kilometres',
                        color='Year',
                        color_continuous_scale='Viridis',
                        hover_data=['Country', 'Year']
                        )

    fig_sc.update_layout(title='Correlation road expenditures and injuries/deaths for ' + country,
                         xaxis_title='Percentage road expenditures',
                         yaxis_title='Injuries/deaths per 1B passenger km'
                         )

    fig_sc.update_traces(hovertemplate='<b>Country:</b> %{customdata[0]}<br>'
                                       '<b>Year:</b> %{customdata[1]}<br>'
                                       '<b>Percentage road expenditures:</b> %{x:,.1f}<br>'
                                       '<b>Injuries/deaths per 1B passenger km:</b> %{y:,.0f}'
                                       '<extra></extra>')

    st.plotly_chart(fig_sc, use_container_width=True)

with col2:
    st.header('Total road expenditures')

    # Replot same scatter plot as the first one in this file
    st.plotly_chart(fig_sr, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>The comparisons above show that spending more money
on road infrastructure does not always equal spending more of your total expenditures. A good example here is the United
Kingdom. Over the years, the United Kingdom spends more money and the road injuries & deaths go down. However,
percentage wise, they actually spend less of their total expenditures on road infrastructure.
</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>We can conclude that our hypothesis which is that more money 
spend on road infrastructure leads to less injuries & deaths has been proven wrong. However, in the comparison above,
later years do seem to heavily correlate with fewer injuries & deaths, just like we noticed before.
We can theorize about a possible causation here. For example, cars have gotten safer throughout the years with built-in
automatic break systems and other tools to help the driver. Another cause could be lessons learned from dangerous
driving situations. Think about intersections being adjusted after several accidents or separation of motor vehicles and
bikes/scooters.</p>""", unsafe_allow_html=True)
