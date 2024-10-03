import numpy as np
import pandas as pd

from arbmark import classify_county_not_mainland
from arbmark import classify_mainland_not_mainland
from arbmark import get_regional_special_codes
from arbmark import get_valid_county_codes


def test_get_valid_county_codes() -> None:
    year = 2023
    test1_result = sorted(get_valid_county_codes(year))
    test1_result_first = test1_result[0]

    test1_expected = "03"

    assert (
        test1_result_first == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result_first}"


def test_get_regional_special_codes() -> None:
    year = 2021
    test2_result = sorted(get_regional_special_codes(year))
    test2_result_first = test2_result[0]

    test2_expected = "21"

    assert (
        test2_result_first == test2_expected
    ), f"Expected {test2_expected}, but got {test2_result_first}"


def test_classify_mainland_not_mainland() -> None:
    municipality_numbers = pd.Series(["0101", "0301", "2100", "9999", "2211"])

    year = 2023

    expected_output = np.array(["Uoppgitt", "FNorge", "IFNorge", "Uoppgitt", "IFNorge"])

    output = classify_mainland_not_mainland(municipality_numbers, year)

    assert np.array_equal(
        output, expected_output
    ), f"Expected {expected_output}, but got {output}"


def test_classify_county_not_mainland() -> None:
    municipality_numbers = pd.Series(["0101", "0301", "2100", "9999", "2211"])

    year = 2019

    expected_output = np.array(["01", "03", "21", "99", "22"])

    output = classify_county_not_mainland(municipality_numbers, year, True)

    assert np.array_equal(
        output, expected_output
    ), f"Expected {expected_output}, but got {output}"
