import pandas as pd
from fagfunksjoner import logger
from klass import KlassClassification


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
