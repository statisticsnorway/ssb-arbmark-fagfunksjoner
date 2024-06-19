# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesStr = pd.Series[str]  # type: ignore[misc]
    NpArrayStr = npt.NDArray[np.str_]  # type: ignore[misc]
else:
    PdSeriesStr = pd.Series
    NpArrayStr = npt.NDArray


def turnuskoder(arb_tid_ordning: PdSeriesStr) -> NpArrayStr:
    """Assigns codes based on work schedule categories.

    This function takes a pandas Series containing work schedule categories and assigns
    corresponding codes based on specific conditions. The conditions are as follows:
    - '20' is assigned to categories ['dogn355', 'helkont336', 'offshore336', 'skift365', 'andre_skift']
    - '25' is assigned to the 'ikke_skift' category
    - '99' is assigned to values ['-2', '', '-1'] or NaN values in the series
    Any value that doesn't match these conditions will be assigned an empty string.

    Parameters:
    arb_tid_ordning: A pandas Series object containing strings that represent
                                 different work schedule categories.

    Returns:
    An array of strings, where each string is a code corresponding to the work schedule
                category in `arb_tid_ordning`.

    Example:
    >>> arb_tid_ordning = pd.Series(['dogn355', 'helkont336', 'ikke_skift', '-2', 'offshore336', ''])
    >>> turnuskoder(arb_tid_ordning)
    array(['20', '20', '25', '99', '20', '99'], dtype='<U2')
    """
    # Define the conditions
    conditions = [
        arb_tid_ordning.isin(
            ["dogn355", "helkont336", "offshore336", "skift365", "andre_skift"]
        ),
        arb_tid_ordning == "ikke_skift",
        arb_tid_ordning.isin(["-2", "", "-1"]) | arb_tid_ordning.isna(),
    ]

    # Define the corresponding values for each condition
    choices = ["20", "25", "99"]

    return np.select(conditions, choices, default="")
