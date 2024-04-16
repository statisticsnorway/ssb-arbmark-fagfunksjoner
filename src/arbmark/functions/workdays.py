# Type hints
from typing import TYPE_CHECKING

# Holidays in Norway
import holidays

# Numpy for data wrangling
import numpy as np

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesTimestamp = pd.Series[pd.Timestamp]  # type: ignore[misc]
    PdSeriesInt = pd.Series[int]  # type: ignore[misc]
else:
    PdSeriesTimestamp = pd.Series
    PdSeriesInt = pd.Series


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

    Raises:
        ValueError: If the length of the calculated workdays list does not match the
            number of date pairs.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy()
    to_dates_np = to_dates.to_numpy()

    # Extract the year from the from_dates and to_dates arrays
    from_years = from_dates_np.astype("datetime64[Y]").astype(int) + 1970
    to_years = to_dates_np.astype("datetime64[Y]").astype(int) + 1970

    # Find the max and min years
    min_year = int(np.min(from_years))
    max_year = int(np.max(to_years))

    if min_year == max_year:
        norwegian_holidays = holidays.country_holidays("NO", years=min_year)
    else:
        norwegian_holidays = holidays.country_holidays(
            "NO", years=range(min_year, max_year + 1)
        )

    # Convert the holiday dates to a numpy array of datetime64 objects
    holiday_dates = np.array(sorted(norwegian_holidays.keys()), dtype="datetime64[D]")

    # Convert from_dates and to_dates to datetime64 arrays
    from_dates_d = from_dates_np.astype("datetime64[D]")
    to_dates_d = to_dates_np.astype("datetime64[D]")

    # Find the max and min dates
    min_date = np.min(from_dates_d)
    max_date = np.max(to_dates_d)

    # Generate a range of dates between the min and max dates
    dates = np.arange(
        min_date, max_date + np.timedelta64(1, "D"), dtype="datetime64[D]"
    )

    # Filter the dates array to exclude holiday dates and weekends
    workdays = dates[
        ~np.isin(dates, holiday_dates)
        & ~np.isin((dates.astype("datetime64[D]").view("int64") - 4) % 7, [5, 6])
    ]

    # Calculate the number of workdays for each from and to date pair
    workdays_list = []
    for from_date, to_date in zip(from_dates_d, to_dates_d, strict=True):
        workdays_in_range = workdays[(workdays >= from_date) & (workdays <= to_date)]
        workdays_list.append(len(workdays_in_range))

    # Check if the length of the workdays_list is the same as the number of date pairs
    if len(workdays_list) != len(from_dates):
        raise ValueError(
            "Unexpected error: length of workdays_list does not match the number of date pairs."
        )

    return pd.Series(workdays_list, dtype="Int64")


def count_holidays(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesInt:
    """Counts the number of holidays between pairs of dates in given series.

    This function calculates the number of holidays for each pair of start and end
    dates provided in the `from_dates` and `to_dates` series. It handles date ranges
    spanning multiple years and counts holidays specific to Norway.
    The function dynamically fetches Norwegian holidays for the relevant years based
    on the input dates.

    Args:
        from_dates: A pandas Series containing the start dates of the periods.
        to_dates: A pandas Series containing the end dates of the periods.

    Returns:
        A Pandas Series containing the number of holidays for each date pair.

    Raises:
        ValueError: If the length of the calculated number of holidays does not match the
            number of date pairs.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy()
    to_dates_np = to_dates.to_numpy()

    # Extract the year from the from_dates and to_dates arrays
    from_years = from_dates_np.astype("datetime64[Y]").astype(int) + 1970
    to_years = to_dates_np.astype("datetime64[Y]").astype(int) + 1970

    # Find the max and min years
    min_year = int(np.min(from_years))
    max_year = int(np.max(to_years))

    if min_year == max_year:
        norwegian_holidays = holidays.country_holidays("NO", years=min_year)
    else:
        norwegian_holidays = holidays.country_holidays(
            "NO", years=range(min_year, max_year + 1)
        )

    # Convert the holiday dates to a numpy array of datetime64 objects
    holiday_dates = np.array(sorted(norwegian_holidays.keys()), dtype="datetime64[D]")

    # Convert from_dates and to_dates to datetime64 arrays
    from_dates_d = from_dates_np.astype("datetime64[D]")
    to_dates_d = to_dates_np.astype("datetime64[D]")

    # Create a list to store the number of holidays for each date range
    holiday_counts = []
    for from_date, to_date in zip(from_dates_d, to_dates_d, strict=True):
        holidays_in_range = holiday_dates[
            (holiday_dates >= from_date) & (holiday_dates <= to_date)
        ]
        holiday_counts.append(len(holidays_in_range))

    # Check if the length of the workdays_list is the same as the number of date pairs
    if len(holiday_counts) != len(from_dates):
        raise ValueError(
            "Unexpected error: length of holiday_counts does not match the number of date pairs."
        )

    return pd.Series(holiday_counts, dtype="Int64")


def count_weekenddays(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesInt:
    """Counts the number of weekend days between pairs of dates in given series.

    This function calculates the number of weekend days for each pair of start and
    end dates provided in the `from_dates` and `to_dates` series. Weekends are
    identified using a calculation that considers the Unix epoch (1970-01-01) as
    the reference starting point. After adjusting with a -4 shift and modulo 7,
    the weekdays are mapped as Monday (0) through Sunday (6), with Saturday (5)
    and Sunday (6) identified as the weekend days.

    Args:
        from_dates: A pandas Series containing the start dates of the periods.
        to_dates: A pandas Series containing the end dates of the periods.

    Returns:
        A Pandas Series containing the number of weekend days for each date pair.

    Raises:
        ValueError: If the length of the calculated number of weekend days does not
            match the number of date pairs.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy()
    to_dates_np = to_dates.to_numpy()

    # Convert from_dates and to_dates to datetime64 arrays
    from_dates_d = from_dates_np.astype("datetime64[D]")
    to_dates_d = to_dates_np.astype("datetime64[D]")

    # Find the max and min dates
    min_date = np.min(from_dates_d)
    max_date = np.max(to_dates_d)

    # Generate a range of dates between the min and max dates
    dates = np.arange(
        min_date, max_date + np.timedelta64(1, "D"), dtype="datetime64[D]"
    )

    # Filter the dates array to exclude holiday dates and weekends
    weekenddays = dates[
        np.isin((dates.astype("datetime64[D]").view("int64") - 4) % 7, [5, 6])
    ]

    # Calculate the number of workdays for each from and to date pair
    weekenddays_counts = []
    for from_date, to_date in zip(from_dates_d, to_dates_d, strict=True):
        weekenddays_in_range = weekenddays[
            (weekenddays >= from_date) & (weekenddays <= to_date)
        ]
        weekenddays_counts.append(len(weekenddays_in_range))

    # Check if the length of the workdays_list is the same as the number of date pairs
    if len(weekenddays_counts) != len(from_dates):
        raise ValueError(
            "Unexpected error: length of weekenddays_counts does not match the number of date pairs."
        )

    return pd.Series(weekenddays_counts, dtype="Int64")
