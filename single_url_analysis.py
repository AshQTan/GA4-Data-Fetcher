"""
Single URL Analysis - Quick analytics for one URL over a specific number of days

This script provides a simple way to check the user traffic for a single URL
over a specified number of days (defaults to 30 days). It's useful for:

1. Quick traffic checks for individual pages
2. Ad-hoc reporting on specific content
3. Testing your GA4 setup and authentication
4. Learning how to use the GA4 modules in a simple context

The script calculates the date range based on the current date minus the 
specified number of days, then retrieves and classifies the user count.

Example usage:
    python single_url_analysis.py --url "https://www.yourpage.com/article" --days 30

Output:
    Displays the URL, date range, user count, and traffic category classifications
"""
import argparse
import datetime
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url
from user_classification import classify_users

def main():
    """
    Main function that:
    1. Takes command-line arguments for URL and time period
    2. Calculates the date range (today minus specified days)
    3. Fetches user count from GA4 for the URL within that date range
    4. Classifies the traffic into user milestone categories
    5. Displays the results
    
    This is the simplest script in the toolkit, designed for quick checks
    of individual URLs without requiring a CSV file.
    """
    parser = argparse.ArgumentParser(description='Quick GA4 data fetch for a single URL')
    parser.add_argument('--url', type=str, required=True, 
                        help='URL to analyze (e.g., "https://www.yourpage.com/article")')
    parser.add_argument('--days', type=int, default=30, 
                        help='Number of days from today to analyze (default: 30)')
    parser.add_argument('--credentials', type=str, default="atanservicekey.json", 
                        help='Path to service account credentials JSON file')
    parser.add_argument('--property-id', type=str, default="315823153", 
                        help='GA4 property ID from your Google Analytics account')
    args = parser.parse_args()
    
    # Initialize the GA4 client
    client = initialize_analytics_client(args.credentials)
    
    # Set the date range
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=args.days)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    # Get user count for the URL
    user_count = get_users_for_url(
        client, args.property_id, args.url, start_date_str, end_date_str
    )
    
    # Classify the user count
    category = classify_users(user_count)
    detailed_category = classify_users(user_count, detailed=True)
    
    # Display results
    print(f"\nResults for {args.url} over the past {args.days} days:")
    print(f"Total Users: {user_count}")
    print(f"Category: {category}")
    print(f"Detailed Category: {detailed_category}")

if __name__ == "__main__":
    main()
