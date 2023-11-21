import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    valid_cities = ['chicago', 'new york', 'washington']
    valid_months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    valid_days = ['Monday','Tuesday','Wednesday','Thrusday','Friday','Saturday','Sunday','All']

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for chicago, new york, washington? ").strip().lower()
    while city not in valid_cities:
        print("Oops. It's not a valid input, please enter either chicago, new york, washington")
        city = input("Would you like to see data for chicago, new york, washington? ").strip().lower()
 
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month? All, January, February, March, April, May, or June ? ").strip().title()
    while month not in valid_months:
        print("Oops. It's not a valid input, please enter either January, February, March, April, May, June or All")
        month = input("Which month? January, February, March, April, May, June or All? ").strip().title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day? please type your response as a string(e.g., All, Monday, Tuesday, ... Sunday) ").strip().title()
    while day not in valid_days:
        print("Oops. It's not a valid input, please enter either All, Monday, Tuesday, .... Sunday)")
        day = input("Which day? please type your response as a string(e.g., All, Monday, Tuesday, ... Sunday) ").strip().title()

    #print("\nFilter Criteria CITY:",city.title()," ", "MONTH:",month," ","DAY:",day,"\n")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week_num'] = df['Start Time'].dt.day_of_week
    df['day_of_week_txt'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week_txt'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # Count the number of occurance of each month and then find the month with the highest value
    most_common_month = df['month'].value_counts().idxmax(axis=0)
    most_common_month_count = df['month'].value_counts().max(axis=0)

    # TO DO: display the most common day of week
    # Count the number of occurance of each week days and then find the week day with the highest value
    most_common_day = df['day_of_week_txt'].value_counts().idxmax(axis=0)
    most_common_day_count = df['day_of_week_txt'].value_counts().max(axis=0)

    # TO DO: display the most common start hour
    # Count the number of occurance of each hour and then find the week day with the highest value
    most_common_start_hour = df['start_hour'].value_counts().idxmax(axis=0)
    most_common_start_hour_count = df['start_hour'].value_counts().max(axis=0)

    print("Most common month:",most_common_month," ",most_common_month_count,"  Most common day of week:",most_common_day," ",most_common_day_count,"   Most common start hour:",most_common_start_hour," ",most_common_start_hour_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # Count the number of occurance of start station and then find the start station with the highest value
    most_commonly_used_start_station = df['Start Station'].value_counts().idxmax(axis=0)
    most_commonly_used_start_station_count = df['Start Station'].value_counts().max(axis=0)

    # TO DO: display most commonly used end station
    # Count the number of occurance of end station and then find the end station with the highest value
    most_commonly_used_end_station = df['End Station'].value_counts().idxmax(axis=0)
    most_commonly_used_end_station_count = df['End Station'].value_counts().max(axis=0)

    # TO DO: display most frequent combination of start station and end station trip
    # Count the number of occurance of start and end station and then find the start & end station with the highest value
    most_frequent_combination_stations = df[['Start Station','End Station']].value_counts().idxmax(axis=0)
    most_frequent_combination_stations_count = df[['Start Station','End Station']].value_counts().max(axis=0)

    print("Most commonly used start station:",most_commonly_used_start_station," ",most_commonly_used_start_station_count
        ,"   Most commonly used end station:",most_commonly_used_end_station," ",most_commonly_used_end_station_count
        ,"   Most common occurance of start and end station:",most_frequent_combination_stations," ",most_frequent_combination_stations_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()

    # TO DO: display total trip count for the given selection
    trip_count = df['Trip Duration'].count()

    # TO DO: display mean travel time
    average_duration = df['Trip Duration'].mean()

    print("Total Duration:",total_duration,"    Count:",trip_count,"   Avg Duration:",average_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("Subscribers:",user_type_counts['Subscriber'],"   Customers:",user_type_counts['Customer'])

    # TO DO: Display counts of gender
    if 'Gender' not in df:
        print("\nAplogize.No gender data is available in the source to share stats.")
    else:
        gender_counts = df['Gender'].value_counts()
        print("\nMale:",gender_counts['Male']," Female:",gender_counts['Female'])

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print("\nApologize.No birth year data is available in the source to share stats.")
    else:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mean()
        print("\nEarliest Birth Year:",earliest_birth_year,"    Recent Birth Year:",recent_birth_year,"    Common Birth Year:",common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df)==0:
            print("Aplogize,The given selection does not have any records in the source dataset")
            print("Please use a different month or day combination in the given city")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        rawdata = input('\nWould you like to see sample raw data? Enter yes or no.\n')
        while rawdata.lower() == 'yes':
            print(df.sample(n = 5))
            rawdata = input('\nWould you like to see sample raw data? Enter yes or no.\n')   

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()