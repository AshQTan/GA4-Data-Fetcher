#!/usr/bin/env python3
"""
Visualization Module - Tools for visualizing Google Analytics 4 data

This module provides functions to visualize GA4 analytics data in various formats:
1. Line charts for trend analysis over time
2. Bar charts for comparing different URLs or time periods
3. Comparison charts for multiple datasets
4. Interactive HTML visualizations (requires plotly)
5. Automatic detection and visualization of GA4 fetcher CSV output files

The module can be used in two ways:
1. As an imported module in other Python scripts
2. As a standalone command-line tool to visualize CSV files

Command line usage:
    python visualization.py your_ga4_data.csv --output chart.png
    python visualization.py your_ga4_data.csv --type bar
    python visualization.py your_ga4_data.csv --interactive

Import usage:
    from visualization import create_trend_chart, visualize_from_csv
    
    # Visualize directly from a CSV file
    visualize_from_csv('ga4_output.csv')
    
    # Or work with a DataFrame
    create_trend_chart(df, 'days', 'users', title='User Growth')
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def create_trend_chart(df, x_column, y_column, title=None, subtitle=None, 
                      x_label=None, y_label=None, output_file=None):
    """
    Create a line chart showing trends over time from DataFrame data.
    
    Args:
        df (DataFrame): pandas DataFrame containing the data to visualize
        x_column (str): Name of the column to use for x-axis values (typically days or dates)
        y_column (str): Name of the column to use for y-axis values (typically user counts)
        title (str, optional): Main title for the chart
        subtitle (str, optional): Subtitle for the chart (e.g., URL being analyzed)
        x_label (str, optional): Label for the x-axis (defaults to x_column name)
        y_label (str, optional): Label for the y-axis (defaults to y_column name)
        output_file (str, optional): Path to save the chart image (defaults to "trend_analysis.png")
        
    Returns:
        str: Path to the saved chart image file
    """
    try:
        # Create figure and axis
        plt.figure(figsize=(12, 7))
        
        # Plot the data
        plt.plot(df[x_column], df[y_column], marker='o', linestyle='-', linewidth=2)
        
        # Set title and subtitle
        if title:
            if subtitle:
                plt.suptitle(title, fontsize=16)
                plt.title(subtitle, fontsize=12, color='gray')
            else:
                plt.title(title, fontsize=16)
                
        # Set axis labels
        plt.xlabel(x_label if x_label else x_column, fontsize=12)
        plt.ylabel(y_label if y_label else y_column, fontsize=12)
        
        # Customize grid
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add data points and values
        for i, v in enumerate(df[y_column]):
            plt.text(df[x_column].iloc[i], v + max(df[y_column])*0.02, 
                     f"{v:,}", ha='center', fontsize=9)
        
        # Save the chart
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"trend_analysis_{timestamp}.png"
            
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        
        return output_file
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return None

def create_bar_chart(df, x_column, y_column, title=None, x_label=None, y_label=None, 
                    output_file=None, color='steelblue'):
    """
    Create a bar chart comparing different items or time periods.
    
    Args:
        df (DataFrame): pandas DataFrame containing the data to visualize
        x_column (str): Name of the column to use for x-axis categories
        y_column (str): Name of the column to use for y-axis values
        title (str, optional): Title for the chart
        x_label (str, optional): Label for the x-axis
        y_label (str, optional): Label for the y-axis
        output_file (str, optional): Path to save the chart image
        color (str, optional): Color for the bars
        
    Returns:
        str: Path to the saved chart image file
    """
    try:
        plt.figure(figsize=(12, 8))
        
        # Create the bar chart
        bars = plt.bar(df[x_column], df[y_column], color=color, alpha=0.8)
        
        # Add title and labels
        if title:
            plt.title(title, fontsize=16)
        plt.xlabel(x_label if x_label else x_column, fontsize=12)
        plt.ylabel(y_label if y_label else y_column, fontsize=12)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + max(df[y_column])*0.01,
                    f'{height:,}', ha='center', fontsize=9)
        
        # Add grid lines for y-axis
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save the chart
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"bar_chart_{timestamp}.png"
            
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        
        return output_file
    except Exception as e:
        print(f"Error creating bar chart: {e}")
        return None

def create_comparison_chart(df_list, labels, x_column, y_column, title, 
                           output_file=None, colors=None):
    """
    Create a line chart comparing multiple datasets.
    
    Args:
        df_list (list): List of DataFrames containing data to compare
        labels (list): Labels for each DataFrame in the legend
        x_column (str): Name of the column to use for x-axis values
        y_column (str): Name of the column to use for y-axis values
        title (str): Title for the chart
        output_file (str, optional): Path to save the chart image
        colors (list, optional): List of colors for each line
        
    Returns:
        str: Path to the saved chart image file
    """
    try:
        plt.figure(figsize=(12, 8))
        
        if not colors:
            colors = ['steelblue', 'darkorange', 'green', 'red', 'purple', 'brown', 'pink']
        
        # Plot each dataset
        for i, df in enumerate(df_list):
            color = colors[i % len(colors)]
            plt.plot(df[x_column], df[y_column], marker='o', linestyle='-', 
                    label=labels[i], color=color)
        
        # Add title, labels, and legend
        plt.title(title, fontsize=16)
        plt.xlabel(x_column, fontsize=12)
        plt.ylabel(y_column, fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Save the chart
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"comparison_chart_{timestamp}.png"
            
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        
        return output_file
    except Exception as e:
        print(f"Error creating comparison chart: {e}")
        return None

def save_interactive_html(df, x_column, y_column, title, output_file=None):
    """
    Create an interactive HTML visualization using Plotly (if available).
    
    Args:
        df (DataFrame): pandas DataFrame containing the data to visualize
        x_column (str): Name of the column to use for x-axis values
        y_column (str): Name of the column to use for y-axis values
        title (str): Title for the chart
        output_file (str, optional): Path to save the HTML file
        
    Returns:
        str: Path to the saved HTML file or None if Plotly is not available
    """
    try:
        import plotly.express as px
        
        # Create the interactive plot
        fig = px.line(df, x=x_column, y=y_column, title=title, markers=True)
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column,
            hovermode="x unified"
        )
        
        # Save the chart
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"interactive_chart_{timestamp}.html"
            
        fig.write_html(output_file)
        return output_file
    
    except ImportError:
        print("Plotly is not installed. Install it with: pip install plotly")
        return None
    except Exception as e:
        print(f"Error creating interactive visualization: {e}")
        return None

def load_ga4_data_from_csv(file_path):
    """
    Load GA4 data from a CSV file generated by one of the GA4 fetcher scripts.
    
    Args:
        file_path (str): Path to the CSV file containing GA4 data
        
    Returns:
        pandas.DataFrame: DataFrame containing the loaded data
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file doesn't appear to be a valid GA4 data file
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Verify this looks like GA4 data by checking for expected columns
        if 'url' not in df.columns:
            if 'days' in df.columns and 'users' in df.columns:
                # This appears to be URL trend analysis data
                print(f"Loaded URL trend data with {len(df)} time periods")
            else:
                print("Warning: File doesn't have a 'url' column. This may not be GA4 fetcher output.")
        else:
            print(f"Loaded GA4 data with {len(df)} URLs")
            
        return df
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        raise
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def detect_data_type(df):
    """
    Detect what type of GA4 data is in the DataFrame based on column patterns.
    
    Args:
        df (pandas.DataFrame): DataFrame containing GA4 data
        
    Returns:
        str: Data type description ('url_trend', 'multi_url_time_periods', 'date_range', 'uptodate', or 'unknown')
    """
    columns = set(df.columns)
    
    # URL trend analysis data (url_trend_analysis.py)
    if 'days' in columns and 'users' in columns and 'start_date' in columns and 'end_date' in columns:
        return 'url_trend'
    
    # Multi-URL with time periods data (ga4_fetcher.py)
    users_pattern = [col for col in columns if col.startswith('users_') and col.endswith('_days')]
    if 'url' in columns and users_pattern:
        return 'multi_url_time_periods'
    
    # Date range analytics data (date_range_analytics.py)
    if 'url' in columns and 'start_date' in columns and 'end_date' in columns and 'user_count' in columns:
        return 'date_range'
    
    # Up-to-date data (ga4_fetcher_uptodate.py)
    users_to_pattern = [col for col in columns if col.startswith('users_to_')]
    if 'url' in columns and 'date_published' in columns and users_to_pattern:
        return 'uptodate'
    
    # Unknown format
    return 'unknown'

