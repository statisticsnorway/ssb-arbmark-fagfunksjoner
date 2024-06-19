# Type hints
from typing import TYPE_CHECKING

# Holidays in Norway
import holidays

# Numpy for data wrangling
import numpy as np
import numpy.typing as npt

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesTimestamp = pd.Series[pd.Timestamp]  # type: ignore[misc]
    PdSeriesInt = pd.Series[int]  # type: ignore[misc]
    NpArrayInt = npt.NDArray[np.int_]  # type: ignore[misc]
    NpArrayDate = npt.NDArray[np.datetime64]  # type: ignore[misc]
    NpArrayBoolean = npt.NDArray[np.dtype[bool]]  # type: ignore[misc]
else:
    PdSeriesTimestamp = pd.Series
    PdSeriesInt = pd.Series
    NpArrayInt = npt.NDArray
    NpArrayDate = npt.NDArray
    NpArrayBoolean = npt.NDArray


def numpy_dates(dates: PdSeriesTimestamp) -> NpArrayDate:
    """Converts a Pandas Series of timestamps to a Numpy array of dates in 'datetime64[D]' format.

    Args:
        dates: A pandas Series containing timestamps.

    Returns:
        A Numpy array containing dates.
    """
    return dates.to_numpy().astype("datetime64[D]")


def get_years(from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp) -> NpArrayInt:
    """Extracts unique years from two series of dates.

    Args:
        from_dates: A Pandas Series of start dates.
        to_dates: A Pandas Series of end dates.

    Returns:
        A Numpy array of unique years derived from the date ranges.
    """
    all_dates = pd.concat([from_dates, to_dates])
    all_years = all_dates.to_numpy().astype("datetime64[Y]").astype(int) + 1970
    return np.unique(all_years)


def count_days(
    from_dates: NpArrayDate, to_dates: NpArrayDate, calendar: NpArrayDate
) -> PdSeriesInt:
    """Counts the days between pairs of start and end dates using a provided calendar.

    Args:
        from_dates: Numpy array of start dates.
        to_dates: Numpy array of end dates.
        calendar: Numpy array representing the days to be counted.

    Returns:
        A Pandas Series with the count of days for each pair.
    """
    counts = []
    for from_date, to_date in zip(from_dates, to_dates, strict=True):
        dates_to_count = calendar[(calendar >= from_date) & (calendar <= to_date)]
        counts.append(len(dates_to_count))
    return pd.Series(counts, dtype="Int64")


def get_calendar(from_date: np.datetime64, to_date: np.datetime64) -> NpArrayDate:
    """Generates a calendar as a range of dates from a start date to an end date.

    Args:
        from_date: The start date.
        to_date: The end date.

    Returns:
        A Numpy array representing a range of dates from start to end.
    """
    return np.arange(from_date, to_date + np.timedelta64(1, "D"), dtype="datetime64[D]")


def get_norwegian_holidays(years: NpArrayInt) -> NpArrayDate:
    """Fetches Norwegian holidays for a given range of years and returns them as a sorted Numpy array of dates.

    Args:
        years: Numpy array of years for which holidays are to be fetched.

    Returns:
        A Numpy array of holiday dates.
    """
    if len(years) == 1:
        norwegian_holidays = holidays.country_holidays("NO", years=int(years[0]))
    else:
        norwegian_holidays = holidays.country_holidays(
            "NO", years=range(np.min(years), np.max(years) + 1)
        )
    return np.array(sorted(norwegian_holidays.keys()), dtype="datetime64[D]")


def is_weekend(calendar: NpArrayDate) -> NpArrayBoolean:
    """Determines which days in a given calendar are weekends.

    Args:
        calendar: Numpy array of dates.

    Returns:
        A Numpy boolean array where True indicates a weekend.
    """
    return np.isin((calendar.astype("datetime64[D]").view("int64") - 4) % 7, [5, 6])


