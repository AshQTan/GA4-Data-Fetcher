# GA4 Data Fetcher

This project provides modular tools for fetching and analyzing Google Analytics 4 (GA4) data.

> **Note:** Replace `yourpage.com` with your actual website domain in all examples and code.

## Modules

The project has been organized into the following modules:

- `ga4_client.py`: Handles authentication and GA4 client initialization
- `ga4_data_fetcher.py`: Provides functions to fetch user data from GA4
- `user_classification.py`: Classifies user counts into milestone categories
- `batch_processor.py`: Contains functions for batch processing URLs from CSV files
- `visualization.py`: Provides tools for creating charts and visualizations from GA4 data
- `ga4_fetcher.py`: Main script for batch processing multiple URLs from a CSV file
- `ga4_fetcher_uptodate.py`: Specialized script for analyzing URLs from publication date to a fixed end date
- `single_url_analysis.py`: Example script for analyzing a single URL
- `date_range_analytics.py`: Script for analyzing multiple URLs for a specific date range
- `url_trend_analysis.py`: Script for analyzing a URL's performance over multiple time periods

## Prerequisites

- Python 3.6+
- Google Analytics 4 property
- Service account with GA4 access

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

If you only need basic functionality without visualization:

```bash
pip install pandas google-analytics-data
```

## Input CSV Format

The input CSV file for batch processing should contain at least the following columns:

- `url`: The full URL of the page (e.g., "https://www.yourpage.com/article-path")
- `date_published`: The publication date of the content in YYYY-MM-DD format (e.g., "2023-07-15")

Example:
```
url,date_published
https://www.yourpage.com/article1,2023-06-01
https://www.yourpage.com/article2,2023-06-15
https://www.yourpage.com/article3,2023-07-01
```

## Usage

### Analyzing a Single URL

The `single_url_analysis.py` script provides a quick way to check traffic for a single URL over a specific number of days up to the current date. This is useful for:

- Quick traffic checks for individual pages
- Testing your GA4 setup and authentication
- Ad-hoc reporting needs

```bash
python single_url_analysis.py --url "https://www.yourpage.com/example-page" --days 30
```

Additional options:
```bash
python single_url_analysis.py \
  --url "https://www.yourpage.com/example-page" \
  --days 90 \
  --credentials "path/to/your-credentials.json" \
  --property-id "your-property-id"
```

### Batch Processing from CSV

The main `ga4_fetcher.py` script processes multiple URLs from a CSV file and analyzes their performance over different time periods after their publication date. This is ideal for:

- Analyzing how content performs at different stages of its lifecycle
- Comparing performance of content at similar ages
- Bulk processing of many URLs
- Creating comprehensive performance reports

```bash
python ga4_fetcher.py --days 30 60 90 --input-file your_input.csv
```

The output will be saved to a file named `ga4_your_input.csv` automatically.

Additional options:
```bash
python ga4_fetcher.py \
  --days 30 90 180 360 \
  --input-file your_input.csv \
  --credentials "path/to/your-credentials.json" \
  --property-id "your-property-id" \
  --sleep-time 5
```

The `--sleep-time` parameter controls how many seconds to wait between API requests to avoid rate limiting.

### Up-to-Date Performance Analysis

The `ga4_fetcher_uptodate.py` script is a specialized variant of the main fetcher that retrieves analytics data for URLs from their publication date up to a specific end date provided by the user. This is useful for:

- Creating point-in-time snapshots of content performance
- Generating historical reports showing how content performed up to a specific date
- Comparing how different pieces of content performed at a fixed calendar point
- Retrospective analysis of content performance

Unlike the main fetcher which analyzes fixed periods after publication (e.g., first 30 days), this script analyzes from publication date to a single fixed end date (the same for all URLs).

```bash
python ga4_fetcher_uptodate.py --date 2023-12-31 --input_file your_input.csv
```

The output will be saved to a file named `ga4_uptodate_your_input.csv` automatically.

Additional options:
```bash
python ga4_fetcher_uptodate.py \
  --date 2023-12-31 \
  --input_file your_input.csv \
  --credentials "path/to/your-credentials.json" \
  --property_id "your-property-id" \
  --sleep 5
```

The `--sleep` parameter controls how many seconds to wait between API requests to avoid rate limiting.

### Date Range Analysis for Multiple URLs

The `date_range_analytics.py` script allows you to analyze multiple URLs for the same fixed date range. This is useful for:

