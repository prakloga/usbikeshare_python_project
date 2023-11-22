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
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['monday','tuesday','wednesday','thrusday','friday','saturday','sunday','all']

    while True:
        city = input("Would you like to see data for chicago, new york, washington?\n").strip().lower()
        if city not in valid_cities:
            print("Oops, It is not a valid city. Try again")
            continue
        else:
            break

    while True:
        month = input("\nWhich month? all, january, february, march, april, may, or june?\n").strip().lower()
        if month not in valid_months:
            print("Oops, It is not a valid month. Try again")
            continue
        else:
            break

    while True:
        day = input("\nWhich day? please type your response as a string(e.g., all, monday, tuesday, ... sunday)\n").strip().lower()
        if day not in valid_days:
            print("Oops, It is not a valid day. Try again")
            continue
        else:
            break
        
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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week_num'] = df['Start Time'].dt.day_of_week
    df['day_of_week_txt'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week_txt'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].value_counts().idxmax(axis=0)
    most_common_month_count = df['month'].value_counts().max(axis=0)

    most_common_day = df['day_of_week_txt'].value_counts().idxmax(axis=0)
    most_common_day_count = df['day_of_week_txt'].value_counts().max(axis=0)

    most_common_start_hour = df['start_hour'].value_counts().idxmax(axis=0)
    most_common_start_hour_count = df['start_hour'].value_counts().max(axis=0)

    print("Most common month:",most_common_month," ",most_common_month_count,"  Most common day of week:",most_common_day," ",most_common_day_count,"   Most common start hour:",most_common_start_hour," ",most_common_start_hour_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_commonly_used_start_station = df['Start Station'].value_counts().idxmax(axis=0)
    most_commonly_used_start_station_count = df['Start Station'].value_counts().max(axis=0)

    most_commonly_used_end_station = df['End Station'].value_counts().idxmax(axis=0)
    most_commonly_used_end_station_count = df['End Station'].value_counts().max(axis=0)

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

    total_duration = df['Trip Duration'].sum()
    trip_count = df['Trip Duration'].count()
    average_duration = df['Trip Duration'].mean()

    print("Total Duration:",total_duration,"    Count:",trip_count,"   Avg Duration:",average_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_counts = df['User Type'].value_counts()
    print("Subscribers:",user_type_counts['Subscriber'],"   Customers:",user_type_counts['Customer'])

    if 'Gender' not in df:
        print("\nAplogize.No gender data is available in the source to share stats.")
    else:
        gender_counts = df['Gender'].value_counts()
        print("\nMale:",gender_counts['Male']," Female:",gender_counts['Female'])

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
            print("Aplogize,The given selection does not have any records in the source dataset.")
            print("Please use a different month or day combination in the given city.")
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