"""A collection of useful functions.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""


# Itertools for functions creating iterators for efficient looping
import itertools

# Type hints
from typing import Any
from typing import Literal
from typing import Optional

# Holidays in Norway
import holidays

# Numpy for data wrangling
import numpy as np

# Pandas for table management
import pandas as pd


def count_workdays(from_dates: pd.Series, to_dates: pd.Series) -> pd.Series:
    """Counts the number of workdays between pairs of dates in given series.

    This function calculates the number of workdays for each pair of start and end dates provided in the `from_dates` and `to_dates` series. It handles date ranges spanning multiple years and excludes weekends and holidays specific to Norway. The function dynamically fetches Norwegian holidays for the relevant years based on the input dates.

    Args:
        from_dates (pd.Series): A pandas Series containing the start dates of the periods.
        to_dates (pd.Series): A pandas Series containing the end dates of the periods.

    Returns:
        pd.Series: A Pandas Series containing the number of workdays for each date pair.

    Raises:
        ValueError: If the length of the calculated workdays list does not match the number of date pairs.

    Note:
        - The function can handle date ranges spanning multiple years.
        - Holidays are determined based on the Norwegian calendar for each year in the date range.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy()
    to_dates_np = to_dates.to_numpy()

    # Extract the year from the from_dates and to_dates arrays
    from_years = from_dates_np.astype("datetime64[Y]").astype(int) + 1970
    to_years = to_dates_np.astype("datetime64[Y]").astype(int) + 1970

    # Find the max and min years
    min_year = np.min(from_years)
    max_year = np.max(to_years)

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
    for from_date, to_date in zip(from_dates_d, to_dates_d):
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
        year_str (str): The year as a string.
        quarter_str (str): The quarter as a string.

    Returns:
        tuple: A tuple containing two strings, the first and
        last dates of the specified quarter in 'YYYY-MM-DD' format.
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
    - 'many-to-zero': Rows in the right DataFrame with multiple identical entries and no matching entries in the left DataFrame.
    - 'zero-to-many': Rows in the left DataFrame with multiple identical entries and no matching entries in the right DataFrame.
    - 'one-to-one': Rows that have a matching entry in both left and right DataFrames.
    - 'many-to-one': Rows in the right DataFrame with multiple matching entries in the left DataFrame.
    - 'one-to-many': Rows in the left DataFrame with multiple matching entries in the right DataFrame.
    - 'many-to-many': Rows in both left and right DataFrames with multiple matching entries.

    Args:
        left (pd.DataFrame): The left DataFrame to be merged.
        right (pd.DataFrame): The right DataFrame to be merged.
        how (str): The type of merge to be performed. Options are: 'inner', 'outer', 'left', 'right'.
        on (list): A list of column names to merge on.

    Returns:
        pd.DataFrame: The merged DataFrame.
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
    for i, j in zip(unique, counts):
        print(f"Number of entries of type '{i}': {j}")

    # Drop the _merge column and return the result
    merged_df.drop(columns="_merge", inplace=True)

    return merged_df


def kv_intervall(start_p: str, slutt_p: str) -> list[str]:
    """This function generates a list of quarterly periods between two given periods.

    The periods are strings in the format 'YYYYkQ', where YYYY is a 4-digit year and Q is a quarter (1 to 4). The function handles cases where the start and end periods are in the same year or in different years.

    Parameters:
    start_p (str): The start period in the format 'YYYYkQ'.
    slutt_p (str): The end period in the format 'YYYYkQ'.

    Returns:
    list: A list of strings representing the quarterly periods from start_p to slutt_p, inclusive.

    Example:
    >>> kv_intervall('2022k3', '2023k2')
    ['2022k3', '2022k4', '2023k1', '2023k2']
    """
    # Extract the year and quarter from the start period
    start_aar4 = int(start_p[:4])
    start_kv = int(start_p[-1])

    # Extract the year and quarter from the end period
    slutt_aar4 = int(slutt_p[:4])
    slutt_kv = int(slutt_p[-1])

    # Initialize an empty list to store the periods
    intervall = []

    # Generate the periods
    for i in range(start_aar4, slutt_aar4 + 1):
        if start_aar4 == slutt_aar4:
            # If the start and end periods are in the same year
            for j in range(start_kv, slutt_kv + 1):
                intervall.append(f"{i}k{j}")
        elif i == start_aar4:
            # If the current year is the start year
            for j in range(start_kv, 4 + 1):
                intervall.append(f"{i}k{j}")
        elif start_aar4 < i and slutt_aar4 > i:
            # If the current year is between the start and end years
            for j in range(1, 4 + 1):
                intervall.append(f"{i}k{j}")
        elif i == slutt_aar4:
            # If the current year is the end year
            for j in range(1, slutt_kv + 1):
                intervall.append(f"{i}k{j}")

    return intervall


