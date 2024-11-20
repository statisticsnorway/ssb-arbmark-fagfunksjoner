"""This function is outdated use 'all_combos_agg' from ssb-fagfunksjoner instead."""

# Itertools for functions creating iterators for efficient looping
from itertools import combinations

# Type hints
from typing import Any

# Pandas for table management
import pandas as pd


def proc_sums(
    df: pd.DataFrame,
    groups: list[str],
    values: list[str] | None = None,
    agg_func: dict[str, Any | list[Any]] | None = None,
) -> pd.DataFrame:
    """Compute aggregations for combinations of columns and return a new DataFrame with these aggregations.
    
    This function is outdated use 'all_combos_agg' from ssb-fagfunksjoner instead.

    Args:
        df: The input DataFrame.
        groups: List of columns to be considered for groupings.
        values: List of columns on which the aggregation functions will be applied.
               If None and agg_func is provided, it defaults to the keys of agg_func.
        agg_func: Dictionary mapping columns to aggregation functions corresponding to
            the 'values' list. If None, defaults to 'sum' for all columns in 'values'.
            Default None.

    Returns:
        A DataFrame containing aggregations for all combinations of 'groups' with
        an additional 'level' column indicating the level of grouping.

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
    print(
        "This function is outdated use 'all_combos_agg' from ssb-fagfunksjoner instead."
    )
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
        # Default aggregation: 'sum' for all 'values' columns
        agg_func = {col: "sum" for col in values}

    # Copy the dataframe and limit input to columns in the parameter
    df_limited = df[list(required_columns)].copy()

    # Create a copy of the limited dataframe to calculate totals
    totals_df = df_limited.copy()

    # Assign a constant value "Total" to the group column(s) for aggregation
    totals_df[groups] = "Total"

    # Aggregate data using the specified 'agg_func'
    sum_df = totals_df.groupby(groups).agg(agg_func).reset_index()

    # Add the 'level' column
    sum_df["level"] = 0

    # Convert columns lists to sets for easier set operations
    groups_set = set(groups)

    # Loop over all possible combinations of 'columns' for aggregation
    for i in range(1, len(groups) + 1):
        for subset in combinations(groups, i):
            # Convert subset of columns list to a set
            subset_set = set(subset)
            # Group by the current subset of columns and aggregate
            sub_sum = df_limited.groupby(list(subset)).agg(agg_func).reset_index()
            # Check if there are missing columns in the subset
            sum_columns = list(groups_set - subset_set)
            if sum_columns:
                # For columns not in the current subset, fill with 'Total'
                sub_sum[sum_columns] = "Total"
            # Indicate level of grouping
            sub_sum["level"] = i
            # Append this subset's aggregation results to the final DataFrame
            sum_df = pd.concat([sum_df, sub_sum], ignore_index=True)
    return sum_df
