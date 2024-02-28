"""A collection of useful groups."""

# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd

# Klass for standard classifications
from klass import KlassVariant

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


def nace_sn07_47grp(nace_sn07: PdSeriesStr, display: str = "label") -> NpArrayStr:
    """Categorize a pandas Series of NACE-codes (SN07) into predefined groups.

    Parameters:
        nace_sn07: A pandas Series containing the NACE-codes.
        display: If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        A numpy Array where the original NACE-codes are replaced by group labels or keys.
    """
    # Removes periods in the NACE codes (if any)
    nace = nace_sn07.str.replace(".", "")

    # Substring of NACE codes at length 2 and 3
    nace2 = pd.to_numeric(nace.str[:2]).to_numpy()
    nace3 = pd.to_numeric(nace.str[:3]).to_numpy()

    # Define the conditions for each group
    conditions = [
        np.isin(
            nace2, [1, 2, 3]
        ),  # Jordbruk, skogbruk, fiske; Bergverksdrift og utvinning, utenom olje og gass
        np.logical_or(
            np.isin(nace2, [5, 7, 8]), nace3 == 99
        ),  # Annen utvinning; Bygging av skip og båter; Reparasjon og installasjon av maskiner og utstyr; Uoppgitt utvinning
        np.logical_or(
            nace2 == 6, nace3 == 91
        ),  # Olje- og gassutvinning; Uoppgitt utvinning av petroleum
        np.isin(nace2, [10, 11, 12]),  # Næringsmiddel-,drikkev.,tobakkind.
        np.isin(nace2, [13, 14, 15]),  # Tekstil-,bekledn.-,lærvareind.
        np.isin(nace2, [16, 17]),  # Trelast- og trevareind.
        (nace2 == 18),  # Trykking, grafisk industri
        np.isin(
            nace2, [19, 20, 21]
        ),  # Petrolieum, kull, kjemisk og farmasøytisk industri
        np.isin(nace2, [22, 23]),  # Gummivare-, plast-,mineralproduktind.
        (nace2 == 24),  # Metallindustri
        (nace2 == 25),  # Metallvareindustri
        np.isin(nace2, [26, 27]),  # Data- og elektronisk industri
        (nace2 == 28),  # Maskinindustri
        np.logical_or(
            np.isin(nace2, [29, 33]), np.logical_and(nace3 >= 302, nace3 <= 309)
        ),  # Transportmidelindustri, utenom 30.1; Produksjon av kjøretøy og tilhengere, unntatt motorvogner og motorsykler
        (nace3 == 301),  # Produksjon av skip og båter, inkl. oljeplattformer
        np.isin(nace2, [31, 32]),  # Møbel og annen industri
        (nace2 == 35),  # Elekstrisitet, gass, damp, varmtvann
        np.logical_and(nace2 >= 36, nace2 <= 39),  # Vann, avløp og renovasjon
        np.isin(nace2, [41, 42, 43]),  # Bygge- og anleggsvirksomhet
        (nace2 == 45),  # Motorvognrep og -handel
        (nace2 == 46),  # Agentur- og engroshandel
        (nace2 == 47),  # Detaljhandel, unntatt motorvogner
        (nace2 == 49),  # Landtransport og rørtransport
        (nace2 == 50),  # Sjøfart
        (nace2 == 51),  # Lufttransport
        (nace2 == 52),  # Lagring og tjenester tilknyttet transport
        (nace2 == 53),  # Posttjenester
        (nace2 == 55),  # Overnattingsvirksomhet
        (nace2 == 56),  # Serveringsvirksomhet
        np.isin(nace2, [58, 59, 60]),  # Forlag, film-, TV-pr, kringkasting
        np.isin(nace2, [61, 62, 63]),  # IKT-virksomhet
        (nace2 == 64),  # Finansieringsvirksomhet (bank, m.m.)
        (nace2 == 65),  # Forsikringsvirksomhet og pensjonskasser
        (nace2 == 66),  # Finansiell tjenesteyting
        (nace2 == 68),  # Omsetning og drift av fast eiendom
        np.isin(nace2, [69, 70, 71]),  # Juridisk-, hovedkontor-, konsulentj.
        (nace2 == 72),  # Forskning og utviklingsarbeid
        np.isin(
            nace2, [73, 74, 75]
        ),  # Faglig, vitenskapelig og teknisk tjenesteyting ellers
        np.logical_and(
            nace2 >= 77, nace2 <= 82
        ),  # Forretningsmessig tjenesteyting ellers
        (nace2 == 84),  # Off.adm., forsvar, sosialforsikring
        (nace2 == 85),  # Undervining
        (nace2 == 86),  # Helsetjenester
        np.isin(nace2, [87, 88]),  # Pleie og omsorg; Fritids- og sportsaktiviteter
        np.logical_and(nace2 >= 90, nace2 <= 93),  # Kultur, underholdning og fritid
        np.isin(nace2, [94, 95, 96]),  # Annen tjenesteyting
        (nace2 == 97),  # Lønnet husarbeid i private husholdninger
        (nace2 == 99),  # Internasjonale organisasjoner
    ]

    # Define the group labels with string keys
    groups = {
        "01": "Jordbruk, skogbruk, fiske; Bergverksdrift og utvinning, utenom olje og gass",
        "02": "Annen utvinning; Bygging av skip og båter; Reparasjon og installasjon av maskiner og utstyr; Uoppgitt utvinning",
        "03": "Olje- og gassutvinning; Uoppgitt utvinning av petroleum",
        "04": "Næringsmiddel-,drikkev.,tobakkind.",
        "05": "Tekstil-,bekledn.-,lærvareind.",
        "06": "Trelast- og trevareind.",
        "07": "Trykking, grafisk industri",
        "08": "Petrolieum, kull, kjemisk og farmasøytisk industri",
        "09": "Gummivare-, plast-,mineralproduktind.",
        "10": "Metallindustri",
        "11": "Metallvareindustri",
        "12": "Data- og elektronisk industri",
        "13": "Maskinindustri",
        "14": "Transportmidelindustri, utenom 30.1; Produksjon av kjøretøy og tilhengere, unntatt motorvogner og motorsykler",
        "15": "Produksjon av skip og båter, inkl. oljeplattformer",
        "16": "Møbel og annen industri",
        "17": "Elekstrisitet, gass, damp, varmtvann",
        "18": "Vann, avløp og renovasjon",
        "19": "Bygge- og anleggsvirksomhet",
        "20": "Motorvognrep og -handel",
        "21": "Agentur- og engroshandel",
        "22": "Detaljhandel, unntatt motorvogner",
        "23": "Landtransport og rørtransport",
        "24": "Sjøfart",
        "25": "Lufttransport",
        "26": "Lagring og tjenester tilknyttet transport",
        "27": "Posttjenester",
        "28": "Overnattingsvirksomhet",
        "29": "Serveringsvirksomhet",
        "30": "Forlag, film-, TV-pr, kringkasting",
        "31": "IKT-virksomhet",
        "32": "Finansieringsvirksomhet (bank, m.m.)",
        "33": "Forsikringsvirksomhet og pensjonskasser",
        "34": "Finansiell tjenesteyting",
        "35": "Omsetning og drift av fast eiendom",
        "36": "Juridisk-, hovedkontor-, konsulentj.",
        "37": "Forskning og utviklingsarbeid",
        "38": "Faglig, vitenskapelig og teknisk tjenesteyting ellers",
        "39": "Forretningsmessig tjenesteyting ellers",
        "40": "Off.adm., forsvar, sosialforsikring",
        "41": "Undervisning",
        "42": "Helsetjenester",
        "43": "Pleie og omsorg; Fritids- og sportsaktiviteter",
        "44": "Kultur, underholdning og fritid",
        "45": "Annen tjenesteyting",
        "46": "Lønnet husarbeid i private husholdninger",
        "47": "Internasjonale organisasjoner",
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


def nace_to_17_groups(nace: PdSeriesStr, label: bool = False) -> PdSeriesStr:
    """Converts NACE codes in a Pandas Series to their corresponding group codes or labels.

    NACE (Nomenclature of Economic Activities) is the European industry standard classification system.
    This function maps NACE codes to a higher-level group (level 2) and optionally returns the group's name instead of its code.

    Parameters:
        nace: A Pandas Series containing NACE codes.
        label: If True, returns the names of the groups instead of their codes. Defaults to False.

    Returns:
        A Pandas Series with the mapped group codes or names, depending on the 'label' argument.

    Note:
        The function relies on a predefined mapping ('KlassVariant(1616).data') to perform the conversion.
        It assumes that this mapping has a specific structure, with 'level', 'code', and 'parentCode' (or 'name' if labels are requested) columns.
    """
    # Retrieve the predefined mapping data for NACE codes
    kv = KlassVariant(1616).data
    # Filter the mapping to include only level 2 categories
    kv_level = kv.query('level == "2"')
    # Create a mapping dictionary from NACE codes to their parent codes
    mapping = kv_level.set_index("code").to_dict()
    # Map the first two characters of each NACE code in the input series to their corresponding group codes
    nace_groups = nace.str[0:2].map(mapping["parentCode"])

    if label:
        # If labels are requested, create a mapping for NACE code names at level 1
        kv_label = kv.query('level == "1"')
        mapping_label = kv_label.set_index("code").to_dict()
        # Map the group codes to their names, filling in 'Uoppgitt' for any missing mappings
        return nace_groups.map(mapping_label["name"]).fillna("Uoppgitt")
    else:
        # If labels are not requested, return the group codes directly
        return nace_groups


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
        default_code = "999"
    elif display == "arblonn":
        results = [str(i) for i in arblonn_groups]
        default_code = "980-990"
    else:
        results = [f"{key} {value}" for key, value in groups.items()]
        default_code = "999 Ukjent"
    grouped = np.select(conditions, results, default=default_code)
    return grouped
