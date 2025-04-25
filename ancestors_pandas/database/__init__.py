"""
Database module for AncestorsPandas.

This module provides functionality for storing and retrieving calculation history
using SQLite database.
"""

# Import database functions
from ancestors_pandas.database.db import (
    get_connection,
    init_database,
    get_schema_version,
    store_summary_statistics,
    store_yearly_comparison,
    store_value_counts,
    get_summary_statistics_history,
    get_yearly_comparison_history,
    get_value_counts_history,
    DatabaseError,
    ConnectionError,
    SchemaError,
    QueryError
)

# Import statistics logging functions
from ancestors_pandas.database.stats_logger import (
    log_summary_statistics,
    log_yearly_comparison,
    log_value_counts,
    log_surname_counts,
    log_all_statistics
)

# Import statistics retrieval functions
from ancestors_pandas.database.stats_retriever import (
    query_summary_statistics,
    query_yearly_comparison,
    query_value_counts,
    export_summary_statistics_to_dataframe,
    export_yearly_comparison_to_dataframe,
    export_value_counts_to_dataframe,
    export_to_csv,
    export_to_excel,
    export_to_json
)

__all__ = [
    # Database functions
    'get_connection',
    'init_database',
    'get_schema_version',
    'store_summary_statistics',
    'store_yearly_comparison',
    'store_value_counts',
    'get_summary_statistics_history',
    'get_yearly_comparison_history',
    'get_value_counts_history',
    'DatabaseError',
    'ConnectionError',
    'SchemaError',
    'QueryError',

    # Statistics logging functions
    'log_summary_statistics',
    'log_yearly_comparison',
    'log_value_counts',
    'log_surname_counts',
    'log_all_statistics',

    # Statistics retrieval functions
    'query_summary_statistics',
    'query_yearly_comparison',
    'query_value_counts',
    'export_summary_statistics_to_dataframe',
    'export_yearly_comparison_to_dataframe',
    'export_value_counts_to_dataframe',
    'export_to_csv',
    'export_to_excel',
    'export_to_json'
]
