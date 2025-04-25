"""
Database operations module for AncestorsPandas.

This module provides functions for database operations, including connection handling,
schema design, table creation, and data storage/retrieval.
"""

import os
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import datetime
import json
from contextlib import contextmanager

from config import (
    STAT_TOTAL_RECORDS, STAT_MISSING_VALUES, STAT_UNIQUE_YEARS,
    STAT_RECORDS_IN_FS, STAT_UNIQUE_SURNAMES, DB_FILE, DB_HISTORY_LIMIT
)

# Database schema version
DB_SCHEMA_VERSION = 1

# Table names
TABLE_SUMMARY_STATS = "summary_statistics"
TABLE_YEARLY_COMPARISON = "yearly_comparison"
TABLE_VALUE_COUNTS = "value_counts"
TABLE_SCHEMA_VERSION = "schema_version"

# Default database path
DEFAULT_DB_PATH = DB_FILE


class DatabaseError(Exception):
    """Base exception for database errors."""
    pass


class ConnectionError(DatabaseError):
    """Exception raised for connection errors."""
    pass


class SchemaError(DatabaseError):
    """Exception raised for schema-related errors."""
    pass


class QueryError(DatabaseError):
    """Exception raised for query execution errors."""
    pass


@contextmanager
def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """
    Context manager for database connections.

    Parameters:
    -----------
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Yields:
    -------
    sqlite3.Connection
        SQLite database connection.

    Raises:
    -------
    ConnectionError
        If there's an error connecting to the database.
    """
    conn = None
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Connect to the database
        conn = sqlite3.connect(db_path)

        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")

        # Return dictionary-like rows
        conn.row_factory = sqlite3.Row

        yield conn
    except sqlite3.Error as e:
        raise ConnectionError(f"Database connection error: {str(e)}")
    finally:
        if conn:
            conn.close()


