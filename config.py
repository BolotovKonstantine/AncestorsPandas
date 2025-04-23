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

# CSV settings
CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8"

# Visualization settings
FIGURE_SIZE = (10, 6)
TITLE_FONTSIZE = 14
LABEL_FONTSIZE = 12