import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title( selected_country + " Overall Performance ")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

nations_over_time = helper.data_over_time(df,'region')
st.title("Participating Nations over the Years")
fig = px.line(nations_over_time, x='Edition', y='region')
st.plotly_chart(fig)

events_over_time = helper.data_over_time(df,'Event')
st.title("Events over the Years")
fig = px.line(events_over_time, x='Edition', y='Event')
st.plotly_chart(fig)

athlete_over_time = helper.data_over_time(df,'Name')
st.title("Athletes over the Years")
fig = px.line(athlete_over_time, x='Edition', y='Name')
st.plotly_chart(fig)

st.title("No. of events over time(Every Sport)")
fig,ax=plt.subplots(figsize=(20,20))
x = df.drop_duplicates(['Year','Sport', 'Event'])
ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
st.pyplot(fig)

st.title("Most successful Athletes")
sport_list = df['Sport'].unique().tolist()
sport_list.sort()
sport_list.insert(0,'Overall')

selected_sport = st.selectbox('Select a sport',sport_list)

x = helper.most_successful(df,selected_sport)
st.table(x)

if user_menu == "Country-wise Analysis":
    country_df = helper.year_wise_medal_tally(df,'USA')
    fig = px.line(country_df, x="Year" , y="Medal")
    st.title("Medal Tally over the years")
    st.plotly_chart(fig)
