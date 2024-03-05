# Type hints
from typing import Literal

# Holidays in Norway
# Numpy for data wrangling
import numpy as np

# Pandas for table management
import pandas as pd


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
