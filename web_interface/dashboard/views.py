from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
import os
import io
from ancestors_pandas.database import stats_retriever, db
from ancestors_pandas.data_loading import loader
from ancestors_pandas.processing import normalizations
from django.conf import settings
from .models import DataSource
from django.http import JsonResponse


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


@login_required
def data_sources(request):
    """
    View for listing all data sources.
    """
    data_sources = DataSource.objects.all().order_by('-created_at')

    context = {
        'page_title': 'Data Sources',
        'data_sources': data_sources,
    }

    return render(request, 'dashboard/data_sources.html', context)


@login_required
def data_source_create(request):
    """
    View for creating a new data source.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        source_type = request.POST.get('source_type')
        description = request.POST.get('description')
        date_column = request.POST.get('date_column')
        surname_column = request.POST.get('surname_column')
        fs_column = request.POST.get('fs_column')

        # Handle file upload
        if 'file' in request.FILES:
            file = request.FILES['file']

            # Create a directory for uploaded files if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Save the file
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Create the data source
            data_source = DataSource(
                name=name,
                source_type=source_type,
                file_path=file_path,
                date_column=date_column,
                surname_column=surname_column,
                fs_column=fs_column,
                description=description,
                created_by=request.user
            )
            data_source.save()

            messages.success(request, f'Data source "{name}" created successfully.')
            return redirect('data_sources')
        else:
            messages.error(request, 'No file was uploaded.')

    context = {
        'page_title': 'Create Data Source',
    }

    return render(request, 'dashboard/data_source_form.html', context)


@login_required
def data_source_edit(request, pk):
    """
    View for editing an existing data source.
    """
    data_source = get_object_or_404(DataSource, pk=pk)

    if request.method == 'POST':
        data_source.name = request.POST.get('name')
        data_source.source_type = request.POST.get('source_type')
        data_source.description = request.POST.get('description')
        data_source.date_column = request.POST.get('date_column')
        data_source.surname_column = request.POST.get('surname_column')
        data_source.fs_column = request.POST.get('fs_column')

        # Handle file upload if a new file is provided
        if 'file' in request.FILES:
            file = request.FILES['file']

            # Create a directory for uploaded files if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Delete the old file if it exists
            if os.path.exists(data_source.file_path):
                os.remove(data_source.file_path)

            # Save the new file
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            data_source.file_path = file_path

        data_source.save()
        messages.success(request, f'Data source "{data_source.name}" updated successfully.')
        return redirect('data_sources')

    context = {
        'page_title': 'Edit Data Source',
        'data_source': data_source,
    }

    return render(request, 'dashboard/data_source_form.html', context)


@login_required
def data_source_delete(request, pk):
    """
    View for deleting a data source.
    """
    data_source = get_object_or_404(DataSource, pk=pk)

    if request.method == 'POST':
        # Delete the file if it exists
        if os.path.exists(data_source.file_path):
            os.remove(data_source.file_path)

        data_source.delete()
        messages.success(request, f'Data source "{data_source.name}" deleted successfully.')
        return redirect('data_sources')

    context = {
        'page_title': 'Delete Data Source',
        'data_source': data_source,
    }

    return render(request, 'dashboard/data_source_confirm_delete.html', context)


@login_required
def data_source_preview(request):
    """
    View for previewing a CSV file.
    """
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']

        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file)

            # Get the first 10 rows and the column names
            preview_data = df.head(10).to_dict('records')
            columns = df.columns.tolist()

            return JsonResponse({
                'success': True,
                'preview_data': preview_data,
                'columns': columns,
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
            })

    return JsonResponse({
        'success': False,
        'error': 'No file was uploaded.',
    })


@login_required
def data_source_normalize(request, pk):
    """
    View for normalizing data in a data source.
    """
    data_source = get_object_or_404(DataSource, pk=pk)

    if request.method == 'POST':
        column = request.POST.get('column')
        normalization_type = request.POST.get('normalization_type')

        try:
            # Load the data
            df = pd.read_csv(data_source.file_path)

            # Apply normalization
            if normalization_type == 'surname':
                df[f'normalized_{column}'] = df[column].apply(normalizations.normalize_surname)
            elif normalization_type == 'date':
                df[f'normalized_{column}'] = df[column].apply(normalizations.normalize_date)
            elif normalization_type == 'location':
                df[f'normalized_{column}'] = df[column].apply(normalizations.normalize_location)

            # Save the normalized data
            df.to_csv(data_source.file_path, index=False)

            messages.success(request, f'Column "{column}" normalized successfully.')
            return redirect('data_source_edit', pk=pk)
        except Exception as e:
            messages.error(request, f'Error normalizing data: {str(e)}')

    # Load the data to get column names
    try:
        df = pd.read_csv(data_source.file_path)
        columns = df.columns.tolist()
    except Exception as e:
        columns = []
        messages.error(request, f'Error loading data: {str(e)}')

    context = {
        'page_title': 'Normalize Data',
        'data_source': data_source,
        'columns': columns,
    }

    return render(request, 'dashboard/data_source_normalize.html', context)
