"""
Test module for the stats_retriever module.

This module contains tests for the statistics retrieval functionality.
"""

import unittest
import os
import tempfile
import pandas as pd
import datetime
from pathlib import Path

from ancestors_pandas.database.db import init_database
from ancestors_pandas.database.stats_logger import log_summary_statistics, log_yearly_comparison, log_value_counts
from ancestors_pandas.database.stats_retriever import (
    query_summary_statistics,
    query_yearly_comparison,
    query_value_counts,
    export_summary_statistics_to_dataframe,
    export_yearly_comparison_to_dataframe,
    export_value_counts_to_dataframe,
    export_to_csv,
    export_to_excel,
    export_to_json
)


class TestStatsRetriever(unittest.TestCase):
    """Test case for the stats_retriever module."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'test.db')
        
        # Initialize the database
        init_database(self.db_path)
        
        # Create test data
        self.create_test_data()

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory and its contents
        self.temp_dir.cleanup()

    def create_test_data(self):
        """Create test data in the database."""
        # Create a test DataFrame for births
        births_data = {
            'year': [1900, 1901, 1902, 1903],
            'in_fs': [True, False, True, False],
            'normalized_surname': ['Smith', 'Johnson', 'Smith', 'Williams']
        }
        births_df = pd.DataFrame(births_data)
        
        # Create a test DataFrame for deaths
        deaths_data = {
            'year': [1950, 1951, 1952, 1953],
            'in_fs': [True, True, False, False],
            'normalized_surname': ['Brown', 'Davis', 'Brown', 'Miller']
        }
        deaths_df = pd.DataFrame(deaths_data)
        
        # Log statistics for births
        log_summary_statistics(births_df, 'births', {'source': 'test'}, self.db_path)
        log_yearly_comparison(births_df, 'births', 'in_fs', 'year', self.db_path)
        log_value_counts(births_df, 'normalized_surname', 'births', self.db_path)
        
        # Log statistics for deaths
        log_summary_statistics(deaths_df, 'deaths', {'source': 'test'}, self.db_path)
        log_yearly_comparison(deaths_df, 'deaths', 'in_fs', 'year', self.db_path)
        log_value_counts(deaths_df, 'normalized_surname', 'deaths', self.db_path)

    def test_query_summary_statistics(self):
        """Test querying summary statistics."""
        # Query all summary statistics
        all_stats = query_summary_statistics(db_path=self.db_path)
        self.assertEqual(len(all_stats), 2)
        
        # Query summary statistics for births
        births_stats = query_summary_statistics(data_source='births', db_path=self.db_path)
        self.assertEqual(len(births_stats), 1)
        self.assertEqual(births_stats[0]['data_source'], 'births')
        
        # Query summary statistics for deaths
        deaths_stats = query_summary_statistics(data_source='deaths', db_path=self.db_path)
        self.assertEqual(len(deaths_stats), 1)
        self.assertEqual(deaths_stats[0]['data_source'], 'deaths')

    def test_query_yearly_comparison(self):
        """Test querying yearly comparison data."""
        # Query all yearly comparison data
        all_comparisons = query_yearly_comparison(db_path=self.db_path)
        self.assertGreater(len(all_comparisons), 0)
        
        # Query yearly comparison data for births
        births_comparisons = query_yearly_comparison(data_source='births', db_path=self.db_path)
        self.assertGreater(len(births_comparisons), 0)
        self.assertEqual(births_comparisons[0]['data_source'], 'births')
        
        # Query yearly comparison data for deaths
        deaths_comparisons = query_yearly_comparison(data_source='deaths', db_path=self.db_path)
        self.assertGreater(len(deaths_comparisons), 0)
        self.assertEqual(deaths_comparisons[0]['data_source'], 'deaths')
        
        # Query yearly comparison data for a specific year
        year_comparisons = query_yearly_comparison(year=1900, db_path=self.db_path)
        self.assertGreater(len(year_comparisons), 0)
        self.assertEqual(year_comparisons[0]['year'], 1900)

    def test_query_value_counts(self):
        """Test querying value counts."""
        # Query all value counts
        all_counts = query_value_counts(db_path=self.db_path)
        self.assertGreater(len(all_counts), 0)
        
        # Query value counts for normalized_surname
        surname_counts = query_value_counts(column_name='normalized_surname', db_path=self.db_path)
        self.assertGreater(len(surname_counts), 0)
        self.assertEqual(surname_counts[0]['column_name'], 'normalized_surname')
        
        # Query value counts for births
        births_counts = query_value_counts(data_source='births', db_path=self.db_path)
        self.assertGreater(len(births_counts), 0)
        self.assertEqual(births_counts[0]['data_source'], 'births')
        
        # Query value counts for a specific value
        smith_counts = query_value_counts(value='Smith', db_path=self.db_path)
        self.assertGreater(len(smith_counts), 0)
        self.assertEqual(smith_counts[0]['value'], 'Smith')

    def test_export_to_dataframe(self):
        """Test exporting data to DataFrames."""
        # Export summary statistics to DataFrame
        summary_df = export_summary_statistics_to_dataframe(db_path=self.db_path)
        self.assertIsInstance(summary_df, pd.DataFrame)
        self.assertEqual(len(summary_df), 2)
        
        # Export yearly comparison to DataFrame
        yearly_df = export_yearly_comparison_to_dataframe(db_path=self.db_path)
        self.assertIsInstance(yearly_df, pd.DataFrame)
        self.assertGreater(len(yearly_df), 0)
        
        # Export value counts to DataFrame
        counts_df = export_value_counts_to_dataframe(db_path=self.db_path)
        self.assertIsInstance(counts_df, pd.DataFrame)
        self.assertGreater(len(counts_df), 0)

    def test_export_to_files(self):
        """Test exporting data to files."""
        # Get a DataFrame to export
        df = export_summary_statistics_to_dataframe(db_path=self.db_path)
        
        # Export to CSV
        csv_path = os.path.join(self.temp_dir.name, 'test.csv')
        export_to_csv(df, csv_path)
        self.assertTrue(os.path.exists(csv_path))
        
        # Export to Excel
        excel_path = os.path.join(self.temp_dir.name, 'test.xlsx')
        export_to_excel(df, excel_path)
        self.assertTrue(os.path.exists(excel_path))
        
        # Export to JSON
        json_path = os.path.join(self.temp_dir.name, 'test.json')
        export_to_json(df, json_path)
        self.assertTrue(os.path.exists(json_path))


if __name__ == '__main__':
    unittest.main()