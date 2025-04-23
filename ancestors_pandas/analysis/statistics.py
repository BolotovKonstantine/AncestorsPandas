"""
Statistical analysis module for AncestorsPandas.

This module provides functions for statistical analysis of genealogical data.
"""

import pandas as pd
from typing import Dict, Tuple, Optional


def count_records_by_year(df: pd.DataFrame, year_col: str = 'year') -> pd.Series:
    """
    Count the number of records per year.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    year_col : str, optional
        Name of the year column. Default is 'year'.

    Returns:
    --------
    pd.Series
        Series with years as index and counts as values.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame or year_col is not a string.
    ValueError
        If year_col is empty.
    KeyError
        If year_col is not found in the DataFrame.
    Exception
        For other errors during counting.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(year_col, str):
        raise TypeError(f"year_col must be a string, got {type(year_col).__name__}")

    if not year_col:
        raise ValueError("year_col cannot be empty")

    if year_col not in df.columns:
        raise KeyError(f"Column '{year_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        return df.groupby(year_col).size()
    except Exception as e:
        raise Exception(f"Error counting records by year: {str(e)}")


def count_records_by_year_with_condition(
    df: pd.DataFrame, condition_col: str, year_col: str = 'year'
) -> pd.Series:
    """
    Count the number of records per year that meet a specific condition.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    condition_col : str
        Name of the boolean column to filter by.
    year_col : str, optional
        Name of the year column. Default is 'year'.

    Returns:
    --------
    pd.Series
        Series with years as index and counts as values.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, condition_col is not a string, or year_col is not a string.
    ValueError
        If condition_col or year_col is empty.
    KeyError
        If condition_col or year_col is not found in the DataFrame.
    Exception
        For other errors during counting.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(condition_col, str):
        raise TypeError(f"condition_col must be a string, got {type(condition_col).__name__}")

    if not isinstance(year_col, str):
        raise TypeError(f"year_col must be a string, got {type(year_col).__name__}")

    if not condition_col:
        raise ValueError("condition_col cannot be empty")

    if not year_col:
        raise ValueError("year_col cannot be empty")

    if condition_col not in df.columns:
        raise KeyError(f"Column '{condition_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    if year_col not in df.columns:
        raise KeyError(f"Column '{year_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        # Check if condition_col contains boolean values
        if not pd.api.types.is_bool_dtype(df[condition_col]) and not all(isinstance(x, bool) for x in df[condition_col].dropna()):
            # Try to convert to boolean if possible
            try:
                df = df.copy()
                df[condition_col] = df[condition_col].astype(bool)
            except Exception:
                raise ValueError(f"Column '{condition_col}' must contain boolean values or values that can be converted to boolean")

        return df[df[condition_col]].groupby(year_col).size()
    except KeyError as e:
        raise KeyError(f"Error accessing columns: {str(e)}")
    except Exception as e:
        raise Exception(f"Error counting records by year with condition: {str(e)}")


def create_yearly_comparison(
    df: pd.DataFrame, condition_col: str, year_col: str = 'year'
) -> pd.DataFrame:
    """
    Create a DataFrame comparing total records vs. records meeting a condition by year.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    condition_col : str
        Name of the boolean column to filter by.
    year_col : str, optional
        Name of the year column. Default is 'year'.

    Returns:
    --------
    pd.DataFrame
        DataFrame with years as index and columns for total records and records meeting the condition.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, condition_col is not a string, or year_col is not a string.
    ValueError
        If condition_col or year_col is empty.
    KeyError
        If condition_col or year_col is not found in the DataFrame.
    Exception
        For other errors during comparison creation.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(condition_col, str):
        raise TypeError(f"condition_col must be a string, got {type(condition_col).__name__}")

    if not isinstance(year_col, str):
        raise TypeError(f"year_col must be a string, got {type(year_col).__name__}")

    if not condition_col:
        raise ValueError("condition_col cannot be empty")

    if not year_col:
        raise ValueError("year_col cannot be empty")

    if condition_col not in df.columns:
        raise KeyError(f"Column '{condition_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    if year_col not in df.columns:
        raise KeyError(f"Column '{year_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        # count_records_by_year and count_records_by_year_with_condition already validate their inputs
        total_records = count_records_by_year(df, year_col)
        condition_records = count_records_by_year_with_condition(df, condition_col, year_col)

        comparison_df = pd.DataFrame({
            'Total Records': total_records,
            f'Records with {condition_col}': condition_records
        }).fillna(0)

        return comparison_df
    except Exception as e:
        raise Exception(f"Error creating yearly comparison: {str(e)}")


def count_values(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Count the occurrences of each unique value in a column.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.
    column : str
        Name of the column to count values from.

    Returns:
    --------
    pd.Series
        Series with unique values as index and counts as values, sorted in descending order.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame or column is not a string.
    ValueError
        If column is empty.
    KeyError
        If column is not found in the DataFrame.
    Exception
        For other errors during counting.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(column, str):
        raise TypeError(f"column must be a string, got {type(column).__name__}")

    if not column:
        raise ValueError("column cannot be empty")

    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        return df[column].value_counts()
    except Exception as e:
        raise Exception(f"Error counting values in column {column}: {str(e)}")


def get_summary_statistics(df: pd.DataFrame) -> Dict[str, int]:
    """
    Get summary statistics for a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing genealogical data.

    Returns:
    --------
    Dict[str, int]
        Dictionary with summary statistics including:
        - total_records: Total number of records in the DataFrame
        - unique_years: Number of unique years (if 'year' column exists)
        - missing_values: Total number of missing values in the DataFrame
        - records_in_fs: Number of records in FS (if 'in_fs' column exists)
        - unique_surnames: Number of unique surnames (if 'normalized_surname' column exists)

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame.
    Exception
        For other errors during statistics calculation.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    try:
        stats = {
            'total_records': len(df),
            'missing_values': df.isna().sum().sum()
        }

        # Add year statistics if the column exists
        if 'year' in df.columns:
            stats['unique_years'] = df['year'].nunique()
        else:
            stats['unique_years'] = 0

        # Add FS statistics if the column exists
        if 'in_fs' in df.columns:
            if pd.api.types.is_bool_dtype(df['in_fs']) or all(isinstance(x, bool) for x in df['in_fs'].dropna()):
                stats['records_in_fs'] = df['in_fs'].sum()
            else:
                # Try to convert to boolean if possible
                try:
                    stats['records_in_fs'] = df['in_fs'].astype(bool).sum()
                except Exception:
                    stats['records_in_fs'] = 0

        # Add surname statistics if the column exists
        if 'normalized_surname' in df.columns:
            stats['unique_surnames'] = df['normalized_surname'].nunique()

        return stats
    except Exception as e:
        raise Exception(f"Error calculating summary statistics: {str(e)}")
