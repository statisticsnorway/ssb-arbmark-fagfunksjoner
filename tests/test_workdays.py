import pandas as pd

from arbmark import count_workdays


def test_count_workdays() -> None:
    test1_from_dates = pd.Series(
        pd.to_datetime(["2023-01-01", "2023-12-20", "2024-05-03"])
    )
    test1_to_dates = pd.Series(
        pd.to_datetime(["2023-01-10", "2024-01-05", "2024-05-31"])
    )
    test1_result = count_workdays(test1_from_dates, test1_to_dates).to_list()
    test1_expected = [7, 10, 18]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"
