"""
GA4 Fetcher - Main script for batch processing multiple URLs from a CSV file

This is the primary script for analyzing traffic data for multiple URLs from a CSV file.
It calculates user counts based on each URL's publication date plus a specified number
of days, allowing you to see how content performs over different time periods.

Key features:
1. Processes multiple URLs from a CSV file containing URLs and publication dates
2. Analyzes each URL for multiple time periods (e.g., 30, 60, 90 days after publication)
3. Handles missing or invalid publication dates
4. Classifies traffic into milestone categories
5. Outputs comprehensive results to a CSV file

This script is particularly useful for:
- Content performance analysis based on age of content
- Comparing how different content performs at similar points in its lifecycle
- Identifying content that reaches traffic milestones quickly

Example usage:
    python ga4_fetcher.py --days 30 90 360 --input-file content_urls.csv
"""
import pandas as pd
import argparse
import datetime
import time

# Import functions from the modularized files
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url
from user_classification import classify_users
from batch_processor import process_url_batch, calculate_user_milestones
    
def main():
    """
    Main function that:
    1. Processes command-line arguments for configuration
    2. Initializes the GA4 client
    3. Processes URLs from the input CSV file
    4. Calculates user metrics for each URL over specified time periods
    5. Classifies traffic into milestone categories
    6. Outputs results to a CSV file
    
    This is the most comprehensive script in the toolkit, designed for 
    batch processing multiple URLs with their respective publication dates.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch GA4 analytics data for URLs based on their publication dates')
    parser.add_argument('--days', type=int, nargs='+', default=[360], 
                        help='Number of days after publication to collect data for (e.g., 30 90 360 for 30-day, 90-day, and 360-day periods)')
    parser.add_argument('--credentials', type=str, default="atanservicekey.json",
                       help='Path to service account credentials JSON file for GA4 authentication')
    parser.add_argument('--property-id', type=str, default="315823153",
                       help='GA4 property ID from your Google Analytics account')
    parser.add_argument('--input-file', type=str, default="wordpress_analytics_2023-07-01_to_2024-06-30.csv",
                       help='Input CSV file with "url" and "date_published" columns')
    # Removed output-prefix argument as we'll use ga4_ automatically
    parser.add_argument('--sleep-time', type=int, default=10,
                       help='Sleep time in seconds between API requests to avoid rate limiting')
    args = parser.parse_args()
    
    # Configuration parameters
    credentials_path = args.credentials
    property_id = args.property_id
    input_file = args.input_file
    output_file = "ga4_" + input_file  # Always use ga4_ prefix
    sleep_time = args.sleep_time
    
    # Get days from arguments
    days_list = args.days
    print(f"Will collect data for these day periods: {days_list}")
    
    print("Initializing GA4 client...")
    client = initialize_analytics_client(credentials_path)
    print("GA4 client initialized successfully!")

    # Process URLs in batch
    df, invalid_dates = process_url_batch(client, property_id, input_file, days_list, sleep_time)
    
    # Save invalid date rows for review
    if invalid_dates:
        invalid_dates_df = pd.DataFrame(invalid_dates)
        invalid_dates_df.to_csv("invalid_date_published_rows.csv", index=False)
        print(f"Saved {len(invalid_dates)} rows with invalid date_published to invalid_date_published_rows.csv")

    # Calculate milestone categories
    df = calculate_user_milestones(df, days_list)
    
    # Save results
    print(f"Saving results to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Done!")


if __name__ == "__main__":
    main()