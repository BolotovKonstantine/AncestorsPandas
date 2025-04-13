# python

import pandas as pd

from normalizations import (
    strip_column_names,
    strip_string_values,
    parse_dates,
    apply_surname_normalization
)
from visualizations import plot_yearly_counts, plot_surname_counts


# Read data from a CSV file
df = pd.read_csv('data/birth.csv', sep=';', encoding='utf-8')

# Apply normalization and cleaning functions
df = strip_column_names(df)
df = strip_string_values(df)
df = parse_dates(df, date_column='Дата рождения')
df = apply_surname_normalization(df, source_col='Фамилия',
                                 target_col='normalized_surname')

# Additional data processing steps
df['year'] = df['Дата рождения'].dt.year
df['in_fs'] = df['FS'].notna()

# Summaries
records_by_year = df.groupby('year').size()
records_by_year_in_fs = df[df['in_fs']].groupby('year').size()

yearly_counts = pd.DataFrame({
    'Total Records': records_by_year,
    'Records in FS': records_by_year_in_fs
}).fillna(0)

surname_counts = df["normalized_surname"].value_counts()

# Quick inspection
print(f'Total records in file: {len(df)}')
print(f'Total records in FS: {df["in_fs"].sum()}')

# Call the separate visualization functions
plot_yearly_counts(yearly_counts)
plot_surname_counts(surname_counts)

