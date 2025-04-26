#!/usr/bin/env python3
"""
Script to test the new models.

This script should be run from the web_interface directory after applying migrations.
"""

import os
import sys
import django
import json
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ancestors_web.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from dashboard.models import DataSource, SummaryStatistics, YearlyComparison, ValueCounts, Visualization

def test_user_profile():
    """Test UserProfile model."""
    print("Testing UserProfile model...")
    
    # Create a test user if it doesn't exist
    username = "testuser"
    try:
        user = User.objects.get(username=username)
        print(f"Using existing user: {username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email="testuser@example.com",
            password="testpassword"
        )
        print(f"Created new user: {username}")
    
    # UserProfile should be created automatically via signal
    profile = user.profile
    
    # Update profile preferences
    profile.default_chart_type = 'pie'
    profile.default_color_scheme = 'vibrant'
    profile.save()
    
    # Verify changes
    updated_profile = UserProfile.objects.get(user=user)
    assert updated_profile.default_chart_type == 'pie'
    assert updated_profile.default_color_scheme == 'vibrant'
    
    print("UserProfile test passed!")

def test_data_source():
    """Test DataSource model."""
    print("Testing DataSource model...")
    
    # Get the test user
    user = User.objects.get(username="testuser")
    
    # Create a test data source
    data_source = DataSource.objects.create(
        name="Test Births",
        source_type="births",
        file_path="../data/births.csv",
        date_column="Дата рождения",
        surname_column="Фамилия",
        fs_column="FS",
        description="Test data source for births",
        created_by=user
    )
    
    # Verify the data source was created
    retrieved_source = DataSource.objects.get(name="Test Births")
    assert retrieved_source.source_type == "births"
    assert retrieved_source.file_path == "../data/births.csv"
    
    print("DataSource test passed!")
    return data_source

def test_summary_statistics(data_source):
    """Test SummaryStatistics model."""
    print("Testing SummaryStatistics model...")
    
    # Create test summary statistics
    stats = SummaryStatistics.objects.create(
        data_source=data_source,
        total_records=1000,
        missing_values=50,
        unique_years=10,
        records_in_fs=800,
        unique_surnames=200
    )
    
    # Add additional data
    additional_data = {
        "average_records_per_year": 100,
        "most_common_year": 1900,
        "most_common_year_count": 150
    }
    stats.set_additional_data(additional_data)
    stats.save()
    
    # Verify the statistics were created and additional data works
    retrieved_stats = SummaryStatistics.objects.get(id=stats.id)
    assert retrieved_stats.total_records == 1000
    assert retrieved_stats.records_in_fs == 800
    
    retrieved_additional_data = retrieved_stats.get_additional_data()
    assert retrieved_additional_data["average_records_per_year"] == 100
    assert retrieved_additional_data["most_common_year"] == 1900
    
    print("SummaryStatistics test passed!")

def test_yearly_comparison(data_source):
    """Test YearlyComparison model."""
    print("Testing YearlyComparison model...")
    
    # Create test yearly comparison data for multiple years
    years = [1900, 1901, 1902, 1903, 1904]
    for year in years:
        YearlyComparison.objects.create(
            data_source=data_source,
            year=year,
            total_records=100 + year - 1900,  # 100, 101, 102, etc.
            records_with_condition=80 + year - 1900,  # 80, 81, 82, etc.
            condition_name="in_fs"
        )
    
    # Verify the data was created
    comparisons = YearlyComparison.objects.filter(
        data_source=data_source
    ).order_by('year')
    
    assert comparisons.count() == 5
    assert comparisons[0].year == 1900
    assert comparisons[0].total_records == 100
    assert comparisons[0].records_with_condition == 80
    
    print("YearlyComparison test passed!")

def test_value_counts(data_source):
    """Test ValueCounts model."""
    print("Testing ValueCounts model...")
    
    # Create test value counts for surnames
    surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown"]
    for i, surname in enumerate(surnames):
        ValueCounts.objects.create(
            data_source=data_source,
            column_name="normalized_surname",
            value=surname,
            count=100 - i * 10  # 100, 90, 80, etc.
        )
    
    # Verify the data was created
    counts = ValueCounts.objects.filter(
        data_source=data_source,
        column_name="normalized_surname"
    ).order_by('-count')
    
    assert counts.count() == 5
    assert counts[0].value == "Smith"
    assert counts[0].count == 100
    assert counts[4].value == "Brown"
    assert counts[4].count == 60
    
    print("ValueCounts test passed!")

def test_visualization(data_source):
    """Test Visualization model."""
    print("Testing Visualization model...")
    
    # Get the test user
    user = User.objects.get(username="testuser")
    
    # Create test visualization
    viz = Visualization.objects.create(
        title="Surname Distribution",
        description="Distribution of surnames in the births dataset",
        visualization_type="pie",
        data_source=data_source,
        created_by=user
    )
    
    # Add configuration
    config = {
        "width": 800,
        "height": 600,
        "colors": ["#ff0000", "#00ff00", "#0000ff"],
        "show_legend": True,
        "legend_position": "right"
    }
    viz.set_config(config)
    
    # Add image data (just a placeholder for testing)
    viz.image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    viz.save()
    
    # Verify the visualization was created and config works
    retrieved_viz = Visualization.objects.get(id=viz.id)
    assert retrieved_viz.title == "Surname Distribution"
    assert retrieved_viz.visualization_type == "pie"
    
    retrieved_config = retrieved_viz.get_config()
    assert retrieved_config["width"] == 800
    assert retrieved_config["colors"][0] == "#ff0000"
    
    print("Visualization test passed!")

def main():
    """Run all model tests."""
    print("Starting model tests...")
    
    try:
        test_user_profile()
        data_source = test_data_source()
        test_summary_statistics(data_source)
        test_yearly_comparison(data_source)
        test_value_counts(data_source)
        test_visualization(data_source)
        
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()