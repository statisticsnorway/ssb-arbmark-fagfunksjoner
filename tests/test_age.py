import numpy as np
import pandas as pd
import pytest

from arbmark import alder_5grp
from arbmark import alder_grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "alder_all": np.random.randint(0, 75, size=100),
            "alder": np.random.randint(15, 70, size=100),
        }
    )


def test_alder_5grp(sample_df):
    df = sample_df
    df["alder_5grp"] = alder_5grp(df["alder_all"]).astype(str)
    assert not df["alder_5grp"].isnull().any(), "Age group contains null values"


def test_alder_5grp_number(sample_df):
    df = sample_df
    df["alder_5grp"] = alder_5grp(df["alder_all"], display="number").astype(str)
    assert not df["alder_5grp"].isnull().any(), "Age group contains null values"


def test_alder_5grp_combined(sample_df):
    df = sample_df
    df["alder_5grp"] = alder_5grp(df["alder_all"], display="combined").astype(str)
    assert not df["alder_5grp"].isnull().any(), "Age group contains null values"


def test_alder_grp(sample_df):
    df = sample_df
    df["alder_grp"] = alder_grp(df["alder"]).astype(str)
    assert not df["alder_grp"].isnull().any(), "Age group contains null values"


def test_alder_grp_number(sample_df):
    df = sample_df
    df["alder_grp"] = alder_grp(df["alder"], display="number").astype(str)
    assert not df["alder_grp"].isnull().any(), "Age group contains null values"


def test_alder_grp_combined(sample_df):
    df = sample_df
    df["alder_grp"] = alder_grp(df["alder"], display="combined").astype(str)
    assert not df["alder_grp"].isnull().any(), "Age group contains null values"
