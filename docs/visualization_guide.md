# AncestorsPandas Visualization Guide

This guide explains how to use the visualization features in AncestorsPandas, particularly focusing on the historical data visualization capabilities.

> **Note:** For ready-to-run examples, see the [example script](../examples/visualize_history_example.py).

## Table of Contents
- [Basic Visualizations](#basic-visualizations)
- [Historical Data Visualizations](#historical-data-visualizations)
  - [Visualizing Changes Over Time](#visualizing-changes-over-time)
  - [Comparing Statistics Between Updates](#comparing-statistics-between-updates)
- [Command Reference](#command-reference)

## Basic Visualizations

AncestorsPandas provides basic visualization capabilities through the `visualize` command:

> **Note:** All visualization operations now display progress indicators to keep you informed during long-running operations.

```bash
python main.py visualize --yearly-counts
python main.py visualize --surname-counts
python main.py visualize --surname-counts --top-n 10
python main.py visualize --yearly-counts --save yearly_plot.png
```

## Historical Data Visualizations

AncestorsPandas now includes powerful features to visualize historical statistics stored in the database. These visualizations help you track changes in your genealogical data over time and compare different data updates.

### Visualizing Changes Over Time

To visualize how a specific statistic changes over time, use the `visualize-history` command with the `--over-time` option:

```bash
python main.py visualize-history --over-time --value-column total_records
```

This command plots the total number of records over time, showing how your dataset has grown.

You can filter by data source:

```bash
python main.py visualize-history --over-time --value-column total_records --data-source births
```

You can also specify a date range:

```bash
python main.py visualize-history --over-time --value-column records_in_fs --start-date 2023-01-01 --end-date 2023-12-31
```

### Comparing Statistics Between Updates

To compare statistics between different data updates, use the `--comparison` option:

```bash
python main.py visualize-history --comparison --value-column total_by_year --group-column year
```

This command creates a bar chart comparing the total records by year across different data updates.

You can specify the type of plot:

```bash
python main.py visualize-history --comparison --value-column total_by_year --group-column year --plot-type line
```

You can limit the number of dates to compare:

```bash
python main.py visualize-history --comparison --value-column count --group-column value --max-dates 3
```

You can also save the visualization to a file:

```bash
python main.py visualize-history --comparison --value-column total_by_year --group-column year --save comparison.png
```

## Command Reference

### visualize-history

Visualize historical statistics from the database.

#### Required Arguments:
- `--value-column`: Column containing the values to visualize (e.g., total_records, records_in_fs)

#### Visualization Type (at least one required):
- `--over-time`: Plot changes in statistics over time
- `--comparison`: Plot comparison between different data updates

#### Optional Arguments:
- `--data-source`: Filter by data source (births, marriages, deaths)
- `--group-column`: Column to group by for comparison (e.g., year, value) - Required for --comparison
- `--start-date`: Start date for filtering (YYYY-MM-DD)
- `--end-date`: End date for filtering (YYYY-MM-DD)
- `--max-dates`: Maximum number of dates to compare (default: 2)
- `--plot-type`: Type of plot for comparison (bar, barh, line) (default: bar)
- `--title`: Custom title for the plot
- `--save`: Save the plot to a file instead of displaying it

#### Value Column Options:
- Summary statistics: `total_records`, `records_in_fs`, etc. (columns starting with 'total_' or 'records_')
- Value counts: `count` (for surname counts and other categorical data)
- Yearly comparison: Any other column name (e.g., `total_by_year`, `in_fs_by_year`)

#### Examples:

1. Plot total records over time for all data sources:
   ```bash
   python main.py visualize-history --over-time --value-column total_records
   ```

2. Compare records in FamilySearch by year between the two most recent data updates:
   ```bash
   python main.py visualize-history --comparison --value-column in_fs_by_year --group-column year
   ```

3. Plot surname counts from the births data source over time:
   ```bash
   python main.py visualize-history --over-time --value-column count --data-source births
   ```

4. Compare the top surnames between the three most recent data updates:
   ```bash
   python main.py visualize-history --comparison --value-column count --group-column value --max-dates 3
   ```

5. Save a visualization to a file:
   ```bash
   python main.py visualize-history --over-time --value-column total_records --save stats_over_time.png
   ```
