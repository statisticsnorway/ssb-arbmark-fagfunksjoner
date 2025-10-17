# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd
from fagfunksjoner import logger
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


def koble_landbakgrunn_546(
    df: pd.DataFrame, land_col: str | None = None
) -> pd.DataFrame:
    """Adds `verdensdel` and `landegruppe` columns to a DataFrame using KLASS classification 546.

    This function uses Statistics Norway's KLASS classification **546** (landbakgrunn)
    to map country codes (in `land_col`) to corresponding continent (`verdensdel`)
    and regional group (`landegruppe`) codes. It retrieves level-3 codes from KLASS,
    constructs mapping dictionaries, and adds the resulting columns to the input
    DataFrame.

    Logging messages are emitted to indicate progress and potential issues such as
    missing mappings (NaN values).

    Args:
        df (pd.DataFrame): Input DataFrame containing a column with country codes.
        land_col (str | None): Name of the column in `df` containing country codes.
            Must be provided.

    Returns:
        pd.DataFrame: The input DataFrame with two new columns:
            - ``verdensdel``: Continent group derived from KLASS 546.
            - ``landegruppe``: Two-character prefix of the continent group.

    Raises:
        ValueError: If `land_col` is not provided or is None.

    Logs:
        - INFO: When fetching the classification and creating columns.
        - WARNING: If NaN values are present in either of the new columns.

    Example:
        >>> df = pd.DataFrame({"landkode": ["NOR", "SWE", "USA"]})
        >>> koble_landbakgrunn_546(df, land_col="landkode")
        >>> df.columns
        Index(['landkode', 'verdensdel', 'landegruppe'], dtype='object')
    """
    if not land_col:
        raise ValueError(
            "You need to specify column containing country codes in parameter 'land_col'."
        )
    map_dict = (
        KlassClassification(546)
        .get_codes(select_level="3")
        .data[["code", "parentCode"]]
        .set_index("code")
        .to_dict()["parentCode"]
    )
    logger.info("Henter ut Klass klassifikasjon 546 for landegrupper")
    df["verdensdel"] = df[land_col].map(map_dict)
    logger.info(
        f"Lager gruppert kolonne ('verdensdel') med grupper: {df['verdensdel'].unique()}"
    )
    if df["verdensdel"].isna().sum() > 0:
        logger.warning("NaN-verdiene i 'verdensdel' må du håndtere selv")
    df["landegruppe"] = df["verdensdel"].str[0:2]
    logger.info(
        f"Lager gruppert kolonne ('landegruppe') med grupper: {df['landegruppe'].unique()}"
    )
    if df["landegruppe"].isna().sum() > 0:
        logger.warning("NaN-verdiene i 'landegruppe' må du håndtere selv")
    return df


def koble_landbakgrunn_545(
    df: pd.DataFrame, land_col: str | None = None
) -> pd.DataFrame:
    """Adds `verdensdel` and `landegruppe` columns to a DataFrame using KLASS classification 545.

    This function uses Statistics Norway's KLASS classification **545** (landbakgrunn)
    to map country codes (in `land_col`) to corresponding continent (`verdensdel`)
    and regional group (`landegruppe`) codes. It retrieves level-4 codes from KLASS,
    constructs mapping dictionaries, and adds the resulting columns to the input
    DataFrame.

    The mapping is done by truncating the parent code from KLASS:
      - ``verdensdel``: The first two characters of the parent code.
      - ``landegruppe``: The first three characters of the parent code.

    Logging messages are emitted to indicate progress and potential issues such as
    missing mappings (NaN values).

    Args:
        df (pd.DataFrame): Input DataFrame containing a column with country codes.
        land_col (str | None): Name of the column in `df` containing country codes.
            Must be provided.

    Returns:
        pd.DataFrame: The input DataFrame with two new columns:
            - ``verdensdel``: Continent group (first two chars of parent code).
            - ``landegruppe``: Regional group (first three chars of parent code).

    Raises:
        ValueError: If `land_col` is not provided or is None.

    Logs:
        - INFO: When fetching the classification and creating columns.
        - WARNING: If NaN values are present in either of the new columns.

    Example:
        >>> df = pd.DataFrame({"landkode": ["NOR", "SWE", "USA"]})
        >>> koble_landbakgrunn_545(df, land_col="landkode")
        >>> df.columns
        Index(['landkode', 'verdensdel', 'landegruppe'], dtype='object')
    """
    if not land_col:
        raise ValueError(
            "You need to specify column containing country codes in parameter 'land_col'."
        )
    map_dict = (
        KlassClassification(545)
        .get_codes(select_level="4")
        .data[["code", "parentCode"]]
        .set_index("code")
        .to_dict()["parentCode"]
    )
    logger.info("Henter ut Klass klassifikasjon 545 for landegrupper")
    df["verdensdel"] = df[land_col].map(map_dict).str[:2]
    logger.info(
        f"Lager gruppert kolonne ('verdensdel') med grupper: {df['verdensdel'].unique()}"
    )
    if df["verdensdel"].isna().sum() > 0:
        logger.warning("NaN-verdiene i 'verdensdel' må du håndtere selv")
    df["landegruppe"] = df[land_col].map(map_dict).str[:3]
    logger.info(
        f"Lager gruppert kolonne ('landegruppe') med grupper: {df['landegruppe'].unique()}"
    )
    if df["landegruppe"].isna().sum() > 0:
        logger.warning("NaN-verdiene i 'landegruppe' må du håndtere selv")
    return df
