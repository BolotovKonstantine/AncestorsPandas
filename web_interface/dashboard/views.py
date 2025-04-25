from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from ancestors_pandas.database import stats_retriever, db
from django.conf import settings


def convert_binary_to_int(df, column_name):
    """
    Convert binary data in a DataFrame column to integers.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the column to convert
    column_name : str
        Name of the column to convert

    Returns:
    --------
    pd.DataFrame
        DataFrame with the column converted to integers
    """
    if not df.empty and column_name in df.columns and df[column_name].dtype == 'object':
        df[column_name] = df[column_name].apply(
            lambda x: int.from_bytes(x, byteorder='little') if isinstance(x, bytes) else x
        )
    return df


@login_required
def dashboard(request):
    """
    Main dashboard view showing summary statistics.
    """
    # Initialize the database if it doesn't exist
    try:
        db.init_database(settings.DATABASES['default']['NAME'])
    except Exception as e:
        # Log the error but continue
        print(f"Error initializing database: {str(e)}")

    # Get summary statistics from the database
    try:
        summary_stats = stats_retriever.export_summary_statistics_to_dataframe(
            db_path=settings.DATABASES['default']['NAME']
        )
    except Exception as e:
        # Handle the error gracefully
        print(f"Error retrieving summary statistics: {str(e)}")
        summary_stats = pd.DataFrame()

    # Convert binary data to integers if needed
    summary_stats = convert_binary_to_int(summary_stats, 'records_in_fs')
    summary_stats = convert_binary_to_int(summary_stats, 'total_records')

    # Calculate percentage in FS if both fields exist
    if not summary_stats.empty and 'records_in_fs' in summary_stats.columns and 'total_records' in summary_stats.columns:
        summary_stats['percentage_in_fs'] = (summary_stats['records_in_fs'] / summary_stats['total_records']) * 100

    context = {
        'summary_stats': summary_stats.to_dict('records') if not summary_stats.empty else [],
        'page_title': 'Dashboard',
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def visualizations(request):
    """
    View for displaying visualizations.
    """
    context = {
        'page_title': 'Visualizations',
    }

    return render(request, 'dashboard/visualizations.html', context)


@login_required
def data_view(request):
    """
    View for displaying and filtering data.
    """
    # Get data source from request parameters
    data_source = request.GET.get('source', 'births')

    # Initialize the database if it doesn't exist
    try:
        db.init_database(settings.DATABASES['default']['NAME'])
    except Exception as e:
        # Log the error but continue
        print(f"Error initializing database: {str(e)}")

    # Get yearly comparison data
    try:
        yearly_data = stats_retriever.export_yearly_comparison_to_dataframe(
            data_source=data_source,
            db_path=settings.DATABASES['default']['NAME']
        )
    except Exception as e:
        # Handle the error gracefully
        print(f"Error retrieving yearly comparison data: {str(e)}")
        yearly_data = pd.DataFrame()

    # Get value counts data
    try:
        value_counts = stats_retriever.export_value_counts_to_dataframe(
            column_name='normalized_surname',
            data_source=data_source,
            db_path=settings.DATABASES['default']['NAME']
        )
    except Exception as e:
        # Handle the error gracefully
        print(f"Error retrieving value counts data: {str(e)}")
        value_counts = pd.DataFrame()

    # Convert binary data to integers if needed in yearly_data
    yearly_data = convert_binary_to_int(yearly_data, 'records_with_condition')
    yearly_data = convert_binary_to_int(yearly_data, 'total_records')

    # Convert binary data to integers if needed in value_counts
    value_counts = convert_binary_to_int(value_counts, 'count')

    context = {
        'page_title': 'Data View',
        'data_source': data_source,
        'yearly_data': yearly_data.to_dict('records') if not yearly_data.empty else [],
        'value_counts': value_counts.to_dict('records') if not value_counts.empty else [],
    }

    return render(request, 'dashboard/data_view.html', context)
