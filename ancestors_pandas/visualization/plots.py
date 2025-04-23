"""
Data visualization module for AncestorsPandas.

This module provides functions for visualizing genealogical data.
"""

import matplotlib.pyplot as plt
from typing import Optional, Tuple, Union
import pandas as pd


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
