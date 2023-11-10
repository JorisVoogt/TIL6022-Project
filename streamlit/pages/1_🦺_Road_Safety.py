import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objs as go

# Set page name
st.set_page_config(
    page_title='Road Safety',
    page_icon=':safety_vest:',
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: white;'>Road injuries & casualties</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: white;'>"
            "Here we analyse the road injuries and deaths for individual countries "
            "and compared to other countries."
            "<br>Let's start with looking at the amount of injuries and deaths per country "
            "and compared to other countries relative to their populations."
            "<br>On the sidebar, a country and year can be chosen to investigate.</p>", unsafe_allow_html=True)

# Read in road safety file
df = pd.read_csv('streamlit/data/app_data/road_safety.csv')

# Create country and year selections
country = st.sidebar.selectbox('Select country:', df['Country'].unique())
year = st.sidebar.select_slider('Select year:', df['Year'].unique())

# Create dataframes based upon year or country
df_country = df[df['Country'] == country].copy()
df_others = df[df['Country'] != country].copy()
df_year = df_others.query('Year==' + str(year)).copy()
df_country_year = df_country.query('Year==' + str(year)).copy()

# Remove entries with no injury data
df_country.dropna(subset=['Injuries'], inplace=True)
df_year.dropna(subset=['Injuries'], inplace=True)

# ----------------------------------------------------------------------------------------------------------------------
# Create streamlit page columns
col1, col2 = st.columns([0.4, 0.6], gap='large')

with col1:
    st.header('Per country')

    st.markdown("<p style='text-align: center; color: white;'>Here, the amount of road injuries and deaths are shown "
                "for a country in the period 1995-2021.</p>", unsafe_allow_html=True)

    # Create injury line graph for a country
    fig_line = px.line(df_country, x='Year', y='Injuries', markers=True)

    fig_line.update_layout(title='Road injuries & deaths in ' + country,
                           yaxis_title='Injuries and deaths')

    fig_line.update_traces(customdata=df_country['Population'],
                           hovertemplate='<b>Year:</b> %{x}<br><b>Population:</b> %{customdata:,.0f}<br><b>'
                                         'Injuries & Deaths:</b> %{y}')

    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.header('Compared to other countries')

    st.markdown("<p style='text-align: center; color: white;'>Here, we compare the chosen country to other countries "
                "by showing the percentage differences in road injuries and deaths relative to the populations "
                "for a particular year.</p>", unsafe_allow_html=True)

    # Calculate percentage change
    df_year['Percentage_change'] = ((df_year['Percentage_inj_pop']
                                     / df_country_year['Percentage_inj_pop'].values[0]) - 1)*100

    # Create histogram for all countries of an entered year
    fig_hist = px.histogram(df_year, x='Country', y='Percentage_change')

    fig_hist.update_layout(title='Percentage change in ' + str(year) + ' compared to ' + country,
                           yaxis_title='Percentage change',
                           showlegend=False
                           )

    fig_hist.update_traces(customdata=np.stack((df_year['Year'],
                                                df_year['Population'],
                                                df_year['Injuries']), axis=-1),
                           hovertemplate='<b>Country:</b> %{x}<br><b>Year:</b> %{customdata[0]}<br>'
                                         '<b>Population:</b> %{customdata[1]:,.0f}<br>'
                                         '<b>Road injuries & deaths:</b> %{customdata[2]:,.0f}<br>'
                                         '<b>Percentage change:</b> %{y:,.1f}%<extra></extra>'
                           )

    # If the chosen country has no injury data, cannot compare it to other countries
    if pd.isnull(df_country_year['Injuries'].iloc[0]):
        st.write('No data available for ' + country + ' in ' + str(year))
    else:
        st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# Get dataframes for the selected year and the year before
df_this_year = df.query('Year==' + str(year)).copy()
df_last_year = df.query('Year==' + str(year-1)).copy()

# Set best and worst percentage changes and countries
safest_val = df_this_year['Percentage_inj_pop'].min()
worst_val = df_this_year['Percentage_inj_pop'].max()
safest_val_last_year = df_last_year['Percentage_inj_pop'].min()
worst_val_last_year = df_last_year['Percentage_inj_pop'].max()
safest_countries = df_this_year[df_this_year['Percentage_inj_pop'] == safest_val]['Country']
worst_countries = df_this_year[df_this_year['Percentage_inj_pop'] == worst_val]['Country']

