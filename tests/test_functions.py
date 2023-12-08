import pandas as pd

from ssb_arbmark_fagfunksjoner.functions import count_workdays
from ssb_arbmark_fagfunksjoner.functions import first_last_date_quarter
from ssb_arbmark_fagfunksjoner.functions import kv_intervall
from ssb_arbmark_fagfunksjoner.functions import proc_sums
from ssb_arbmark_fagfunksjoner.functions import ref_day
from ssb_arbmark_fagfunksjoner.functions import ref_week


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


def test_first_last_date_quarter() -> None:
    test_cases = [
        ("2023", "1", ("2023-01-01", "2023-03-31")),
        ("2023", "2", ("2023-04-01", "2023-06-30")),
        ("2023", "3", ("2023-07-01", "2023-09-30")),
        ("2023", "4", ("2023-10-01", "2023-12-31")),
        # Add more test cases if necessary
    ]

    for year, quarter, expected in test_cases:
        result = first_last_date_quarter(year, quarter)
        assert (
            result == expected
        ), f"For {year} Q{quarter}, expected {expected}, but got {result}"


def test_kv_intervall() -> None:
    test_cases = [
        ("2022k1", "2022k4", ["2022k1", "2022k2", "2022k3", "2022k4"]),
        ("2022k2", "2023k1", ["2022k2", "2022k3", "2022k4", "2023k1"]),
        ("2022k3", "2023k2", ["2022k3", "2022k4", "2023k1", "2023k2"]),
        # Add more test cases as necessary
    ]

    for start_p, slutt_p, expected in test_cases:
        result = kv_intervall(start_p, slutt_p)
        assert (
            result == expected
        ), f"For {start_p} to {slutt_p}, expected {expected}, but got {result}"


def sample_df():
    return pd.DataFrame(
        {
            "A": ["foo", "foo", "foo", "bar", "bar", "bar"],
            "B": ["one", "one", "two", "two", "two", "two"],
            "C": [1, 2, 3, 4, 5, 6],
            "D": [10, 20, 30, 40, 50, 60],
            "E": ["1", "0", "1", "1", "0", "1"],
        }
    )


def test_proc_sums_count_nunique(sample_df):
    test1_result = proc_sums(
        sample_df, groups=["B"], values=["E"], agg_func={"E": ["count", "nunique"]}
    ).to_dict()
    test1_expected = {
        ("B", ""): {0: "one", 1: "two"},
        ("E", "count"): {0: 2, 1: 4},
        ("E", "nunique"): {0: 2, 1: 2},
        ("level", ""): {0: 1, 1: 1},
    }
    assert test1_result == test1_expected, "Test 1 failed"


def test_proc_sums_default_sum(sample_df):
    test2_result = proc_sums(sample_df, groups=["A", "B"], values=["C"]).to_dict()
    test2_expected = {
        "A": {0: "bar", 1: "foo", 2: "foo", 3: "bar", 4: "foo", 5: "Total", 6: "Total"},
        "B": {0: "two", 1: "one", 2: "two", 3: "Total", 4: "Total", 5: "one", 6: "two"},
        "C": {0: 15, 1: 3, 2: 3, 3: 15, 4: 6, 5: 3, 6: 18},
        "level": {0: 2, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1},
    }
    assert test2_result == test2_expected, "Test 2 failed"


def test_proc_sums_custom_aggregations(sample_df):
    test3_result = proc_sums(
        sample_df,
        groups=["A", "B"],
        values=["C", "D"],
        agg_func={"C": "sum", "D": "mean"},
    ).to_dict()
    test3_expected = {
        "A": {0: "bar", 1: "foo", 2: "foo", 3: "bar", 4: "foo", 5: "Total", 6: "Total"},
        "B": {0: "two", 1: "one", 2: "two", 3: "Total", 4: "Total", 5: "one", 6: "two"},
        "C": {0: 15, 1: 3, 2: 3, 3: 15, 4: 6, 5: 3, 6: 18},
        "D": {0: 50.0, 1: 15.0, 2: 30.0, 3: 50.0, 4: 20.0, 5: 15.0, 6: 45.0},
        "level": {0: 2, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1},
    }
    assert test3_result == test3_expected, "Test 3 failed"


def test_ref_day_within_range():
    from_dates = pd.Series(["2023-01-01", "2023-02-10"])
    to_dates = pd.Series(["2023-01-20", "2023-02-18"])
    expected = pd.Series([True, True])
    assert ref_day(from_dates, to_dates).equals(
        expected
    ), "16th day within range test failed"


def test_ref_day_outside_range():
    from_dates = pd.Series(["2023-03-17", "2023-04-18"])
    to_dates = pd.Series(["2023-03-30", "2023-04-25"])
    expected = pd.Series([False, False])
    assert ref_day(from_dates, to_dates).equals(
        expected
    ), "16th day outside range test failed"


def test_ref_week_within_range():
    from_dates = pd.Series(
        pd.to_datetime(
            [
                "2023-01-22",
                "2023-04-01",
            ]
        )
    )
    to_dates = pd.Series(
        pd.to_datetime(
            [
                "2023-01-31",
                "2023-04-15",
            ]
        )
    )
    expected = pd.Series([True, True])
    assert ref_week(from_dates, to_dates).equals(
        expected
    ), "Reference week within range test failed"


def test_ref_week_outside_range():
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-04-17"]))
    to_dates = pd.Series(pd.to_datetime(["2023-01-15", "2023-04-30"]))
    expected = pd.Series([False, False])
    assert ref_week(from_dates, to_dates).equals(
        expected
    ), "Reference week outside range test failed"
