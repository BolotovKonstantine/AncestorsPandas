#!/usr/bin/env python3
"""
Main entry point for the AncestorsPandas application.

This script provides a simple interface to run the application with default settings.
For more advanced usage, use the CLI module directly.
"""

import sys
from ancestors_pandas import logger
from ancestors_pandas.data_loading import loader
from ancestors_pandas.analysis import statistics
from ancestors_pandas.visualization import plots
from ancestors_pandas.database import db
from ancestors_pandas import cli
from config import (
    BIRTHS_FILE, MARRIAGES_FILE, DEATHS_FILE,
    BIRTHS_DATE_COL, MARRIAGES_DATE_COL, DEATHS_DATE_COL,
    SURNAME_COL, FS_COL, IN_FS_COL, NORMALIZED_SURNAME_COL
)


def main():
    """
    Main function that loads data, performs analysis, and generates visualizations.

    This function uses the new package structure and modules to perform the same
    operations as the original main.py file.
    """
    # Set up logging
    log = logger.setup_logger()
    log.info("Starting AncestorsPandas application")

    # Initialize database
    try:
        log.info("Initializing database...")
        db.init_database()
    except db.SchemaError as e:
        log.error(f"Database initialization error: {str(e)}")
        return 1

    try:
        # Load data
        log.info("Loading data...")
        births_df = loader.load_and_normalize(
            BIRTHS_FILE, date_col=BIRTHS_DATE_COL, surname_col=SURNAME_COL, fs_col=FS_COL
        )
        marriages_df = loader.load_and_normalize(
            MARRIAGES_FILE, date_col=MARRIAGES_DATE_COL, surname_col=SURNAME_COL, fs_col=FS_COL
        )
        deaths_df = loader.load_and_normalize(
            DEATHS_FILE, date_col=DEATHS_DATE_COL, surname_col=SURNAME_COL, fs_col=FS_COL
        )

        # Display basic information
        log.info(f"Total records in Births file: {len(births_df)}")
        log.info(f"Total records in Births FS: {births_df[IN_FS_COL].sum()}")
        log.info(f"Total records in Marriages file: {len(marriages_df)}")
        log.info(f"Total records in Marriages FS: {marriages_df[IN_FS_COL].sum()}")
        log.info(f"Total records in Deaths file: {len(deaths_df)}")
        log.info(f"Total records in Deaths FS: {deaths_df[IN_FS_COL].sum()}")

        # Analyze data
        log.info("Analyzing data...")
        yearly_comparison = statistics.create_yearly_comparison(births_df, IN_FS_COL)
        surname_counts = statistics.count_values(births_df, NORMALIZED_SURNAME_COL)

        # Store statistics in database
        log.info("Storing statistics in database...")
        try:
            # Get summary statistics for each data source
            births_stats = statistics.get_summary_statistics(births_df)
            marriages_stats = statistics.get_summary_statistics(marriages_df)
            deaths_stats = statistics.get_summary_statistics(deaths_df)

            # Store summary statistics
            db.store_summary_statistics(births_stats, "births")
            db.store_summary_statistics(marriages_stats, "marriages")
            db.store_summary_statistics(deaths_stats, "deaths")

            # Store yearly comparison
            db.store_yearly_comparison(yearly_comparison, "births", IN_FS_COL)

            # Store surname counts
            db.store_value_counts(surname_counts, NORMALIZED_SURNAME_COL, "births")

            log.info("Statistics stored successfully")
        except db.QueryError as e:
            log.error(f"Error storing statistics: {str(e)}")

        # Visualize data
        log.info("Visualizing data...")
        plots.plot_yearly_counts(yearly_comparison)
        plots.plot_surname_counts(surname_counts)

        log.info("AncestorsPandas application completed successfully")
        return 0
    except Exception as e:
        log.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    # If command-line arguments are provided, use the CLI module
    if len(sys.argv) > 1:
        sys.exit(cli.main())
    # Otherwise, run the main function
    else:
        sys.exit(main())