def visualize_from_csv(file_path, output_file=None, chart_type='auto'):
    """
    Create visualizations directly from a GA4 fetcher CSV output file.
    
    This function:
    1. Loads data from a GA4 fetcher output CSV
    2. Detects the type of data
    3. Creates an appropriate visualization
    
    Args:
        file_path (str): Path to the GA4 data CSV file
        output_file (str, optional): Path for the output image file
        chart_type (str): Type of chart to create ('line', 'bar', 'auto')
        
    Returns:
        str: Path to the saved chart image
    """
    # Load the data
    df = load_ga4_data_from_csv(file_path)
    
    # Detect data type
    data_type = detect_data_type(df)
    print(f"Detected data type: {data_type}")
    
    # Generate output file path if not provided
    if not output_file:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{base_name}_chart_{timestamp}.png"
    
    # Create appropriate visualization based on data type
    if data_type == 'url_trend':
        # URL trend analysis data - create a trend chart
        return create_trend_chart(
            df=df,
            x_column='days',
            y_column='users',
            title='User Growth Over Time',
            subtitle=f"Analysis from {df['start_date'].iloc[0]} to {df['end_date'].iloc[-1]}",
            x_label='Days Since Start Date',
            y_label='Total Users',
            output_file=output_file
        )
    
    elif data_type == 'multi_url_time_periods':
        # Multiple URLs with various time periods - create a bar chart for a selected period
        # Find the time period columns (users_X_days)
        time_periods = [col for col in df.columns if col.startswith('users_') and col.endswith('_days')]
        if not time_periods:
            print("Error: No time period columns found")
            return None
            
        # Use the last time period by default (typically the longest)
        selected_period = time_periods[-1]
        period_days = selected_period.replace('users_', '').replace('_days', '')
        
        # Sort by user count for better visualization
        df_sorted = df.sort_values(by=selected_period, ascending=False).head(20)  # Limit to top 20
        
        if chart_type == 'auto' or chart_type == 'bar':
            return create_bar_chart(
                df=df_sorted,
                x_column='url',
                y_column=selected_period,
                title=f'Top Content Performance ({period_days} Days After Publication)',
                x_label='URL',
                y_label=f'Users ({period_days} Days)',
                output_file=output_file
            )
        else:
            # Create a line chart comparing top 5 URLs over different time periods
            df_top5 = df.sort_values(by=time_periods[-1], ascending=False).head(5)
            
            # Create a list of DataFrames for comparison
            df_list = []
            labels = []
            
            for _, row in df_top5.iterrows():
                url = row['url']
                url_short = url.split('/')[-1] if '/' in url else url
                
                # Create a DataFrame for this URL with all time periods
                url_data = {'days': [], 'users': []}
                for period in time_periods:
                    days = int(period.replace('users_', '').replace('_days', ''))
                    users = row[period]
                    url_data['days'].append(days)
                    url_data['users'].append(users)
                
                df_list.append(pd.DataFrame(url_data))
                labels.append(url_short)
            
            return create_comparison_chart(
                df_list=df_list,
                labels=labels,
                x_column='days',
                y_column='users',
                title='Top Content Performance Over Time',
                output_file=output_file
            )
    
    elif data_type == 'date_range':
        # Date range analytics data - create a bar chart
        # Sort by user count
        df_sorted = df.sort_values(by='user_count', ascending=False)
        
        return create_bar_chart(
            df=df_sorted,
            x_column='url',
            y_column='user_count',
            title=f'URL Performance ({df["start_date"].iloc[0]} to {df["end_date"].iloc[0]})',
            x_label='URL',
            y_label='Users',
            output_file=output_file
        )
    
    elif data_type == 'uptodate':
        # Up-to-date data - create a bar chart
        # Find the users_to_X column
        users_columns = [col for col in df.columns if col.startswith('users_to_')]
        if not users_columns:
            print("Error: No users_to_X columns found")
            return None
        
        # Use the first users_to_X column
        selected_column = users_columns[0]
        date_str = selected_column.replace('users_to_', '')
        
        # Sort by user count
        df_sorted = df.sort_values(by=selected_column, ascending=False).head(20)  # Limit to top 20
        
        return create_bar_chart(
            df=df_sorted,
            x_column='url',
            y_column=selected_column,
            title=f'Content Performance (Up to {date_str})',
            x_label='URL',
            y_label='Total Users',
            output_file=output_file
        )
    
    else:
        print("Unknown data format. Cannot create visualization automatically.")
        return None