def filter_workdays(calendar: NpArrayDate, holidays: NpArrayDate) -> NpArrayDate:
    """Filters out weekends and holidays from a calendar, leaving only workdays.

    Args:
        calendar: Numpy array of dates.
        holidays: Numpy array of holiday dates.

    Returns:
        A Numpy array of dates that are workdays.
    """
    return calendar[~np.isin(calendar, holidays) & ~is_weekend(calendar)]


def filter_holidays(calendar: NpArrayDate, holidays: NpArrayDate) -> NpArrayDate:
    """Filters out the holiday dates from a given calendar.

    This function identifies and returns only the dates in the calendar that are recognized as holidays, excluding holidays on weekends.

    Args:
        calendar: Numpy array of dates.
        holidays: Numpy array of dates that are holidays.

    Returns:
        A Numpy array of dates that are recognized as holidays.
    """
    return calendar[np.isin(calendar, holidays) & ~is_weekend(calendar)]


def filter_weekends(calendar: NpArrayDate) -> NpArrayDate:
    """Filters out the weekend dates from a given calendar.

    This function identifies which days in the provided calendar are weekends and returns only those dates.

    Args:
        calendar: Numpy array of dates, typically encompassing multiple weeks.

    Returns:
        A Numpy array of dates that fall on weekends (Saturday and Sunday).
    """
    return calendar[is_weekend(calendar)]


def count_workdays(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesInt:
    """Counts the number of workdays between pairs of dates in given series.

    This function calculates the number of workdays for each pair of start and end
    dates provided in the `from_dates` and `to_dates` series. It handles date ranges
    spanning multiple years and excludes weekends and holidays specific to Norway.
    The function dynamically fetches Norwegian holidays for the relevant years based
    on the input dates. Weekends are identified using a calculation that considers
    the Unix epoch (1970-01-01) as the reference starting point. After adjusting
    with a -4 shift and modulo 7, the weekdays are mapped as Monday (0) through
    Sunday (6), with Saturday (5) and Sunday (6) identified as the weekend days.

    Args:
        from_dates: A pandas Series containing the start dates of the periods.
        to_dates: A pandas Series containing the end dates of the periods.

    Returns:
        A Pandas Series containing the number of workdays for each date pair.
    """
    from_dates_np = numpy_dates(from_dates)
    to_dates_np = numpy_dates(to_dates)
    return count_days(
        from_dates_np,
        to_dates_np,
        filter_workdays(
            get_calendar(np.min(from_dates_np), np.max(to_dates_np)),
            get_norwegian_holidays(get_years(from_dates, to_dates)),
        ),
    )


def count_holidays(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesInt:
    """Counts the number of holidays between pairs of dates in given series.

    This function calculates the number of holidays for each pair of start and end dates provided in
    the `from_dates` and `to_dates` series. It uses the holidays specific to Norway and considers
    each pair's specific date range.

    Args:
        from_dates: A pandas Series containing the start dates of the periods.
        to_dates: A pandas Series containing the end dates of the periods.

    Returns:
        A Pandas Series containing the number of holidays for each date pair.
    """
    from_dates_np = numpy_dates(from_dates)
    to_dates_np = numpy_dates(to_dates)
    return count_days(
        from_dates_np,
        to_dates_np,
        filter_holidays(
            get_calendar(np.min(from_dates_np), np.max(to_dates_np)),
            get_norwegian_holidays(get_years(from_dates, to_dates)),
        ),
    )


def count_weekend_days(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesInt:
    """Counts the number of weekend days between pairs of dates in given series.

    This function calculates the number of weekend days for each pair of start and end dates provided in
    the `from_dates` and `to_dates` series. It identifies weekends based on a calculation using the Unix
    epoch as the reference point. The result includes the total number of Saturdays and Sundays within each
    specified date range.

    Args:
        from_dates: A pandas Series containing the start dates of the periods.
        to_dates: A pandas Series containing the end dates of the periods.

    Returns:
        A Pandas Series containing the number of weekend days for each date pair.
    """
    from_dates_np = numpy_dates(from_dates)
    to_dates_np = numpy_dates(to_dates)
    return count_days(
        from_dates_np,
        to_dates_np,
        filter_weekends(get_calendar(np.min(from_dates_np), np.max(to_dates_np))),
    )
