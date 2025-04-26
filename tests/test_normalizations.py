"""
Unit tests for the normalizations.py module.
"""

import os
import unittest
import pandas as pd
import numpy as np
from io import StringIO
import tempfile
from datetime import datetime

# Import the functions to test
from normalizations import (
    load_and_normalize,
    strip_column_names,
    strip_string_values,
    parse_dates,
    normalize_surname,
    apply_surname_normalization
)

# Import constants from config
from config import (
    CSV_SEPARATOR, CSV_ENCODING, DATE_FORMAT_DAYFIRST,
    YEAR_COL, NORMALIZED_SURNAME_COL, IN_FS_COL,
    FEMALE_SURNAME_SUFFIX
)


class TestNormalizations(unittest.TestCase):
    """Test cases for the normalizations module."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a sample DataFrame for testing
        self.sample_data = pd.DataFrame({
            ' Name ': ['John Doe', ' Jane Smith ', 'Alex Johnson'],
            'Age': [30, 25, 40],
            ' Birth Date ': ['01/02/1990', '15/07/1995', '30/12/1980'],
            'Surname': ['Иванов', 'Петрова', 'Сидоров'],
            'FS_ID': ['FS123', None, 'FS456']
        })

    def test_strip_column_names(self):
        """Test that strip_column_names removes whitespace from column names."""
        result = strip_column_names(self.sample_data)
        expected_columns = ['Name', 'Age', 'Birth Date', 'Surname', 'FS_ID']
        self.assertListEqual(list(result.columns), expected_columns)

    def test_strip_string_values(self):
        """Test that strip_string_values removes whitespace from string values."""
        result = strip_string_values(self.sample_data)
        self.assertEqual(result.loc[0, ' Name '], 'John Doe')
        self.assertEqual(result.loc[1, ' Name '], 'Jane Smith')
        # Non-string values should remain unchanged
        self.assertEqual(result.loc[0, 'Age'], 30)

    def test_parse_dates(self):
        """Test that parse_dates correctly converts date strings to datetime objects."""
        df = strip_column_names(self.sample_data.copy())
        result = parse_dates(df, 'Birth Date')

        # Check that the column has been converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_dtype(result['Birth Date']))

        # Check specific date conversions
        expected_dates = [
            datetime(1990, 2, 1),
            datetime(1995, 7, 15),
            datetime(1980, 12, 30)
        ]
        for i, expected_date in enumerate(expected_dates):
            self.assertEqual(result.loc[i, 'Birth Date'].date(), expected_date.date())

    def test_normalize_surname(self):
        """Test that normalize_surname correctly handles various surname normalization cases."""
        # Test with simple feminine suffix
        self.assertEqual(normalize_surname('Петрова'), 'петров')

        # Test with masculine surname (should be converted to lowercase)
        self.assertEqual(normalize_surname('Иванов'), 'иванов')

        # Test with complex feminine endings
        self.assertEqual(normalize_surname('Иванова'), 'иванов')
        self.assertEqual(normalize_surname('Соколова'), 'соколов')
        self.assertEqual(normalize_surname('Королева'), 'королев')
        self.assertEqual(normalize_surname('Пушкина'), 'пушкин')
        self.assertEqual(normalize_surname('Достоевская'), 'достоевский')

        # Test with special characters and numbers
        self.assertEqual(normalize_surname('Иванов123'), 'иванов')
        self.assertEqual(normalize_surname('Петров!@#'), 'петров')

        # Test with prefixes
        self.assertEqual(normalize_surname('McDonald'), 'mcdonald')
        self.assertEqual(normalize_surname('MacArthur'), 'macarthur')
        self.assertEqual(normalize_surname('VanDyke'), 'vandyke')

        # Test with hyphenated surnames
        self.assertEqual(normalize_surname('Иванова-Петрова'), 'иванов-петров')
        self.assertEqual(normalize_surname('Смит-Джонсон'), 'смит-джонсон')

        # Test with non-string input
        self.assertEqual(normalize_surname(None), None)
        self.assertEqual(normalize_surname(123), 123)

        # Test with empty string
        self.assertEqual(normalize_surname(''), '')
        self.assertEqual(normalize_surname('   '), '   ')

    def test_apply_surname_normalization(self):
        """Test that apply_surname_normalization correctly adds a normalized surname column."""
        df = self.sample_data.copy()
        result = apply_surname_normalization(df, 'Surname', NORMALIZED_SURNAME_COL)

        # Check that the new column exists
        self.assertIn(NORMALIZED_SURNAME_COL, result.columns)

        # Check normalization results
        self.assertEqual(result.loc[0, NORMALIZED_SURNAME_COL], 'иванов')
        self.assertEqual(result.loc[1, NORMALIZED_SURNAME_COL], 'петров')
        self.assertEqual(result.loc[2, NORMALIZED_SURNAME_COL], 'сидоров')

    def test_load_and_normalize(self):
        """Test that load_and_normalize correctly loads and processes a CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding=CSV_ENCODING) as temp_file:
            # Write sample data to the temp file
            temp_file.write(' Name ' + CSV_SEPARATOR + 'Age' + CSV_SEPARATOR + ' Birth Date ' + CSV_SEPARATOR + 'Surname' + CSV_SEPARATOR + 'FS_ID\n')
            temp_file.write('John Doe' + CSV_SEPARATOR + '30' + CSV_SEPARATOR + '01/02/1990' + CSV_SEPARATOR + 'Иванов' + CSV_SEPARATOR + 'FS123\n')
            temp_file.write(' Jane Smith ' + CSV_SEPARATOR + '25' + CSV_SEPARATOR + '15/07/1995' + CSV_SEPARATOR + 'Петрова' + CSV_SEPARATOR + '\n')
            temp_file.write('Alex Johnson' + CSV_SEPARATOR + '40' + CSV_SEPARATOR + '30/12/1980' + CSV_SEPARATOR + 'Сидоров' + CSV_SEPARATOR + 'FS456\n')
            temp_file_path = temp_file.name

        try:
            # Test with all optional parameters
            result = load_and_normalize(
                temp_file_path,
                date_col='Birth Date',
                surname_col='Surname',
                fs_col='FS_ID'
            )

            # Check that column names are stripped
            self.assertIn('Name', result.columns)
            self.assertIn('Birth Date', result.columns)

            # Check that date parsing worked
            self.assertIn(YEAR_COL, result.columns)
            self.assertEqual(result.loc[0, YEAR_COL], 1990)

            # Check that surname normalization worked
            self.assertIn(NORMALIZED_SURNAME_COL, result.columns)
            self.assertEqual(result.loc[1, NORMALIZED_SURNAME_COL], 'петров')

            # Check that FS flag was added
            self.assertIn(IN_FS_COL, result.columns)
            self.assertTrue(result.loc[0, IN_FS_COL])
            self.assertFalse(result.loc[1, IN_FS_COL])

        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()
