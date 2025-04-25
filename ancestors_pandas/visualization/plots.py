"""
Data visualization module for AncestorsPandas.

This module provides functions for visualizing genealogical data.
"""

import matplotlib.pyplot as plt
from typing import Optional, Tuple, Union, List, Dict, Any
import pandas as pd
import datetime


def plot_yearly_counts(
    yearly_counts: pd.DataFrame,
    figsize: Tuple[int, int] = (10, 6),
    title: str = 'Total Records vs. Records in FS',
    xlabel: str = 'Year',
    ylabel: str = 'Number of Records',
    save_path: Optional[str] = None
) -> None:
    """
    Plots a bar chart of the total records by year vs. records in FS by year.

    Parameters:
    -----------
    yearly_counts : pd.DataFrame
        A dataframe with columns 'Total Records' and 'Records in FS'
        indexed by year.
    figsize : Tuple[int, int], optional
        Figure size as (width, height) in inches. Default is (10, 6).
    title : str, optional
        Title of the plot. Default is 'Total Records vs. Records in FS'.
    xlabel : str, optional
        Label for the x-axis. Default is 'Year'.
    ylabel : str, optional
        Label for the y-axis. Default is 'Number of Records'.
    save_path : str, optional
        Path to save the figure. If None, the figure is displayed but not saved.

    Raises:
    -------
    TypeError
        If yearly_counts is not a pandas DataFrame, or if other parameters have incorrect types.
    ValueError
        If figsize contains non-positive values or if required columns are missing.
    Exception
        For other errors during plotting.
    """
    # Validate input
    if not isinstance(yearly_counts, pd.DataFrame):
        raise TypeError(f"yearly_counts must be a pandas DataFrame, got {type(yearly_counts).__name__}")

    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError(f"figsize must be a tuple of length 2, got {type(figsize).__name__}")

    if not all(isinstance(x, (int, float)) for x in figsize):
        raise TypeError("figsize elements must be numeric")

    if any(x <= 0 for x in figsize):
        raise ValueError("figsize elements must be positive")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")

    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")

    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")

    if save_path is not None and not isinstance(save_path, str):
        raise TypeError(f"save_path must be a string or None, got {type(save_path).__name__}")

    # Check if DataFrame has at least one column
    if yearly_counts.empty:
        raise ValueError("yearly_counts DataFrame is empty")

    try:
        yearly_counts.plot(kind='bar', figsize=figsize)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    except Exception as e:
        raise Exception(f"Error plotting yearly counts: {str(e)}")


def plot_surname_counts(
    surname_counts: pd.Series,
    figsize: Tuple[int, int] = (10, 6),
    title: str = "Instances of Each Normalized Surname",
    xlabel: str = "Normalized Surname",
    ylabel: str = "Count",
    top_n: Optional[int] = None,
    save_path: Optional[str] = None
) -> None:
    """
    Plots a bar chart of surname counts.

    Parameters:
    -----------
    surname_counts : pd.Series
        A series with the count of surnames (already normalized).
    figsize : Tuple[int, int], optional
        Figure size as (width, height) in inches. Default is (10, 6).
    title : str, optional
        Title of the plot. Default is 'Instances of Each Normalized Surname'.
    xlabel : str, optional
        Label for the x-axis. Default is 'Normalized Surname'.
    ylabel : str, optional
        Label for the y-axis. Default is 'Count'.
    top_n : int, optional
        If provided, only the top N surnames by count will be plotted.
    save_path : str, optional
        Path to save the figure. If None, the figure is displayed but not saved.

    Raises:
    -------
    TypeError
        If surname_counts is not a pandas Series, or if other parameters have incorrect types.
    ValueError
        If figsize contains non-positive values, if top_n is not positive, or if the Series is empty.
    Exception
        For other errors during plotting.
    """
    # Validate input
    if not isinstance(surname_counts, pd.Series):
        raise TypeError(f"surname_counts must be a pandas Series, got {type(surname_counts).__name__}")

    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError(f"figsize must be a tuple of length 2, got {type(figsize).__name__}")

    if not all(isinstance(x, (int, float)) for x in figsize):
        raise TypeError("figsize elements must be numeric")

    if any(x <= 0 for x in figsize):
        raise ValueError("figsize elements must be positive")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")

    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")

    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")

    if top_n is not None:
        if not isinstance(top_n, int):
            raise TypeError(f"top_n must be an integer or None, got {type(top_n).__name__}")
        if top_n <= 0:
            raise ValueError("top_n must be positive")

    if save_path is not None and not isinstance(save_path, str):
        raise TypeError(f"save_path must be a string or None, got {type(save_path).__name__}")

    # Check if Series is empty
    if surname_counts.empty:
        raise ValueError("surname_counts Series is empty")

    try:
        plt.figure(figsize=figsize)

        if top_n is not None and top_n > 0:
            surname_counts = surname_counts.head(top_n)

        surname_counts.plot(kind='bar')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    except Exception as e:
        raise Exception(f"Error plotting surname counts: {str(e)}")


