# python

import matplotlib.pyplot as plt


def plot_yearly_counts(yearly_counts):
    """
    Plots a bar chart of the total records by year vs. records in FS by year.

    Parameters:
    -----------
    yearly_counts : pandas.DataFrame
        A dataframe with columns 'Total Records' and 'Records in FS'
        indexed by year.
    """
    yearly_counts.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('Year')
    plt.ylabel('Number of Records')
    plt.title('Total Records vs. Records in FS')
    plt.show()


def plot_surname_counts(surname_counts):
    """
    Plots a bar chart of surname counts.

    Parameters:
    -----------
    surname_counts : pandas.Series
        A series with the count of surnames (already normalized).
    """
    plt.figure(figsize=(10, 6))
    surname_counts.plot(kind='bar')
    plt.title("Instances of Each Normalized Surname")
    plt.xlabel("Normalized Surname")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
