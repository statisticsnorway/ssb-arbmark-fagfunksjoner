import pandas as pd
import pytest

from arbmark import get_reference_week_start_end
from arbmark import ref_day
from arbmark import ref_tuesday
from arbmark import ref_week


def test_reference_week_when_16th_is_midweek():
    result = get_reference_week_start_end(2026, 6)

    assert result == ("2026-06-15", "2026-06-21")


def test_reference_week_when_16th_is_monday():
    result = get_reference_week_start_end(2026, 2)

    assert result == ("2026-02-16", "2026-02-22")


def test_reference_week_when_16th_is_sunday():
    result = get_reference_week_start_end(2025, 2)

    assert result == ("2025-02-10", "2025-02-16")


def test_accepts_string_inputs():
    result = get_reference_week_start_end("2026", "06")

    assert result == ("2026-06-15", "2026-06-21")


def test_returns_iso_formatted_strings():
    result = get_reference_week_start_end(2026, 6)

    assert isinstance(result[0], str)
    assert isinstance(result[1], str)
    assert result[0] == "2026-06-15"
    assert result[1] == "2026-06-21"


@pytest.mark.parametrize("month", [0, 13, "abc", ""])
def test_invalid_month_raises_value_error(month):
    with pytest.raises(ValueError):
        get_reference_week_start_end(2026, month)


@pytest.mark.parametrize("year", ["abc", ""])
def test_invalid_year_raises_value_error(year):
    with pytest.raises(ValueError):
        get_reference_week_start_end(year, 6)


def test_ref_day_within_range() -> None:
    from_dates = pd.Series(["2023-01-01", "2023-02-10"])
    to_dates = pd.Series(["2023-01-20", "2023-02-18"])
    expected = pd.Series([True, True])
    assert (
        ref_day(from_dates, to_dates) == expected
    ).all(), "16th day within range test failed"


def test_ref_day_outside_range() -> None:
    from_dates = pd.Series(["2023-03-17", "2023-04-18"])
    to_dates = pd.Series(["2023-03-30", "2023-04-25"])
    expected = pd.Series([False, False])
    assert (
        ref_day(from_dates, to_dates) == expected
    ).all(), "16th day outside range test failed"


def test_ref_week_within_range() -> None:
    from_dates = pd.Series(
        pd.to_datetime(["2022-02-20", "2022-04-01", "2022-01-01", "2022-12-01"])
    )
    to_dates = pd.Series(
        pd.to_datetime(["2022-02-28", "2022-04-11", "2022-01-31", "2022-12-31"])
    )
    expected = pd.Series([True, True, True, True])
    assert (
        ref_week(from_dates, to_dates) == expected
    ).all(), "Reference week within range test failed"


def test_ref_week_outside_range() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-04-17"]))
    to_dates = pd.Series(pd.to_datetime(["2023-01-15", "2023-04-30"]))
    expected = pd.Series([False, False])
    assert (
        ref_week(from_dates, to_dates) == expected
    ).all(), "Reference week outside range test failed"


def test_ref_tuesday_within_range() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-12-11", "2023-11-13"]))
    to_dates = pd.Series(pd.to_datetime(["2023-12-15", "2023-11-14"]))
    expected = pd.Series([True, True])
    assert (
        ref_tuesday(from_dates, to_dates) == expected
    ).all(), "Tuesday in the same week as the 16th within range test failed"


def test_ref_tuesday_outside_range() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-11-15", "2023-12-14"]))
    to_dates = pd.Series(pd.to_datetime(["2023-11-30", "2023-12-24"]))
    expected = pd.Series([False, False])
    assert (
        ref_tuesday(from_dates, to_dates) == expected
    ).all(), "Tuesday in the same week as the 16th outside range test failed"


def test_ref_day_different_years() -> None:
    from_dates = pd.Series(["2023-01-01", "2023-01-20"])
    to_dates = pd.Series(["2024-02-10", "2024-02-18"])
    try:
        ref_day(from_dates, to_dates)
        raise AssertionError("Different year test should have raised ValueError")
    except ValueError:
        pass


def test_ref_day_different_months() -> None:
    from_dates = pd.Series(["2023-01-01", "2023-01-20"])
    to_dates = pd.Series(["2023-03-10", "2023-02-18"])
    try:
        ref_day(from_dates, to_dates)
        raise AssertionError("Different month test should have raised ValueError")
    except ValueError:
        pass


def test_ref_week_different_years() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-01-15"]))
    to_dates = pd.Series(pd.to_datetime(["2024-04-01", "2024-04-15"]))
    try:
        ref_week(from_dates, to_dates)
        raise AssertionError("Different year test should have raised ValueError")
    except ValueError:
        pass


def test_ref_week_different_months() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-01-15"]))
    to_dates = pd.Series(pd.to_datetime(["2023-03-01", "2023-04-15"]))
    try:
        ref_week(from_dates, to_dates)
        raise AssertionError("Different month test should have raised ValueError")
    except ValueError:
        pass


def test_ref_tuesday_different_years() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-01-20"]))
    to_dates = pd.Series(pd.to_datetime(["2024-02-10", "2024-02-18"]))
    try:
        ref_tuesday(from_dates, to_dates)
        raise AssertionError("Different year test should have raised ValueError")
    except ValueError:
        pass


def test_ref_tuesday_different_months() -> None:
    from_dates = pd.Series(pd.to_datetime(["2023-01-01", "2023-01-20"]))
    to_dates = pd.Series(pd.to_datetime(["2023-03-10", "2023-02-18"]))
    try:
        ref_tuesday(from_dates, to_dates)
        raise AssertionError("Different month test should have raised ValueError")
    except ValueError:
        pass