def plot_pie_chart(
    data: Union[pd.Series, dict],
    figsize: Tuple[int, int] = (8, 8),
    title: str = "Distribution",
    autopct: str = '%1.1f%%',
    save_path: Optional[str] = None
) -> None:
    """
    Plots a pie chart of the provided data.

    Parameters:
    -----------
    data : pd.Series or dict
        Data to plot as a pie chart. If a Series, the index is used for labels.
    figsize : Tuple[int, int], optional
        Figure size as (width, height) in inches. Default is (8, 8).
    title : str, optional
        Title of the plot. Default is 'Distribution'.
    autopct : str, optional
        Format string for the percentages. Default is '%1.1f%%'.
    save_path : str, optional
        Path to save the figure. If None, the figure is displayed but not saved.

    Raises:
    -------
    TypeError
        If data is not a pandas Series or dict, or if other parameters have incorrect types.
    ValueError
        If figsize contains non-positive values, if data is empty, or if data contains non-numeric values.
    Exception
        For other errors during plotting.
    """
    # Validate input
    if not isinstance(data, (pd.Series, dict)):
        raise TypeError(f"data must be a pandas Series or dict, got {type(data).__name__}")

    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError(f"figsize must be a tuple of length 2, got {type(figsize).__name__}")

    if not all(isinstance(x, (int, float)) for x in figsize):
        raise TypeError("figsize elements must be numeric")

    if any(x <= 0 for x in figsize):
        raise ValueError("figsize elements must be positive")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")

    if not isinstance(autopct, str):
        raise TypeError(f"autopct must be a string, got {type(autopct).__name__}")

    if save_path is not None and not isinstance(save_path, str):
        raise TypeError(f"save_path must be a string or None, got {type(save_path).__name__}")

    # Check if data is empty
    if isinstance(data, pd.Series):
        if data.empty:
            raise ValueError("data Series is empty")
        # Check if all values are numeric
        if not pd.api.types.is_numeric_dtype(data):
            raise ValueError("data Series must contain numeric values")
    else:  # dict
        if not data:
            raise ValueError("data dict is empty")
        # Check if all values are numeric
        if not all(isinstance(v, (int, float)) for v in data.values()):
            raise ValueError("data dict values must be numeric")

    try:
        plt.figure(figsize=figsize)

        if isinstance(data, pd.Series):
            data.plot(kind='pie', autopct=autopct)
        else:
            labels = list(data.keys())
            values = list(data.values())
            plt.pie(values, labels=labels, autopct=autopct)

        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    except Exception as e:
        raise Exception(f"Error plotting pie chart: {str(e)}")


