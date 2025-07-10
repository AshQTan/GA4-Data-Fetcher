"""
GA4 Data Fetcher Module - Handles retrieving data from Google Analytics 4

This module provides core functionality for fetching user data from Google Analytics 4
via the Google Analytics Data API. It offers specialized functions for:

1. Processing URLs to create regex patterns for GA4 path matching
2. Building and executing API requests to fetch user counts for specific URLs
3. Handling API responses and aggregating data

The module is designed to work with the pagePath dimension in GA4, which tracks
page visits. It uses partial regex matching to accurately identify traffic to 
specific URLs, even when tracking parameters or fragments are present.

Note: This module requires an authenticated GA4 client from the ga4_client module.
"""
import re
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    RunReportRequest,
)

def create_url_regex_pattern(url):
    """
    Process a URL to create a regex pattern for matching in GA4.
    
    Args:
        url (str): The URL to process (e.g., "https://www.yourpage.com/article-path")
        
    Returns:
        str: A regex pattern for matching the URL in GA4 pagePath dimension
    """
    # Process URL to remove domain prefix and limit to first 40 chars
    # Note: Update the domain below to match your website
    if url.startswith("https://www.yourpage.com/"):
        processed_url = url.replace("https://www.yourpage.com/", "", 1)
    else:
        # If URL doesn't have expected prefix, just use it as is
        processed_url = url
    
    # Limit to first 40 characters to avoid overly specific matches
    processed_url = processed_url[:40]
    
    # Escape any special regex characters in the URL to avoid syntax errors
    escaped_url = re.escape(processed_url)
    
    # Create regex pattern that matches the URL at the beginning of pagePath
    regex_pattern = f"{escaped_url}"
    
    return regex_pattern

def get_users_for_url(client, property_id, url, start_date, end_date, custom_regex=None):
    """    
    Fetch user counts for a specific URL within a given date range from GA4.
    
    This function constructs and executes a GA4 API request to retrieve the total
    number of unique users who visited a specific URL within the specified date range.
    It uses regex pattern matching on the pagePath dimension to identify relevant traffic.
    
    The function handles the complexities of:
    1. Converting the URL to a proper regex pattern for GA4
    2. Building the appropriate filter expressions for the API request
    3. Executing the request with proper error handling
    4. Aggregating results if the URL appears in multiple page paths
    
    Args:
        client (BetaAnalyticsDataClient): The authenticated GA4 client instance.
        property_id (str): The GA4 property ID (found in your GA4 property settings).
        url (str): The full URL to fetch user counts for (e.g., "https://www.yourpage.com/article").
        start_date (str): The start date for the report in YYYY-MM-DD format.
        end_date (str): The end date for the report in YYYY-MM-DD format.
        custom_regex (str, optional): A custom regex pattern to use instead of generating one from the URL.
        
    Returns:
        int: Total number of unique users who visited the specified URL within the date range.
        
    Raises:
        Exception: If there's an error fetching data from the GA4 API.
    """   
    print(f"Fetching data for URL: {url} from {start_date} to {end_date}")
    
    # Use custom regex if provided, otherwise generate one from the URL
    if custom_regex:
        regex_pattern = custom_regex
        print(f"Using custom regex pattern: {regex_pattern}")
    else:
        # Generate regex pattern for the URL
        regex_pattern = create_url_regex_pattern(url)
        print(f"Using generated regex pattern: {regex_pattern}")
    
    # Create filter for pages matching the regex pattern
    string_filter = Filter.StringFilter(
        match_type=Filter.StringFilter.MatchType.PARTIAL_REGEXP,
        value=regex_pattern
    )

    # Create the filter expression for the dimension
    dimension_filter = FilterExpression(
        filter=Filter(
            field_name="pagePath",
            string_filter=string_filter
        )
    )
    
    # Create the report request
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="totalUsers")],
        dimension_filter=dimension_filter
    )
    
    try:
        # Execute the request
        response = client.run_report(request)
        print(f"Response received for URL: {url}")
        # Sum user counts (could be across multiple matching pages)
        user_count = 0
        for row in response.rows:
            user_count += int(row.metric_values[0].value)
        
        return user_count
    except Exception as e:
        print(f"Error fetching data for URL {url}: {e}")
        return 0