def proc_sums(
    df: pd.DataFrame,
    groups: list[str],
    values: list[str],
    agg_func: Optional[dict[str, Any | list[Any]]] = None,
) -> pd.DataFrame:
    """Compute aggregations for all combinations of columns and return a new DataFrame with these aggregations.

    Parameters:
        df : pd.DataFrame
            The input DataFrame.
        groups : list[str]
            List of columns to be considered for groupings.
        values : list[str]
            List of columns on which the aggregation functions will be applied.
        agg_func : Optional[Dict[str, Callable]], default None
            Dictionary mapping columns to aggregation functions corresponding to
            the 'values' list. If None, defaults to 'sum' for all columns in 'values'.

    Returns:
        pd.DataFrame: A DataFrame containing aggregations for all combinations of 'columns'.

    Raises:
        ValueError: If any of the specified columns in 'groups' or 'values' are not present in the DataFrame.
        ValueError: If any columns in 'values' are not numeric and no aggregation function is provided.

    Notes:
        - The returned DataFrame also contains an additional column named 'level'
          indicating the level of grouping.
        - Columns not used in a particular level of grouping will have a value 'Total'.
    """
    # All columns used from the input dataframe
    required_columns = groups + values

    # Check that the parameters references columns in the dataframe
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Columns {', '.join(missing_columns)} are not present in the dataframe!"
        )

    # Check if all columns in 'values' are numeric
    non_numeric_cols = [
        col for col in values if not pd.api.types.is_numeric_dtype(df[col])
    ]

    # Copy the dataframe and limit input to columns in the parameter
    df = df[required_columns].copy()

    if agg_func is not None:
        for col, funcs in agg_func.items():
            # Check if funcs is a list
            if isinstance(funcs, list) and len(funcs) == 1:
                # If funcs is a list with exactly one item, extract that item
                agg_func[col] = funcs[0]
    elif agg_func is None:
        if not non_numeric_cols:
            # Default aggregation: 'sum' for all 'values' columns.
            agg_func = {col: "sum" for col in values}
        else:
            raise ValueError(
                f"Values {', '.join(non_numeric_cols)} are not numeric! Specify aggregation functions!"
            )

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


def ref_day(from_dates: pd.Series, to_dates: pd.Series) -> pd.Series:
    """Determines if the reference day falls between given date ranges.

    This function checks if the 16th day of each month (reference day) is within the range specified by the corresponding 'from_dates' and 'to_dates'. It requires that both 'from_dates' and 'to_dates' are in the same year and month.

    Args:
        from_dates (pd.Series): A Series of dates representing the start of a period.
            These dates should be in the 'YYYY-MM-DD' format.
        to_dates (pd.Series): A Series of dates representing the end of a period.
            These dates should also be in the 'YYYY-MM-DD' format.

    Returns:
        np.ndarray: An array of booleans. Each element corresponds to whether the
        16th day of the month for each period is within the respective date range.

    Raises:
        ValueError: If 'from_dates' and 'to_dates' are not in the same year, or if they are not in the same month, or if multiple years are present across the dates.
    """
    # Convert the from_dates and to_dates columns to numpy arrays
    from_dates_np = from_dates.to_numpy().astype("datetime64[D]")
    to_dates_np = to_dates.to_numpy().astype("datetime64[D]")

    # Extract the year from the from_dates array
    year = from_dates_np.astype("datetime64[Y]").astype(int) + 1970

    # Check if the year is the same in the to_dates array
    if not np.all(year == to_dates_np.astype("datetime64[Y]").astype(int) + 1970):
        # If the year is not the same, raise an error
        raise ValueError("Function can only be applied to dates in the same year!")

    # Check if there is more than one unique year in the array
    if np.unique(year).size > 1:
        # If there is more than one unique year, raise an error
        raise ValueError("Function can only be applied to a single year!")

    # Extract the month from the from_dates array
    month = from_dates_np.astype("datetime64[M]").astype(int) % 12 + 1

    # Check if the month is the same in the to_dates array
    if not np.all(month == to_dates_np.astype("datetime64[M]").astype(int) % 12 + 1):
        # If the month is not the same, raise an error
        raise ValueError("Function can only be applied to dates in the same months!")

    # Create a reference day for each month
    ref_days = np.array([f"{year[0]}-{m:02d}-16" for m in month], dtype="datetime64[D]")

    # Check if the reference day is within the range of the from_date and to_date
    result = np.logical_and(from_dates_np <= ref_days, ref_days <= to_dates_np)

    # Return the result as an array of boolean values
    return pd.Series(result, dtype="boolean")


def ref_week(from_dates: pd.Series, to_dates: pd.Series) -> pd.Series:
    """Determines if any date in each date range falls in the reference week.

    This function checks if any date between the 'from_dates' and 'to_dates' is within the reference week. The reference week is defined as the week which includes the 16th day of each month. It requires that both 'from_dates' and 'to_dates' are in the same year and the same month.

    Args:
        from_dates (pd.Series): A Series of dates representing the start of a period.
            These dates should be in the 'YYYY-MM-DD' format.
        to_dates (pd.Series): A Series of dates representing the end of a period.
            These dates should also be in the 'YYYY-MM-DD' format.

    Returns:
        pd.Series: A Series of booleans, where each boolean corresponds to whether any date in the period from 'from_dates' to 'to_dates' falls within the reference week of the month.

    Raises:
        ValueError: If 'from_dates' and 'to_dates' are not in the same year, or if they are not in the same month.
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
            [f"{y}-{m:02d}-16" for y, m in zip(from_dates.dt.year, from_dates.dt.month)]
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
