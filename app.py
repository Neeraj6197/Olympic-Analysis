import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://w1.pngwing.com/pngs/978/29/png-transparent-summer-symbol-olympic-games-rio-2016-2020-summer-olympics-london-2012-summer-olympics-1968-summer-olympics-pyeongchang-2018-olympic-winter-games-1904-summer-olympics-sports.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

st.header("Overall Olympic Analysis")
st.dataframe(df)

if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics.")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "\'s overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "\'s performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':

    st.title("Overall Statistics")
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(events)
    with col5:
        st.header('Athletes')
        st.title(athletes)
    with col6:
        st.header('Nations')
        st.title(nations)

    #plotting the graphs:
    countries_over_years = helper.data_over_years(df,'region')
    fig = px.line(countries_over_years, x="Edition", y="region")
    st.title("Participating Countries over the years")
    st.plotly_chart(fig)

    events_over_years = helper.data_over_years(df, 'Event')
    fig = px.line(events_over_years, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_years = helper.data_over_years(df, 'Name')
    fig = px.line(athletes_over_years, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title('No. of Events over years(Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    #creating a select box to select the sport:
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.title("Country-wise Analysis")

    #creating a drop down to select country:
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0,'Overall')
    selected_country = st.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "\'s Medal Tally over the years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df,selected_country)
    st.title(selected_country + "\'s performance in the following sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athelets of " + selected_country)
    top10_df = helper.most_successful2(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    # distributing dataset to plot the graph:
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    st.title("Distribution of Age")
    st.plotly_chart(fig)

    #plotting the weight vs height graph:
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    st.title("Height vs Weight")
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=40)
    st.pyplot(fig)

    # plotting a graph for no. of men vs no.of women in every year:
    st.title("Men VS Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)


