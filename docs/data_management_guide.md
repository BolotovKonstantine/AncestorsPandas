# AncestorsPandas Data Management Guide

This guide explains how to use the data management features in AncestorsPandas, particularly focusing on the data upload, validation, and normalization capabilities in the web interface.

## Table of Contents
- [Data Sources Overview](#data-sources-overview)
- [Managing Data Sources](#managing-data-sources)
  - [Creating a New Data Source](#creating-a-new-data-source)
  - [Editing Data Sources](#editing-data-sources)
  - [Deleting Data Sources](#deleting-data-sources)
- [Data Normalization](#data-normalization)
  - [Surname Normalization](#surname-normalization)
  - [Date Normalization](#date-normalization)
  - [Location Normalization](#location-normalization)
- [Best Practices](#best-practices)

## Data Sources Overview

In AncestorsPandas, a data source represents a CSV file containing genealogical data such as births, marriages, or deaths. Each data source has the following properties:

- **Name**: A descriptive name for the data source
- **Source Type**: The type of data (births, marriages, deaths, or other)
- **File Path**: The location of the CSV file
- **Date Column**: The column in the CSV file that contains date information
- **Surname Column**: The column in the CSV file that contains surname information
- **FamilySearch Column**: The column in the CSV file that indicates whether the record is in FamilySearch
- **Description**: An optional description of the data source

## Managing Data Sources

### Creating a New Data Source

To create a new data source:

1. Navigate to the **Data Sources** page from the main navigation menu
2. Click the **Add New Data Source** button
3. Fill in the required information:
   - **Name**: Enter a descriptive name for the data source
   - **Source Type**: Select the type of data (births, marriages, deaths, or other)
   - **Description**: (Optional) Enter a description of the data source
   - **CSV File**: Upload a CSV file containing the data
4. After uploading the file, you can preview the data and select the appropriate columns:
   - **Date Column**: Select the column containing date information
   - **Surname Column**: Select the column containing surname information
   - **FamilySearch Column**: Select the column indicating whether the record is in FamilySearch
5. Click **Create Data Source** to save the data source

### Editing Data Sources

To edit an existing data source:

1. Navigate to the **Data Sources** page
2. Find the data source you want to edit and click the **Edit** button
3. Update the information as needed
4. If you want to replace the CSV file, upload a new file
5. Click **Update Data Source** to save your changes

### Deleting Data Sources

To delete a data source:

1. Navigate to the **Data Sources** page
2. Find the data source you want to delete and click the **Delete** button
3. Confirm the deletion on the confirmation page

> **Warning**: Deleting a data source will permanently remove the data source and its associated file. This action cannot be undone.

## Data Normalization

AncestorsPandas provides tools to normalize data in your CSV files. Normalization helps standardize data formats, making analysis more accurate and consistent.

To normalize data in a data source:

1. Navigate to the **Data Sources** page
2. Find the data source you want to normalize and click the **Normalize** button
3. Select the column you want to normalize
4. Choose the normalization type (surname, date, or location)
5. Click **Apply Normalization** to normalize the data

> **Note**: Normalization will create a new column in your CSV file with the prefix "normalized_" followed by the original column name.

### Surname Normalization

Surname normalization performs the following operations:

- Converts text to lowercase
- Removes special characters and numbers
- Standardizes common surname variations
- Handles prefixes like "Mc", "Mac", etc.

### Date Normalization

Date normalization performs the following operations:

- Converts various date formats to ISO format (YYYY-MM-DD)
- Handles partial dates (year only, year and month)
- Standardizes date separators
- Extracts year from date strings

### Location Normalization

Location normalization performs the following operations:

- Standardizes location names
- Removes common prefixes and suffixes
- Handles abbreviations for states, provinces, and countries
- Standardizes separators in location hierarchies

## Best Practices

Here are some best practices for managing data sources in AncestorsPandas:

1. **Use descriptive names**: Give your data sources clear, descriptive names that indicate their content and purpose.
2. **Add detailed descriptions**: Include information about the data source, such as where the data came from, when it was collected, and any special considerations.
3. **Back up your data**: Before normalizing data, make a backup of your original CSV files.
4. **Validate your data**: Use the preview feature to ensure your CSV file is correctly formatted and contains the expected data.
5. **Organize your files**: Keep your CSV files organized in a consistent directory structure.
6. **Update regularly**: If you receive updated data, create a new data source rather than overwriting an existing one to maintain a history of your data.