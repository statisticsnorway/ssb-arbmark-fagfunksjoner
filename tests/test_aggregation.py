import pandas as pd
import pytest

from arbmark import proc_sums


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "A": ["foo", "foo", "foo", "bar", "bar", "bar"],
            "B": ["one", "one", "two", "two", "two", "two"],
            "C": [1, 2, 3, 4, 5, 6],
            "D": [10, 20, 30, 40, 50, 60],
            "E": ["1", "0", "1", "1", "0", "1"],
        }
    )


def test_proc_sums_count_nunique(sample_df: pd.DataFrame) -> None:
    test1_result = proc_sums(
        sample_df, groups=["B"], agg_func={"E": ["count", "nunique"]}
    ).to_dict()
    test1_expected = {
        ("B", ""): {0: "Total", 1: "one", 2: "two"},
        ("E", "count"): {0: 6, 1: 2, 2: 4},
        ("E", "nunique"): {0: 2, 1: 2, 2: 2},
        ("level", ""): {0: 0, 1: 1, 2: 1},
    }
    assert test1_result == test1_expected, "Test 1 failed"


def test_proc_sums_default_sum(sample_df: pd.DataFrame) -> None:
    test2_result = proc_sums(sample_df, groups=["A", "B"], values=["C"]).to_dict()
    test2_expected = {
        "A": {
            0: "Total",
            1: "bar",
            2: "foo",
            3: "Total",
            4: "Total",
            5: "bar",
            6: "foo",
            7: "foo",
        },
        "B": {
            0: "Total",
            1: "Total",
            2: "Total",
            3: "one",
            4: "two",
            5: "two",
            6: "one",
            7: "two",
        },
        "C": {0: 21, 1: 15, 2: 6, 3: 3, 4: 18, 5: 15, 6: 3, 7: 3},
        "level": {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2},
    }
    assert test2_result == test2_expected, "Test 2 failed"


def test_proc_sums_custom_aggregations(sample_df: pd.DataFrame) -> None:
    test3_result = proc_sums(
        sample_df,
        groups=["A", "B"],
        values=["C", "D"],
        agg_func={"C": "sum", "D": "mean"},
    ).to_dict()
    test3_expected = {
        "A": {
            0: "Total",
            1: "bar",
            2: "foo",
            3: "Total",
            4: "Total",
            5: "bar",
            6: "foo",
            7: "foo",
        },
        "B": {
            0: "Total",
            1: "Total",
            2: "Total",
            3: "one",
            4: "two",
            5: "two",
            6: "one",
            7: "two",
        },
        "C": {0: 21, 1: 15, 2: 6, 3: 3, 4: 18, 5: 15, 6: 3, 7: 3},
        "D": {0: 35.0, 1: 50.0, 2: 20.0, 3: 15.0, 4: 45.0, 5: 50.0, 6: 15.0, 7: 30.0},
        "level": {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2},
    }
    assert test3_result == test3_expected, "Test 3 failed"
