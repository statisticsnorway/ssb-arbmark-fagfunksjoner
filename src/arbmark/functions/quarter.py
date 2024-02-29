# Pandas for table management
import pandas as pd


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
