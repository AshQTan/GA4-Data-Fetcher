"""
Date Range Analytics - Script for fetching Google Analytics 4 (GA4) data for a specific date range

This script allows you to analyze user traffic for multiple URLs within a fixed date range.
Unlike ga4_fetcher.py which analyzes URLs based on their publication date plus a number of days,
this script uses the same exact date range for all URLs, making it useful for:

1. Comparing performance of different URLs during the same time period
2. Analyzing seasonal traffic patterns across multiple pages
3. Measuring the impact of marketing campaigns on multiple pages
4. Generating reports for specific reporting periods (e.g., monthly, quarterly)

The script outputs a CSV file with user counts and classifications for each URL.

Example usage:
    python date_range_analytics.py --start-date 2023-01-01 --end-date 2023-01-31 \
      --urls "https://www.yourpage.com/article1" "https://www.yourpage.com/article2"

Output format:
    - url: The full URL of the page
    - start_date: The start date of the analysis period
    - end_date: The end date of the analysis period
    - users: Total number of users who visited the page during the period
    - category: User milestone classification (e.g., "0-10k", "10-20k")
    - detailed_category: More detailed user milestone classification
"""
import argparse
import pandas as pd
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url
from user_classification import classify_users

def main():
    """
    Main function that:
    1. Takes command-line arguments for date range and URLs to analyze
    2. Fetches user traffic data from GA4 for each URL within the specified date range
    3. Classifies each URL's performance into user milestone categories
    4. Outputs results to a CSV file for further analysis
    
    Unlike ga4_fetcher.py which analyzes URLs from their publication date,
    this script applies the same fixed date range to all URLs.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Fetch GA4 analytics data for URLs within specific date range')
    parser.add_argument('--start-date', type=str, required=True,
                        help='Start date in YYYY-MM-DD format (e.g., 2023-01-01)')
    parser.add_argument('--end-date', type=str, required=True,
                        help='End date in YYYY-MM-DD format (e.g., 2023-01-31)')
    parser.add_argument('--credentials', type=str, default="atanservicekey.json",
                       help='Path to service account credentials file for GA4 authentication')
    parser.add_argument('--property-id', type=str, default="315823153",
                       help='GA4 property ID - found in your GA4 property settings')
    parser.add_argument('--urls', nargs='+', required=True,
                       help='One or more URLs to analyze (e.g., "https://www.yourpage.com/article1" "https://www.yourpage.com/article2")')
    parser.add_argument('--output-file', type=str, default="date_range_results.csv",
                       help='Filename for the output CSV file with analytics results')
    args = parser.parse_args()
    
    # Get parameters
    start_date = args.start_date
    end_date = args.end_date
    credentials_path = args.credentials
    property_id = args.property_id
    urls = args.urls
    output_file = args.output_file
    
    print(f"Will analyze {len(urls)} URLs from {start_date} to {end_date}")
    
    # Initialize GA4 client
    print("Initializing GA4 client...")
    client = initialize_analytics_client(credentials_path)
    print("GA4 client initialized successfully!")
    
    # Create dataframe to store results
    results = []
    
    # Process each URL - analyzing them all for the same date range
    for i, url in enumerate(urls):
        print(f"Processing {i+1}/{len(urls)}: {url}")
        
        # Get user count for this URL and date range
        # This calls the GA4 API to fetch the total number of users who visited this URL 
        # between the start_date and end_date
        users_count = get_users_for_url(
            client, property_id, url, start_date, end_date
        )
        
        # Classify the user count into milestone categories
        # Standard classification: 0-10k, 10-20k, 20-30k, 30-40k, >40k
        category = classify_users(users_count)
        # Detailed classification: includes additional 40k-100k and >100k categories
        detailed_category = classify_users(users_count, detailed=True)
        
        # Add all data for this URL to the results collection
        results.append({
            'url': url,
            'start_date': start_date,
            'end_date': end_date,
            'users': users_count,
            'category': category,
            'detailed_category': detailed_category
        })
        
        print(f"  Users: {users_count}")
        print(f"  Category: {category}")
        print(f"  Detailed Category: {detailed_category}")
    
    # Convert results to dataframe and save as CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Display a summary of the results
    print("\nSummary:")
    print(f"- Date Range: {start_date} to {end_date}")
    print(f"- URLs Analyzed: {len(urls)}")
    print(f"- Total Users Across All URLs: {df['users'].sum():,}")
    
    # Show the top performing URL if available
    if not df.empty:
        top_url = df.loc[df['users'].idxmax()]
        print(f"- Top Performing URL: {top_url['url']} with {top_url['users']:,} users")

if __name__ == "__main__":
    main()
