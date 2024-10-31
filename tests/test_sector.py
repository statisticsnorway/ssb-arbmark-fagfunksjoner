import numpy as np
import pandas as pd
import pytest

from arbmark import sektor2_grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sektor": np.random.choice(["6100", "6500", "1510", "1520"], size=100),
        }
    )


def test_sektor2_grp(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(df["sektor"]).astype(str)
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"


def test_sektor2_grp_number(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(df["sektor"], display="number").astype(str)
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"
