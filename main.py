# python

import pandas as pd

from normalizations import (
    load_and_normalize
)
from visualizations import plot_yearly_counts, plot_surname_counts

# Read data from a CSV files
births_df = load_and_normalize('data/births.csv', date_col='Дата рождения', surname_col='Фамилия', fs_col='FS')
marriages_df = load_and_normalize('data/marriages.csv', date_col='Дата', surname_col='Фамилия', fs_col='FS')
deaths_df = load_and_normalize('data/deaths.csv', date_col='Дата смерти', surname_col='Фамилия', fs_col='FS')




# Summaries
records_by_year_births = births_df.groupby('year').size()
records_by_year_in_fs_births = births_df[births_df['in_fs']].groupby('year').size()

yearly_counts = pd.DataFrame({
    'Total Records': records_by_year_births,
    'Records in FS': records_by_year_in_fs_births
}).fillna(0)

surname_counts_births = births_df["normalized_surname"].value_counts()

# Quick inspection
print(f'Total records in Births file: {len(births_df)}')
print(f'Total records in Births FS: {births_df["in_fs"].sum()}')
print(f'Total records in Marriages file: {len(marriages_df)}')
print(f'Total records in Marriages FS: {marriages_df["in_fs"].sum()}')
print(f'Total records in Deaths file: {len(deaths_df)}')
print(f'Total records in Deaths FS: {deaths_df["in_fs"].sum()}')
# Call the separate visualization functions
plot_yearly_counts(yearly_counts)
plot_surname_counts(surname_counts_births)