st.markdown("""<p style='text-align: center; color: white;'>Below, we show the two countries with the lowest and 
highest percentage of the countries population that is injured or dies in road accidents, and the difference between 
the two. We also look at the difference compared to the previous year.<p>""", unsafe_allow_html=True)

# Create columns for the metric data
col1, col2, col3 = st.columns([0.43, 0.43, 0.14])

# Set previous year values to this year if this year is the first year
if year == 1995:
    safest_val_last_year = safest_val
    worst_val_last_year = worst_val

# Create the metrics
with col1:
    st.metric(label='Relative best: ' + safest_countries.iloc[0],
              value='%.3f' % safest_val + '%',
              delta='%.4f' % float(safest_val-safest_val_last_year) + '%',
              delta_color='inverse'
              )

with col2:
    st.metric(label='Relative worst: ' + worst_countries.iloc[0],
              value='%.3f' % worst_val + '%',
              delta='%.4f' % float(worst_val-worst_val_last_year) + '%',
              delta_color='inverse'
              )

with col3:
    st.metric(label='Difference best worst',
              value='%.3f' % float(worst_val-safest_val) + '%',
              delta='%.4f' % float((worst_val-safest_val)-(worst_val_last_year-safest_val_last_year)) + '%',
              delta_color='inverse'
              )

# ----------------------------------------------------------------------------------------------------------------------

st.markdown("""<p style='text-align: center; color: white;'>To get an idea about the trend of road injuries & deaths, 
we plot the best and worst countries of each year against each other.</p>""", unsafe_allow_html=True)

years = []
rel_best = []
country_best = []
rel_worst = []
country_worst = []

# Create columns so relative best and worst countries can be put in a graph
for yr in df['Year'].unique():
    years.append(yr)
    df_y = df[df['Year'] == yr]

    df_b = df_y[df_y['Percentage_inj_pop'] == df_y['Percentage_inj_pop'].min()]
    df_w = df_y[df_y['Percentage_inj_pop'] == df_y['Percentage_inj_pop'].max()]

    rel_best.append(df_b['Percentage_inj_pop'].iloc[0])
    country_best.append(df_b['Country'].iloc[0])

    rel_worst.append(df_w['Percentage_inj_pop'].iloc[0])
    country_worst.append(df_w['Country'].iloc[0])

# New dataframe with relative best and worst countries
df_perc = pd.DataFrame(data={'Year': years,
                             'rel_b': rel_best,
                             'country_best': country_best,
                             'rel_w': rel_worst,
                             'country_worst': country_worst
                             })

# Create a line graph of relative best and worst countries
fig_line = px.line(df_perc,
                   x='Year',
                   y=['rel_b', 'rel_w'],
                   markers=True,
                   hover_data=['country_best', 'country_worst']
                   )

fig_line.update_layout(title='The lowest and highest percentages of road injuries & deaths relative to the populations',
                       yaxis_title='Percentage of population',
                       legend_title_text=''
                       )

# Update names for hovertemplate and legend
newnames = {'rel_b': 'Least injuries & deaths', 'rel_w': 'Most injuries & deaths'}
fig_line.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                           legendgroup=newnames[t.name]))

fig_line.data[0].hovertemplate = ('<b>Country:</b> %{customdata[0]}<br><b>Year:</b> %{x}<br><b>Percentage of '
                                  'population:</b> %{y:.4f}%<extra></extra>')
fig_line.data[1].hovertemplate = ('<b>Country:</b> %{customdata[1]}<br><b>Year:</b> %{x}<br><b>Percentage of '
                                  'population:</b> %{y:.2f}%<extra></extra>')

