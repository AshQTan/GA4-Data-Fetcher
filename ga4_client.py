"""
GA4 Client Module - Handles authentication and client initialization for Google Analytics 4

This module provides the functionality to authenticate with Google Analytics 4 (GA4)
using a service account and initialize a client that can make API requests. The
authentication process uses a service account JSON key file that must be created
in the Google Cloud Console and granted appropriate permissions in GA4.

Key features:
1. Authentication with GA4 using service account credentials
2. Creation of an authenticated API client for making GA4 data requests
3. Proper scope configuration for read-only access to analytics data

This module is a core dependency for all other scripts in this project as it
establishes the authenticated connection to the GA4 API.
"""
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account

def initialize_analytics_client(credentials_path):
    """
    Initialize and return a GA4 analytics client using service account credentials.
    
    This function creates an authenticated client that can make requests to the
    Google Analytics Data API (GA4). It requires a service account JSON key file
    that has been granted permissions to access the GA4 property.
    
    Args:
        credentials_path (str): Path to the service account credentials JSON file.
            This file must be downloaded from the Google Cloud Console after 
            creating a service account with appropriate permissions.
        
    Returns:
        BetaAnalyticsDataClient: Authenticated GA4 client that can be used to 
            make API requests to fetch analytics data.
            
    Raises:
        FileNotFoundError: If the credentials file doesn't exist at the specified path.
        ValueError: If the credentials file is invalid or has incorrect format.
        
    Example:
        client = initialize_analytics_client("path/to/service-account-key.json")
    """
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    return BetaAnalyticsDataClient(credentials=credentials)