- Comparing the performance of different pages during the same time period
- Analyzing seasonal traffic patterns across multiple pages
- Measuring the impact of marketing campaigns on different content
- Generating reports for specific reporting periods (monthly, quarterly, etc.)

Unlike `ga4_fetcher.py` which analyzes URLs from their publication date, this script applies the exact same date range to all URLs.

```bash
python date_range_analytics.py --start-date 2024-01-01 --end-date 2024-01-31 \
  --urls "https://www.yourpage.com/url1" "https://www.yourpage.com/url2"
```

The script will output a CSV file with:
- URL
- Start date
- End date
- User count
- Category classification
- Detailed category classification

### URL Performance Trend Analysis

The `url_trend_analysis.py` script helps you understand how traffic to a specific URL grows over different time periods from its publication date. This is useful for:

- Tracking the traffic growth pattern of content
- Understanding how quickly content reaches different user milestones
- Visualizing long-term performance trajectory
- Identifying which time periods show significant growth

The script can generate both tabular data and a visualization graph showing the growth curve.

```bash
python url_trend_analysis.py --url "https://www.yourpage.com/example-page" \
  --start-date 2024-01-01 --periods 7 30 90 180
```

The script will output:
1. A CSV file with data for each time period
2. A PNG graph visualization (if matplotlib is installed)
3. A summary in the terminal showing total users and growth patterns

## Module Usage

If you want to incorporate these functions in your own scripts, you can import the modules directly. This allows you to build custom analysis tools or integrate GA4 data into other applications.

### Basic Usage Example

```python
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url
from user_classification import classify_users

# Initialize client
client = initialize_analytics_client("path/to/credentials.json")

# Get user data for your URL
url = "https://www.yourpage.com/your-article"  # Replace with your actual URL
users = get_users_for_url(client, "your-property-id", url, "2023-01-01", "2023-01-31")

# Classify users
category = classify_users(users)
print(f"User category: {category}")
```

### Advanced Example: Compare Multiple URLs

```python
import pandas as pd
from ga4_client import initialize_analytics_client
from ga4_data_fetcher import get_users_for_url

# Initialize client
client = initialize_analytics_client("path/to/credentials.json")
property_id = "your-property-id"

# Define URLs and date range
urls = [
    "https://www.yourpage.com/article1",
    "https://www.yourpage.com/article2",
    "https://www.yourpage.com/article3"
]
start_date = "2023-01-01"
end_date = "2023-01-31"

# Collect data
results = []
for url in urls:
    users = get_users_for_url(client, property_id, url, start_date, end_date)
    results.append({"url": url, "users": users})

# Create DataFrame and analyze
df = pd.DataFrame(results)
print(f"Total users: {df['users'].sum()}")
print(f"Average users per URL: {df['users'].mean():.2f}")
print(f"Best performing URL: {df.loc[df['users'].idxmax()]['url']}")
```

### Using the Visualization Module

The visualization module can be used as both a command-line tool and an imported library.

#### Using as a Command-Line Tool

After collecting data with any of the GA4 fetcher scripts, you can directly visualize the results:

```bash
# Basic usage - automatically detects data type and creates appropriate chart
python visualization.py ga4_your_data.csv

# Specify output file
python visualization.py ga4_your_data.csv --output my_chart.png

# Choose chart type
python visualization.py ga4_your_data.csv --type bar

# Create interactive HTML visualization (requires plotly)
python visualization.py ga4_your_data.csv --interactive
```

The tool automatically detects the type of GA4 data in your CSV file (url trend analysis, batch processing, date range analysis, etc.) and creates an appropriate visualization.

#### Using as an Imported Module

You can also import the visualization functions in your own Python scripts:

```python
from visualization import create_trend_chart, create_bar_chart, visualize_from_csv
import pandas as pd

# Directly visualize a CSV file
visualize_from_csv('ga4_your_data.csv', output_file='chart.png')

# Or work with DataFrame data manually
df = pd.DataFrame({
    'days': [7, 30, 90, 180, 360],
    'users': [1200, 5400, 12500, 28000, 45000]
})

# Create a trend line chart
create_trend_chart(
    df=df,
    x_column='days',
    y_column='users',
    title='User Growth Over Time',
    subtitle='https://www.yourpage.com/article',
    x_label='Days Since Publication',
    y_label='Total Users',
    output_file='trend_chart.png'
)

# Create a bar chart for comparison
create_bar_chart(
    df=df,
    x_column='days',
    y_column='users',
    title='User Growth by Time Period',
    output_file='bar_chart.png'
)
```

