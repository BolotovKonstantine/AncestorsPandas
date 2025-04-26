"""
Data normalization module for AncestorsPandas.

This module provides functions for normalizing and cleaning data.
"""

import pandas as pd
import re
from typing import Any, Union
from config import (
    FEMALE_SURNAME_SUFFIX,
    FEMALE_SURNAME_ENDINGS,
    MALE_SURNAME_ENDINGS,
    SURNAME_PREFIXES
)


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
        available_cols = ', '.join(df.columns)
        raise ValueError(
            f"Column '{date_column}' not found in DataFrame. "
            f"Available columns: {available_cols}"
        )

    try:
        df[date_column] = pd.to_datetime(
            df[date_column], dayfirst=True, errors='coerce'
        )
        return df
    except Exception as e:
        raise ValueError(f"Error parsing dates in column {date_column}: {str(e)}")


def normalize_surname(surname: Union[str, Any]) -> Union[str, Any]:
    """
    Normalizes a given surname by applying several transformations:

    1. Converts text to lowercase
    2. Removes special characters and numbers
    3. Standardizes common surname variations (e.g., feminine/masculine forms)
    4. Handles prefixes like "Mc", "Mac", etc.

    This function is designed to handle any input type safely. If the input is not a string,
    it will be returned unchanged.

    Parameters:
    -----------
    surname : str or Any
        Input surname string or any other value.

    Returns:
    --------
    str or Any
        Normalized surname if input is a string,
        otherwise the input value unchanged.
    """
    # Return non-string values unchanged
    if not isinstance(surname, str):
        return surname

    # Skip empty strings
    if not surname.strip():
        return surname

    # Convert to lowercase
    normalized = surname.lower()

    # Remove special characters and numbers
    normalized = re.sub(r'[^a-zа-яё\s-]', '', normalized)

    # Handle hyphenated surnames by normalizing each part
    if '-' in normalized:
        parts = normalized.split('-')
        normalized_parts = []
        for part in parts:
            # Apply normalization to each part
            normalized_part = part.strip()
            normalized_part = _normalize_surname_endings(normalized_part)
            normalized_part = _normalize_surname_prefixes(normalized_part)
            normalized_parts.append(normalized_part)
        return '-'.join(normalized_parts)

    # Normalize surname endings (e.g., feminine to masculine forms)
    normalized = _normalize_surname_endings(normalized)

    # Normalize surname prefixes
    normalized = _normalize_surname_prefixes(normalized)

    return normalized


def _normalize_surname_endings(surname: str) -> str:
    """
    Helper function to normalize surname endings, particularly for Russian surnames
    where feminine forms often end with specific suffixes.

    Parameters:
    -----------
    surname : str
        Input surname string.

    Returns:
    --------
    str
        Surname with normalized endings.
    """
    # Handle simple case with just the feminine suffix
    if surname.endswith(FEMALE_SURNAME_SUFFIX):
        return surname[:-1]

    # Handle more complex feminine endings
    for i, ending in enumerate(FEMALE_SURNAME_ENDINGS):
        if surname.endswith(ending):
            # Replace with corresponding masculine ending
            return surname[:-len(ending)] + MALE_SURNAME_ENDINGS[i]

    return surname


def _normalize_surname_prefixes(surname: str) -> str:
    """
    Helper function to normalize surname prefixes like "Mc", "Mac", etc.

    Parameters:
    -----------
    surname : str
        Input surname string.

    Returns:
    --------
    str
        Surname with normalized prefixes.
    """
    # Standardize prefixes
    for prefix in SURNAME_PREFIXES:
        # Check if surname starts with prefix (case insensitive)
        prefix_pattern = r'^' + prefix + r'(?=[a-zа-яё])'
        if re.search(prefix_pattern, surname, re.IGNORECASE):
            # Standardize the prefix capitalization
            prefix_length = len(prefix)
            return prefix + surname[prefix_length:]

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
        available_cols = ', '.join(df.columns)
        raise KeyError(
            f"Column '{source_col}' not found in DataFrame. "
            f"Available columns: {available_cols}"
        )

    try:
        df[target_col] = df[source_col].apply(normalize_surname)
        return df
    except Exception as e:
        raise Exception(f"Error normalizing surnames: {str(e)}")
