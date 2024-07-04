# Type hints
from typing import TYPE_CHECKING, Any

# Pandas for table management
import pandas as pd

if TYPE_CHECKING:
    PdSeriesAny = pd.Series[Any]  # type: ignore[misc]
else:
    PdSeriesAny = pd.Series

def sb_integer(number: PdSeriesAny, unit: int = 0) -> PdSeriesAny:
    """
    Format a pandas Series of numbers as rounded integers, with optional unit scaling.

    Args:
        number (pd.Series): A pandas Series containing numeric values.
        unit (int, optional): The power of 10 to which to round the numbers. Default is 0 (no scaling).

    Returns:
        pd.Series: A pandas Series with the numbers rounded to the specified unit, 
                   converted to strings, and with NaNs replaced by empty strings.
    """
    return (
        number
        .fillna(-1 * 10**abs(unit))  # Replace NaN values with a placeholder
        .round(-abs(unit))  # Round numbers to the nearest specified unit
        .astype(int)  # Convert the Series to integer type
        .astype(str)  # Convert the Series to string type
        .replace(f"{-1 * 10**abs(unit)}", "")  # Replace placeholder with empty strings
    )

def sb_percent(fraction: PdSeriesAny, decimals: int = 1) -> PdSeriesAny:
    """
    Convert a pandas Series of fractions to percentages, formatted as strings.

    Args:
        fraction (pd.Series): A pandas Series containing fractional values (e.g., 0.25 for 25%).
        decimals (int, optional): Number of decimal places to round the percentage values to. Default is 1.

    Returns:
        pd.Series: A pandas Series with the percentage values formatted as strings, 
                   with a comma as the decimal separator and empty strings for NaNs and infinities.
    """
    return (
        fraction
        .multiply(100)  # Convert fractions to percentages
        .round(decimals)  # Round to the specified number of decimal places
        .fillna('')  # Replace NaN values with empty strings
        .astype(str)  # Convert the Series to string type
        .replace('inf', '')  # Replace 'inf' strings with empty strings
        .str.replace('.', ',')  # Replace periods with commas
    )
