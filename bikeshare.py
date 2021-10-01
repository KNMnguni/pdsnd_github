import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply 
            no month filter
        (str) day - day of week number to filter by, or "all" to apply 
            no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs

    city = ""
    cities = ('chicago', 'new york', 'washington')
    while (city.title() != "Chicago", city.title() != "New York", city.title != "Washington"):
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        if city.lower() in cities:
            break

    print("You have selected to see data for {}! If this is not true, restart the program now!".format(city.title()))

    filter_type = ""
    filter_types = ('none', 'month', 'day', 'both')
    while (filter_type.lower() not in filter_types):
        filter_type = input('How would you like to filter the data, by month, day, both or not at all? Type "none" for no time filters.\n')

    # get user input for month (all, january, february, ... , june)
    if (filter_type == 'month' or filter_type == 'both'):
        if(filter_type == 'month'):
            day = 'all'
        month = ""
        months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
        while (month != 'january', month != 'february', month != 'march',
               month != 'april', month != 'may', month != 'may'):
            month = input('Please type in the month to filter the data by: January, February, March, April, May and June.\n').lower()
            if (month in months):
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if (filter_type == 'day' or filter_type == 'both'):
        if filter_type == 'day':
            month = 'all'

        day = ''
        days = ['all', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday']
        while (day != all and day not in days):
            day = days[int(input('Please select the day to filter the day by as integer(1 =Sunday, 2 = Monday etc.)\n'))]

    if filter_type == 'none':
        month = 'all'
        day = 'all'

    # format city to lowercase.
    city = city.lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
            month filter
        (str) day - name of the day of week to filter by, or "all" to apply
            no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of the week if applicable
    if day != 'all':
        # filter by the day of the week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # computes the most common month
    common_month = df['month'].mode()[0]

    # identifies the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    # computes the most common start hour
    common_start_hour = df['start_hour'].mode()[0]

    # computes the 'count' for the most common hour
    hour_count = 0
    for t in df['start_hour']:
        if t == common_start_hour:
            hour_count += 1

    # computing values for Filter

    print('Most popular hour: {}, Count: {}, Filter:{} and {}'
          .format(common_start_hour, hour_count, common_month,
                  common_day_of_week))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # computes the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # computes the 'count' for the most commonly used start station
    count_start_station = 0
    for ss in df['Start Station']:
        if ss == common_start_station:
            count_start_station += 1

    # computes the most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # computes the 'count' for the most commonly used end station
    count_end_station = 0
    for es in df['End Station']:
        if es == common_end_station:
            count_end_station += 1

    # computes the most frequent combination of start station and
    # end station trip
    df['trip'] = df['Start Station'] +' to '+ df['End Station']
    common_trip = df['trip'].mode()[0]

    # computes the 'count' for the most frequent combination of
    # start station and end station trip
    count_trip = 0
    for trip in df['trip']:
        if trip == common_trip:
            count_trip += 1

    print('Start Station: {}, Count: {}, End Station: {}, COunt: {}, Filter: {} and {}'
          .format(common_start_station, count_start_station,
                  common_end_station, count_end_station, df['month'].mode()[0],
                  df['day_of_week'].mode()[0]))
    print('Trip: {}, Count: {}, Filter: {} and {}'
          .format(common_trip, count_trip, df['month'].mode()[0],
                  df['day_of_week'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # since the Start Time column was converted to datetime during the
    # load data function, we also nhave to convert the End Time column.
    df['End Time'] = pd.to_datetime(df['End Time'])

    # computes total travel time
    df['travel_time'] = (df['End Time'] - df['Start Time'])
    sum_travel_time = df['travel_time'].sum()

    # computes mean travel time
    avg_travel_time = df['travel_time'].mean()

    # computes the count for travel time
    count_travel_time = df['travel_time'].count()

    print('Total Trips Duration:{}, Count:{}, AVG Trip Duration:{}'
          .format(sum_travel_time, count_travel_time, avg_travel_time))    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # computes counts of user types
    user_types = df['User Type'].value_counts()

    print('Filtered by:{} and {} \n \nUser Type Distribution: \n{}'
          .format(df['month'].mode()[0], df['day_of_week'].mode()[0],
                  user_types))

    print(' ')
    # computes counts of gender
    if 'Gender' in df.columns:
        """The Washington Dataset does not have 'gender' data, 
        therefore, we need to validate the Gender column. """
        index = pd.Index(df['Gender'])
        gender_distr = index.value_counts()
        if gender_distr is None:
            print('There is no Gender Distribution data')
        else:
            print('Gender Distribution:\n{}'.format(gender_distr))
    else:
        print('There is no Gender Distribution data')

    # computes earliest, most recent, and most common year of birth
    print(' ')
    if 'Birth Year' in df.columns:
        """The Washington Dataset does not have 'birth year' data,
        therefore, we need to validate the Birth Year column. """
        print('The oldest commuter was born in the year:{} \nThe youngest commuter was born in the year:{} \nMost of the commuters were born in the year:{}'
              .format(int((df['Birth Year']).min()), int((df['Birth Year']).max()), int(df['Birth Year'].mode()[0])))
    else:
        print('There is no Birth Year data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """This will allow the user to view the raw data used in for determining the Stats"""
    start_time = time.time()
    if input("Would you like to see the raw data used to generate these bikeshare usage patterns? (y/n):") == 'y':
        print('\nRaw Data...\n')
        start_row = 0
        end_row = 5
        max_rows = len(df)

        print(df[start_row:end_row])
        while end_row < max_rows:
            user_input = input('Next set of rows? (y/n):')
            if user_input == 'y':
                start_row += 5
                end_row += 5
                print(df[start_row:end_row])
            else:
                print(" ")
                break
    else:
        print('You selected not to view the raw data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
