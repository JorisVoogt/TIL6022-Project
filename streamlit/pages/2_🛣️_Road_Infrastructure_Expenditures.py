import pandas as pd
import streamlit as st
import plotly.express as px

# Set page name
st.set_page_config(
    page_title='Road Expenditures',
    page_icon=':motorway:',
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: white;'>Road infrastructure expenditures</h1>",
            unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>Here we analyse the road maintenance and investment costs
for different countries relative to the total government expenditures.<br>On the sidebar, a particular year can be
chosen to investigate and compare countries, or a country can be chosen to investigate and see how the expenditures
change over the years.</p>""", unsafe_allow_html=True)

# Read in road expenditures file
df = pd.read_csv('streamlit/data/app_data/road_expenditures.csv')

# Create year and country selections
year = st.sidebar.select_slider('Select year:', df['Year'].unique())
country = st.sidebar.selectbox('Select country:', df['Country'].unique())

# ----------------------------------------------------------------------------------------------------------------------
# Create dataframe based upon chosen year
df_year = df[df['Year'] == year].copy()
# Drop entries with no maintenance and investments percentages
df_year.dropna(subset=['Perc_Maintenance', 'Perc_Investments'], inplace=True)

# Plot bar chart of countries maintenance and investments percentages for a specified year
fig_bar = px.bar(df_year,
                 x='Country',
                 y=['Perc_Maintenance', 'Perc_Investments']
                 )

fig_bar.update_layout(title='Percentage of total government expenditures spend on road maintenance and investments in '
                      + str(year),
                      yaxis_title='Percentage',
                      legend_title_text=''
                      )

# Update names for hovertemplate and legend
newnames = {'Perc_Maintenance': 'Percentage Maintenance', 'Perc_Investments': 'Percentage Investments'}
fig_bar.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name]))

fig_bar.data[0].hovertemplate = ('<b>Country:</b> %{x}<br><b>Year:</b> ' + str(year)
                                 + '<br><b>Percentage spend on maintenance:</b> %{y:.1f}%<extra></extra>')
fig_bar.data[1].hovertemplate = ('<b>Country:</b> %{x}<br><b>Year:</b> ' + str(year)
                                 + '<br><b>Percentage spend on investments:</b> %{y:.1f}%<extra></extra>')

st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# Create dataframe based upon chosen country
df_country = df[df['Country'] == country].copy()
# Drop entries with no maintenance and investments percentages
df_country.dropna(subset=['Perc_Maintenance', 'Perc_Investments'], inplace=True)

# Plot the bar
fig_bar = px.bar(df_country,
                 x='Year',
                 y=['Perc_Maintenance', 'Perc_Investments']
                 )

# Plot bar chart of a chosen countries maintenance and investments percentages
fig_bar.update_layout(title='Percentage of total government expenditures spend on road maintenance and investments of '
                      + country,
                      yaxis_title='Percentage',
                      legend_title_text=''
                      )

# Update the names for hovertemplate and legend
fig_bar.for_each_trace(lambda t: t.update(name=newnames[t.name], legendgroup=newnames[t.name]))

fig_bar.data[0].hovertemplate = ('<b>Country:</b> ' + country
                                 + '<br><b>Year:</b> %{x}<br>'
                                   '<b>Percentage spend on maintenance:</b> %{y:.1f}%<extra></extra>')
fig_bar.data[1].hovertemplate = ('<b>Country:</b> ' + country
                                 + '<br><b>Year:</b> %{x}<br>'
                                   '<b>Percentage spend on investments:</b> %{y:.1f}%<extra></extra>')

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>Most countries are below 5% total road costs for the period
1995-2021. Croatia, however, spends more and more to over 60% in 2003 after which it decreases
these expenditures to about 20% in 2021. Searching online, it seems that Croatia is indeed heavily investing in roads
while its rail network has actually reduced in size 
(<a href=https://bnn.network/world/croatia/croatias-road-rail-investment-gap-a-concern-for-sustainable-mobility/>
ref</a>). This article also states that it is unusual for a European country to do so, but looking at our data, it is 
also unusual compared to countries outside of the European Union.</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>We assume that investment costs are usually higher than 
maintenance costs. Although this seems to hold for most of the countries here, there are a few countries like Canada, 
Italy, and New Zealand for which this doesn't hold. In the case of Canada, this is true for the 90s and early 2000s.
For Italy and New Zealand, it seems to be more common. A reason for Italy could be the use of the established roads by 
the Roman Empire and thus requiring a lot of maintenance. For New Zealand, the fact that it is an island limits to a 
degree the amount of roads that can be build.</p>""", unsafe_allow_html=True)
