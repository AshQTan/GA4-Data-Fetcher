#!/usr/bin/env python3
"""
GA4 Fetcher Up-To-Date - Fetch GA4 data for URLs from publication date to a specific end date

This script is a specialized variant of ga4_fetcher.py that retrieves analytics data
for URLs from their publication date up to a specific end date provided by the user.
It's useful for creating point-in-time snapshots of content performance.

Key features:
1. Processes multiple URLs from a CSV file containing URLs and publication dates
2. Analyzes traffic from publication date to a fixed end date (same for all URLs)
3. Supports regex patterns for more precise URL matching
4. Classifies traffic into milestone categories
5. Outputs comprehensive results to a CSV file

Example usage:
    python ga4_fetcher_uptodate.py --date 2023-12-31 --input_file your_input.csv
"""
import pandas as pd
import datetime
import argparse
import os

# Import functions from the modularized files
from ga4_client import initialize_analytics_client
from batch_processor import process_url_batch_to_date, calculate_user_milestones_to_date


def main():
    """
    Main function that:
    1. Processes command-line arguments for configuration
    2. Initializes the GA4 client
    3. Processes URLs from the input CSV file
    4. Calculates user metrics for each URL from publication date to a specific end date
    5. Classifies traffic into milestone categories
    6. Outputs results to a CSV file
    
    This script is specialized for analyzing content performance from
    publication date up to a fixed end date (the same for all URLs).
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch GA4 analytics data for URLs up to a specific date')
    parser.add_argument('--date', type=str, required=True, 
                        help='End date (YYYY-MM-DD) to collect data up to for each URL')
    parser.add_argument('--input_file', type=str, default="wordpress_analytics_2023-07-01_to_2024-06-30.csv", 
                        help='Input CSV file with URLs and publication dates')
    parser.add_argument('--credentials', type=str, default="atanservicekey.json",
                        help='Path to the Google service account credentials JSON file')
    parser.add_argument('--property_id', type=str, default="315823153",
                        help='Google Analytics 4 property ID')
    parser.add_argument('--sleep', type=int, default=10,
                        help='Sleep time between API requests (seconds) to avoid rate limiting')
    args = parser.parse_args()
    
    # Configuration parameters
    credentials_path = args.credentials
    property_id = args.property_id
    input_file = args.input_file
    output_file = "ga4_uptodate_" + os.path.basename(input_file)
    sleep_time = args.sleep
    
    # Get end date from arguments
    end_date_str = args.date
    try:
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: {end_date_str}. Please use YYYY-MM-DD.")
        return
    print(f"Will collect data up to: {end_date_str}")
    
    # Initialize GA4 client
    print("Initializing GA4 client...")
    client = initialize_analytics_client(credentials_path)
    print("GA4 client initialized successfully!")
    
    # Process the batch of URLs up to the specified end date
    df, invalid_dates, users_column = process_url_batch_to_date(
        client, property_id, input_file, end_date, sleep_time
    )
    
    # Save invalid date rows for review
    if invalid_dates:
        invalid_dates_df = pd.DataFrame(invalid_dates)
        invalid_dates_df.to_csv("invalid_date_published_rows.csv", index=False)
        print(f"Saved {len(invalid_dates)} rows with invalid date_published to invalid_date_published_rows.csv")

    # Calculate milestone categories for the period
    df = calculate_user_milestones_to_date(df, users_column)
    
    # Save results
    print(f"Saving results to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Done!")


if __name__ == "__main__":
    """
    Script entry point. Handles exceptions at the top level.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation canceled by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