if __name__ == "__main__":
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Visualize GA4 data from CSV files')
    parser.add_argument('input_file', type=str, help='Path to the CSV file containing GA4 data')
    parser.add_argument('--output', '-o', type=str, default=None, 
                        help='Output file path for the visualization (optional)')
    parser.add_argument('--type', '-t', choices=['line', 'bar', 'auto'], default='auto',
                        help='Type of chart to create (default: auto)')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Create interactive HTML visualization instead of static image')
    
    args = parser.parse_args()
    
    # Process the input file
    if args.interactive:
        try:
            # Try to create an interactive visualization
            df = load_ga4_data_from_csv(args.input_file)
            data_type = detect_data_type(df)
            
            if data_type == 'url_trend':
                output_file = args.output or args.input_file.replace('.csv', '.html')
                html_file = save_interactive_html(
                    df=df,
                    x_column='days',
                    y_column='users',
                    title='User Growth Over Time',
                    output_file=output_file
                )
                if html_file:
                    print(f"Interactive visualization saved to: {html_file}")
            elif data_type == 'multi_url_time_periods' or data_type == 'date_range' or data_type == 'uptodate':
                print("Interactive visualizations for this data type are not yet implemented")
                print("Creating static visualization instead...")
                chart_path = visualize_from_csv(args.input_file, args.output, args.type)
                if chart_path:
                    print(f"Visualization saved to: {chart_path}")
            else:
                print("Cannot create interactive visualization for unknown data format")
        except ImportError:
            print("Plotly is not installed. Install with: pip install plotly")
            print("Creating static visualization instead...")
            chart_path = visualize_from_csv(args.input_file, args.output, args.type)
            if chart_path:
                print(f"Visualization saved to: {chart_path}")
    else:
        # Create static visualization
        chart_path = visualize_from_csv(args.input_file, args.output, args.type)
        if chart_path:
            print(f"Visualization saved to: {chart_path}")
            
    print("\nExample direct usage in Python:")
    print("  from visualization import create_trend_chart, visualize_from_csv")
    print("  visualize_from_csv('your_data.csv', 'output_chart.png')")
    print("  # or")
    print("  create_trend_chart(df, 'days', 'users', title='User Growth', output_file='chart.png')")
