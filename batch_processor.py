"""
Batch Processing Module - Functions for batch processing URLs from CSV files

This module provides utility functions for processing batches of URLs from CSV files
and calculating analytics metrics for them. It handles:

1. Loading and parsing CSV files containing URLs and publication dates
2. Processing each URL for multiple time periods
3. Handling missing or invalid publication dates
4. Calculating user milestone categories for the results

The module is designed to be used by the main ga4_fetcher.py script but can also
be imported directly by other scripts that need batch processing functionality.
"""
import pandas as pd
import time
import datetime
from ga4_data_fetcher import get_users_for_url, create_url_regex_pattern
from user_classification import classify_users

def process_url_batch(client, property_id, input_file, days_list, sleep_time=10):
    """
    Process a batch of URLs from a CSV file and collect GA4 analytics data.
    
    This function:
    1. Reads a CSV file containing URLs and their publication dates
    2. For each URL, calculates custom time ranges based on publication date plus days
    3. Fetches user metrics from GA4 for each URL and time period
    4. Handles missing or invalid dates by tracking them separately
    5. Implements rate limiting with sleep intervals to avoid API quota issues
    
    The input CSV must contain at least two columns:
    - 'url': The full URL of the page
    - 'date_published': The publication date in a format pandas can parse to datetime
    
    Args:
        client: GA4 analytics client from initialize_analytics_client()
        property_id (str): GA4 property ID from your Google Analytics account
        input_file (str): Path to CSV file with URLs and publication dates
        days_list (list): List of time periods in days to collect data for (e.g., [30, 90, 360])
        sleep_time (int): Sleep time in seconds between API requests to avoid rate limiting
        
    Returns:
        tuple: (DataFrame with results, list of invalid date entries)
            - DataFrame contains original data plus user counts for each time period
            - invalid_dates is a list of dictionaries with row numbers and URLs
    """
    # Load the input CSV file
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Convert date column to datetime
    df['date_published'] = pd.to_datetime(df['date_published'])
    
    # Add columns for user counts for each time period
    for days in days_list:
        df[f'users_{days}_days'] = 0
    
    print("Fetching analytics data for each URL...")
    # Collect rows with missing or invalid date_published
    invalid_dates = []

    # Process each URL
    for i, row in df.iterrows():
        url = row['url']
        pub_date = row['date_published']

        # Check for missing or invalid date_published
        if pd.isna(pub_date):
            print(f"Skipping row {i+1}: Missing or invalid date_published for URL: {url}")
            invalid_dates.append({'row': i+1, 'url': url})
            continue

        start_date_str = pub_date.strftime("%Y-%m-%d")
        print(f"Processing {i+1}/{len(df)}: {url}")

        # Get metrics for each time period
        for days in days_list:
            end_date_str = (pub_date + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

            users_count = get_users_for_url(
                client, property_id, url, start_date_str, end_date_str
            )
            df.at[i, f'users_{days}_days'] = users_count
            print(f"  {days} days: {users_count} users")

            # Sleep to avoid API rate limiting
            time.sleep(sleep_time)
    
    return df, invalid_dates

def calculate_user_milestones(df, days_list):
    """
    Calculate user milestone categories for each time period.
    
    This function:
    1. Takes a DataFrame containing user counts for different time periods
    2. For each time period, classifies the user counts into milestone categories
    3. Adds new columns to the DataFrame with these classifications
    4. Creates both standard and detailed classification columns
    
    This classification makes it easier to:
    - Identify high-performing content at a glance
    - Filter content by performance tiers
    - Create summary reports of content performance
    
    Args:
        df (DataFrame): DataFrame with user count data in columns named 'users_X_days'
        days_list (list): List of time periods in days (e.g., [30, 90, 360])
        
    Returns:
        DataFrame: Original DataFrame with additional columns for milestone categories:
            - user_milestone_X_days: Standard classification 
            - user_milestone_X_days_detailed: Detailed classification
    """
    print("Calculating user milestones...")
    for days in days_list:
        df[f'user_milestone_{days}_days'] = df[f'users_{days}_days'].apply(
            lambda x: classify_users(x, detailed=False)
        )
        
        df[f'user_milestone_{days}_days_detailed'] = df[f'users_{days}_days'].apply(
            lambda x: classify_users(x, detailed=True)
        )
    
    return df

def process_url_batch_to_date(client, property_id, input_file, end_date, sleep_time=10):
    """
    Process a batch of URLs from a CSV file and collect GA4 analytics data up to a specific end date.
    
    This specialized function:
    1. Reads a CSV file containing URLs and their publication dates
    2. For each URL, calculates the range from publication date to the specified end date
    3. Fetches user metrics from GA4 for each URL within that range
    4. Handles missing or invalid dates by tracking them separately
    5. Implements rate limiting with sleep intervals to avoid API quota issues
    
    The input CSV must contain at least two columns:
    - 'url': The full URL of the page
    - 'date_published': The publication date in a format pandas can parse to datetime
    
    Args:
        client: GA4 analytics client from initialize_analytics_client()
        property_id (str): GA4 property ID from your Google Analytics account
        input_file (str): Path to CSV file with URLs and publication dates
        end_date (datetime.datetime): End date to collect data up to
        sleep_time (int): Sleep time in seconds between API requests to avoid rate limiting
        
    Returns:
        tuple: (DataFrame with results, list of invalid date entries)
            - DataFrame contains original data plus user counts to the end date
            - invalid_dates is a list of dictionaries with row numbers and URLs
    """
    # Load the input CSV file
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Convert date column to datetime
    df['date_published'] = pd.to_datetime(df['date_published'])
    
    # Add column for user counts up to the specified end date
    end_date_str = end_date.strftime("%Y-%m-%d")
    users_column = f'users_to_{end_date_str}'
    df[users_column] = 0
    
    print("Fetching analytics data for each URL...")
    # Collect rows with missing or invalid date_published
    invalid_dates = []

    # Process each URL
    for i, row in df.iterrows():
        url = row['url']
        pub_date = row['date_published']

        # Check for missing or invalid date_published
        if pd.isna(pub_date):
            print(f"Skipping row {i+1}: Missing or invalid date_published for URL: {url}")
            invalid_dates.append({'row': i+1, 'url': url})
            continue

        start_date_str = pub_date.strftime("%Y-%m-%d")
        print(f"Processing {i+1}/{len(df)}: {url}")

        # Only fetch if published before or on the end date
        if pub_date > end_date:
            print(f"  Skipping: Published after end date.")
            continue

        # Use regex pattern from the row if available, otherwise use the URL directly
        if 'regex' in row and pd.notna(row['regex']):
            regex_pattern = row['regex']
            print(f"  Using provided regex: {regex_pattern}")
            users_count = get_users_for_url(
                client, property_id, url, start_date_str, end_date_str, 
                custom_regex=regex_pattern
            )
        else:
            users_count = get_users_for_url(
                client, property_id, url, start_date_str, end_date_str
            )
            
        df.at[i, users_column] = users_count
        print(f"  Users from {start_date_str} to {end_date_str}: {users_count}")

        # Sleep to avoid API rate limiting
        time.sleep(sleep_time)
    
    return df, invalid_dates, users_column

def calculate_user_milestones_to_date(df, users_column):
    """
    Calculate user milestone categories for data up to a specific date.
    
    This function:
    1. Takes a DataFrame containing user counts up to a specific date
    2. Classifies the user counts into milestone categories
    3. Adds new columns to the DataFrame with these classifications
    4. Creates both standard and detailed classification columns
    
    Args:
        df (DataFrame): DataFrame with user count data in the specified column
        users_column (str): Name of the column containing user counts
        
    Returns:
        DataFrame: Original DataFrame with additional columns for milestone categories:
            - user_milestone_to_date: Standard classification 
            - user_milestone_to_date_detailed: Detailed classification
    """
    print("Calculating user milestones...")
    milestone_column = users_column.replace('users_', 'user_milestone_')
    detailed_milestone_column = milestone_column + '_detailed'
    
    df[milestone_column] = df[users_column].apply(
        lambda x: classify_users(x, detailed=False)
    )
    
    df[detailed_milestone_column] = df[users_column].apply(
        lambda x: classify_users(x, detailed=True)
    )
    
    return df
