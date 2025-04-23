"""
Command-line interface for AncestorsPandas.

This module provides a command-line interface for running different analyses
and visualizations.
"""

import argparse
import sys
import pandas as pd
from typing import List, Optional

from ancestors_pandas import logger
from ancestors_pandas.data_loading import loader
from ancestors_pandas.analysis import statistics
from ancestors_pandas.visualization import plots


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


if __name__ == "__main__":
    sys.exit(main())
