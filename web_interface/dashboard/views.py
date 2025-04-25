from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from ancestors_pandas.database import stats_retriever, db
from django.conf import settings


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

    context = {
        'page_title': 'Data View',
        'data_source': data_source,
        'yearly_data': yearly_data.to_dict('records') if not yearly_data.empty else [],
        'value_counts': value_counts.to_dict('records') if not value_counts.empty else [],
    }

    return render(request, 'dashboard/data_view.html', context)
