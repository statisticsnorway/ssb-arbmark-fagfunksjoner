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
