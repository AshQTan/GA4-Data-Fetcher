#!/usr/bin/env python3
"""
Visualization Module - Tools for visualizing Google Analytics 4 data

This module provides functions to visualize GA4 analytics data in various formats:
1. Line charts for trend analysis over time
2. Bar charts for comparing different URLs or time periods
3. Saving visualizations to various file formats

The module is designed to work with pandas DataFrames containing GA4 data
and can be imported by other scripts that need visualization functionality.
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

if __name__ == "__main__":
    print("This module is intended to be imported by other scripts.")
    print("Example usage:")
    print("  from visualization import create_trend_chart")
    print("  create_trend_chart(df, 'days', 'users', title='User Growth', output_file='chart.png')")
