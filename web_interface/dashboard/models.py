from django.db import models
from django.contrib.auth.models import User
import json
from datetime import datetime


class DataSource(models.Model):
    """
    Model representing a data source (births, marriages, deaths).
    Stores metadata about the data source and its file.
    """
    SOURCE_TYPES = [
        ('births', 'Births'),
        ('marriages', 'Marriages'),
        ('deaths', 'Deaths'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_path = models.CharField(max_length=255)
    date_column = models.CharField(max_length=100)
    surname_column = models.CharField(max_length=100)
    fs_column = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='data_sources')
    
    def __str__(self):
        return f"{self.name} ({self.source_type})"
    
    class Meta:
        verbose_name = "Data Source"
        verbose_name_plural = "Data Sources"


class SummaryStatistics(models.Model):
    """
    Model representing summary statistics for a data source.
    Maps to the summary_statistics table in the existing database.
    """
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='summary_statistics')
    timestamp = models.DateTimeField(default=datetime.now)
    total_records = models.IntegerField()
    missing_values = models.IntegerField()
    unique_years = models.IntegerField()
    records_in_fs = models.IntegerField()
    unique_surnames = models.IntegerField()
    additional_data = models.TextField(blank=True, null=True)
    
    def set_additional_data(self, data_dict):
        """Store additional data as JSON string"""
        self.additional_data = json.dumps(data_dict)
    
    def get_additional_data(self):
        """Retrieve additional data as Python dictionary"""
        if self.additional_data:
            return json.loads(self.additional_data)
        return {}
    
    def __str__(self):
        return f"Statistics for {self.data_source.name} at {self.timestamp}"
    
    class Meta:
        verbose_name = "Summary Statistics"
        verbose_name_plural = "Summary Statistics"
        ordering = ['-timestamp']


class YearlyComparison(models.Model):
    """
    Model representing yearly comparison data.
    Maps to the yearly_comparison table in the existing database.
    """
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='yearly_comparisons')
    timestamp = models.DateTimeField(default=datetime.now)
    year = models.IntegerField()
    total_records = models.IntegerField()
    records_with_condition = models.IntegerField()
    condition_name = models.CharField(max_length=50, default='in_fs')
    
    def __str__(self):
        return f"{self.data_source.name} - {self.year} ({self.condition_name})"
    
    class Meta:
        verbose_name = "Yearly Comparison"
        verbose_name_plural = "Yearly Comparisons"
        ordering = ['-timestamp', 'year']
        unique_together = ['data_source', 'year', 'timestamp', 'condition_name']


class ValueCounts(models.Model):
    """
    Model representing value counts for a column.
    Maps to the value_counts table in the existing database.
    """
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='value_counts')
    timestamp = models.DateTimeField(default=datetime.now)
    column_name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    count = models.IntegerField()
    
    def __str__(self):
        return f"{self.column_name}: {self.value} ({self.count})"
    
    class Meta:
        verbose_name = "Value Counts"
        verbose_name_plural = "Value Counts"
        ordering = ['-timestamp', '-count']
        unique_together = ['data_source', 'column_name', 'value', 'timestamp']


class Visualization(models.Model):
    """
    Model representing a saved visualization.
    """
    VISUALIZATION_TYPES = [
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
        ('scatter', 'Scatter Plot'),
        ('histogram', 'Histogram'),
        ('heatmap', 'Heatmap'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visualization_type = models.CharField(max_length=20, choices=VISUALIZATION_TYPES)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='visualizations')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visualizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Configuration for the visualization
    config = models.TextField(blank=True, null=True)
    
    # Image file or data URL of the visualization
    image_data = models.TextField(blank=True, null=True)
    
    def set_config(self, config_dict):
        """Store configuration as JSON string"""
        self.config = json.dumps(config_dict)
    
    def get_config(self):
        """Retrieve configuration as Python dictionary"""
        if self.config:
            return json.loads(self.config)
        return {}
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Visualization"
        verbose_name_plural = "Visualizations"
        ordering = ['-created_at']