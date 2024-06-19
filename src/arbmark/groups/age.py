# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesInt = pd.Series[int]  # type: ignore[misc]
    PdSeriesStr = pd.Series[str]  # type: ignore[misc]
    NpArrayInt = npt.NDArray[np.int_]  # type: ignore[misc]
    NpArrayStr = npt.NDArray[np.unicode_]  # type: ignore[misc]
else:
    PdSeriesInt = pd.Series
    PdSeriesStr = pd.Series
    NpArrayInt = npt.NDArray
    NpArrayStr = npt.NDArray


def alder_grp(alder: PdSeriesInt, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of person ages into predefined groups used in SYKEFR.

    Parameters:
        alder: A pandas Series containing the person ages.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original person ages are replaced by group labels, keys, or a combination.
    """
    # Define the conditions for each group
    conditions = [
        np.logical_and(alder >= 16, alder <= 19),  # 16-19 år
        np.logical_and(alder >= 20, alder <= 24),  # 20-24 år
        np.logical_and(alder >= 25, alder <= 29),  # 25-29 år
        np.logical_and(alder >= 30, alder <= 34),  # 30-34 år
        np.logical_and(alder >= 35, alder <= 39),  # 35-39 år
        np.logical_and(alder >= 40, alder <= 44),  # 40-44 år
        np.logical_and(alder >= 45, alder <= 49),  # 45-49 år
        np.logical_and(alder >= 50, alder <= 54),  # 50-54 år
        np.logical_and(alder >= 55, alder <= 59),  # 55-59 år
        np.logical_and(alder >= 60, alder <= 64),  # 60-64 år
        np.logical_or(alder == 65, alder == 66),  # 65-66 år
        (alder == 67).to_numpy(),  # 67 år
        (alder == 68).to_numpy(),  # 68 år
        (alder == 69).to_numpy(),  # 69 år
    ]

    # Define the group labels with string keys
    groups = {
        "1": "16-19 år",
        "2": "20-24 år",
        "3": "25-29 år",
        "4": "30-34 år",
        "5": "35-39 år",
        "6": "40-44 år",
        "7": "45-49 år",
        "8": "50-54 år",
        "9": "55-59 år",
        "10": "60-64 år",
        "11": "65-66 år",
        "12": "67 år",
        "13": "68 år",
        "14": "69 år",
    }

    # Determine the format of the results based on the display parameter
    if display == "label":
        results = [str(value) for value in groups.values()]
    elif display == "number":
        results = [str(key) for key in groups.keys()]
    else:
        results = [f"{key} {value}" for key, value in groups.items()]

    # Apply the selected format to the series
    return np.select(conditions, results, default=".")


def alder_5grp(alder: PdSeriesInt, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of person ages into predefined groups used in ARBLONN.

    Parameters:
        alder: A pandas Series containing the person ages.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original person ages are replaced by group labels, keys, or a combination.
    """
    # Define the conditions for each group
    conditions = [
        np.logical_and(alder >= 0, alder <= 24),  # Under 25 år
        np.logical_and(alder >= 25, alder <= 39),  # 25-39 år
        np.logical_and(alder >= 40, alder <= 54),  # 40-54 år
        np.logical_and(alder >= 55, alder <= 66),  # 55-66 år
        (alder >= 67).to_numpy(),  # 67 år eller eldre
    ]

    # Define the group labels with string keys
    groups = {
        "1": "-24",
        "2": "25-39",
        "3": "40-54",
        "4": "55-66",
        "5": "67+",
    }

    # Determine the format of the results based on the display parameter
    if display == "label":
        results = [str(value) for value in groups.values()]
    elif display == "number":
        results = [str(key) for key in groups.keys()]
    else:
        results = [f"{key} {value}" for key, value in groups.items()]

    # Apply the selected format to the series
    return np.select(conditions, results, default="")
