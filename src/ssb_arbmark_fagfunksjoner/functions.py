"""A collection of useful functions."""


# Itertools for functions creating iterators for efficient looping
import itertools

# Type hints
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal

# Holidays in Norway
import holidays

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


def first_last_date_quarter(year_str: str, quarter_str: str) -> tuple[str, str]:
    """Given a year and a quarter, this function calculates the first and last dates of the specified quarter using pandas.

    Args:
        year_str: The year as a string.
        quarter_str: The quarter as a string.

    Returns:
        A tuple containing two strings, the first and last dates of the specified
        quarter in 'YYYY-MM-DD' format.
    """
    # Convert input year and quarter strings to integers
    year = int(year_str)
    quarter = int(quarter_str)

    # Calculate the starting month of the quarter
    start_month = (quarter - 1) * 3 + 1

    # Create the start date of the quarter
    start_date = pd.Timestamp(year, start_month, 1)

    # Calculate the end date of the quarter
    end_date = start_date + pd.offsets.QuarterEnd()

    # Format dates as strings in 'YYYY-MM-DD' format
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    return start_date_str, end_date_str


def indicate_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    how: Literal["left", "right", "outer", "inner", "cross"],
    on: str | list[str],
) -> pd.DataFrame:
    """Perform a merge of two DataFrames and prints a frequency table indicating the merge type for each row.

    The merge types are determined as follows (left-to-right):
        - 'one-to-zero': Rows that exist only in the left DataFrame.
        - 'zero-to-one': Rows that exist only in the right DataFrame.
        - 'many-to-zero': Rows in the right DataFrame with multiple identical entries
          and no matching entries in the left DataFrame.
        - 'zero-to-many': Rows in the left DataFrame with multiple identical entries
          and no matching entries in the right DataFrame.
        - 'one-to-one': Rows that have a matching entry in both left and right
          DataFrames.
        - 'many-to-one': Rows in the right DataFrame with multiple matching entries in
          the left DataFrame.
        - 'one-to-many': Rows in the left DataFrame with multiple matching entries in
          the right DataFrame.
        - 'many-to-many': Rows in both left and right DataFrames with multiple matching
          entries.

    Args:
        left: The left DataFrame to be merged.
        right: The right DataFrame to be merged.
        how: The type of merge to be performed. Options are: 'inner', 'outer', 'left',
             'right'.
        on: A list of column names to merge on.

    Returns:
        The merged DataFrame.
    """
    # Perform the merge operation
    merged_df = pd.merge(left, right, how=how, on=on, indicator=True)

    # Convert _merge column to numpy
    np_merge = merged_df["_merge"].to_numpy()

    # Identify duplicate rows in each DataFrame
    duplicated_left = left.duplicated(subset=on, keep=False)
    duplicated_right = right.duplicated(subset=on, keep=False)

    # Different treatment depending on if "on" is a single column or not
    if isinstance(on, str):
        duplicated_from_left = (
            merged_df[on]
            .isin(left.loc[duplicated_left, on].drop_duplicates())
            .to_numpy()
        )
        duplicated_from_right = (
            merged_df[on]
            .isin(right.loc[duplicated_right, on].drop_duplicates())
            .to_numpy()
        )
    else:
        duplicated_from_left = (
            merged_df[on]
            .apply(tuple, axis=1)
            .isin(left[on][duplicated_left].drop_duplicates().apply(tuple, axis=1))
            .to_numpy()
        )
        duplicated_from_right = (
            merged_df[on]
            .apply(tuple, axis=1)
            .isin(right[on][duplicated_right].drop_duplicates().apply(tuple, axis=1))
            .to_numpy()
        )

    # Define the conditions and choices for np.select
    conditions = [
        np.logical_and(np_merge == "left_only", ~duplicated_from_left),
        np.logical_and(np_merge == "right_only", ~duplicated_from_right),
        np.logical_and(np_merge == "left_only", duplicated_from_left),
        np.logical_and(np_merge == "right_only", duplicated_from_right),
        np.logical_and(
            np_merge == "both",
            np.logical_and(~duplicated_from_left, ~duplicated_from_right),
        ),
        np.logical_and(
            np_merge == "both",
            np.logical_and(duplicated_from_left, ~duplicated_from_right),
        ),
        np.logical_and(
            np_merge == "both",
            np.logical_and(~duplicated_from_left, duplicated_from_right),
        ),
        np.logical_and(
            np_merge == "both",
            np.logical_and(duplicated_from_right, duplicated_from_left),
        ),
    ]

    choices = [
        "one-to-zero",
        "zero-to-one",
        "many-to-zero",
        "zero-to-many",
        "one-to-one",
        "many-to-one",
        "one-to-many",
        "many-to-many",
    ]

    # Use np.select to create new column
    merge_type = np.select(conditions, choices, default="unknown")

    # Print the frequency of each merge type
    unique, counts = np.unique(merge_type, return_counts=True)
    print(f"Sum of entries after merge: {merged_df.shape[0]}")
    for i, j in zip(unique, counts, strict=True):
        print(f"Number of entries of type '{i}': {j}")

    # Drop the _merge column and return the result
    merged_df.drop(columns="_merge", inplace=True)

    return merged_df


