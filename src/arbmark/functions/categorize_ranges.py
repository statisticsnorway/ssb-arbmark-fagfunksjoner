from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    PdSeriesStr = pd.Series[str]  # type: ignore[misc]
else:
    PdSeriesStr = pd.Series


def categorize_ranges(
    obj: PdSeriesStr, format_name: str, format_dict: dict
) -> PdSeriesStr:
    """Categorize a pandas Series based on predefined ranges specified in a dictionary.

    Parameters:
    obj: The pandas Series to be categorized.
    format_name (str): The key name in the format_dict that contains the range definitions.
    format_dict (dict): A dictionary containing the range definitions.
                        The keys should be format names, and the values should be dictionaries where:
                        - keys are string representations of integer cut-off points,
                        - values are the corresponding categories.

    Returns:
        A pandas Series with the same index as obj, where each value is categorized
        according to the ranges defined in format_dict[format_name]. NaNs are replaced with None.

    Raises:
    ValueError: If format_name is not in format_dict.
                If there are non-digit keys in the format_dict[format_name].
    """
    try:
        # Access the format dictionary for the specified format_name
        format_dict = format_dict[format_name]
    except KeyError:
        # Raise an error if the specified format_name is not found
        raise ValueError(f"No format with name {format_name} within given dictionary")

    # Ensure all keys in the format dictionary are digits
    if not all(key.isdigit() for key in format_dict):
        raise ValueError("Non-digits in dictionary keys. Fix your JSON-file")

    # Sort the dictionary by its integer keys
    sorted_dict = {
        int(k): v for k, v in sorted(format_dict.items(), key=lambda item: int(item[0]))
    }

    # Define bins for categorization, appending infinity to cover all ranges
    bins: list[Union[int, float]] = list(sorted_dict.keys())
    bins.append(np.inf)

    # Extract the labels for the bins
    labels = list(sorted_dict.values())

    # Categorize the Series based on the bins and labels
    categories = pd.cut(
        obj.astype(int), bins=bins, labels=labels, right=False, ordered=False
    )

    # Convert the resulting categories to object dtype and replace NaNs with None
    return categories.astype("object").where(categories.notna(), None)
