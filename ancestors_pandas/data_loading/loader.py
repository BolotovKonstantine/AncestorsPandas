"""
Data loading module for AncestorsPandas.

This module provides functions for loading genealogical data from CSV files.
"""

import pandas as pd
from typing import Optional

from ancestors_pandas.processing import normalizations


def load_csv(filepath: str, separator: str = ';', encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file.
    separator : str, optional
        Delimiter used in the CSV file. Default is ';'.
    encoding : str, optional
        Encoding of the CSV file. Default is 'utf-8'.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing the data from the CSV file.

    Raises:
    -------
    ValueError
        If filepath is not a string or is empty.
        If separator is not a string or is empty.
        If encoding is not a string or is empty.
    FileNotFoundError
        If the file does not exist.
    Exception
        For other errors during file loading.
    """
    # Validate input parameters
    if not isinstance(filepath, str):
        raise ValueError(f"filepath must be a string, got {type(filepath).__name__}")
    if not filepath:
        raise ValueError("filepath cannot be empty")

    if not isinstance(separator, str):
        raise ValueError(f"separator must be a string, got {type(separator).__name__}")
    if not separator:
        raise ValueError("separator cannot be empty")

    if not isinstance(encoding, str):
        raise ValueError(f"encoding must be a string, got {type(encoding).__name__}")
    if not encoding:
        raise ValueError("encoding cannot be empty")

    try:
        df = pd.read_csv(filepath, sep=separator, encoding=encoding)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error loading file {filepath}: {str(e)}")


def load_and_normalize(
    filepath: str,
    date_col: Optional[str] = None,
    surname_col: Optional[str] = None,
    fs_col: Optional[str] = None,
    separator: str = ';',
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """
    Load data from a CSV file and perform initial normalization.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file.
    date_col : str, optional
        Name of the date column to parse.
    surname_col : str, optional
        Name of the surname column to normalize.
    fs_col : str, optional
        Name of the FamilySearch ID column.
    separator : str, optional
        Delimiter used in the CSV file. Default is ';'.
    encoding : str, optional
        Encoding of the CSV file. Default is 'utf-8'.

    Returns:
    --------
    pd.DataFrame
        Normalized DataFrame containing the data from the CSV file.

    Raises:
    -------
    ValueError
        If any of the provided parameters are invalid.
    Exception
        For other errors during file processing.
    """
    # Validate optional parameters
    if date_col is not None and not isinstance(date_col, str):
        raise ValueError(f"date_col must be a string or None, got {type(date_col).__name__}")

    if surname_col is not None and not isinstance(surname_col, str):
        raise ValueError(f"surname_col must be a string or None, got {type(surname_col).__name__}")

    if fs_col is not None and not isinstance(fs_col, str):
        raise ValueError(f"fs_col must be a string or None, got {type(fs_col).__name__}")

    try:
        # load_csv function already validates filepath, separator, and encoding
        df = load_csv(filepath, separator, encoding)

        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"Expected DataFrame from load_csv, got {type(df).__name__}")

        df = normalizations.strip_column_names(df)
        df = normalizations.strip_string_values(df)

        if date_col:
            # Check if date_col exists in the DataFrame
            if date_col not in df.columns:
                raise ValueError(f"Date column '{date_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

            df = normalizations.parse_dates(df, date_column=date_col)
            # Add a year column
            df['year'] = df[date_col].dt.year

        if surname_col:
            # Check if surname_col exists in the DataFrame
            if surname_col not in df.columns:
                raise ValueError(f"Surname column '{surname_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

            df = normalizations.apply_surname_normalization(
                df, source_col=surname_col, target_col='normalized_surname'
            )

        if fs_col:
            # Check if fs_col exists in the DataFrame
            if fs_col not in df.columns:
                raise ValueError(f"FS column '{fs_col}' not found in DataFrame. Available columns: {', '.join(df.columns)}")

            df['in_fs'] = df[fs_col].notna()

        return df
    except Exception as e:
        raise Exception(f"Error processing file {filepath}: {str(e)}")