def pinterval(start_p: str, end_p: str, sep: str = "", freq: str = "m") -> list[str]:
    """This function generates a list of monthly or quarterly periods between two given periods.

    The periods are strings in the format 'YYYY<separator>MM' or 'YYYYMM' for monthly intervals,
    and 'YYYY<separator>Q' for quarterly intervals, where YYYY is a 4-digit year and MM is a 2-digit month
    (01 to 12) or Q is a 1-digit quarter (1 to 4). The function handles cases where the start and end
    periods are in the same year or in different years. The separator between year and month/quarter is customizable.

    Args:
        start_p: The start period in the format 'YYYY<sep>MM' or 'YYYYMM' for monthly intervals,
                 and 'YYYY<sep>Q' for quarterly intervals.
        end_p: The end period in the format 'YYYY<sep>MM' or 'YYYYMM' for monthly intervals,
               and 'YYYY<sep>Q' for quarterly intervals.
        sep: A string to separate the year and month/quarter. Defaults to empty.
        freq: The intervals frequency, 'm' for monthly or 'q' for quarterly. Defaults to 'm'.

    Returns:
        A list of strings representing the monthly or quarterly periods from start_p to end_p, inclusive.

    Raises:
        ValueError: If the frequency is not 'monthly' or 'quarterly'.
        ValueError: If the start and end period do not include the specified separator.

    Example:
    >>> pinterval('2022k1', '2023k2', sep='k', freq='quarterly')
    ['2022k1', '2022k2', '2022k3', '2022k4', '2023k1', '2023k2']
    """
    freq = freq[:1].lower()
    if freq not in ["m", "q"]:
        raise ValueError("Frequency needs to be either monthly or quarterly.")
    if sep not in start_p or sep not in end_p:
        raise ValueError(
            "Start and end period must be in the same format as the interval."
        )

    # Extract the year and month/quarter from the start and end periods based on the separator
    if sep:
        start_year, start_unit = start_p.split(sep)
        end_year, end_unit = end_p.split(sep)
    else:
        start_year, start_unit = start_p[:4], start_p[4:]
        end_year, end_unit = end_p[:4], end_p[4:]

    # Determine the range for the loop based on interval type
    unit_range = 4 if freq == "q" else 12

    # Initialize an empty list to store the periods
    interval = []

    # Generate the periods
    for year in range(int(start_year), int(end_year) + 1):
        start = int(start_unit) if year == int(start_year) else 1
        end = int(end_unit) if year == int(end_year) else unit_range

        for unit in range(start, end + 1):
            unit_str = str(unit).zfill(2) if freq == "m" else str(unit)
            formatted_period = f"{year}{sep}{unit_str}"

            interval.append(formatted_period)

    return interval


def proc_sums(
    df: pd.DataFrame,
    groups: list[str],
    values: list[str] | None = None,
    agg_func: dict[str, Any | list[Any]] | None = None,
) -> pd.DataFrame:
    """Compute aggregations for all combinations of columns and return a new DataFrame with these aggregations.

    Args:
        df: The input DataFrame.
        groups: List of columns to be considered for groupings.
        values: List of columns on which the aggregation functions will be applied.
               If None and agg_func is provided, it defaults to the keys of agg_func.
        agg_func: Dictionary mapping columns to aggregation functions corresponding to
            the 'values' list. If None, defaults to 'sum' for all columns in 'values'.
            Default None.

    Returns:
        A DataFrame containing aggregations for all combinations of 'columns'.

    Raises:
        ValueError: If any of the specified columns in 'groups' or 'values' are not
            present in the DataFrame.
        ValueError: If any columns in 'values' are not numeric and no aggregation
            function is provided.

    Note:
        - The returned DataFrame also contains an additional column named 'level'
          indicating the level of grouping.
        - Columns not used in a particular level of grouping will have a value 'Total'.
        - If 'values' is None and 'agg_func' is provided, 'values' is automatically
          set to the keys of 'agg_func'.
    """
    # Set 'values' based on 'agg_func' if 'values' is not provided
    if values is None:
        if agg_func is not None:
            values = list(agg_func.keys())
        else:
            values = []

    # Combine groups and values for column existence check
    required_columns = set(groups + values)

    # Initialize lists for missing and non-numeric columns
    missing_columns = []
    non_numeric_cols = []

    # Check for missing and non-numeric columns in a single loop
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)
        elif col in values and not pd.api.types.is_numeric_dtype(df[col]):
            non_numeric_cols.append(col)

    # Raise errors if necessary
    if missing_columns:
        raise ValueError(
            f"Columns {', '.join(missing_columns)} are not present in the dataframe!"
        )
    if non_numeric_cols and agg_func is None:
        raise ValueError(
            f"Values {', '.join(non_numeric_cols)} are not numeric! Specify aggregation functions!"
        )

    # Process 'agg_func' if provided
    if agg_func is not None:
        for col, funcs in agg_func.items():
            # If funcs is a list with exactly one item, use the item directly
            if isinstance(funcs, list) and len(funcs) == 1:
                agg_func[col] = funcs[0]
    else:
        # Default aggregation: 'sum' for all 'values' columns.
        agg_func = {col: "sum" for col in values}

    # Copy the dataframe and limit input to columns in the parameter
    df = df[list(required_columns)].copy()

    # Initialize empty datframe
    sum_df = pd.DataFrame()

    # Convert columns lists to sets for easier set operations.
    groups_set = set(groups)

    # Loop over all possible combinations of 'columns' for aggregation.
    for i in reversed(range(1, len(groups) + 1)):
        for subset in itertools.combinations(groups, i):
            # Convert subset of columns list to a set.
            subset_set = set(subset)
            # Group by the current subset of columns and aggregate.
            sub_sum = df.groupby(list(subset)).agg(agg_func).reset_index()
            # Check if there are missing columns in the subset
            sum_columns = list(groups_set - subset_set)
            if sum_columns:
                # For columns not in the current subset, fill with 'Total'.
                sub_sum[sum_columns] = "Total"
            # Indicate level of grouping
            sub_sum["level"] = i
            # Append this subset's aggregation results to the final DataFrame.
            sum_df = pd.concat([sum_df, sub_sum], ignore_index=True)
    return sum_df


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
