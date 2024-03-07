import pandas as pd

from arbmark import turnuskoder


def test_turnuskoder():
    test_case = pd.Series(
        ["dogn355", "helkont336", "ikke_skift", "-2", "offshore336", ""]
    )
    result = turnuskoder(test_case)
    expected = pd.Series(["20", "20", "25", "99", "20", "99"])
    assert (result == expected).all(), f"Expected {expected}, but got {result}"
