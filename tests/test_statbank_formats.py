import numpy as np
import pandas as pd
import pytest

from arbmark import sb_integer
from arbmark import sb_percent


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "antall_ansatte": pd.to_numeric([np.nan, None, 0, 1.00001, 975, 25]),
            "sykefravaersprosent": pd.to_numeric(
                [np.nan, None, 0, 0.9999, 0.5, 0.3246588]
            ),
        }
    )


def test_sb_integer(sample_df: pd.DataFrame) -> None:
    test1_result = sb_integer(sample_df["antall_ansatte"], unit=2).to_list()
    test1_expected = ["", "", "0", "0", "1000", "0"]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"

    test2_result = sb_integer(sample_df["antall_ansatte"], unit=1).to_list()
    test2_expected = ["", "", "0", "0", "980", "20"]

    assert (
        test2_result == test2_expected
    ), f"Expected {test2_expected}, but got {test2_result}"

    test3_result = sb_integer(sample_df["antall_ansatte"], unit=0).to_list()
    test3_expected = ["", "", "0", "1", "975", "25"]

    assert (
        test3_result == test3_expected
    ), f"Expected {test3_expected}, but got {test3_result}"


def test_sb_percent(sample_df: pd.DataFrame) -> None:
    test1_result = sb_percent(sample_df["sykefravaersprosent"], decimals=1).to_list()
    test1_expected = ["", "", "0,0", "100,0", "50,0", "32,5"]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"

    test2_result = sb_percent(sample_df["sykefravaersprosent"], decimals=2).to_list()
    test2_expected = ["", "", "0,0", "99,99", "50,0", "32,47"]

    assert (
        test2_result == test2_expected
    ), f"Expected {test2_expected}, but got {test2_result}"