st.plotly_chart(fig_line, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>When looking at the above plot, overall the percentage 
of road injuries & deaths for the best countries seems to stay equal while the worst countries perform better over the 
years. However, as not all countries have data for each year, this affects both the set of best and worst countries. 
In the case of the worst countries, the United States performs worst for most of the years but is missing from 2019 
onwards. This is also seen in a relatively steep decline in the percentage of injuries and deaths. 
Although the best countries percentages do not seem to fluctuate as much, both The Netherlands and India have missing 
data while these two have the lowest percentages overall. This should both be taken into account when looking at the 
above plot.</p>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align: center; color: white;'>Of course, we should also take into account the amount of 
kilometres driven in a country. The assumption here is that the more people drive, the higher the total road injuries 
& deaths are. Let's see if the data shows this by scattering countries based upon passenger kilometres and road
injuries & deaths, and see if we have a linear increasing trend.</p>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------------------------

st.header('Passenger kilometres')

# Creating scatter plot dataframe using chosen year
df_sc = df.query('Year==' + str(year)).copy()

# Drop entries with no rows or passenger kilometres
df_sc.dropna(subset=['Injuries', 'Passenger_kilometres'], inplace=True)

# Plot passenger kilometres against injuries in a scatter plot
fig_scatter_pk = px.scatter(df_sc,
                            x='Passenger_kilometres',
                            y='Injuries',
                            size='Population',
                            color='Country',
                            color_discrete_sequence=px.colors.qualitative.Alphabet,
                            hover_data=['Country', 'Year', 'Population']
                            )

fig_scatter_pk.update_traces(hovertemplate='<b>Country:</b> %{customdata[0]}<br><b>Year:</b> %{customdata[1]}<br>'
                                           '<b>Population:</b> %{customdata[2]:,.0f}<br>'
                                           '<b>Passenger km in millions:</b> %{x}<br><b>Road injuries & deaths:'
                                           '</b> %{y}<extra></extra>')

# Get the line that best fits the scatter plot
p = np.polyfit(df_sc['Passenger_kilometres'], df_sc['Injuries'], 1)

# Create line data
df_line = df_sc['Passenger_kilometres'].sort_values()
f = np.poly1d(p)
x = df_sc['Passenger_kilometres'].sort_values()
y = f(x)

# Plot the best-fit line
fig_sc_line = px.line(df_sc, x=x, y=y)

# Combine scatter plot with best-fit line
fig_comb = go.Figure(data=fig_scatter_pk.data + fig_sc_line.data)

# Remembers scale button state
if 'clicked' not in st.session_state:
    st.session_state.clicked = False


# Changes state from True to False to True etc. when pressing the scale button
# Requires parameter to work, but is not used
def click_button(useless):
    st.session_state.clicked = not st.session_state.clicked


# Scale button
# Useless parameter makes it actually work as needed, but is not used
st.button('Click here to change the :scales: of the scatter plot', on_click=click_button, args=('Useless', ))


# Changes the scale of the scatter plot from linear to log and back again when scale button is clicked
def change_scales():
    if st.session_state.clicked:
        fig_comb.update_xaxes(type='log')
        fig_comb.update_yaxes(type='log')
    else:
        fig_comb.update_xaxes(type='linear')
        fig_comb.update_yaxes(type='linear')


change_scales()

fig_comb.update_layout(title='Road injuries and deaths relative to passenger km in ' + str(year),
                       xaxis_title='Passenger km in millions',
                       yaxis_title='Road injuries and deaths'
                       )

st.plotly_chart(fig_comb, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>Unsurprisingly, the scatter plot above shows a correlation
between km driven and road injuries & deaths. Therefore, we should take into account the total amount of passenger 
kilometres driven in a country when analysing road safety.</p>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------------------------------------
# Create columns
col1, col2 = st.columns([0.4, 0.6], gap='large')

with col1:
    st.header('Take into account passenger kilometres')

    st.markdown("""<p style='text-align: center; color: white;'>Here, the amount of road injuries and deaths per 1B "
                "passenger kilometres are shown for a country in the period 1995-2021.</p>""", unsafe_allow_html=True)

    # Create line graph for a countries injuries per passenger kilometres
    fig_line = px.line(df_country,
                       x='Year',
                       y='Injuries_passenger_kilometres',
                       markers=True
                       )

    fig_line.update_layout(title='Road injuries & deaths <br>per 1B passenger km in ' + country,
                           yaxis_title='Injuries and deaths'
                           )

    fig_line.update_traces(customdata=df_country['Population'],
                           hovertemplate='<b>Year:</b> %{x}<br><b>Population:</b> %{customdata:,.0f}<br>'
                                         '<b>Injuries & deaths per 1B passenger km:</b> %{y:.1f}')

    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.header('And compared to other countries')

    st.markdown("""<p style='text-align: center; color: white;'>Here, we compare the chosen country to other countries "
                "by showing the percentage differences in road injuries and deaths per 1B passenger kilometres "
                "relative to the populations for a particular year.</p>""", unsafe_allow_html=True)

    # Drop entries with no passenger kilometres
    df_year.dropna(subset=['Passenger_kilometres'], inplace=True)

    # Calculate percentage change
    df_year['Percentage_change'] = ((df_year['Percentage_inj_pk_pop']
                                     / df_country_year['Percentage_inj_pk_pop'].values[0]) - 1) * 100

    # Create histogram for specified year
    fig_hist = px.histogram(df_year, x='Country', y='Percentage_change')

    fig_hist.update_layout(title='Percentage change in ' + str(year) + ' compared to ' + country,
                           yaxis_title='Percentage change',
                           showlegend=False
                           )

    fig_hist.update_traces(customdata=np.stack((df_year['Year'],
                                                df_year['Population'],
                                                df_year['Passenger_kilometres'],
                                                df_year['Injuries_passenger_kilometres']
                                                ), axis=-1),
                           hovertemplate='<b>Country:</b> %{x}<br><b>Year:</b> %{customdata[0]}<br>'
                                         '<b>Population:</b> %{customdata[1]:,.0f}<br>'
                                         '<b>Passenger km in millions:</b> %{customdata[2]:,.0f}<br>'
                                         '<b>Road injuries & deaths per 1B passenger km:</b> %{customdata[3]:,.1f}<br>'
                                         '<b>Percentage change:</b> %{y:,.1f}%<extra></extra>')

    # If chosen country does not have a passenger kilometres value, we cannot compare it to other countries
    if pd.isnull(df_country_year['Passenger_kilometres'].iloc[0]):
        st.write('No data available for ' + country + ' in ' + str(year))
    else:
        st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------

st.markdown("""<p style='text-align: center; color: white;'>As before, we plot the best and worst countries of 
each year against each other. In this case, we look at the amount of road injuries & deaths per 1B passenger kilometres
relative to the countries' populations.</p>""", unsafe_allow_html=True)

years = []
rel_best = []
country_best = []
rel_worst = []
country_worst = []

# Get best and worst values and countries
for yr in df['Year'].unique():
    years.append(yr)
    df_y = df[df['Year'] == yr]

    df_b = df_y[df_y['Percentage_inj_pk_pop'] == df_y['Percentage_inj_pk_pop'].min()]
    df_w = df_y[df_y['Percentage_inj_pk_pop'] == df_y['Percentage_inj_pk_pop'].max()]

    rel_best.append(df_b['Percentage_inj_pk_pop'].iloc[0])
    country_best.append(df_b['Country'].iloc[0])

    rel_worst.append(df_w['Percentage_inj_pk_pop'].iloc[0])
    country_worst.append(df_w['Country'].iloc[0])

# Create dataframe of best and worst values and countries
df_perc_pk = pd.DataFrame(data={'Year': years,
                                'rel_b': rel_best,
                                'country_best': country_best,
                                'rel_w': rel_worst,
                                'country_worst': country_worst
                                })

# Plot the line graph of best and worst countries
fig_line = px.line(df_perc_pk,
                   x='Year',
                   y=['rel_b', 'rel_w'],
                   markers=True,
                   hover_data=['country_best', 'country_worst']
                   )

fig_line.update_layout(title='The lowest and highest percentages of road injuries & deaths per 1B passenger km '
                             'relative to the populations',
                       yaxis_title='Percentage of population',
                       legend_title_text=''
                       )

# Update names for hovertemplate and legend
newnames = {'rel_b': 'Least injuries & deaths', 'rel_w': 'Most injuries & deaths'}
fig_line.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                           legendgroup=newnames[t.name]))

