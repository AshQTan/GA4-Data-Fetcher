#!/usr/bin/env python3
"""
URL Trend Analysis - Analyze a URL's performance over multiple time periods

This script tracks how a single URL's traffic grows over different time periods
from its publication or start date. It helps you understand:

1. The traffic growth pattern of a specific piece of content
2. How quickly a URL reaches different user milestones
3. The long-term performance trajectory of content
4. Which time periods show the most significant growth

The script can output both CSV data and (optionally) a visualization graph
showing the user growth curve over time.

Example usage:
    python url_trend_analysis.py --url "https://www.yourpage.com/article" \
      --start-date 2023-01-01 --periods 7 30 90 180 360

Output format:
    - CSV file with columns for days, start/end dates, user counts, and categories
    - Optional visualization graph saved as PNG file
"""
import argparse
import datetime
import pandas as pd
import os
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url
from user_classification import classify_users
from visualization import create_trend_chart

def main():
    """
    Main function that:
    1. Takes command-line arguments for URL, start date, and time periods
    2. Fetches GA4 analytics data for each time period from the start date
    3. Builds a growth curve showing how user traffic increases over time
    4. Outputs both tabular data (CSV) and visual representation (PNG graph)
    
    This helps content creators and marketers understand how traffic to a 
    specific URL grows over different time periods from its publication.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze a URL\'s performance over multiple time periods')
    parser.add_argument('--url', type=str, required=True, 
                        help='URL to analyze (e.g., "https://www.yourpage.com/article")')
    parser.add_argument('--start-date', type=str, required=True,
                        help='Publication or start date in YYYY-MM-DD format (e.g., "2023-01-01")')
    parser.add_argument('--periods', type=int, nargs='+', default=[7, 14, 30, 60, 90, 180, 360],
                       help='Time periods in days to analyze (e.g., 7 30 90 means 7-day, 30-day, and 90-day periods)')
    parser.add_argument('--credentials', type=str, default="atanservicekey.json",
                       help='Path to service account credentials file')
    parser.add_argument('--property-id', type=str, default="315823153",
                       help='GA4 property ID')
    parser.add_argument('--output-file', type=str, default=None,
                       help='Output CSV file name (optional)')
    args = parser.parse_args()
    
    # Get parameters
    url = args.url
    start_date = args.start_date
    credentials_path = args.credentials
    property_id = args.property_id
    periods = sorted(args.periods)
    output_file = args.output_file
    
    # Initialize GA4 client
    print("Initializing GA4 client...")
    client = initialize_analytics_client(credentials_path)
    print("GA4 client initialized successfully!")
    
    # Convert start date
    pub_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    
    # Collect data for each time period
    results = []
    for days in periods:
        end_date = pub_date + datetime.timedelta(days=days)
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        print(f"Fetching data for {days} days period ({start_date} to {end_date_str})...")
        user_count = get_users_for_url(
            client, property_id, url, start_date, end_date_str
        )
        
        category = classify_users(user_count)
        detailed_category = classify_users(user_count, detailed=True)
        
        results.append({
            'days': days,
            'start_date': start_date,
            'end_date': end_date_str,
            'users': user_count,
            'category': category,
            'detailed_category': detailed_category
        })
        
        print(f"  Users: {user_count}")
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Print summary
    print("\nURL Performance Summary:")
    print(f"URL: {url}")
    print(f"Publication Date: {start_date}")
    print("\nUser count by period:")
    for _, row in df.iterrows():
        print(f"  {row['days']} days: {row['users']} users ({row['category']})")
    
    # Save to file if specified
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"\nResults saved to {output_file}")
    else:
        # Create a default output filename if none was specified
        filename_safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        output_file = f"url_trend_{filename_safe_url}_{timestamp}.csv"
        df.to_csv(output_file, index=False)
        print(f"\nResults saved to {output_file}")
    
    # Create visualization using the visualization module
    try:
        # Generate a filename for the chart
        plot_file = output_file.replace(".csv", ".png")
        
        # Create the trend chart
        chart_path = create_trend_chart(
            df=df,
            x_column='days',
            y_column='users',
            title='User Growth Over Time',
            subtitle=url,
            x_label='Days Since Publication',
            y_label='Total Users',
            output_file=plot_file
        )
        
        if chart_path:
            print(f"Visualization saved to {chart_path}")
        else:
            print("Failed to create visualization.")
    except Exception as e:
        print(f"\nError creating visualization: {e}")

if __name__ == "__main__":
    main()