For interactive charts (requires plotly):

```python
from visualization import save_interactive_html

# Create an interactive HTML chart
save_interactive_html(
    df=df,
    x_column='days',
    y_column='users',
    title='Interactive User Growth Chart',
    output_file='interactive_chart.html'
)
```

#### Recommended Workflow

1. Collect data using the appropriate GA4 fetcher script:
   ```bash
   python ga4_fetcher.py --days 30 90 180 --input-file your_urls.csv
   ```

2. Visualize the results:
   ```bash
   python visualization.py ga4_your_urls.csv
   ```

This separation allows you to:
- Collect data once and create multiple visualizations
- Share CSV data files with colleagues who can visualize them without API access
- Batch process data collection overnight and review visualizations later

## Example Workflow with ga4_fetcher

This section provides a step-by-step example workflow using `ga4_fetcher.py` from data preparation to visualization and analysis.

### Step 1: Prepare Your Input Data

Create a CSV file with your URLs and publication dates. For example, save the following as `content_analysis.csv`:

```
url,date_published
https://www.yourpage.com/report-2024,2024-01-15
https://www.yourpage.com/analysis-2024,2024-02-01
https://www.yourpage.com/news-update-2024,2024-03-10
https://www.yourpage.com/feature-story,2024-04-22
https://www.yourpage.com/special-report,2024-05-05
```

### Step 2: Collect Analytics Data

Run the `ga4_fetcher.py` script to collect analytics data for different time periods after publication:

```bash
python ga4_fetcher.py --days 7 30 90 --input-file content_analysis.csv --property-id "your-property-id" --credentials "your-credentials.json"
```

This command:
- Analyzes each URL for three time periods: 7 days, 30 days, and 90 days after publication
- Uses your GA4 property ID and service account credentials
- Processes all URLs in the input file

The script will:
1. Read your input CSV file
2. Connect to the GA4 API using your credentials
3. For each URL, calculate the date ranges based on publication date
4. Fetch user counts for each time period
5. Classify results into performance categories
6. Save the output to `ga4_content_analysis.csv`

### Step 3: Review the Results

The output file `ga4_content_analysis.csv` will contain the following columns:
- `url`: The original URL
- `date_published`: The content publication date
- `users_7_days`: Number of users in the first 7 days
- `users_30_days`: Number of users in the first 30 days
- `users_90_days`: Number of users in the first 90 days
- `milestone_7_days`: Performance category for the 7-day period
- `milestone_30_days`: Performance category for the 30-day period
- `milestone_90_days`: Performance category for the 90-day period
- `detailed_milestone_7_days`: Detailed performance category for 7-day period
- `detailed_milestone_30_days`: Detailed performance category for 30-day period
- `detailed_milestone_90_days`: Detailed performance category for 90-day period

Example output:
```
url,date_published,users_7_days,users_30_days,users_90_days,milestone_7_days,milestone_30_days,milestone_90_days,detailed_milestone_7_days,detailed_milestone_30_days,detailed_milestone_90_days
https://www.yourpage.com/report-2024,2024-01-15,1250,4300,8900,Medium,Medium,Medium,1k-5k,1k-10k,5k-10k
https://www.yourpage.com/analysis-2024,2024-02-01,750,2100,5600,Low,Low,Medium,500-1k,1k-5k,5k-10k
https://www.yourpage.com/news-update-2024,2024-03-10,4500,15000,32000,High,High,High,1k-5k,10k-50k,10k-50k
...
```

### Step 4: Visualize the Results

Create visualizations from the output data using the `visualization.py` module:

```bash
# Create a default visualization based on detected data type
python visualization.py ga4_content_analysis.csv

# Create a bar chart showing 30-day performance
python visualization.py ga4_content_analysis.csv --type bar

# Create an interactive HTML visualization (requires plotly)
python visualization.py ga4_content_analysis.csv --interactive
```

### Step 5: Advanced Analysis

For deeper analysis, you can import the data into your own Python scripts:

```python
import pandas as pd
from visualization import create_comparison_chart

# Load the data
df = pd.read_csv('ga4_content_analysis.csv')

# Filter to most successful content
top_performers = df.sort_values(by='users_90_days', ascending=False).head(3)

# Create separate DataFrames for comparison
df_list = []
labels = []

for _, row in top_performers.iterrows():
    url_short = row['url'].split('/')[-1]
    
    # Create a DataFrame with time periods and user counts
    data = {
        'days': [7, 30, 90],
        'users': [row['users_7_days'], row['users_30_days'], row['users_90_days']]
    }
    df_list.append(pd.DataFrame(data))
    labels.append(url_short)

# Create a comparison chart
create_comparison_chart(
    df_list=df_list,
    labels=labels,
    x_column='days',
    y_column='users',
    title='Top Content Performance Over Time',
    output_file='top_content_comparison.png'
)
```

