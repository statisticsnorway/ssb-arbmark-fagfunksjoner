import pandas as pd
import numpy as np
import pytest

from arbmark import categorize_ranges


def test_categorize_ranges():
    obj = pd.Series([5, 15, 25, np.nan, 35, 45, 55])

    format_dict = {
        'example_format': {
            '10': 'Low',
            '20': 'Medium',
            '30': 'High'
        }
    }

    expected_output = pd.Series(['Low', 'Medium', 'High', None, 'High', 'High', 'High'], dtype='object')

    output = categorize_ranges(obj, 'example_format', format_dict)
    pd.testing.assert_series_equal(output, expected_output)

def test_invalid_format_name():
    obj = pd.Series([5, 15, 25, 35])

    format_dict = {
        'example_format': {
            '10': 'Low',
            '20': 'Medium',
            '30': 'High'
        }
    }

    with pytest.raises(ValueError, match="No format with name invalid_format within given dictionary"):
        categorize_ranges(obj, 'invalid_format', format_dict)

def test_invalid_keys_in_format_dict():
    obj = pd.Series([5, 15, 25, 35])

    format_dict = {
        'example_format': {
            '10': 'Low',
            'twenty': 'Medium',  # Non-digit key
            '30': 'High'
        }
    }

    with pytest.raises(ValueError, match="Non-digits in dictionary keys. Fix your JSON-file"):
        categorize_ranges(obj, 'example_format', format_dict)

def test_edge_case_values():
    obj = pd.Series([10, 20, 30, 40])

    format_dict = {
        'example_format': {
            '10': 'Low',
            '20': 'Medium',
            '30': 'High'
        }
    }

    expected_output = pd.Series(['Low', 'Medium', 'High', 'High'], dtype='object')

    output = categorize_ranges(obj, 'example_format', format_dict)
    pd.testing.assert_series_equal(output, expected_output)