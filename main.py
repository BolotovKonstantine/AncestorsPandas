import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/birth.csv', sep=';', encoding='utf-8')
df.columns = df.columns.str.strip()
df = df.apply(
    lambda col: col.map(lambda val: val.strip() if isinstance(val, str) else val)
)

df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], dayfirst=True, errors='coerce')
df["normalized_surname"] = df["Фамилия"].apply(
    lambda s: s[:-1] if isinstance(s, str) and s.endswith("а") else s
)

df['year'] = df['Дата рождения'].dt.year
df['in_fs'] = df['FS'].notna()
records_by_year = df.groupby('year').size()
records_by_year_in_fs = df[df['in_fs']].groupby('year').size()
yearly_counts = pd.DataFrame({
    'Total Records': records_by_year,
    'Records in FS': records_by_year_in_fs
}).fillna(0)
surname_counts = df["normalized_surname"].value_counts()

# Quick inspection
print(f'Total records in file {len(df)}')
print(f'Total records in FS {len(df[df["in_fs"]])}')

yearly_counts.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Year')
plt.ylabel('Number of Records')
plt.title('Total Records vs. Records in FS')
plt.show()
plt.figure(figsize=(10, 6))
surname_counts.plot(kind="bar")
plt.title("Instances of Each Normalized Surname")
plt.xlabel("Normalized Surname")
plt.ylabel("Count")
plt.tight_layout()
plt.show()



