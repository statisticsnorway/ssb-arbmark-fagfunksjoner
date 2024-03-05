import numpy as np
import pandas as pd
import pytest

from arbmark import landbakgrunn_grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "landbakgrunn": np.char.zfill(
                np.random.randint(0, 799, size=100).astype(str), 3
            ),
        }
    )


def test_landbakgrunn_grp(sample_df):
    df = sample_df
    df["verdensregion"] = landbakgrunn_grp(df["landbakgrunn"]).astype(str)
    assert not df["verdensregion"].isnull().any(), "World region contains null values"


def test_landbakgrunn_grp_number(sample_df):
    df = sample_df
    df["verdensregion"] = landbakgrunn_grp(df["landbakgrunn"], display="number").astype(
        str
    )
    assert not df["verdensregion"].isnull().any(), "World region contains null values"


def test_landbakgrunn_grp_combined(sample_df):
    df = sample_df
    df["verdensregion"] = landbakgrunn_grp(
        df["landbakgrunn"], display="combined"
    ).astype(str)
    assert not df["verdensregion"].isnull().any(), "World region contains null values"


def test_landbakgrunn_grp_arblonn(sample_df):
    df = sample_df
    df["verdensregion"] = landbakgrunn_grp(
        df["landbakgrunn"], display="arblonn"
    ).astype(str)
    assert not df["verdensregion"].isnull().any(), "World region contains null values"
