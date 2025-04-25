"""
Command-line interface for AncestorsPandas.

This module provides a command-line interface for running different analyses
and visualizations.
"""

import argparse
import sys
import pandas as pd
import datetime
from typing import List, Optional, Union

from ancestors_pandas import logger
from ancestors_pandas.data_loading import loader
from ancestors_pandas.analysis import statistics
from ancestors_pandas.visualization import plots
from ancestors_pandas.database import stats_retriever
from config import DB_FILE, DB_HISTORY_LIMIT


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Parameters:
    -----------
    args : List[str], optional
        Command-line arguments. If None, sys.argv[1:] is used.

    Returns:
    --------
    argparse.Namespace
        Parsed arguments.

    Raises:
    -------
    TypeError
        If args is not a list of strings or None.
    """
    # Validate input
    if args is not None:
        if not isinstance(args, list):
            raise TypeError(f"args must be a list or None, got {type(args).__name__}")
        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("all elements in args must be strings")

    parser = argparse.ArgumentParser(
        description="AncestorsPandas - Genealogical data analysis tool"
    )

    # Add global arguments
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level"
    )
    parser.add_argument(
        "--log-file",
        help="Path to the log file"
    )
    parser.add_argument(
        "--db-path",
        default=DB_FILE,
        help=f"Path to the database file (default: {DB_FILE})"
    )
    parser.add_argument(
        "--db-history-limit",
        type=int,
        default=DB_HISTORY_LIMIT,
        help=f"Maximum number of historical records to retrieve (default: {DB_HISTORY_LIMIT})"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Load command
    load_parser = subparsers.add_parser(
        "load", help="Load and display basic information about the data"
    )
    load_parser.add_argument(
        "--births", default="data/births.csv", help="Path to births CSV file"
    )
    load_parser.add_argument(
        "--marriages", default="data/marriages.csv", help="Path to marriages CSV file"
    )
    load_parser.add_argument(
        "--deaths", default="data/deaths.csv", help="Path to deaths CSV file"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze the data"
    )
    analyze_parser.add_argument(
        "--births", default="data/births.csv", help="Path to births CSV file"
    )
    analyze_parser.add_argument(
        "--marriages", default="data/marriages.csv", help="Path to marriages CSV file"
    )
    analyze_parser.add_argument(
        "--deaths", default="data/deaths.csv", help="Path to deaths CSV file"
    )
    analyze_parser.add_argument(
        "--by-year", action="store_true", help="Analyze records by year"
    )
    analyze_parser.add_argument(
        "--by-surname", action="store_true", help="Analyze records by surname"
    )

    # Visualize command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize the data"
    )
    visualize_parser.add_argument(
        "--births", default="data/births.csv", help="Path to births CSV file"
    )
    visualize_parser.add_argument(
        "--marriages", default="data/marriages.csv", help="Path to marriages CSV file"
    )
    visualize_parser.add_argument(
        "--deaths", default="data/deaths.csv", help="Path to deaths CSV file"
    )
    visualize_parser.add_argument(
        "--yearly-counts", action="store_true", help="Plot yearly counts"
    )
    visualize_parser.add_argument(
        "--surname-counts", action="store_true", help="Plot surname counts"
    )
    visualize_parser.add_argument(
        "--top-n", type=int, help="Plot only the top N surnames"
    )
    visualize_parser.add_argument(
        "--save", help="Save the plot to a file instead of displaying it"
    )

    # View History command
    view_history_parser = subparsers.add_parser(
        "view-history", help="View historical statistics from the database"
    )
    view_history_parser.add_argument(
        "--type", required=True,
        choices=["summary", "yearly", "value-counts"],
        help="Type of statistics to view"
    )
    view_history_parser.add_argument(
        "--data-source", 
        help="Filter by data source (births, marriages, deaths)"
    )
    view_history_parser.add_argument(
        "--start-date", 
        help="Start date for filtering (YYYY-MM-DD)"
    )
    view_history_parser.add_argument(
        "--end-date", 
        help="End date for filtering (YYYY-MM-DD)"
    )
    view_history_parser.add_argument(
        "--column-name",
        help="Column name for value counts (required for value-counts type)"
    )
    view_history_parser.add_argument(
        "--condition-name",
        help="Condition name for yearly comparison (default: in_fs)"
    )
    view_history_parser.add_argument(
        "--year",
        type=int,
        help="Filter by specific year (for yearly comparison)"
    )
    view_history_parser.add_argument(
        "--value",
        help="Filter by specific value (for value counts)"
    )
    view_history_parser.add_argument(
        "--format", choices=["table", "csv", "json", "excel"], default="table",
        help="Output format (default: table)"
    )
    view_history_parser.add_argument(
        "--output",
        help="Output file path (required for csv, json, and excel formats)"
    )
    view_history_parser.add_argument(
        "--limit", type=int,
        help=f"Maximum number of records to retrieve (default: {DB_HISTORY_LIMIT})"
    )

    # Visualize History command
    visualize_history_parser = subparsers.add_parser(
        "visualize-history", help="Visualize historical statistics from the database"
    )
    visualize_history_parser.add_argument(
        "--over-time", action="store_true", 
        help="Plot changes in statistics over time"
    )
    visualize_history_parser.add_argument(
        "--comparison", action="store_true", 
        help="Plot comparison between different data updates"
    )
    visualize_history_parser.add_argument(
        "--data-source", 
        help="Filter by data source (births, marriages, deaths)"
    )
    visualize_history_parser.add_argument(
        "--value-column", required=True,
        help="Column containing the values to visualize (e.g., total_records, records_in_fs)"
    )
    visualize_history_parser.add_argument(
        "--group-column", 
        help="Column to group by for comparison (e.g., year, value)"
    )
    visualize_history_parser.add_argument(
        "--start-date", 
        help="Start date for filtering (YYYY-MM-DD)"
    )
    visualize_history_parser.add_argument(
        "--end-date", 
        help="End date for filtering (YYYY-MM-DD)"
    )
    visualize_history_parser.add_argument(
        "--max-dates", type=int, default=2,
        help="Maximum number of dates to compare (default: 2)"
    )
    visualize_history_parser.add_argument(
        "--plot-type", choices=["bar", "barh", "line"], default="bar",
        help="Type of plot for comparison (default: bar)"
    )
    visualize_history_parser.add_argument(
        "--title", 
        help="Custom title for the plot"
    )
    visualize_history_parser.add_argument(
        "--save", 
        help="Save the plot to a file instead of displaying it"
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.

    Parameters:
    -----------
    args : List[str], optional
        Command-line arguments. If None, sys.argv[1:] is used.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not a list of strings or None.
    Exception
        For other errors during command execution.
    """
    # parse_args already validates args
    try:
        parsed_args = parse_args(args)
    except Exception as e:
        print(f"Error parsing arguments: {str(e)}")
        return 1

    # Set up logging
    try:
        log_level = getattr(logger.logging, parsed_args.log_level)
        log = logger.setup_logger(level=log_level, log_file=parsed_args.log_file)
    except Exception as e:
        print(f"Error setting up logger: {str(e)}")
        return 1

    try:
        if parsed_args.command == "load":
            return cmd_load(parsed_args, log)
        elif parsed_args.command == "analyze":
            return cmd_analyze(parsed_args, log)
        elif parsed_args.command == "visualize":
            return cmd_visualize(parsed_args, log)
        elif parsed_args.command == "view-history":
            return cmd_view_history(parsed_args, log)
        elif parsed_args.command == "visualize-history":
            return cmd_visualize_history(parsed_args, log)
        else:
            log.error("No command specified. Use --help for usage information.")
            return 1
    except Exception as e:
        log.error(f"Error: {str(e)}")
        return 1


