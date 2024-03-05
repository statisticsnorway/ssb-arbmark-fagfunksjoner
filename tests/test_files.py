import os

from arbmark import read_latest


def test_read_latest() -> None:
    cwd = os.getcwd()
    result = read_latest(
        path=os.path.normpath(f"{cwd}/tests/test_data"), name="dataset"
    )
    expected = os.path.normpath(f"{cwd}/tests/test_data/dataset_v3.parquet")

    assert result == expected, f"Expected {expected}, but got {result}."
