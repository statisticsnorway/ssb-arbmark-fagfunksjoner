import pandas as pd
import pytest

from arbmark import count_holidays
from arbmark import count_weekend_days
from arbmark import count_workdays


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "from_dates": pd.to_datetime(["2023-01-01", "2023-12-20", "2024-05-03"]),
            "to_dates": pd.to_datetime(["2023-01-10", "2024-01-05", "2024-05-31"]),
        }
    )


def test_count_workdays(sample_df: pd.DataFrame) -> None:
    test1_result = count_workdays(
        sample_df["from_dates"], sample_df["to_dates"]
    ).to_list()
    test1_expected = [7, 10, 18]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"


def test_count_holidays(sample_df: pd.DataFrame) -> None:
    test1_result = count_holidays(
        sample_df["from_dates"], sample_df["to_dates"]
    ).to_list()
    test1_expected = [1, 3, 4]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"


def test_count_weekend_days(sample_df: pd.DataFrame) -> None:
    test1_result = count_weekend_days(
        sample_df["from_dates"], sample_df["to_dates"]
    ).to_list()
    test1_expected = [3, 4, 8]

    assert (
        test1_result == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result}"
