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
    NpArrayStr = npt.NDArray[np.dtype[str]]  # type: ignore[misc]
else:
    PdSeriesInt = pd.Series
    PdSeriesStr = pd.Series
    NpArrayInt = npt.NDArray
    NpArrayStr = npt.NDArray


def virk_str_8grp(ansatte: PdSeriesInt, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of employee counts into predefined groups.

    Parameters:
        ansatte: A pandas Series containing the employee counts.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original employee counts are replaced by group labels or keys.
    """
    # Define the conditions for each group
    conditions = [
        (ansatte == 0).to_numpy(),  # No employees
        np.logical_and(ansatte >= 1, ansatte <= 4),  # 1-4 employees
        np.logical_and(ansatte >= 5, ansatte <= 9),  # 5-9 employees
        np.logical_and(ansatte >= 10, ansatte <= 19),  # 10-19 employees
        np.logical_and(ansatte >= 20, ansatte <= 49),  # 20-49 employees
        np.logical_and(ansatte >= 50, ansatte <= 99),  # 50-99 employees
        np.logical_and(ansatte >= 100, ansatte <= 249),  # 100-249 employees
        (ansatte >= 250).to_numpy(),  # 250 employees or more
    ]

    # Define the group labels with string keys
    groups = {
        "1": "Ingen ansatte",
        "2": "1-4 ansatte",
        "3": "5-9 ansatte",
        "4": "10-19 ansatte",
        "5": "20-49 ansatte",
        "6": "50-99 ansatte",
        "7": "100-249 ansatte",
        "8": "250 ansatte og over",
    }

    # Determine and apply the selected format based on the labels parameter
    if display == "label":
        results = [str(value) for value in groups.values()]
        default_code = "Uoppgitt"
    elif display == "number":
        results = [str(key) for key in groups.keys()]
        default_code = "99"
    else:
        results = [f"{key} {value}" for key, value in groups.items()]
        default_code = "99 Uoppgitt"
    grouped = np.select(conditions, results, default=default_code)
    return grouped
