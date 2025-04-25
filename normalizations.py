"""
This module contains reusable normalization and cleaning functions
for data preprocessing. All functions accept and return pandas
DataFrames (except for purely string-level transformations).
"""

import pandas as pd
from config import (
    CSV_SEPARATOR, CSV_ENCODING, DATE_FORMAT_DAYFIRST,
    YEAR_COL, NORMALIZED_SURNAME_COL, IN_FS_COL,
    FEMALE_SURNAME_SUFFIX
)

def load_and_normalize(filepath, date_col=None, surname_col=None, fs_col=None):
    """
    Load a CSV file and apply normalization operations.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file to load.
    date_col : str, optional
        Name of the date column to parse. If provided, a year column will be added.
    surname_col : str, optional
        Name of the surname column to normalize. If provided, a normalized surname column will be added.
    fs_col : str, optional
        Name of the FamilySearch ID column. If provided, an in_fs boolean column will be added.

    Returns:
    --------
    pd.DataFrame
        Normalized DataFrame with additional columns based on the provided parameters.
    """
    df = pd.read_csv(filepath, sep=CSV_SEPARATOR, encoding=CSV_ENCODING)
    df = strip_column_names(df)
    df = strip_string_values(df)
    if date_col:
        df = parse_dates(df, date_column=date_col)
        # Example: add a year column
        df[YEAR_COL] = df[date_col].dt.year
    if surname_col:
        df = apply_surname_normalization(df, source_col=surname_col,
                                         target_col=NORMALIZED_SURNAME_COL)
    if fs_col:
        df[IN_FS_COL] = df[fs_col].notna()
    return df


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
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=DATE_FORMAT_DAYFIRST, errors='coerce')
    return df


def normalize_surname(surname: str) -> str:
    """
    Normalizes a given surname by removing a trailing feminine suffix.

    Parameters:
    surname (str): Input surname string.

    Returns:
    str: Normalized surname.
    """
    if isinstance(surname, str) and surname.endswith(FEMALE_SURNAME_SUFFIX):
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
