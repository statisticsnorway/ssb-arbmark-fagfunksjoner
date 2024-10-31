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


def sektor2_grp(sektor: PdSeriesStr, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of sectors into predefined groups.

    Parameters:
        sektor: A pandas Series containing the sector codes.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original sector is replaced by group labels or keys.
    """
    # Define the conditions for each group
    conditions = [
        (sektor == "6100").to_numpy(),
        (sektor == "6500").to_numpy(),
        (sektor == "1510").to_numpy(),
        (sektor == "1520").to_numpy(),
    ]

    groups = {
        "110": "Statlig forvaltning",
        "550": "Kommunal forvaltning",
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
