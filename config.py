"""
Configuration settings for the AncestorsPandas project.

This module contains constants and configuration settings used throughout the project,
including file paths, column names, and other parameters.
"""

# File paths
DATA_DIR = "data"
BIRTHS_FILE = f"{DATA_DIR}/births.csv"
MARRIAGES_FILE = f"{DATA_DIR}/marriages.csv"
DEATHS_FILE = f"{DATA_DIR}/deaths.csv"

# Column names
BIRTHS_DATE_COL = "Дата рождения"
MARRIAGES_DATE_COL = "Дата"
DEATHS_DATE_COL = "Дата смерти"
SURNAME_COL = "Фамилия"
FS_COL = "FS"
YEAR_COL = "year"
NORMALIZED_SURNAME_COL = "normalized_surname"
IN_FS_COL = "in_fs"

# CSV settings
CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8"
DATE_FORMAT_DAYFIRST = True

# Visualization settings
FIGURE_SIZE = (10, 6)
TITLE_FONTSIZE = 14
LABEL_FONTSIZE = 12

# Plot labels and titles
YEARLY_PLOT_TITLE = "Total Records vs. Records in FS"
YEARLY_PLOT_XLABEL = "Year"
YEARLY_PLOT_YLABEL = "Number of Records"
SURNAME_PLOT_TITLE = "Instances of Each Normalized Surname"
SURNAME_PLOT_XLABEL = "Normalized Surname"
SURNAME_PLOT_YLABEL = "Count"

# Column names for statistics
TOTAL_RECORDS_COL = "Total Records"
RECORDS_WITH_CONDITION_FORMAT = "Records with {}"

# Surname normalization
FEMALE_SURNAME_SUFFIX = "а"

# Summary statistics keys
STAT_TOTAL_RECORDS = "total_records"
STAT_MISSING_VALUES = "missing_values"
STAT_UNIQUE_YEARS = "unique_years"
STAT_RECORDS_IN_FS = "records_in_fs"
STAT_UNIQUE_SURNAMES = "unique_surnames"