### Step 6: Recurring Analysis

For ongoing content monitoring, set up a scheduled task to run the analysis regularly:

```bash
# Create a bash script named analyze_content.sh
echo '#!/bin/bash
python ga4_fetcher.py --days 7 30 90 --input-file content_analysis.csv
python visualization.py ga4_content_analysis.csv --output weekly_report.png
' > analyze_content.sh

# Make it executable
chmod +x analyze_content.sh

# Add to crontab to run weekly (adjust path as needed)
# crontab -e
# 0 7 * * 1 /path/to/analyze_content.sh
```

This workflow enables you to consistently monitor content performance across different time periods, identify trends, and optimize your content strategy based on data-driven insights.

## Google Analytics 4 Authentication Setup

To use this toolkit, you need to set up authentication with Google Analytics 4:

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Make note of your project ID

### Step 2: Enable the Google Analytics Data API
1. In your Google Cloud project, navigate to "APIs & Services" > "Library"
2. Search for "Google Analytics Data API"
3. Click on the API and select "Enable"

### Step 3: Create a Service Account
1. In your Google Cloud project, navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Enter a name and description for your service account
4. Click "Create and Continue"
5. (Optional) Grant the service account a role in your project (not required for GA4 access)
6. Click "Done"

### Step 4: Create a Service Account Key
1. In the service accounts list, click on your newly created service account
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select JSON format
5. Click "Create" - this will download a JSON key file
6. Keep this key file secure - it will be used to authenticate with GA4

### Step 5: Grant Access in GA4
1. Log in to your Google Analytics 4 account
2. Navigate to Admin > Property > Property Access Management
3. Click the "+" button to add a user
4. Enter the email address of your service account (it looks like: `name@project-id.iam.gserviceaccount.com`)
5. Assign "Viewer" or "Analyst" role (Viewer is sufficient for read-only access)
6. Click "Add"

### Step 6: Get Your Property ID
1. In Google Analytics 4, go to Admin > Property Settings
2. Find your Property ID (it's a number like "315823153")

### Step 7: Update Configuration
1. Place your downloaded JSON key file in your project directory
2. Update the `credentials_path` parameter in your scripts to point to this file
3. Update the `property_id` parameter with your GA4 Property ID

Now you're ready to use the GA4 Data Fetcher toolkit!

> **Note**: For information about the GA4 Data API dimensions, metrics, and filter specifications used in this project, refer to the [official Google Analytics 4 Data API Schema documentation](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema).

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. **Check your credentials file**: Ensure the JSON key file exists and is properly formatted
2. **Verify service account permissions**: Make sure the service account has been added to your GA4 property with proper permissions
3. **Check property ID**: Verify that you're using the correct GA4 property ID
4. **API enablement**: Ensure the Google Analytics Data API is enabled in your Google Cloud project

### No Data or Zero Results

If your queries return zero users or no data:

1. **Verify URL format**: Ensure URLs include the full path with "https://" prefix
2. **Check domain in ga4_data_fetcher.py**: Update the domain check in `create_url_regex_pattern()` to match your site
3. **Date range issues**: Ensure the date range is valid and within the time your GA4 property has been collecting data
4. **Property configuration**: Verify that your GA4 property is correctly collecting data for the URLs you're querying

### Rate Limiting

If you encounter rate limit errors:

1. **Increase sleep time**: Use the `--sleep-time` parameter to increase the wait between API requests
2. **Reduce batch size**: Process fewer URLs at once
3. **Check quotas**: Review your Google Cloud project quotas for the Analytics Data API

### Installation Problems

If you have issues installing dependencies:

1. **Upgrade pip**: `pip install --upgrade pip`
2. **Check Python version**: Ensure you're using Python 3.6+
3. **Virtual environment**: Consider using a virtual environment for clean installation
4. **Dependencies**: If only installing core packages: `pip install google-analytics-data pandas`

## References and Documentation

- [Google Analytics 4 Data API Schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) - Official documentation for the GA4 Data API, including dimensions, metrics, and filter specifications used in this project.
