from datetime import datetime
from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt
import pandas as pd
from klass import KlassClassification

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


def get_valid_county_codes(year: int | str) -> list[str]:
    """Retrieves valid Norwegian county codes for a given year, excluding the special code "99".

    Parameters:
    year (Union[int, str]): The year for which valid county codes are needed. It can be provided as an integer or a string.

    Returns:
    List[str]: A list of valid county codes as strings, excluding "99".
    """
    year = int(year)
    year = datetime(year, 1, 1).strftime("%Y-%m-%d")

    fylke_klass = KlassClassification(104)

    valid_county_codes = list(fylke_klass.get_codes(from_date=year).data["code"])
    valid_county_codes.remove("99")

    return valid_county_codes


def get_regional_special_codes(year: int | str) -> list[str]:
    """Retrieves regional special codes (e.g., Svalbard, Jan Mayen) for a specified year.

    Parameters:
    year (Union[int, str]): The year for which regional special codes are needed. It can be provided as an integer or a string.

    Returns:
    List[str]: A list of regional special codes as strings.
    """
    year = int(year)
    year = datetime(year, 1, 1).strftime("%Y-%m-%d")

    reg_klass = KlassClassification(4)
    return list(reg_klass.get_codes(from_date=year).data["code"])


def classify_mainland_not_mainland(
    municipality_no: PdSeriesStr, year: int | str
) -> NpArrayStr:
    """Classifies municipalities based on whether they belong to mainland Norway, not mainland Norway, or are unspecified.

    Parameters:
    municipality_no: A pandas Series containing municipality numbers.
    year (Union[int, str]): The year for which the classification is needed. It can be provided as an integer or a string.

    Returns:
    An array containing the classification for each municipality number.
      ("FNorge" for mainland, "IFNorge" for not mainland, "Uoppgitt" for unspecified).
    """
    year = int(year)
    valid_county_codes = get_valid_county_codes(year)
    regional_special_codes = get_regional_special_codes(year)

    return np.where(
        np.isin(municipality_no.str[:2], valid_county_codes),
        "FNorge",
        np.where(
            np.isin(municipality_no.str[:2], regional_special_codes),
            "IFNorge",
            "Uoppgitt",
        ),
    )


def classify_county_not_mainland(
    municipality_no: PdSeriesStr, year: int | str, detailed=True
) -> NpArrayStr:
    """Classifies municipality numbers based on valid mainland or non-mainland county codes.
    Optionally provides specific non-mainland codes if detailed = True.

    Parameters:
    municipality_no: A pandas Series containing municipality numbers.
    year (Union[int, str]): The year for which the classification is needed. It can be provided as an integer or a string.
    detailed (bool): If True, returns specific non-mainland codes. If False, non-mainland is classified as "99g".

    Returns:
    An array with classified county numbers or fallback codes.
      Detailed mode uses specific non-mainland codes ("21", "22", etc.),
      while simplified mode returns "99g" for special regional codes or "99" as the default.
    """
    year = int(year)
    valid_county_codes = get_valid_county_codes(year)
    regional_special_codes = get_regional_special_codes(year)
    county_no = municipality_no.str[:2]

    if detailed:
        # county_no is valid and mainland -> county_no
        # county_no is in list of special_regional_codes from klass -> keep special regional code
        # default: "99"
        selected_not_mainland_codes = ["21", "22", "23", "24"]

        return np.where(
            np.isin(county_no, valid_county_codes),
            county_no,
            np.where(np.isin(county_no, selected_not_mainland_codes), county_no, "99"),
        )

    else:
        # county_no is valid and mainland -> county_no
        # county_no is in list of special_regional_codes from klass -> "99g"
        # default: "99"
        return np.where(
            np.isin(county_no, valid_county_codes),
            county_no,
            np.where(np.isin(county_no, regional_special_codes), "99g", "99"),
        )