def cmd_load(args: argparse.Namespace, log: logger.logging.Logger) -> int:
    """
    Load and display basic information about the data.

    Parameters:
    -----------
    args : argparse.Namespace
        Parsed arguments.
    log : logging.Logger
        Logger instance.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not an argparse.Namespace or log is not a logger.logging.Logger.
    Exception
        For other errors during data loading.
    """
    # Validate input
    if not isinstance(args, argparse.Namespace):
        raise TypeError(f"args must be an argparse.Namespace, got {type(args).__name__}")

    if not isinstance(log, logger.logging.Logger):
        raise TypeError(f"log must be a logging.Logger, got {type(log).__name__}")

    # Validate required arguments
    if not hasattr(args, 'births') or not args.births:
        log.error("Missing required argument: births")
        return 1

    if not hasattr(args, 'marriages') or not args.marriages:
        log.error("Missing required argument: marriages")
        return 1

    if not hasattr(args, 'deaths') or not args.deaths:
        log.error("Missing required argument: deaths")
        return 1

    log.info("Loading data...")

    births_df = loader.load_and_normalize(
        args.births, date_col="Дата рождения", surname_col="Фамилия", fs_col="FS"
    )
    marriages_df = loader.load_and_normalize(
        args.marriages, date_col="Дата", surname_col="Фамилия", fs_col="FS"
    )
    deaths_df = loader.load_and_normalize(
        args.deaths, date_col="Дата смерти", surname_col="Фамилия", fs_col="FS"
    )

    log.info(f"Total records in Births file: {len(births_df)}")
    log.info(f"Total records in Births FS: {births_df['in_fs'].sum()}")
    log.info(f"Total records in Marriages file: {len(marriages_df)}")
    log.info(f"Total records in Marriages FS: {marriages_df['in_fs'].sum()}")
    log.info(f"Total records in Deaths file: {len(deaths_df)}")
    log.info(f"Total records in Deaths FS: {deaths_df['in_fs'].sum()}")

    return 0


