"""A collection of useful groups."""

# Numpy for data wrangling
import numpy as np

# Pandas for table management
import pandas as pd


def alder_grp(alder: pd.Series[int], display: str = "label") -> pd.Series[str]:
    """Categorize a pandas Series of person ages into predefined groups.

    Parameters:
        alder (pd.Series): A pandas Series containing the person ages.
        display (str): If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        pd.Series: A pandas Series where the original person ages are replaced by group labels, keys, or a combination.
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
    return pd.Series(np.select(conditions, results, default="."), dtype="string")


def nace_sn07_47grp(
    nace_sn07: pd.Series[str], display: str = "label"
) -> pd.Series[str]:
    """Categorize a pandas Series of NACE-codes (SN07) into predefined groups.

    Parameters:
        nace_sn07 (pd.Series): A pandas Series containing the NACE-codes.
        display (str): If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        pd.Series: A pandas Series where the original NACE-codes are replaced by group labels or keys.
    """
    # Removes periods in the NACE codes (if any)
    nace_sn07 = nace_sn07.replace(".", "")

    # Substring of NACE codes at length 2 and 3
    nace2 = pd.Series(nace_sn07.str[:2], name="nace2")
    nace3 = pd.Series(nace_sn07.str[:3], name="nace3")

    # Define the conditions for each group
    conditions = [
        np.isin(
            nace2, ["01", "02", "03"]
        ),  # Jordbruk, skogbruk, fiske; Bergverksdrift og utvinning, utenom olje og gass
        np.logical_or(
            np.isin(nace2, ["05", "07", "08"]), nace3 == "099"
        ),  # Annen utvinning; Bygging av skip og båter; Reparasjon og installasjon av maskiner og utstyr; Uoppgitt utvinning
        np.logical_or(
            nace2 == "06", nace3 == "091"
        ),  # Olje- og gassutvinning; Uoppgitt utvinning av petroleum
        np.isin(nace2, ["10", "11", "12"]),  # Næringsmiddel-,drikkev.,tobakkind.
        np.isin(nace2, ["13", "14", "15"]),  # Tekstil-,bekledn.-,lærvareind.
        np.isin(nace2, ["16", "17"]),  # Trelast- og trevareind.
        (nace2 == "18").to_numpy(),  # Trykking, grafisk industri
        np.isin(
            nace2, ["19", "20", "21"]
        ),  # Petrolieum, kull, kjemisk og farmasøytisk industri
        np.isin(nace2, ["22", "23"]),  # Gummivare-, plast-,mineralproduktind.
        (nace2 == "24").to_numpy(),  # Metallindustri
        (nace2 == "25").to_numpy(),  # Metallvareindustri
        np.isin(nace2, ["26", "27"]),  # Data- og elektronisk industri
        (nace2 == "28").to_numpy(),  # Maskinindustri
        np.logical_or(
            np.isin(nace2, ["29", "33"]), np.logical_and(nace3 >= "302", nace3 <= "309")
        ),  # Transportmidelindustri, utenom 30.1; Produksjon av kjøretøy og tilhengere, unntatt motorvogner og motorsykler
        (
            nace3 == "301"
        ).to_numpy(),  # Produksjon av skip og båter, inkl. oljeplattformer
        np.isin(nace2, ["31", "32"]),  # Møbel og annen industri
        (nace2 == "35").to_numpy(),  # Elekstrisitet, gass, damp, varmtvann
        np.logical_and(nace2 >= "36", nace2 <= "39"),  # Vann, avløp og renovasjon
        np.isin(nace2, ["41", "42", "43"]),  # Bygge- og anleggsvirksomhet
        (nace2 == "45").to_numpy(),  # Motorvognrep og -handel
        (nace2 == "46").to_numpy(),  # Agentur- og engroshandel
        (nace2 == "47").to_numpy(),  # Detaljhandel, unntatt motorvogner
        (nace2 == "49").to_numpy(),  # Landtransport og rørtransport
        (nace2 == "50").to_numpy(),  # Sjøfart
        (nace2 == "51").to_numpy(),  # Lufttransport
        (nace2 == "52").to_numpy(),  # Lagring og tjenester tilknyttet transport
        (nace2 == "53").to_numpy(),  # Posttjenester
        (nace2 == "55").to_numpy(),  # Overnattingsvirksomhet
        (nace2 == "56").to_numpy(),  # Serveringsvirksomhet
        np.isin(nace2, ["58", "59", "60"]),  # Forlag, film-, TV-pr, kringkasting
        np.isin(nace2, ["61", "62", "63"]),  # IKT-virksomhet
        (nace2 == "64").to_numpy(),  # Finansieringsvirksomhet (bank, m.m.)
        (nace2 == "65").to_numpy(),  # Forsikringsvirksomhet og pensjonskasser
        (nace2 == "66").to_numpy(),  # Finansiell tjenesteyting
        (nace2 == "68").to_numpy(),  # Omsetning og drift av fast eiendom
        np.isin(nace2, ["69", "70", "71"]),  # Juridisk-, hovedkontor-, konsulentj.
        (nace2 == "72").to_numpy(),  # Forskning og utviklingsarbeid
        np.isin(
            nace2, ["73", "74", "75"]
        ),  # Faglig, vitenskapelig og teknisk tjenesteyting ellers
        np.logical_and(
            nace2 >= "77", nace2 <= "82"
        ),  # Forretningsmessig tjenesteyting ellers
        (nace2 == "84").to_numpy(),  # Off.adm., forsvar, sosialforsikring
        (nace2 == "85").to_numpy(),  # Undervining
        (nace2 == "86").to_numpy(),  # Helsetjenester
        np.isin(nace2, ["87", "88"]),  # Pleie og omsorg; Fritids- og sportsaktiviteter
        np.logical_and(nace2 >= "90", nace2 <= "93"),  # Kultur, underholdning og fritid
        np.isin(nace2, ["94", "95", "96"]),  # Annen tjenesteyting
        (nace2 == "97").to_numpy(),  # Lønnet husarbeid i private husholdninger
        (nace2 == "99").to_numpy(),  # Internasjonale organisasjoner
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
    return pd.Series(grouped, dtype="string")


def nace_sn07_17grp(
    nace_sn07: pd.Series[str], display: str = "label"
) -> pd.Series[str]:
    """Categorize a pandas Series of NACE-codes (SN07) into predefined groups.

    Parameters:
        nace_sn07 (pd.Series): A pandas Series containing the NACE-codes.
        display (str): If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        pd.Series: A pandas Series where the original NACE-codes are replaced by group labels or keys.
    """
    # Removes labels (if any)
    nace_str2 = nace_sn07.str[:2]

    # Counts the number of unique groups of nace codes
    n_unique_grp = len(nace_str2.unique())

    # Check if nace codes are already grouped into 47-groups
    if n_unique_grp > 48:
        print(
            f"Warning: There are {n_unique_grp} unique industry divisions on 2-number level. The function first groups the input into the 47 groups standard."
        )
        nace_str2 = nace_sn07_47grp(nace_sn07, display="number")

    # Define the conditions for each group
    conditions = [
        (nace_str2 == "01").to_numpy(),  # 01-03 Jordbruk, skogbruk og fiske
        np.logical_and(
            nace_str2 >= "01", nace_str2 <= "03"
        ),  # 05-09 Bergverksdrift og utvinning
        np.logical_and(nace_str2 >= "04", nace_str2 <= "16"),  # 10-33 Industri
        np.logical_and(
            nace_str2 >= "17", nace_str2 <= "18"
        ),  # 35-39 Elektrisitet, vann og renovasjon
        (nace_str2 == "19").to_numpy(),  # 41-43 Bygge- og anleggsvirksomhet
        np.logical_and(
            nace_str2 >= "20", nace_str2 <= "22"
        ),  # 45-47 Varehandel, reparasjon av motorvogner
        np.logical_and(
            nace_str2 >= "23", nace_str2 <= "27"
        ),  # 49-53 Transport og lagring
        np.logical_and(
            nace_str2 >= "28", nace_str2 <= "29"
        ),  # 55-56 Overnattings- og serveringsvirksomhet
        np.logical_and(
            nace_str2 >= "30", nace_str2 <= "31"
        ),  # 58-63 Informasjon og kommunikasjon
        np.logical_and(
            nace_str2 >= "32", nace_str2 <= "34"
        ),  # 64-66 Finansiering og forsikring
        np.logical_and(
            nace_str2 >= "35", nace_str2 <= "38"
        ),  # 68-75 Teknisk tjenesteyting, eiendomsdrift
        (nace_str2 == "39").to_numpy(),  # 77-82 Forretningsmessig tjenesteyting
        (nace_str2 == "40").to_numpy(),  # 84 Off.adm., forsvar, sosialforsikring
        (nace_str2 == "41").to_numpy(),  # 85 Undervisning
        np.logical_and(
            nace_str2 >= "42", nace_str2 <= "43"
        ),  # 86-88 Helse- og sosialtjenester
        np.logical_and(
            nace_str2 >= "44", nace_str2 <= "47"
        ),  # 90-99 Personlig tjenesteyting
    ]

    # Define the group labels with string keys
    groups = {
        "01-03": "Jordbruk, skogbruk og fiske",
        "05-09": "Bergverksdrift og utvinning",
        "10-33": "Industri",
        "35-39": "Elektrisitet, vann og renovasjon",
        "41-43": "Bygge- og anleggsvirksomhet",
        "45-47": "Varehandel, reparasjon av motorvogner",
        "49-53": "Transport og lagring",
        "55-56": "Overnattings- og serveringsvirksomhet",
        "58-63": "Informasjon og kommunikasjon",
        "64-66": "Finansiering og forsikring",
        "68-75": "Teknisk tjenesteyting, eiendomsdrift",
        "77-82": "Forretningsmessig tjenesteyting",
        "84": "Off.adm., forsvar, sosialforsikring",
        "85": "Undervisning",
        "86-88": "Helse- og sosialtjenester",
        "90-99": "Personlig tjenesteyting",
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
    return pd.Series(grouped, dtype="string")


def sektor2_grp(
    sektor: pd.Series[str], undersektor: pd.Series[str], display: str = "label"
) -> pd.Series[str]:
    """Categorize a pandas Series of sectors and subsectors into predefined groups.

    Parameters:
        sektor (pd.Series): A pandas Series containing the sector codes.
        undersektor (pd.Series): A pandas Series containing the subsector codes.
        display (str): If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        pd.Series: A pandas Series where the original sector and subsectors are replaced by group labels or keys.
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
    return pd.Series(grouped, dtype="string")


def virk_str_8grp(ansatte: pd.Series[int], display: str = "label") -> pd.Series[str]:
    """Categorize a pandas Series of employee counts into predefined groups.

    Parameters:
        ansatte (pd.Series): A pandas Series containing the employee counts.
        display (str): If 'label', returns group labels; if 'number', returns keys;
                       for any other string, returns a combination of keys and labels.

    Returns:
        pd.Series: A pandas Series where the original employee counts are replaced by group labels or keys.
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
    return pd.Series(grouped, dtype="string")
