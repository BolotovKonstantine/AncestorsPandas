#!/usr/bin/env python3
"""
Example script demonstrating how to use the historical data visualization features.

This script provides examples of using the visualize-history command to create
different types of visualizations of historical statistics.
"""

import sys
import os
import argparse

# Add the parent directory to the path so we can import the ancestors_pandas package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ancestors_pandas.cli import main


def run_over_time_example():
    """Run an example of visualizing statistics over time."""
    print("Example 1: Visualizing total records over time")
    args = [
        "visualize-history",
        "--over-time",
        "--value-column", "total_records"
    ]
    main(args)


def run_comparison_example():
    """Run an example of comparing statistics between updates."""
    print("Example 2: Comparing records by year between updates")
    args = [
        "visualize-history",
        "--comparison",
        "--value-column", "total_by_year",
        "--group-column", "year"
    ]
    main(args)


def run_value_counts_example():
    """Run an example of visualizing value counts over time."""
    print("Example 3: Visualizing surname counts over time")
    args = [
        "visualize-history",
        "--over-time",
        "--value-column", "count",
        "--data-source", "births"
    ]
    main(args)


def run_custom_example():
    """Run an example with custom options."""
    print("Example 4: Custom visualization with line plot and title")
    args = [
        "visualize-history",
        "--comparison",
        "--value-column", "count",
        "--group-column", "value",
        "--max-dates", "3",
        "--plot-type", "line",
        "--title", "Top Surnames Comparison"
    ]
    main(args)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run examples of historical data visualizations"
    )
    parser.add_argument(
        "--example", type=int, choices=[1, 2, 3, 4], default=1,
        help="Which example to run (1-4)"
    )
    parser.add_argument(
        "--save", help="Save the plot to a file instead of displaying it"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    # Add save option if provided
    if args.save:
        sys.argv.append("--save")
        sys.argv.append(args.save)
    
    # Run the selected example
    if args.example == 1:
        run_over_time_example()
    elif args.example == 2:
        run_comparison_example()
    elif args.example == 3:
        run_value_counts_example()
    elif args.example == 4:
        run_custom_example()