import numpy as np
import pandas as pd
import pytest

from arbmark import nace_sn07_47grp
from arbmark import nace_to_17_groups


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "nace_sn07": np.random.choice(
                ["49.100", "56.101", "84.110", "85.421", "93.130", "95.110"], size=100
            ),
        }
    )


def test_nace_sn07_47grp(sample_df):
    df = sample_df
    df["nace_sn07_47grp"] = nace_sn07_47grp(df["nace_sn07"]).astype(str)
    assert (
        not df["nace_sn07_47grp"].isnull().any()
    ), "NACE SN07 47 group contains null values"


def test_nace_sn07_47grp_number(sample_df):
    df = sample_df
    df["nace_sn07_47grp"] = nace_sn07_47grp(df["nace_sn07"], display="number").astype(
        str
    )
    assert (
        not df["nace_sn07_47grp"].isnull().any()
    ), "NACE SN07 47 group contains null values"


def test_nace_sn07_47grp_combined(sample_df):
    df = sample_df
    df["nace_sn07_47grp"] = nace_sn07_47grp(df["nace_sn07"], display="combined").astype(
        str
    )
    assert (
        not df["nace_sn07_47grp"].isnull().any()
    ), "NACE SN07 47 group contains null values"


def test_nace_to_17_groups(sample_df):
    df = sample_df
    df["nace_sn07_17grp"] = nace_to_17_groups(df["nace_sn07"]).astype(str)
    assert (
        not df["nace_sn07_17grp"].nunique == 1
    ), "NACE 17 group only found 1 group, likely did not find any matches to map"


def test_nace_to_17_groups_label(sample_df):
    df = sample_df
    df["nace_sn07_17grp"] = nace_to_17_groups(df["nace_sn07"], label=True).astype(str)
    assert (
        not df["nace_sn07_17grp"].isnull().any()
    ), "NACE 17 group contains null values"
