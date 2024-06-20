# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd

# Klass for standard classifications
from klass.classes.variant import KlassVariant

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


def clean_nace_17_groups(val: str) -> str:
    """Cleans the NACE code value by removing redundant parts.

    This function checks if the input string `val` contains a hyphen ('-') and if the parts
    before and after the hyphen are identical. If they are, it returns only the part before the hyphen.
    Otherwise, it returns the original input value.

    Args:
        val: A string containing the NACE code to be cleaned.

    Returns:
        A string with the cleaned NACE code.

    """
    # Check if the hyphen is in the string
    if "-" in val:
        # Split the string at the hyphen
        parts = val.split("-")
        # Check if parts before and after hyphen are the same
        if parts[0] == parts[1]:
            # Return the part before the hyphen if true
            return parts[0]
    # Return original value if no modifications are made
    return val


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
    kv = KlassVariant("1616").data
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
        return nace_groups.apply(clean_nace_17_groups)


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
