"""
Visualization module for AncestorsPandas.

This module provides functions for visualizing genealogical data.
"""

import matplotlib.pyplot as plt
from config import (
    FIGURE_SIZE, TITLE_FONTSIZE, LABEL_FONTSIZE,
    YEARLY_PLOT_TITLE, YEARLY_PLOT_XLABEL, YEARLY_PLOT_YLABEL,
    SURNAME_PLOT_TITLE, SURNAME_PLOT_XLABEL, SURNAME_PLOT_YLABEL
)


def plot_yearly_counts(yearly_counts):
    """
    Plots a bar chart of the total records by year vs. records in FS by year.

    Parameters:
    -----------
    yearly_counts : pandas.DataFrame
        A dataframe with columns 'Total Records' and 'Records in FS'
        indexed by year.
    """
    yearly_counts.plot(kind='bar', figsize=FIGURE_SIZE)
    plt.xlabel(YEARLY_PLOT_XLABEL, fontsize=LABEL_FONTSIZE)
    plt.ylabel(YEARLY_PLOT_YLABEL, fontsize=LABEL_FONTSIZE)
    plt.title(YEARLY_PLOT_TITLE, fontsize=TITLE_FONTSIZE)
    plt.show()


def plot_surname_counts(surname_counts):
    """
    Plots a bar chart of surname counts.

    Parameters:
    -----------
    surname_counts : pandas.Series
        A series with the count of surnames (already normalized).
    """
    plt.figure(figsize=FIGURE_SIZE)
    surname_counts.plot(kind='bar')
    plt.title(SURNAME_PLOT_TITLE, fontsize=TITLE_FONTSIZE)
    plt.xlabel(SURNAME_PLOT_XLABEL, fontsize=LABEL_FONTSIZE)
    plt.ylabel(SURNAME_PLOT_YLABEL, fontsize=LABEL_FONTSIZE)
    plt.tight_layout()
    plt.show()
