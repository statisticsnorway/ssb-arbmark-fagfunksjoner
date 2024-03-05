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
    NpArrayStr = npt.NDArray[np.str_]  # type: ignore[misc]
else:
    PdSeriesInt = pd.Series
    PdSeriesStr = pd.Series
    NpArrayInt = npt.NDArray
    NpArrayStr = npt.NDArray


def sektor2_grp(
    sektor: PdSeriesStr, undersektor: PdSeriesStr, display: str = "label"
) -> NpArrayStr:
    """Categorize a pandas Series of sectors and subsectors into predefined groups.

    Parameters:
        sektor: A pandas Series containing the sector codes.
        undersektor: A pandas Series containing the subsector codes.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original sector and subsectors are replaced by group labels or keys.
    """
    # Define the conditions for each group
    conditions = [
        (sektor == "6100").to_numpy(),
        np.logical_and(sektor == "6500", undersektor != "007"),
        np.logical_and(sektor == "6500", undersektor == "007"),
        (sektor == "1510").to_numpy(),
        (sektor == "1520").to_numpy(),
    ]

    groups = {
        "110": "Statlig forvaltning",
        "550": "Kommunal forvaltning",
        "510": "Fylkeskommunal forvaltning",
        "660": "Kommunale foretak med ubegrenset ansvar",
        "680": "Kommunalt eide aksjeselskaper m.v.",
    }

    # Determine and apply the selected format based on the labels parameter
    if display == "label":
        results = [str(value) for value in groups.values()]
        default_code = "Uoppgitt"
    elif display == "number":
        results = [str(key) for key in groups.keys()]
        default_code = "999"
    else:
        results = [f"{key} {value}" for key, value in groups.items()]
        default_code = "999 Uoppgitt"
    grouped = np.select(conditions, results, default=default_code)
    return grouped