fig_line.data[0].hovertemplate = ('<b>Country:</b> %{customdata[0]}<br><b>Year:</b> %{x}<br><b>Percentage of '
                                  'population:</b> %{y:.6f}%<extra></extra>')
fig_line.data[1].hovertemplate = ('<b>Country:</b> %{customdata[1]}<br><b>Year:</b> %{x}<br><b>Percentage of '
                                  'population:</b> %{y:.3f}%<extra></extra>')

st.plotly_chart(fig_line, use_container_width=True)

st.markdown("""<p style='text-align: center; color: white;'>Iceland is overall the country with the highest percentage
of road injuries and deaths relative to passenger kilometres and the population. One explanation could be that due to
the ruggedness of the country, tourists tour the island using cars, but are not as used to the environment as
the locals are, therefore causing accidents. On the other hand, India is still seen as a safe driving country as it was
when only taking the populations into account. An explanation could be the enormous population versus the relative small
amount of passenger kilometres, suggesting that driving might not be the main mode of transport.
The United States went from having the most road injuries & deaths relative to the population to having some of the
fewest when taking passenger kilometres into account. It is well-known that the USA has a big car culture, and with the
distances people have to cover each day, it explains that when taking distance travelled into account the USA seems
safer.</p>""", unsafe_allow_html=True)