def cmd_analyze(args: argparse.Namespace, log: logger.logging.Logger) -> int:
    """
    Analyze the data.

    Parameters:
    -----------
    args : argparse.Namespace
        Parsed arguments.
    log : logging.Logger
        Logger instance.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not an argparse.Namespace or log is not a logger.logging.Logger.
    Exception
        For other errors during data analysis.
    """
    # Validate input
    if not isinstance(args, argparse.Namespace):
        raise TypeError(f"args must be an argparse.Namespace, got {type(args).__name__}")

    if not isinstance(log, logger.logging.Logger):
        raise TypeError(f"log must be a logging.Logger, got {type(log).__name__}")

    # Validate required arguments
    if not hasattr(args, 'births') or not args.births:
        log.error("Missing required argument: births")
        return 1

    # Check if at least one analysis option is selected
    if not (hasattr(args, 'by_year') and args.by_year) and not (hasattr(args, 'by_surname') and args.by_surname):
        log.warning("No analysis option selected. Use --by-year or --by-surname.")

    log.info("Analyzing data...")

    births_df = loader.load_and_normalize(
        args.births, date_col="Дата рождения", surname_col="Фамилия", fs_col="FS"
    )

    if args.by_year:
        log.info("Analyzing records by year...")
        yearly_comparison = statistics.create_yearly_comparison(births_df, "in_fs")
        log.info("\nYearly comparison:\n" + str(yearly_comparison))

    if args.by_surname:
        log.info("Analyzing records by surname...")
        surname_counts = statistics.count_values(births_df, "normalized_surname")
        log.info("\nTop 10 surnames:\n" + str(surname_counts.head(10)))

    return 0


def cmd_visualize(args: argparse.Namespace, log: logger.logging.Logger) -> int:
    """
    Visualize the data.

    Parameters:
    -----------
    args : argparse.Namespace
        Parsed arguments.
    log : logging.Logger
        Logger instance.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not an argparse.Namespace or log is not a logger.logging.Logger.
    ValueError
        If top_n is provided but not positive.
    Exception
        For other errors during data visualization.
    """
    # Validate input
    if not isinstance(args, argparse.Namespace):
        raise TypeError(f"args must be an argparse.Namespace, got {type(args).__name__}")

    if not isinstance(log, logger.logging.Logger):
        raise TypeError(f"log must be a logging.Logger, got {type(log).__name__}")

    # Validate required arguments
    if not hasattr(args, 'births') or not args.births:
        log.error("Missing required argument: births")
        return 1

    # Check if at least one visualization option is selected
    if not (hasattr(args, 'yearly_counts') and args.yearly_counts) and not (hasattr(args, 'surname_counts') and args.surname_counts):
        log.warning("No visualization option selected. Use --yearly-counts or --surname-counts.")

    # Validate top_n if provided
    if hasattr(args, 'top_n') and args.top_n is not None:
        if not isinstance(args.top_n, int):
            log.error(f"top_n must be an integer, got {type(args.top_n).__name__}")
            return 1
        if args.top_n <= 0:
            log.error("top_n must be positive")
            return 1

    log.info("Visualizing data...")

    births_df = loader.load_and_normalize(
        args.births, date_col="Дата рождения", surname_col="Фамилия", fs_col="FS"
    )

    if args.yearly_counts:
        log.info("Plotting yearly counts...")
        records_by_year = statistics.count_records_by_year(births_df)
        records_by_year_in_fs = statistics.count_records_by_year_with_condition(
            births_df, "in_fs"
        )

        yearly_counts = {
            'Total Records': records_by_year,
            'Records in FS': records_by_year_in_fs
        }
        yearly_counts_df = pd.DataFrame(yearly_counts).fillna(0)

        plots.plot_yearly_counts(
            yearly_counts_df, save_path=args.save
        )

    if args.surname_counts:
        log.info("Plotting surname counts...")
        surname_counts = statistics.count_values(births_df, "normalized_surname")

        plots.plot_surname_counts(
            surname_counts, top_n=args.top_n, save_path=args.save
        )

    return 0


