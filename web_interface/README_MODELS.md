# Django Models for AncestorsPandas Web Interface

This document provides information about the Django models implemented for the AncestorsPandas web interface.

## Models Overview

### Accounts App
- **UserProfile**: Extends the built-in Django User model with additional preferences and settings.

### Dashboard App
- **DataSource**: Represents a data source (births, marriages, deaths) with metadata.
- **SummaryStatistics**: Stores summary statistics for a data source.
- **YearlyComparison**: Stores yearly comparison data.
- **ValueCounts**: Stores value counts for different columns.
- **Visualization**: Represents saved visualizations with configuration and image data.

## How to Apply Migrations

To create and apply the migrations for these models, follow these steps:

1. Navigate to the web_interface directory:
   ```
   cd web_interface
   ```

2. Create the migrations:
   ```
   python make_migrations.py
   ```

3. Apply the migrations:
   ```
   python manage.py migrate
   ```

## Testing the Models

A test script is provided to verify that the models work correctly. To run the tests:

1. Navigate to the web_interface directory:
   ```
   cd web_interface
   ```

2. Run the test script:
   ```
   python test_models.py
   ```

The test script will create test instances of each model, save them to the database, and verify that they can be retrieved with the expected values.

## Model Details

### UserProfile

The UserProfile model extends the built-in Django User model with additional preferences:

- **default_chart_type**: User's preferred chart type (bar, line, pie, scatter)
- **default_color_scheme**: User's preferred color scheme (default, pastel, vibrant, monochrome)
- **show_data_tooltips**: Whether to show tooltips on data visualizations
- **enable_email_notifications**: Whether to send email notifications

A signal handler automatically creates or updates the UserProfile when a User is created or updated.

### DataSource

The DataSource model represents a data source (births, marriages, deaths) with metadata:

- **name**: Name of the data source
- **source_type**: Type of data source (births, marriages, deaths, other)
- **file_path**: Path to the data file
- **date_column**: Name of the date column in the data file
- **surname_column**: Name of the surname column in the data file
- **fs_column**: Name of the FamilySearch column in the data file
- **description**: Description of the data source
- **created_by**: User who created the data source

### SummaryStatistics

The SummaryStatistics model stores summary statistics for a data source:

- **data_source**: Reference to the DataSource
- **timestamp**: When the statistics were calculated
- **total_records**: Total number of records in the data source
- **missing_values**: Number of missing values in the data source
- **unique_years**: Number of unique years in the data source
- **records_in_fs**: Number of records in FamilySearch
- **unique_surnames**: Number of unique surnames in the data source
- **additional_data**: Additional data stored as JSON

### YearlyComparison

The YearlyComparison model stores yearly comparison data:

- **data_source**: Reference to the DataSource
- **timestamp**: When the comparison was calculated
- **year**: Year of the comparison
- **total_records**: Total number of records for the year
- **records_with_condition**: Number of records meeting a condition (e.g., in FamilySearch)
- **condition_name**: Name of the condition (default: "in_fs")

### ValueCounts

The ValueCounts model stores value counts for different columns:

- **data_source**: Reference to the DataSource
- **timestamp**: When the counts were calculated
- **column_name**: Name of the column being counted
- **value**: Value being counted
- **count**: Number of occurrences of the value

### Visualization

The Visualization model represents saved visualizations:

- **title**: Title of the visualization
- **description**: Description of the visualization
- **visualization_type**: Type of visualization (bar, line, pie, scatter, etc.)
- **data_source**: Reference to the DataSource
- **created_by**: User who created the visualization
- **config**: Configuration for the visualization (stored as JSON)
- **image_data**: Image data or URL for the visualization