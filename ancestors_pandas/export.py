"""
Data export module for AncestorsPandas.

This module provides functions for exporting data to various formats (CSV, JSON, Excel, etc.).
"""

import pandas as pd
from typing import Optional, Dict, Any, Union, List
import json
import csv
import yaml
import xml.dom.minidom
import xml.etree.ElementTree as ET


def export_to_csv(
    data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    index: bool = False,
    **kwargs
) -> None:
    """
    Export data to a CSV file.

    Parameters:
    -----------
    data : Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a pandas DataFrame, a dictionary, or a list of dictionaries.
    output_path : str
        Path to save the CSV file.
    index : bool, optional
        Whether to include the index in the CSV file. Default is False.
    **kwargs : dict
        Additional keyword arguments to pass to pandas.DataFrame.to_csv() or csv.writer.

    Raises:
    -------
    TypeError
        If data is not a pandas DataFrame, dictionary, or list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(output_path, index=index, **kwargs)
        elif isinstance(data, dict):
            # Convert dictionary to DataFrame
            df = pd.DataFrame.from_dict(data, orient='index')
            df.to_csv(output_path, index=index, **kwargs)
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=index, **kwargs)
        else:
            raise TypeError(
                "Data must be a pandas DataFrame, a dictionary, or a list of dictionaries"
            )
    except Exception as e:
        raise IOError(f"Error exporting to CSV: {str(e)}")


def export_to_json(
    data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    orient: str = 'records',
    indent: int = 4,
    **kwargs
) -> None:
    """
    Export data to a JSON file.

    Parameters:
    -----------
    data : Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a pandas DataFrame, a dictionary, or a list of dictionaries.
    output_path : str
        Path to save the JSON file.
    orient : str, optional
        The format of the JSON string if data is a DataFrame. Default is 'records'.
    indent : int, optional
        Number of spaces for indentation in the JSON file. Default is 4.
    **kwargs : dict
        Additional keyword arguments to pass to pandas.DataFrame.to_json() or json.dump().

    Raises:
    -------
    TypeError
        If data is not a pandas DataFrame, dictionary, or list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    try:
        if isinstance(data, pd.DataFrame):
            data.to_json(output_path, orient=orient, indent=indent, **kwargs)
        elif isinstance(data, (dict, list)):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, **kwargs)
        else:
            raise TypeError(
                "Data must be a pandas DataFrame, a dictionary, or a list of dictionaries"
            )
    except Exception as e:
        raise IOError(f"Error exporting to JSON: {str(e)}")


def export_to_excel(
    data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    sheet_name: str = 'Sheet1',
    index: bool = False,
    **kwargs
) -> None:
    """
    Export data to an Excel file.

    Parameters:
    -----------
    data : Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a pandas DataFrame, a dictionary, or a list of dictionaries.
    output_path : str
        Path to save the Excel file.
    sheet_name : str, optional
        Name of the sheet in the Excel file. Default is 'Sheet1'.
    index : bool, optional
        Whether to include the index in the Excel file. Default is False.
    **kwargs : dict
        Additional keyword arguments to pass to pandas.DataFrame.to_excel().

    Raises:
    -------
    TypeError
        If data is not a pandas DataFrame, dictionary, or list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    try:
        if isinstance(data, pd.DataFrame):
            data.to_excel(output_path, sheet_name=sheet_name, index=index, **kwargs)
        elif isinstance(data, dict):
            # Convert dictionary to DataFrame
            df = pd.DataFrame.from_dict(data, orient='index')
            df.to_excel(output_path, sheet_name=sheet_name, index=index, **kwargs)
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(data)
            df.to_excel(output_path, sheet_name=sheet_name, index=index, **kwargs)
        else:
            raise TypeError(
                "Data must be a pandas DataFrame, a dictionary, or a list of dictionaries"
            )
    except Exception as e:
        raise IOError(f"Error exporting to Excel: {str(e)}")


def export_to_yaml(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    **kwargs
) -> None:
    """
    Export data to a YAML file.

    Parameters:
    -----------
    data : Union[Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a dictionary or a list of dictionaries.
    output_path : str
        Path to save the YAML file.
    **kwargs : dict
        Additional keyword arguments to pass to yaml.dump().

    Raises:
    -------
    TypeError
        If data is not a dictionary or a list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    try:
        if isinstance(data, pd.DataFrame):
            # Convert DataFrame to dictionary
            data_dict = data.to_dict(orient='records')
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data_dict, f, **kwargs)
        elif isinstance(data, (dict, list)):
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, **kwargs)
        else:
            raise TypeError(
                "Data must be a pandas DataFrame, a dictionary, or a list of dictionaries"
            )
    except Exception as e:
        raise IOError(f"Error exporting to YAML: {str(e)}")


