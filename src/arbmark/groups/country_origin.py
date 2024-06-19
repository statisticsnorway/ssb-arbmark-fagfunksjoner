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


def landbakgrunn_grp(landbakgrunn: PdSeriesStr, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of country origins from 3 generations into world regions.

    Parameters:
        landbakgrunn: A pandas Series containing the country origins.
        display: If 'label', returns group labels; if 'number', returns keys;
                       if 'arblonn', returns specific labels for ARBLONN;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original country origins are replaced by group labels or keys.
    """
    # Convert Series to Numpy array
    landbakgrunn_np = pd.to_numeric(landbakgrunn).to_numpy()

    # Define the conditions for each group
    conditions = [
        np.logical_and(landbakgrunn_np >= 0, landbakgrunn_np <= 106),
        np.isin(
            landbakgrunn_np,
            [
                112,
                114,
                117,
                118,
                119,
                121,
                123,
                126,
                127,
                128,
                129,
                130,
                132,
                134,
                137,
                139,
                141,
                144,
                151,
                153,
                154,
                162,
                163,
                164,
                194,
                196,
                199,
                500,
            ],
        ),
        np.isin(
            landbakgrunn_np,
            [113, 115, 122, 124, 131, 133, 136, 142, 146, 152, 157, 158],
        ),
        np.isin(
            landbakgrunn_np,
            [111, 120, 125, 135, 138, 140, 148, 155, 156, 159, 160, 161, 195],
        ),
        np.logical_or(
            np.isin(landbakgrunn_np, [612, 684]),
            np.logical_and(landbakgrunn_np >= 802, landbakgrunn_np <= 899),
        ),
        np.logical_or.reduce(
            [
                landbakgrunn_np == 143,
                np.logical_and(landbakgrunn_np >= 404, landbakgrunn_np <= 496),
                np.logical_and(landbakgrunn_np >= 502, landbakgrunn_np <= 599),
            ]
        ),
        np.logical_and(landbakgrunn_np >= 203, landbakgrunn_np <= 399),
        np.logical_or.reduce(
            [
                np.logical_and(landbakgrunn_np >= 601, landbakgrunn_np <= 608),
                np.logical_and(landbakgrunn_np >= 613, landbakgrunn_np <= 681),
                np.logical_and(landbakgrunn_np >= 685, landbakgrunn_np <= 799),
            ]
        ),
    ]

    groups = {
        "00": "Norden",
        "194": "Vest-Europa ellers",
        "015a": "EU-land i Øst-Europa",
        "100c": "Øst-Europa ellers",
        "694c": "Nord-Amerika, Oseania",
        "400": "Asia",
        "200b": "Afrika",
        "794a": "Sør- og Mellom-Amerika",
    }

    arblonn_groups = ["200", "2", "3", "40", "350", "60", "5", "8"]

    # Determine and apply the selected format based on the labels parameter
    if display == "label":
        results = [str(value) for value in groups.values()]
        default_code = "Ukjent"
    elif display == "number":
        results = [str(key) for key in groups.keys()]
        default_code = "990"
    elif display == "arblonn":
        results = [str(i) for i in arblonn_groups]
        default_code = "980-990"
    else:
        results = [f"{key} {value}" for key, value in groups.items()]
        default_code = "990 Ukjent"
    grouped = np.select(conditions, results, default=default_code)
    return grouped