def plot_statistics_over_time(
    df: pd.DataFrame,
    value_column: str,
    date_column: str = 'timestamp',
    data_source_column: Optional[str] = 'data_source',
    figsize: Tuple[int, int] = (12, 6),
    title: str = 'Statistics Over Time',
    xlabel: str = 'Date',
    ylabel: Optional[str] = None,
    include_legend: bool = True,
    save_path: Optional[str] = None
) -> None:
    """
    Plots changes in statistics over time from historical data.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the historical statistics data.
    value_column : str
        Name of the column containing the values to plot.
    date_column : str, optional
        Name of the column containing the dates. Default is 'timestamp'.
    data_source_column : str, optional
        Name of the column containing the data source. If provided, data will be grouped by this column.
        If None, all data will be plotted together. Default is 'data_source'.
    figsize : Tuple[int, int], optional
        Figure size as (width, height) in inches. Default is (12, 6).
    title : str, optional
        Title of the plot. Default is 'Statistics Over Time'.
    xlabel : str, optional
        Label for the x-axis. Default is 'Date'.
    ylabel : str, optional
        Label for the y-axis. If None, uses the value_column name. Default is None.
    include_legend : bool, optional
        Whether to include a legend in the plot. Default is True.
    save_path : str, optional
        Path to save the figure. If None, the figure is displayed but not saved.

    Raises:
    -------
    TypeError
        If parameters have incorrect types.
    ValueError
        If required columns are missing or if figsize contains non-positive values.
    Exception
        For other errors during plotting.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(value_column, str):
        raise TypeError(f"value_column must be a string, got {type(value_column).__name__}")

    if not isinstance(date_column, str):
        raise TypeError(f"date_column must be a string, got {type(date_column).__name__}")

    if data_source_column is not None and not isinstance(data_source_column, str):
        raise TypeError(f"data_source_column must be a string or None, got {type(data_source_column).__name__}")

    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError(f"figsize must be a tuple of length 2, got {type(figsize).__name__}")

    if not all(isinstance(x, (int, float)) for x in figsize):
        raise TypeError("figsize elements must be numeric")

    if any(x <= 0 for x in figsize):
        raise ValueError("figsize elements must be positive")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")

    if not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string, got {type(xlabel).__name__}")

    if ylabel is not None and not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string or None, got {type(ylabel).__name__}")

    if not isinstance(include_legend, bool):
        raise TypeError(f"include_legend must be a boolean, got {type(include_legend).__name__}")

    if save_path is not None and not isinstance(save_path, str):
        raise TypeError(f"save_path must be a string or None, got {type(save_path).__name__}")

    # Check if required columns exist
    if value_column not in df.columns:
        raise ValueError(f"Column '{value_column}' not found in DataFrame")

    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")

    if data_source_column is not None and data_source_column not in df.columns:
        raise ValueError(f"Column '{data_source_column}' not found in DataFrame")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("DataFrame is empty")

    try:
        # Make a copy to avoid modifying the original DataFrame
        plot_df = df.copy()

        # Ensure date column is datetime type
        if not pd.api.types.is_datetime64_any_dtype(plot_df[date_column]):
            plot_df[date_column] = pd.to_datetime(plot_df[date_column])

        # Sort by date
        plot_df = plot_df.sort_values(by=date_column)

        plt.figure(figsize=figsize)

        # If data_source_column is provided, group by it
        if data_source_column is not None and data_source_column in plot_df.columns:
            for source, group in plot_df.groupby(data_source_column):
                plt.plot(group[date_column], group[value_column], marker='o', linestyle='-', label=source)
            if include_legend:
                plt.legend()
        else:
            plt.plot(plot_df[date_column], plot_df[value_column], marker='o', linestyle='-')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel if ylabel is not None else value_column)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    except Exception as e:
        raise Exception(f"Error plotting statistics over time: {str(e)}")


def plot_statistics_comparison(
    df: pd.DataFrame,
    value_column: str,
    group_column: str,
    date_column: str = 'timestamp',
    comparison_dates: Optional[List[Union[str, datetime.datetime]]] = None,
    max_dates: int = 2,
    figsize: Tuple[int, int] = (12, 8),
    title: str = 'Statistics Comparison Between Updates',
    xlabel: Optional[str] = None,
    ylabel: str = 'Value',
    kind: str = 'bar',
    save_path: Optional[str] = None
) -> None:
    """
    Plots a comparison of statistics between different data updates.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the historical statistics data.
    value_column : str
        Name of the column containing the values to compare.
    group_column : str
        Name of the column to group by (e.g., 'year', 'value', etc.).
    date_column : str, optional
        Name of the column containing the dates. Default is 'timestamp'.
    comparison_dates : List[Union[str, datetime.datetime]], optional
        Specific dates to compare. If None, the most recent dates will be used.
    max_dates : int, optional
        Maximum number of dates to compare if comparison_dates is None. Default is 2.
    figsize : Tuple[int, int], optional
        Figure size as (width, height) in inches. Default is (12, 8).
    title : str, optional
        Title of the plot. Default is 'Statistics Comparison Between Updates'.
    xlabel : str, optional
        Label for the x-axis. If None, uses the group_column name. Default is None.
    ylabel : str, optional
        Label for the y-axis. Default is 'Value'.
    kind : str, optional
        Kind of plot to create. Options include 'bar', 'barh', 'line'. Default is 'bar'.
    save_path : str, optional
        Path to save the figure. If None, the figure is displayed but not saved.

    Raises:
    -------
    TypeError
        If parameters have incorrect types.
    ValueError
        If required columns are missing, if figsize contains non-positive values,
        or if kind is not a supported plot type.
    Exception
        For other errors during plotting.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(value_column, str):
        raise TypeError(f"value_column must be a string, got {type(value_column).__name__}")

    if not isinstance(group_column, str):
        raise TypeError(f"group_column must be a string, got {type(group_column).__name__}")

    if not isinstance(date_column, str):
        raise TypeError(f"date_column must be a string, got {type(date_column).__name__}")

    if comparison_dates is not None:
        if not isinstance(comparison_dates, list):
            raise TypeError(f"comparison_dates must be a list or None, got {type(comparison_dates).__name__}")
        if not all(isinstance(d, (str, datetime.datetime)) for d in comparison_dates):
            raise TypeError("All elements in comparison_dates must be strings or datetime objects")

    if not isinstance(max_dates, int):
        raise TypeError(f"max_dates must be an integer, got {type(max_dates).__name__}")

    if max_dates <= 0:
        raise ValueError("max_dates must be positive")

    if not isinstance(figsize, tuple) or len(figsize) != 2:
        raise TypeError(f"figsize must be a tuple of length 2, got {type(figsize).__name__}")

    if not all(isinstance(x, (int, float)) for x in figsize):
        raise TypeError("figsize elements must be numeric")

    if any(x <= 0 for x in figsize):
        raise ValueError("figsize elements must be positive")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string, got {type(title).__name__}")

    if xlabel is not None and not isinstance(xlabel, str):
        raise TypeError(f"xlabel must be a string or None, got {type(xlabel).__name__}")

    if not isinstance(ylabel, str):
        raise TypeError(f"ylabel must be a string, got {type(ylabel).__name__}")

    if not isinstance(kind, str):
        raise TypeError(f"kind must be a string, got {type(kind).__name__}")

    if kind not in ['bar', 'barh', 'line']:
        raise ValueError(f"kind must be one of 'bar', 'barh', 'line', got '{kind}'")

    if save_path is not None and not isinstance(save_path, str):
        raise TypeError(f"save_path must be a string or None, got {type(save_path).__name__}")

    # Check if required columns exist
    if value_column not in df.columns:
        raise ValueError(f"Column '{value_column}' not found in DataFrame")

    if group_column not in df.columns:
        raise ValueError(f"Column '{group_column}' not found in DataFrame")

    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("DataFrame is empty")

    try:
        # Make a copy to avoid modifying the original DataFrame
        plot_df = df.copy()

        # Ensure date column is datetime type
        if not pd.api.types.is_datetime64_any_dtype(plot_df[date_column]):
            plot_df[date_column] = pd.to_datetime(plot_df[date_column])

        # Get the dates to compare
        if comparison_dates is not None:
            # Convert string dates to datetime
            dates_to_compare = []
            for d in comparison_dates:
                if isinstance(d, str):
                    dates_to_compare.append(pd.to_datetime(d))
                else:
                    dates_to_compare.append(d)
        else:
            # Get the most recent dates
            unique_dates = plot_df[date_column].dt.date.unique()
            unique_dates = sorted(unique_dates, reverse=True)[:max_dates]
            dates_to_compare = [pd.to_datetime(d) for d in unique_dates]

        # Filter data for the selected dates
        filtered_data = []
        date_labels = []

        for date in dates_to_compare:
            # Get data for this date (matching only the date part)
            date_data = plot_df[plot_df[date_column].dt.date == date.date()]

            if not date_data.empty:
                # Create a pivot table with group_column as index and date as column
                pivot_data = date_data.pivot_table(
                    values=value_column,
                    index=group_column,
                    aggfunc='first'  # Take the first value if there are duplicates
                )

                filtered_data.append(pivot_data)
                date_labels.append(date.strftime('%Y-%m-%d'))

        if not filtered_data:
            raise ValueError("No data found for the specified dates")

        # Combine the data for all dates
        combined_data = pd.concat(filtered_data, axis=1, keys=date_labels)

        # Plot the data
        plt.figure(figsize=figsize)

        if kind == 'line':
            combined_data.plot(kind=kind, marker='o')
        else:
            combined_data.plot(kind=kind)

        plt.title(title)
        plt.xlabel(xlabel if xlabel is not None else group_column)
        plt.ylabel(ylabel)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(title='Date')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    except Exception as e:
        raise Exception(f"Error plotting statistics comparison: {str(e)}")
