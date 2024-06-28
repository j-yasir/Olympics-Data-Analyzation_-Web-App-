import streamlit as st
import pandas as pd
import  preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Summer Olympics Analysis")
user_menu = st.sidebar.radio(
    'select an Option',
    ('Medal Tally' , 'Overall Analysis' , 'Country wise Analysis' , 'Athelete wise Analysis')
)
# st.dataframe(df)

if user_menu == "Medal Tally":

    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'overall' and selected_year == 'overall':
        st.title("Overall Medal Tally")
    if selected_country == 'overall' and selected_year != 'overall':
        st.title("Medal tally in " + str(selected_year))
    if selected_country != 'overall' and selected_year == 'overall':
        st.title("Medal tally of " + selected_country)
    if selected_country != 'overall' and selected_year != 'overall':
        st.title("Medal tally of " + selected_country + " in " + str(selected_year))

    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    st.title("Top Statistics")

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    st.write("\n\n\n")
    st.markdown("\n\n\n")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    st.write("\n\n\n\n\n")
    st.markdown("\n\n\n\n\n\n")
    nations_over_time = helper.participating_nations_over_time(df)
    #st.table(nations_over_time)
    fig = px.line(nations_over_time, x="Edition", y="No of Countries")
    st.title("Participating nations over the Years")
    st.plotly_chart(fig)

    st.write("\n\n\n\n\n")
    events_over_time = helper.Events_over_time(df)
    # st.table(nations_over_time)
    fig = px.line(events_over_time, x="Edition", y="No of events")
    st.title("Events over the Years")
    st.plotly_chart(fig)

    st.write("\n\n\n\n\n")
    athletes_over_time = helper.athletes_over_time(df)
    # st.table(nations_over_time)
    fig = px.line(athletes_over_time, x="Edition", y="No of athletes")
    st.title("Athletes over the Years")
    st.plotly_chart(fig)

    st.write("\n\n\n\n\n")
    st.title("Number of events over time(Every Sport)")
    fig, ax = plt.subplots(figsize = (20,20))

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0 , 'overall')
    selected_sport = st.selectbox('Select a sport' , sports_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country wise Analysis':

    st.title("Country wise Statistics")
    st.write("\n\n\n\n\n\n\n\n")
    st.header("Country wise Medals over the years")
    country_list = df['region'].unique().tolist()
    country_list = [str(item) for item in country_list]
    country_list.sort()
    selected_country = st.selectbox('Select a country' , country_list)


    st.header(str(selected_country))
    x = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(x, x="Year", y="Medal")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt , annot = True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top_10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top_10_df)


if user_menu == 'Athelete wise Analysis':

    st.title('Athlete wise analysis')


