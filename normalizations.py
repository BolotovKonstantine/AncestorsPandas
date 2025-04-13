"""
This module contains reusable normalization and cleaning functions
for data preprocessing. All functions accept and return pandas
DataFrames (except for purely string-level transformations).
"""

import pandas as pd


def strip_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading and trailing whitespace from all column names in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with stripped column names.
    """
    df.columns = df.columns.str.strip()
    return df


def strip_string_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading and trailing whitespace from string values in all columns.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with stripped string values.
    """
    df = df.apply(
        lambda col: col.map(lambda val: val.strip() if isinstance(val, str) else val)
    )
    return df


def parse_dates(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Converts the specified column in the DataFrame to a datetime type.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    date_column (str): Name of the date column.

    Returns:
    pd.DataFrame: DataFrame with converted date column.
    """
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=True, errors='coerce')
    return df


def normalize_surname(surname: str) -> str:
    """
    Normalizes a given surname by removing a trailing 'а'.

    Parameters:
    surname (str): Input surname string.

    Returns:
    str: Normalized surname.
    """
    if isinstance(surname, str) and surname.endswith("а"):
        return surname[:-1]
    return surname


def apply_surname_normalization(df: pd.DataFrame, source_col: str,
                                target_col: str) -> pd.DataFrame:
    """
    Creates a new column with normalized surnames.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    source_col (str): Name of the initial surname column.
    target_col (str): Name of the new column to store normalized surnames.

    Returns:
    pd.DataFrame: DataFrame with the added normalized surname column.
    """
    df[target_col] = df[source_col].apply(normalize_surname)
    return df
