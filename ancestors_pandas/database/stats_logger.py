"""
Statistics logging module for AncestorsPandas.

This module provides functions for logging statistics to the database.
"""

import pandas as pd
from typing import Dict, List, Optional, Any

from ancestors_pandas.analysis.statistics import (
    get_summary_statistics,
    create_yearly_comparison,
    count_values
)
from ancestors_pandas.database.db import (
    store_summary_statistics,
    store_yearly_comparison,
    store_value_counts
)
from config import (
    YEAR_COL, IN_FS_COL, NORMALIZED_SURNAME_COL
)


def log_summary_statistics(
    df: pd.DataFrame,
    data_source: str,
    additional_data: Optional[Dict[str, Any]] = None,
    db_path: Optional[str] = None
) -> int:
    """
    Calculate and log summary statistics for a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    additional_data : Optional[Dict[str, Any]], optional
        Additional data to store with the statistics.
    db_path : Optional[str], optional
        Path to the SQLite database file. If None, uses the default path.

    Returns:
    --------
    int
        ID of the inserted record.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame or data_source is not a string.
    ValueError
        If data_source is empty.
    Exception
        For other errors during logging.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(data_source, str):
        raise TypeError(f"data_source must be a string, got {type(data_source).__name__}")

    if not data_source:
        raise ValueError("data_source cannot be empty")

    try:
        # Calculate summary statistics
        stats = get_summary_statistics(df)

        # Store statistics in the database
        kwargs = {'db_path': db_path} if db_path else {}
        return store_summary_statistics(stats, data_source, additional_data, **kwargs)
    except Exception as e:
        raise Exception(f"Error logging summary statistics: {str(e)}")


def log_yearly_comparison(
    df: pd.DataFrame,
    data_source: str,
    condition_col: str = IN_FS_COL,
    year_col: str = YEAR_COL,
    db_path: Optional[str] = None
) -> List[int]:
    """
    Calculate and log yearly comparison data for a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    condition_col : str, optional
        Name of the boolean column to filter by. Default is 'in_fs'.
    year_col : str, optional
        Name of the year column. Default is 'year'.
    db_path : Optional[str], optional
        Path to the SQLite database file. If None, uses the default path.

    Returns:
    --------
    List[int]
        List of IDs of the inserted records.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, data_source is not a string,
        condition_col is not a string, or year_col is not a string.
    ValueError
        If data_source, condition_col, or year_col is empty.
    KeyError
        If condition_col or year_col is not found in the DataFrame.
    Exception
        For other errors during logging.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(data_source, str):
        raise TypeError(f"data_source must be a string, got {type(data_source).__name__}")

    if not isinstance(condition_col, str):
        raise TypeError(f"condition_col must be a string, got {type(condition_col).__name__}")

    if not isinstance(year_col, str):
        raise TypeError(f"year_col must be a string, got {type(year_col).__name__}")

    if not data_source:
        raise ValueError("data_source cannot be empty")

    if not condition_col:
        raise ValueError("condition_col cannot be empty")

    if not year_col:
        raise ValueError("year_col cannot be empty")

    if condition_col not in df.columns:
        raise KeyError(f"Column '{condition_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    if year_col not in df.columns:
        raise KeyError(f"Column '{year_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        # Create yearly comparison DataFrame
        comparison_df = create_yearly_comparison(df, condition_col, year_col)

        # Store comparison data in the database
        kwargs = {'db_path': db_path} if db_path else {}
        return store_yearly_comparison(comparison_df, data_source, condition_col, **kwargs)
    except Exception as e:
        raise Exception(f"Error logging yearly comparison: {str(e)}")


def log_value_counts(
    df: pd.DataFrame,
    column_name: str,
    data_source: str,
    db_path: Optional[str] = None
) -> List[int]:
    """
    Calculate and log value counts for a column in a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    column_name : str
        Name of the column to count values from.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    db_path : Optional[str], optional
        Path to the SQLite database file. If None, uses the default path.

    Returns:
    --------
    List[int]
        List of IDs of the inserted records.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, column_name is not a string,
        or data_source is not a string.
    ValueError
        If column_name or data_source is empty.
    KeyError
        If column_name is not found in the DataFrame.
    Exception
        For other errors during logging.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(column_name, str):
        raise TypeError(f"column_name must be a string, got {type(column_name).__name__}")

    if not isinstance(data_source, str):
        raise TypeError(f"data_source must be a string, got {type(data_source).__name__}")

    if not column_name:
        raise ValueError("column_name cannot be empty")

    if not data_source:
        raise ValueError("data_source cannot be empty")

    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        # Count values in the column
        counts = count_values(df, column_name)

        # Store value counts in the database
        kwargs = {'db_path': db_path} if db_path else {}
        return store_value_counts(counts, column_name, data_source, **kwargs)
    except Exception as e:
        raise Exception(f"Error logging value counts: {str(e)}")


def log_surname_counts(
    df: pd.DataFrame,
    data_source: str,
    surname_col: str = NORMALIZED_SURNAME_COL,
    db_path: Optional[str] = None
) -> List[int]:
    """
    Calculate and log surname counts for a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    surname_col : str, optional
        Name of the surname column. Default is 'normalized_surname'.
    db_path : Optional[str], optional
        Path to the SQLite database file. If None, uses the default path.

    Returns:
    --------
    List[int]
        List of IDs of the inserted records.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, data_source is not a string,
        or surname_col is not a string.
    ValueError
        If data_source or surname_col is empty.
    KeyError
        If surname_col is not found in the DataFrame.
    Exception
        For other errors during logging.
    """
    return log_value_counts(df, surname_col, data_source, db_path)


def log_all_statistics(
    df: pd.DataFrame,
    data_source: str,
    additional_data: Optional[Dict[str, Any]] = None,
    condition_col: str = IN_FS_COL,
    year_col: str = YEAR_COL,
    surname_col: str = NORMALIZED_SURNAME_COL,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate and log all statistics for a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    additional_data : Optional[Dict[str, Any]], optional
        Additional data to store with the summary statistics.
    condition_col : str, optional
        Name of the boolean column to filter by. Default is 'in_fs'.
    year_col : str, optional
        Name of the year column. Default is 'year'.
    surname_col : str, optional
        Name of the surname column. Default is 'normalized_surname'.
    db_path : Optional[str], optional
        Path to the SQLite database file. If None, uses the default path.

    Returns:
    --------
    Dict[str, Any]
        Dictionary with IDs of the inserted records:
        - summary_id: ID of the summary statistics record
        - yearly_ids: List of IDs of the yearly comparison records
        - surname_ids: List of IDs of the surname counts records

    Raises:
    -------
    Exception
        For errors during logging.
    """
    result = {}
    kwargs = {'db_path': db_path} if db_path else {}

    try:
        # Log summary statistics
        result['summary_id'] = log_summary_statistics(df, data_source, additional_data, **kwargs)

        # Log yearly comparison if year_col and condition_col exist in the DataFrame
        if year_col in df.columns and condition_col in df.columns:
            result['yearly_ids'] = log_yearly_comparison(df, data_source, condition_col, year_col, **kwargs)
        else:
            result['yearly_ids'] = []

        # Log surname counts if surname_col exists in the DataFrame
        if surname_col in df.columns:
            result['surname_ids'] = log_surname_counts(df, data_source, surname_col, **kwargs)
        else:
            result['surname_ids'] = []

        return result
    except Exception as e:
        raise Exception(f"Error logging all statistics: {str(e)}")