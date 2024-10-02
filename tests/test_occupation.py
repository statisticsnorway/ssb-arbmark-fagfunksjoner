import numpy as np
import pandas as pd

from arbmark import nyk08yrkeregsys1


def test_nyk08yrkeregsys1() -> None:
    occupation_codes = pd.Series(["24", "5421", "9999", "0000", "0111101"])

    expected_output = np.array(["2", "5", "9", "0b", "3_01-03"])

    output = nyk08yrkeregsys1(occupation_codes)

    assert np.array_equal(
        output, expected_output
    ), f"Expected {expected_output}, but got {output}"