def export_to_xml(
    data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    root_element: str = 'data',
    item_element: str = 'item',
    pretty: bool = True
) -> None:
    """
    Export data to an XML file.

    Parameters:
    -----------
    data : Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a pandas DataFrame, a dictionary, or a list of dictionaries.
    output_path : str
        Path to save the XML file.
    root_element : str, optional
        Name of the root element in the XML file. Default is 'data'.
    item_element : str, optional
        Name of the item elements in the XML file. Default is 'item'.
    pretty : bool, optional
        Whether to format the XML with indentation. Default is True.

    Raises:
    -------
    TypeError
        If data is not a pandas DataFrame, dictionary, or list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    try:
        root = ET.Element(root_element)
        
        if isinstance(data, pd.DataFrame):
            # Convert DataFrame to list of dictionaries
            data_list = data.to_dict(orient='records')
            for item in data_list:
                item_elem = ET.SubElement(root, item_element)
                for key, value in item.items():
                    if pd.isna(value):
                        continue
                    elem = ET.SubElement(item_elem, str(key))
                    elem.text = str(value)
        elif isinstance(data, dict):
            for key, value in data.items():
                elem = ET.SubElement(root, str(key))
                if isinstance(value, (dict, list)):
                    elem.text = str(value)  # Simplified handling for nested structures
                else:
                    elem.text = str(value)
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            for item in data:
                item_elem = ET.SubElement(root, item_element)
                for key, value in item.items():
                    elem = ET.SubElement(item_elem, str(key))
                    if isinstance(value, (dict, list)):
                        elem.text = str(value)  # Simplified handling for nested structures
                    else:
                        elem.text = str(value)
        else:
            raise TypeError(
                "Data must be a pandas DataFrame, a dictionary, or a list of dictionaries"
            )
        
        # Convert to string and format if needed
        xml_str = ET.tostring(root, encoding='utf-8')
        if pretty:
            dom = xml.dom.minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="  ")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
        else:
            with open(output_path, 'wb') as f:
                f.write(xml_str)
    except Exception as e:
        raise IOError(f"Error exporting to XML: {str(e)}")


def export_data(
    data: Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]],
    output_path: str,
    format: str = 'csv',
    **kwargs
) -> None:
    """
    Export data to a file in the specified format.

    Parameters:
    -----------
    data : Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
        Data to export. Can be a pandas DataFrame, a dictionary, or a list of dictionaries.
    output_path : str
        Path to save the file.
    format : str, optional
        Format to export the data to. Default is 'csv'.
        Supported formats: 'csv', 'json', 'excel', 'yaml', 'xml'.
    **kwargs : dict
        Additional keyword arguments to pass to the specific export function.

    Raises:
    -------
    ValueError
        If the format is not supported.
    TypeError
        If data is not a pandas DataFrame, dictionary, or list of dictionaries.
    IOError
        If there's an error writing to the file.
    """
    format = format.lower()
    
    if format == 'csv':
        export_to_csv(data, output_path, **kwargs)
    elif format == 'json':
        export_to_json(data, output_path, **kwargs)
    elif format == 'excel':
        export_to_excel(data, output_path, **kwargs)
    elif format == 'yaml':
        export_to_yaml(data, output_path, **kwargs)
    elif format == 'xml':
        export_to_xml(data, output_path, **kwargs)
    else:
        raise ValueError(
            f"Unsupported format: {format}. Supported formats: 'csv', 'json', 'excel', 'yaml', 'xml'"
        )