def cmd_view_history(args: argparse.Namespace, log: logger.logging.Logger) -> int:
    """
    View historical statistics from the database.

    Parameters:
    -----------
    args : argparse.Namespace
        Parsed arguments.
    log : logging.Logger
        Logger instance.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not an argparse.Namespace or log is not a logger.logging.Logger.
    ValueError
        If required arguments are missing or invalid.
    Exception
        For other errors during data retrieval.
    """
    # Validate input
    if not isinstance(args, argparse.Namespace):
        raise TypeError(f"args must be an argparse.Namespace, got {type(args).__name__}")

    if not isinstance(log, logger.logging.Logger):
        raise TypeError(f"log must be a logging.Logger, got {type(log).__name__}")

    # Get database path from arguments or use default
    db_path = args.db_path if hasattr(args, 'db_path') and args.db_path else DB_FILE

    # Get history limit from arguments or use default
    limit = args.limit if hasattr(args, 'limit') and args.limit is not None else DB_HISTORY_LIMIT

    # Validate required arguments
    if not hasattr(args, 'type') or not args.type:
        log.error("Missing required argument: type")
        return 1

    # For value-counts type, column_name is required
    if args.type == "value-counts" and (not hasattr(args, 'column_name') or not args.column_name):
        log.error("Missing required argument for value-counts: column_name")
        return 1

    # For non-table formats, output is required
    if hasattr(args, 'format') and args.format != "table" and (not hasattr(args, 'output') or not args.output):
        log.error(f"Missing required argument for {args.format} format: output")
        return 1

    log.info(f"Retrieving {args.type} statistics from database...")

    try:
        # Retrieve data based on the type
        if args.type == "summary":
            df = stats_retriever.export_summary_statistics_to_dataframe(
                start_date=args.start_date if hasattr(args, 'start_date') else None,
                end_date=args.end_date if hasattr(args, 'end_date') else None,
                data_source=args.data_source if hasattr(args, 'data_source') else None,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} summary statistics records")
        elif args.type == "yearly":
            df = stats_retriever.export_yearly_comparison_to_dataframe(
                start_date=args.start_date if hasattr(args, 'start_date') else None,
                end_date=args.end_date if hasattr(args, 'end_date') else None,
                data_source=args.data_source if hasattr(args, 'data_source') else None,
                condition_name=args.condition_name if hasattr(args, 'condition_name') else None,
                year=args.year if hasattr(args, 'year') else None,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} yearly comparison records")
        elif args.type == "value-counts":
            df = stats_retriever.export_value_counts_to_dataframe(
                column_name=args.column_name,
                start_date=args.start_date if hasattr(args, 'start_date') else None,
                end_date=args.end_date if hasattr(args, 'end_date') else None,
                data_source=args.data_source if hasattr(args, 'data_source') else None,
                value=args.value if hasattr(args, 'value') else None,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} value counts records")
        else:
            log.error(f"Invalid type: {args.type}")
            return 1

        # Check if we got any data
        if df.empty:
            log.error("No data found with the specified filters")
            return 1

        # Output the data in the requested format
        if args.format == "table":
            # Print as a formatted table
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            print(df)
        elif args.format == "csv":
            # Export to CSV
            stats_retriever.export_to_csv(df, args.output)
            log.info(f"Data exported to CSV: {args.output}")
        elif args.format == "json":
            # Export to JSON
            stats_retriever.export_to_json(df, args.output)
            log.info(f"Data exported to JSON: {args.output}")
        elif args.format == "excel":
            # Export to Excel
            stats_retriever.export_to_excel(df, args.output)
            log.info(f"Data exported to Excel: {args.output}")
        else:
            log.error(f"Invalid format: {args.format}")
            return 1

        return 0
    except ValueError as e:
        log.error(f"Value error: {str(e)}")
        return 1
    except Exception as e:
        log.error(f"Error retrieving historical data: {str(e)}")
        return 1


