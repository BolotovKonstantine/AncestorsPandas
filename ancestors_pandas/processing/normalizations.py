"""
Data normalization module for AncestorsPandas.

This module provides functions for normalizing and cleaning data.
"""

import pandas as pd
from typing import Any, Union


def strip_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading and trailing whitespace from all column names in the DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.

    Returns:
    --------
    pd.DataFrame
        DataFrame with stripped column names.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    df.columns = df.columns.str.strip()
    return df


def strip_string_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading and trailing whitespace from string values in all columns.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.

    Returns:
    --------
    pd.DataFrame
        DataFrame with stripped string values.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    try:
        df = df.apply(
            lambda col: col.map(lambda val: val.strip() if isinstance(val, str) else val)
        )
        return df
    except Exception as e:
        raise ValueError(f"Error stripping string values: {str(e)}")


def parse_dates(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Converts the specified column in the DataFrame to a datetime type.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    date_column : str
        Name of the date column.

    Returns:
    --------
    pd.DataFrame
        DataFrame with converted date column.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame or date_column is not a string.
    ValueError
        If date_column is empty or not found in the DataFrame.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(date_column, str):
        raise TypeError(f"date_column must be a string, got {type(date_column).__name__}")

    if not date_column:
        raise ValueError("date_column cannot be empty")

    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        df[date_column] = pd.to_datetime(df[date_column], dayfirst=True, errors='coerce')
        return df
    except Exception as e:
        raise ValueError(f"Error parsing dates in column {date_column}: {str(e)}")


def normalize_surname(surname: Union[str, Any]) -> Union[str, Any]:
    """
    Normalizes a given surname by removing a trailing 'а'.

    This function is designed to handle any input type safely. If the input is not a string,
    it will be returned unchanged. If the input is a string but doesn't end with 'а',
    it will also be returned unchanged.

    Parameters:
    -----------
    surname : str or Any
        Input surname string or any other value.

    Returns:
    --------
    str or Any
        Normalized surname if input is a string ending with 'а',
        otherwise the input value unchanged.
    """
    # No need for additional validation as the function already handles any input type
    if isinstance(surname, str) and surname.endswith("а"):
        return surname[:-1]
    return surname


def apply_surname_normalization(
    df: pd.DataFrame, source_col: str, target_col: str
) -> pd.DataFrame:
    """
    Creates a new column with normalized surnames.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    source_col : str
        Name of the initial surname column.
    target_col : str
        Name of the new column to store normalized surnames.

    Returns:
    --------
    pd.DataFrame
        DataFrame with the added normalized surname column.

    Raises:
    -------
    TypeError
        If df is not a pandas DataFrame, source_col is not a string, or target_col is not a string.
    ValueError
        If source_col or target_col is empty.
    KeyError
        If source_col is not found in the DataFrame.
    Exception
        For other errors during surname normalization.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")

    if not isinstance(source_col, str):
        raise TypeError(f"source_col must be a string, got {type(source_col).__name__}")

    if not isinstance(target_col, str):
        raise TypeError(f"target_col must be a string, got {type(target_col).__name__}")

    if not source_col:
        raise ValueError("source_col cannot be empty")

    if not target_col:
        raise ValueError("target_col cannot be empty")

    if source_col not in df.columns:
        raise KeyError(f"Column '{source_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

    try:
        df[target_col] = df[source_col].apply(normalize_surname)
        return df
    except Exception as e:
        raise Exception(f"Error normalizing surnames: {str(e)}")
