# Type hints
from typing import TYPE_CHECKING

# Numpy for data wrangling
import numpy as np

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesTimestamp = pd.Series[pd.Timestamp]  # type: ignore[misc]
    PdSeriesInt = pd.Series[int]  # type: ignore[misc]
    PdSeriesStr = pd.Series[str]  # type: ignore[misc]
    PdSeriesBool = pd.Series[bool]  # type: ignore[misc]
else:
    PdSeriesTimestamp = pd.Series
    PdSeriesInt = pd.Series
    PdSeriesStr = pd.Series
    PdSeriesBool = pd.Series


def ref_day(from_dates: PdSeriesStr, to_dates: PdSeriesStr) -> PdSeriesBool:
    """Determines if the reference day falls between given date ranges.

    This function checks if the 16th day of each month (reference day) is within the
    range specified by the corresponding 'from_dates' and 'to_dates'. It requires that
    both 'from_dates' and 'to_dates' are in the same year and month.

    Args:
        from_dates: A Series of dates representing the start of a period.
            These dates should be in the 'YYYY-MM-DD' format.
        to_dates: A Series of dates representing the end of a period.
            These dates should also be in the 'YYYY-MM-DD' format.

    Returns:
        A Pandas Series of boolean values. Each element in the Series
        corresponds to whether the 16th day of the month for each period is within
        the respective date range.

    Raises:
        ValueError: If 'from_dates' and 'to_dates' are not in the same year, or if
            they are not in the same month.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy().astype("datetime64[D]")
    to_dates_np = to_dates.to_numpy().astype("datetime64[D]")

    # Extract the year and month from the from_dates array
    year = from_dates_np.astype("datetime64[Y]").astype(int) + 1970
    month = from_dates_np.astype("datetime64[M]").astype(int) % 12 + 1

    # Check if the year and month are the same in the to_dates array
    if not np.all(year == to_dates_np.astype("datetime64[Y]").astype(int) + 1970):
        raise ValueError("Function can only be applied to dates in the same year!")

    if not np.all(month == to_dates_np.astype("datetime64[M]").astype(int) % 12 + 1):
        raise ValueError(
            "Function can only be applied to date pairs in the same month!"
        )

    # Create a reference day for each year-month pair
    ref_days = np.array(
        [f"{y}-{m:02d}-16" for y, m in zip(year, month, strict=True)],
        dtype="datetime64[D]",
    )

    # Check if the reference day is within the range of the from_date and to_date
    result = np.logical_and(from_dates_np <= ref_days, ref_days <= to_dates_np)

    # Return the result as an array of boolean values
    return pd.Series(result, dtype="boolean")


def ref_week(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesBool:
    """Determines if any date in each date range falls in the reference week.

    This function checks if any date between the 'from_dates' and 'to_dates' is within
    the reference week. The reference week is defined as the ISO week which includes the
    16th day of each month. The use of the ISO week date system ensures consistency with
    international standards, where the week starts on Monday and the first week of the year
    is the one containing the first Thursday. It requires that both 'from_dates' and
    'to_dates' are in the same year and month.

    Args:
        from_dates: A Series of dates representing the start of a period.
            These dates should be in the 'YYYY-MM-DD' format.
        to_dates: A Series of dates representing the end of a period.
            These dates should also be in the 'YYYY-MM-DD' format.

    Returns:
        A Series of booleans, where each boolean corresponds to whether any date in
        the period from 'from_dates' to 'to_dates' falls within the reference week
        of the month as defined by the ISO week date system.

    Raises:
        ValueError: If 'from_dates' and 'to_dates' are not in the same year, or if
            they are not in the same month.
    """
    # Check if the year is the same in the to_dates array
    if not np.all(from_dates.dt.year == to_dates.dt.year):
        # If the year is not the same, raise an error
        raise ValueError("Function can only be applied to dates in the same year!")

    # Check if the month is the same in the to_dates array
    if not np.all(from_dates.dt.month == to_dates.dt.month):
        # If the month is not the same, raise an error
        raise ValueError("Function can only be applied to dates in the same months!")

    # Create a reference day for each month
    ref_days = pd.Series(
        pd.to_datetime(
            [
                f"{y}-{m:02d}-16"
                for y, m in zip(from_dates.dt.year, from_dates.dt.month, strict=True)
            ]
        )
    )

    # Calculate the week numbers using pandas with Monday as the starting day
    from_weeks = from_dates.dt.isocalendar().week
    to_weeks = to_dates.dt.isocalendar().week
    ref_weeks = ref_days.dt.isocalendar().week

    # Check if any of the weeks between from_dates and to_dates is the reference week
    result = np.logical_and(from_weeks <= ref_weeks, ref_weeks <= to_weeks)

    # Return the result as a series of boolean values
    return pd.Series(result, dtype="boolean")


def ref_tuesday(
    from_dates: PdSeriesTimestamp, to_dates: PdSeriesTimestamp
) -> PdSeriesBool:
    """Determines if the Tuesday in the same week as the 16th falls between given date ranges.

    This function finds the Tuesday in the same week as the 16th day of each month
    and checks if it is within the range specified by the corresponding 'from_dates'
    and 'to_dates'. It requires that both 'from_dates' and 'to_dates' are in the
    same year and month.

    Args:
        from_dates: A Series of dates representing the start of a period.
            These dates should be in the 'YYYY-MM-DD' format.
        to_dates: A Series of dates representing the end of a period.
            These dates should also be in the 'YYYY-MM-DD' format.

    Returns:
        A Pandas Series of boolean values. Each element in the Series
        corresponds to whether the Tuesday in the week of the 16th day of the month
        for each period is within the respective date range.

    Raises:
        ValueError: If 'from_dates' and 'to_dates' are not in the same year, or if
            they are not in the same month.
    """
    # Check if the year and month are the same in the from_dates and to_dates
    if not np.all(from_dates.dt.year == to_dates.dt.year):
        raise ValueError("Function can only be applied to dates in the same year!")
    if not np.all(from_dates.dt.month == to_dates.dt.month):
        raise ValueError(
            "Function can only be applied to date pairs in the same month!"
        )

    # Compute the date of the 16th for each period
    reference_16th = pd.to_datetime(
        from_dates.dt.year.astype(str) + "-" + from_dates.dt.month.astype(str) + "-16"
    )

    # Calculate the day of the week for the 16th (0=Monday, ..., 6=Sunday)
    weekday_16th = reference_16th.dt.dayofweek

    # Calculate the Tuesday in the same week as the 16th
    tuesday_ref = reference_16th + pd.to_timedelta(1 - weekday_16th, unit="d")

    # Check if the Tuesday reference day is within the range of the from_date and to_date
    result = np.logical_and(from_dates <= tuesday_ref, tuesday_ref <= to_dates)

    # Return the result as an array of boolean values
    return pd.Series(result, dtype="boolean")