def cmd_visualize_history(args: argparse.Namespace, log: logger.logging.Logger) -> int:
    """
    Visualize historical statistics from the database.

    Parameters:
    -----------
    args : argparse.Namespace
        Parsed arguments.
    log : logging.Logger
        Logger instance.

    Returns:
    --------
    int
        Exit code.

    Raises:
    -------
    TypeError
        If args is not an argparse.Namespace or log is not a logger.logging.Logger.
    ValueError
        If required arguments are missing or invalid.
    Exception
        For other errors during data visualization.
    """
    # Validate input
    if not isinstance(args, argparse.Namespace):
        raise TypeError(f"args must be an argparse.Namespace, got {type(args).__name__}")

    if not isinstance(log, logger.logging.Logger):
        raise TypeError(f"log must be a logging.Logger, got {type(log).__name__}")

    # Check if at least one visualization option is selected
    if not (hasattr(args, 'over_time') and args.over_time) and not (hasattr(args, 'comparison') and args.comparison):
        log.warning("No visualization option selected. Use --over-time or --comparison.")
        return 1

    # Validate required arguments
    if not hasattr(args, 'value_column') or not args.value_column:
        log.error("Missing required argument: value_column")
        return 1

    # For comparison visualization, group_column is required
    if args.comparison and (not hasattr(args, 'group_column') or not args.group_column):
        log.error("Missing required argument for comparison: group_column")
        return 1

    log.info("Visualizing historical statistics...")

    # Get database path from arguments or use default
    db_path = args.db_path if hasattr(args, 'db_path') and args.db_path else DB_FILE

    # Get history limit from arguments or use default
    max_dates = args.max_dates if hasattr(args, 'max_dates') and args.max_dates else DB_HISTORY_LIMIT

    # Process date arguments
    start_date = None
    end_date = None

    if hasattr(args, 'start_date') and args.start_date:
        try:
            start_date = args.start_date
        except ValueError:
            log.error(f"Invalid start date format: {args.start_date}. Use YYYY-MM-DD.")
            return 1

    if hasattr(args, 'end_date') and args.end_date:
        try:
            end_date = args.end_date
        except ValueError:
            log.error(f"Invalid end date format: {args.end_date}. Use YYYY-MM-DD.")
            return 1

    # Determine which type of data to retrieve based on the value_column
    if args.value_column.startswith('total_') or args.value_column.startswith('records_'):
        # Summary statistics
        try:
            df = stats_retriever.export_summary_statistics_to_dataframe(
                start_date=start_date,
                end_date=end_date,
                data_source=args.data_source,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} summary statistics records")
        except Exception as e:
            log.error(f"Error retrieving summary statistics: {str(e)}")
            return 1
    elif args.value_column == 'count':
        # Value counts
        try:
            df = stats_retriever.export_value_counts_to_dataframe(
                column_name=args.group_column,
                start_date=start_date,
                end_date=end_date,
                data_source=args.data_source,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} value counts records")
        except Exception as e:
            log.error(f"Error retrieving value counts: {str(e)}")
            return 1
    else:
        # Yearly comparison
        try:
            df = stats_retriever.export_yearly_comparison_to_dataframe(
                start_date=start_date,
                end_date=end_date,
                data_source=args.data_source,
                db_path=db_path
            )
            log.info(f"Retrieved {len(df)} yearly comparison records")
        except Exception as e:
            log.error(f"Error retrieving yearly comparison data: {str(e)}")
            return 1

    # Check if we got any data
    if df.empty:
        log.error("No data found with the specified filters")
        return 1

    # Visualize the data
    try:
        if args.over_time:
            log.info("Plotting statistics over time...")

            # Set custom title if provided
            title = args.title if hasattr(args, 'title') and args.title else f"{args.value_column} Over Time"

            plots.plot_statistics_over_time(
                df=df,
                value_column=args.value_column,
                data_source_column='data_source' if hasattr(args, 'data_source') and args.data_source is None else None,
                title=title,
                save_path=args.save if hasattr(args, 'save') and args.save else None
            )
            log.info("Statistics over time plot created successfully")

        if args.comparison:
            log.info("Plotting statistics comparison...")

            # Set custom title if provided
            title = args.title if hasattr(args, 'title') and args.title else f"{args.value_column} Comparison"

            # Get plot type
            kind = args.plot_type if hasattr(args, 'plot_type') and args.plot_type else 'bar'

            # Get max dates
            max_dates = args.max_dates if hasattr(args, 'max_dates') and args.max_dates else 2

            plots.plot_statistics_comparison(
                df=df,
                value_column=args.value_column,
                group_column=args.group_column,
                max_dates=max_dates,
                title=title,
                kind=kind,
                save_path=args.save if hasattr(args, 'save') and args.save else None
            )
            log.info("Statistics comparison plot created successfully")

    except Exception as e:
        log.error(f"Error visualizing historical data: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
