import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years,country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df

    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == year]

    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()

    else:
        x = temp_df.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                   ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x



def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'index')
    nations_over_time.rename(columns = {'index' : "Edition" , "Year" : "No of Countries"} , inplace = True)
    return nations_over_time

def Events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(
        'index')
    events_over_time.rename(columns = {'index' : "Edition" , "Year" : "No of events"} , inplace = True)
    return events_over_time

def athletes_over_time(df):
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'index')
    athletes_over_time.rename(columns = {'index' : "Edition" , "Year" : "No of athletes"} , inplace = True)
    return athletes_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset = ['Medal'])

    if sport != 'overall':
        temp_df = temp_df[temp_df["Sport"] == sport]

    # Count the occurrences of each name and reset the index
    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Medals']
    top_names = name_counts.head(15)
    result = top_names.merge(df, on='Name', how='left')[['Name', 'Medals' ,'Sport', 'region']].drop_duplicates('Name')
    return result

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, region):
    temp_df = df.dropna(subset = ['Medal'])


    temp_df = temp_df[temp_df["region"] == region]

    # Count the occurrences of each name and reset the index
    name_counts = temp_df['Name'].value_counts().reset_index()

# Rename the columns to be more descriptive
    name_counts.columns = ['Name', 'Medals']

# Select the top 15 names
    top_names = name_counts.head(10)

# Merge with the original data on the 'Name' column
    result = top_names.merge(df, on='Name', how='left')[['Name', 'Medals' ,'Sport']].drop_duplicates('Name')
    return result

