"""
Statistics retrieval module for AncestorsPandas.

This module provides functions for retrieving historical statistics from the database
with filtering options and export functionality.
"""

import pandas as pd
import datetime
from typing import Dict, List, Optional, Any, Tuple, Union

from ancestors_pandas.database.db import (
    get_connection,
    TABLE_SUMMARY_STATS,
    TABLE_YEARLY_COMPARISON,
    TABLE_VALUE_COUNTS,
    DEFAULT_DB_PATH,
    QueryError
)


def query_summary_statistics(
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Query historical summary statistics with filtering options.

    Parameters:
    -----------
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[Dict[str, Any]]
        List of dictionaries with filtered summary statistics.

    Raises:
    -------
    QueryError
        If there's an error retrieving the statistics.
    ValueError
        If date format is invalid.
    """
    try:
        # Convert string dates to datetime objects if provided
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # Set time to end of day for inclusive end date
            end_date = end_date.replace(hour=23, minute=59, second=59)

        with get_connection(db_path) as conn:
            query = f"SELECT * FROM {TABLE_SUMMARY_STATS}"
            params = []
            conditions = []

            if data_source:
                conditions.append("data_source = ?")
                params.append(data_source)

            if start_date:
                conditions.append("timestamp >= ?")
                params.append(start_date)

            if end_date:
                conditions.append("timestamp <= ?")
                params.append(end_date)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY timestamp DESC"

            cursor = conn.execute(query, params)

            result = []
            for row in cursor:
                row_dict = dict(row)
                if row_dict.get('additional_data'):
                    import json
                    row_dict['additional_data'] = json.loads(row_dict['additional_data'])
                result.append(row_dict)

            return result
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")
    except Exception as e:
        raise QueryError(f"Error querying summary statistics: {str(e)}")


def query_yearly_comparison(
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    condition_name: Optional[str] = None,
    year: Optional[int] = None,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Query historical yearly comparison data with filtering options.

    Parameters:
    -----------
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    condition_name : Optional[str], optional
        Filter by condition name. If None, returns data for all conditions.
    year : Optional[int], optional
        Filter by specific year. If None, returns data for all years.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[Dict[str, Any]]
        List of dictionaries with filtered yearly comparison data.

    Raises:
    -------
    QueryError
        If there's an error retrieving the comparison data.
    ValueError
        If date format is invalid.
    """
    try:
        # Convert string dates to datetime objects if provided
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # Set time to end of day for inclusive end date
            end_date = end_date.replace(hour=23, minute=59, second=59)

        with get_connection(db_path) as conn:
            query = f"SELECT * FROM {TABLE_YEARLY_COMPARISON}"
            params = []
            conditions = []

            if data_source:
                conditions.append("data_source = ?")
                params.append(data_source)

            if condition_name:
                conditions.append("condition_name = ?")
                params.append(condition_name)

            if year:
                conditions.append("year = ?")
                params.append(year)

            if start_date:
                conditions.append("timestamp >= ?")
                params.append(start_date)

            if end_date:
                conditions.append("timestamp <= ?")
                params.append(end_date)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY timestamp DESC, year ASC"

            cursor = conn.execute(query, params)

            result = []
            for row in cursor:
                result.append(dict(row))

            return result
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")
    except Exception as e:
        raise QueryError(f"Error querying yearly comparison data: {str(e)}")


def query_value_counts(
    column_name: Optional[str] = None,
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    value: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Query historical value counts with filtering options.

    Parameters:
    -----------
    column_name : Optional[str], optional
        Filter by column name. If None, returns data for all columns.
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    value : Optional[str], optional
        Filter by specific value. If None, returns data for all values.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[Dict[str, Any]]
        List of dictionaries with filtered value counts.

    Raises:
    -------
    QueryError
        If there's an error retrieving the value counts.
    ValueError
        If date format is invalid.
    """
    try:
        # Convert string dates to datetime objects if provided
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # Set time to end of day for inclusive end date
            end_date = end_date.replace(hour=23, minute=59, second=59)

        with get_connection(db_path) as conn:
            query = f"SELECT * FROM {TABLE_VALUE_COUNTS}"
            params = []
            conditions = []

            if column_name:
                conditions.append("column_name = ?")
                params.append(column_name)

            if data_source:
                conditions.append("data_source = ?")
                params.append(data_source)

            if value:
                conditions.append("value = ?")
                params.append(value)

            if start_date:
                conditions.append("timestamp >= ?")
                params.append(start_date)

            if end_date:
                conditions.append("timestamp <= ?")
                params.append(end_date)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY timestamp DESC, count DESC"

            cursor = conn.execute(query, params)

            result = []
            for row in cursor:
                result.append(dict(row))

            return result
    except ValueError as e:
        raise ValueError(f"Invalid date format: {str(e)}")
    except Exception as e:
        raise QueryError(f"Error querying value counts: {str(e)}")


def export_summary_statistics_to_dataframe(
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> pd.DataFrame:
    """
    Export summary statistics to a pandas DataFrame.

    Parameters:
    -----------
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing the summary statistics.

    Raises:
    -------
    QueryError
        If there's an error retrieving the statistics.
    ValueError
        If date format is invalid.
    """
    data = query_summary_statistics(start_date, end_date, data_source, db_path)
    return pd.DataFrame(data)


def export_yearly_comparison_to_dataframe(
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    condition_name: Optional[str] = None,
    year: Optional[int] = None,
    db_path: str = DEFAULT_DB_PATH
) -> pd.DataFrame:
    """
    Export yearly comparison data to a pandas DataFrame.

    Parameters:
    -----------
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    condition_name : Optional[str], optional
        Filter by condition name. If None, returns data for all conditions.
    year : Optional[int], optional
        Filter by specific year. If None, returns data for all years.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing the yearly comparison data.

    Raises:
    -------
    QueryError
        If there's an error retrieving the comparison data.
    ValueError
        If date format is invalid.
    """
    data = query_yearly_comparison(start_date, end_date, data_source, condition_name, year, db_path)
    return pd.DataFrame(data)


def export_value_counts_to_dataframe(
    column_name: Optional[str] = None,
    start_date: Optional[Union[str, datetime.datetime]] = None,
    end_date: Optional[Union[str, datetime.datetime]] = None,
    data_source: Optional[str] = None,
    value: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> pd.DataFrame:
    """
    Export value counts to a pandas DataFrame.

    Parameters:
    -----------
    column_name : Optional[str], optional
        Filter by column name. If None, returns data for all columns.
    start_date : Optional[Union[str, datetime.datetime]], optional
        Start date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    end_date : Optional[Union[str, datetime.datetime]], optional
        End date for filtering (inclusive). If string, format should be 'YYYY-MM-DD'.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    value : Optional[str], optional
        Filter by specific value. If None, returns data for all values.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing the value counts.

    Raises:
    -------
    QueryError
        If there's an error retrieving the value counts.
    ValueError
        If date format is invalid.
    """
    data = query_value_counts(column_name, start_date, end_date, data_source, value, db_path)
    return pd.DataFrame(data)


def export_to_csv(
    df: pd.DataFrame,
    output_path: str,
    index: bool = False
) -> None:
    """
    Export a DataFrame to a CSV file.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to export.
    output_path : str
        Path to save the CSV file.
    index : bool, optional
        Whether to include the index in the CSV file. Default is False.

    Raises:
    -------
    IOError
        If there's an error writing to the file.
    """
    try:
        df.to_csv(output_path, index=index)
    except Exception as e:
        raise IOError(f"Error exporting to CSV: {str(e)}")


def export_to_excel(
    df: pd.DataFrame,
    output_path: str,
    sheet_name: str = 'Sheet1',
    index: bool = False
) -> None:
    """
    Export a DataFrame to an Excel file.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to export.
    output_path : str
        Path to save the Excel file.
    sheet_name : str, optional
        Name of the sheet in the Excel file. Default is 'Sheet1'.
    index : bool, optional
        Whether to include the index in the Excel file. Default is False.

    Raises:
    -------
    IOError
        If there's an error writing to the file.
    """
    try:
        df.to_excel(output_path, sheet_name=sheet_name, index=index)
    except Exception as e:
        raise IOError(f"Error exporting to Excel: {str(e)}")


def export_to_json(
    df: pd.DataFrame,
    output_path: str,
    orient: str = 'records'
) -> None:
    """
    Export a DataFrame to a JSON file.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to export.
    output_path : str
        Path to save the JSON file.
    orient : str, optional
        The format of the JSON string. Default is 'records'.

    Raises:
    -------
    IOError
        If there's an error writing to the file.
    """
    try:
        df.to_json(output_path, orient=orient)
    except Exception as e:
        raise IOError(f"Error exporting to JSON: {str(e)}")