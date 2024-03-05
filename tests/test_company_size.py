import numpy as np
import pandas as pd
import pytest

from arbmark import virk_str_8grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"ansatte": np.random.randint(0, 300, size=100)})


def test_virk_str_8grp(sample_df):
    df = sample_df
    df["virk_str_8grp"] = virk_str_8grp(df["ansatte"]).astype(str)
    assert not df["virk_str_8grp"].isnull().any(), "Employee group contains null values"


def test_virk_str_8grp_number(sample_df):
    df = sample_df
    df["virk_str_8grp"] = virk_str_8grp(df["ansatte"], display="number").astype(str)
    assert not df["virk_str_8grp"].isnull().any(), "Employee group contains null values"


def test_virk_str_8grp_combined(sample_df):
    df = sample_df
    df["virk_str_8grp"] = virk_str_8grp(df["ansatte"], display="combined").astype(str)
    assert not df["virk_str_8grp"].isnull().any(), "Employee group contains null values"
