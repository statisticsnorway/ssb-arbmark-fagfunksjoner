from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt
import pandas as pd

if TYPE_CHECKING:
    PdSeriesInt = pd.Series[int]  # type: ignore[misc]
    PdSeriesStr = pd.Series[str]  # type: ignore[misc]
    NpArrayInt = npt.NDArray[np.int_]  # type: ignore[misc]
    NpArrayStr = npt.NDArray[np.str_]  # type: ignore[misc]
else:
    PdSeriesInt = pd.Series
    PdSeriesStr = pd.Series
    NpArrayInt = npt.NDArray
    NpArrayStr = npt.NDArray


def nyk08yrkeregsys1(occupation_code: PdSeriesStr) -> NpArrayStr:
    """Classifies occupation codes based on the first few characters.

    Parameters:
        occupation_code: A pandas Series containing occupation codes. Occupation code must contain at least two digits.

    Returns:
        An array with classified occupation codes. Codes starting with "01", "02", or "03" are grouped under "3_01-03".
        Other valid codes are categorized based on their first digit, with invalid codes defaulting to "0b".
    """
    # Define the valid occupation codes from "1" to "9"
    valid_occupation_codes = [str(i) for i in range(1, 10)]

    # First check if the first two digits are "01", "02", or "03" or first digit is "3" and group them under "3_01-03"
    condition_1 = (occupation_code.str[:2].isin(["01", "02", "03"])) | (
        occupation_code.str.startswith("3")
    )

    # Next, check if the first digit is between "1" and "9", and classify it as that digit
    condition_2 = occupation_code.str[:1].isin(valid_occupation_codes)

    # If neither condition is met, assign the code "0b"
    return np.select(
        [condition_1, condition_2], ["3_01-03", occupation_code.str[:1]], default="0b"
    )