def init_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initialize the database by creating necessary tables if they don't exist.

    Parameters:
    -----------
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Raises:
    -------
    SchemaError
        If there's an error creating the database schema.
    """
    try:
        with get_connection(db_path) as conn:
            # Create schema version table
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_SCHEMA_VERSION} (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    version INTEGER NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
            """)

            # Create summary statistics table
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_SUMMARY_STATS} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    data_source TEXT NOT NULL,
                    total_records INTEGER NOT NULL,
                    missing_values INTEGER NOT NULL,
                    unique_years INTEGER NOT NULL,
                    records_in_fs INTEGER NOT NULL,
                    unique_surnames INTEGER NOT NULL,
                    additional_data TEXT
                )
            """)

            # Create yearly comparison table
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_YEARLY_COMPARISON} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    data_source TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    total_records INTEGER NOT NULL,
                    records_with_condition INTEGER NOT NULL,
                    condition_name TEXT NOT NULL,
                    UNIQUE(data_source, year, timestamp, condition_name)
                )
            """)

            # Create value counts table
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_VALUE_COUNTS} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    data_source TEXT NOT NULL,
                    column_name TEXT NOT NULL,
                    value TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    UNIQUE(data_source, column_name, value, timestamp)
                )
            """)

            # Set schema version if not already set
            cursor = conn.execute(f"SELECT version FROM {TABLE_SCHEMA_VERSION} WHERE id = 1")
            if not cursor.fetchone():
                conn.execute(
                    f"INSERT INTO {TABLE_SCHEMA_VERSION} (id, version, updated_at) VALUES (1, ?, ?)",
                    (DB_SCHEMA_VERSION, datetime.datetime.now())
                )

            conn.commit()
    except (ConnectionError, sqlite3.Error) as e:
        raise SchemaError(f"Error initializing database schema: {str(e)}")


def get_schema_version(db_path: str = DEFAULT_DB_PATH) -> int:
    """
    Get the current schema version from the database.

    Parameters:
    -----------
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    int
        Current schema version.

    Raises:
    -------
    QueryError
        If there's an error querying the schema version.
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.execute(f"SELECT version FROM {TABLE_SCHEMA_VERSION} WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return row['version']
            return 0
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error getting schema version: {str(e)}")


def store_summary_statistics(
    stats: Dict[str, int],
    data_source: str,
    additional_data: Optional[Dict[str, Any]] = None,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Store summary statistics in the database.

    Parameters:
    -----------
    stats : Dict[str, int]
        Dictionary with summary statistics.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    additional_data : Optional[Dict[str, Any]], optional
        Additional data to store as JSON.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    int
        ID of the inserted record.

    Raises:
    -------
    QueryError
        If there's an error storing the statistics.
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.execute(
                f"""
                INSERT INTO {TABLE_SUMMARY_STATS} (
                    timestamp, data_source, total_records, missing_values,
                    unique_years, records_in_fs, unique_surnames, additional_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.datetime.now(),
                    data_source,
                    stats.get(STAT_TOTAL_RECORDS, 0),
                    stats.get(STAT_MISSING_VALUES, 0),
                    stats.get(STAT_UNIQUE_YEARS, 0),
                    stats.get(STAT_RECORDS_IN_FS, 0),
                    stats.get(STAT_UNIQUE_SURNAMES, 0),
                    json.dumps(additional_data) if additional_data else None
                )
            )
            conn.commit()
            return cursor.lastrowid
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error storing summary statistics: {str(e)}")


def store_yearly_comparison(
    comparison_df: pd.DataFrame,
    data_source: str,
    condition_name: str = "in_fs",
    db_path: str = DEFAULT_DB_PATH
) -> List[int]:
    """
    Store yearly comparison data in the database.

    Parameters:
    -----------
    comparison_df : pd.DataFrame
        DataFrame with yearly comparison data.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    condition_name : str, optional
        Name of the condition column. Default is 'in_fs'.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[int]
        List of IDs of the inserted records.

    Raises:
    -------
    QueryError
        If there's an error storing the comparison data.
    """
    try:
        now = datetime.datetime.now()
        ids = []

        with get_connection(db_path) as conn:
            for year, row in comparison_df.iterrows():
                cursor = conn.execute(
                    f"""
                    INSERT INTO {TABLE_YEARLY_COMPARISON} (
                        timestamp, data_source, year, total_records,
                        records_with_condition, condition_name
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        now,
                        data_source,
                        year,
                        int(row.iloc[0]),  # Total records
                        int(row.iloc[1]),  # Records with condition
                        condition_name
                    )
                )
                ids.append(cursor.lastrowid)

            conn.commit()
            return ids
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error storing yearly comparison: {str(e)}")


def store_value_counts(
    counts: pd.Series,
    column_name: str,
    data_source: str,
    db_path: str = DEFAULT_DB_PATH
) -> List[int]:
    """
    Store value counts in the database.

    Parameters:
    -----------
    counts : pd.Series
        Series with value counts.
    column_name : str
        Name of the column the counts are for.
    data_source : str
        Name of the data source (e.g., 'births', 'marriages', 'deaths').
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[int]
        List of IDs of the inserted records.

    Raises:
    -------
    QueryError
        If there's an error storing the value counts.
    """
    try:
        now = datetime.datetime.now()
        ids = []

        with get_connection(db_path) as conn:
            for value, count in counts.items():
                cursor = conn.execute(
                    f"""
                    INSERT INTO {TABLE_VALUE_COUNTS} (
                        timestamp, data_source, column_name, value, count
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        now,
                        data_source,
                        column_name,
                        str(value),
                        int(count)
                    )
                )
                ids.append(cursor.lastrowid)

            conn.commit()
            return ids
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error storing value counts: {str(e)}")


def get_summary_statistics_history(
    data_source: Optional[str] = None,
    limit: int = DB_HISTORY_LIMIT,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Get historical summary statistics from the database.

    Parameters:
    -----------
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    limit : int, optional
        Maximum number of records to return. Default is 10.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    List[Dict[str, Any]]
        List of dictionaries with historical summary statistics.

    Raises:
    -------
    QueryError
        If there's an error retrieving the statistics.
    """
    try:
        with get_connection(db_path) as conn:
            query = f"SELECT * FROM {TABLE_SUMMARY_STATS}"
            params = []

            if data_source:
                query += " WHERE data_source = ?"
                params.append(data_source)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(query, params)

            result = []
            for row in cursor:
                row_dict = dict(row)
                if row_dict['additional_data']:
                    row_dict['additional_data'] = json.loads(row_dict['additional_data'])
                result.append(row_dict)

            return result
    except (ConnectionError, sqlite3.Error, json.JSONDecodeError) as e:
        raise QueryError(f"Error retrieving summary statistics history: {str(e)}")


def get_yearly_comparison_history(
    data_source: Optional[str] = None,
    condition_name: Optional[str] = None,
    limit: int = DB_HISTORY_LIMIT,
    db_path: str = DEFAULT_DB_PATH
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get historical yearly comparison data from the database.

    Parameters:
    -----------
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    condition_name : Optional[str], optional
        Filter by condition name. If None, returns data for all conditions.
    limit : int, optional
        Maximum number of distinct timestamps to return. Default is 10.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    Dict[str, List[Dict[str, Any]]]
        Dictionary with timestamps as keys and lists of yearly comparison data as values.

    Raises:
    -------
    QueryError
        If there's an error retrieving the comparison data.
    """
    try:
        with get_connection(db_path) as conn:
            # First, get distinct timestamps
            timestamp_query = f"SELECT DISTINCT timestamp FROM {TABLE_YEARLY_COMPARISON}"
            timestamp_params = []

            if data_source:
                timestamp_query += " WHERE data_source = ?"
                timestamp_params.append(data_source)

            if condition_name:
                if data_source:
                    timestamp_query += " AND condition_name = ?"
                else:
                    timestamp_query += " WHERE condition_name = ?"
                timestamp_params.append(condition_name)

            timestamp_query += " ORDER BY timestamp DESC LIMIT ?"
            timestamp_params.append(limit)

            timestamp_cursor = conn.execute(timestamp_query, timestamp_params)
            timestamps = [row['timestamp'] for row in timestamp_cursor]

            result = {}
            for timestamp in timestamps:
                # Get data for each timestamp
                data_query = f"SELECT * FROM {TABLE_YEARLY_COMPARISON} WHERE timestamp = ?"
                data_params = [timestamp]

                if data_source:
                    data_query += " AND data_source = ?"
                    data_params.append(data_source)

                if condition_name:
                    data_query += " AND condition_name = ?"
                    data_params.append(condition_name)

                data_query += " ORDER BY year"

                data_cursor = conn.execute(data_query, data_params)
                result[timestamp] = [dict(row) for row in data_cursor]

            return result
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error retrieving yearly comparison history: {str(e)}")


def get_value_counts_history(
    column_name: str,
    data_source: Optional[str] = None,
    limit: int = DB_HISTORY_LIMIT,
    db_path: str = DEFAULT_DB_PATH
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get historical value counts from the database.

    Parameters:
    -----------
    column_name : str
        Name of the column to get counts for.
    data_source : Optional[str], optional
        Filter by data source. If None, returns data for all sources.
    limit : int, optional
        Maximum number of distinct timestamps to return. Default is 10.
    db_path : str, optional
        Path to the SQLite database file. Default is the value from config.

    Returns:
    --------
    Dict[str, List[Dict[str, Any]]]
        Dictionary with timestamps as keys and lists of value counts as values.

    Raises:
    -------
    QueryError
        If there's an error retrieving the value counts.
    """
    try:
        with get_connection(db_path) as conn:
            # First, get distinct timestamps
            timestamp_query = f"SELECT DISTINCT timestamp FROM {TABLE_VALUE_COUNTS} WHERE column_name = ?"
            timestamp_params = [column_name]

            if data_source:
                timestamp_query += " AND data_source = ?"
                timestamp_params.append(data_source)

            timestamp_query += " ORDER BY timestamp DESC LIMIT ?"
            timestamp_params.append(limit)

            timestamp_cursor = conn.execute(timestamp_query, timestamp_params)
            timestamps = [row['timestamp'] for row in timestamp_cursor]

            result = {}
            for timestamp in timestamps:
                # Get data for each timestamp
                data_query = f"SELECT * FROM {TABLE_VALUE_COUNTS} WHERE timestamp = ? AND column_name = ?"
                data_params = [timestamp, column_name]

                if data_source:
                    data_query += " AND data_source = ?"
                    data_params.append(data_source)

                data_query += " ORDER BY count DESC"

                data_cursor = conn.execute(data_query, data_params)
                result[timestamp] = [dict(row) for row in data_cursor]

            return result
    except (ConnectionError, sqlite3.Error) as e:
        raise QueryError(f"Error retrieving value counts history: {str(e)}")
