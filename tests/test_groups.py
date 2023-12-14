import numpy as np
import pandas as pd
import pytest

from ssb_arbmark_fagfunksjoner.functions import alder_grp
from ssb_arbmark_fagfunksjoner.functions import nace_sn07_17grp
from ssb_arbmark_fagfunksjoner.functions import nace_sn07_47grp
from ssb_arbmark_fagfunksjoner.functions import sektor2_grp
from ssb_arbmark_fagfunksjoner.functions import virk_str_8grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "alder": np.random.randint(15, 70, size=100),
            "nace_sn07": [f"{i:02d}" for i in np.random.randint(1, 100, size=100)],
            "sektor": np.random.choice(["6100", "6500", "1510", "1520"], size=100),
            "undersektor": np.random.choice(["007", "008", "009"], size=100),
            "ansatte": np.random.randint(0, 300, size=100),
        }
    )


def test_alder_grp(sample_df):
    df = sample_df
    df["alder_grp"] = alder_grp(df["alder"])
    assert not df["alder_grp"].isnull().any(), "Age group contains null values"
    assert df["alder_grp"].dtype == "string", "Age group is not of type string"


def test_nace_sn07_47grp(sample_df):
    df = sample_df
    df["nace_sn07_47grp"] = nace_sn07_47grp(df["nace_sn07"])
    assert (
        not df["nace_sn07_47grp"].isnull().any()
    ), "NACE SN07 47 group contains null values"
    assert (
        df["nace_sn07_47grp"].dtype == "string"
    ), "NACE SN07 47 group is not of type string"


def test_nace_sn07_17grp(sample_df):
    df = sample_df
    df["nace_sn07_17grp"] = nace_sn07_17grp(df["nace_sn07"])
    assert (
        not df["nace_sn07_17grp"].isnull().any()
    ), "NACE SN07 17 group contains null values"
    assert (
        df["nace_sn07_17grp"].dtype == "string"
    ), "NACE SN07 17 group is not of type string"


def test_sektor2_grp(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(df["sektor"], df["undersektor"])
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"
    assert df["sektor2_grp"].dtype == "string", "Sector 2 group is not of type string"


def test_virk_str_8grp(sample_df):
    df = sample_df
    df["virk_str_8grp"] = virk_str_8grp(df["ansatte"])
    assert not df["virk_str_8grp"].isnull().any(), "Employee group contains null values"
    assert df["virk_str_8grp"].dtype == "string", "Employee group is not of type string"
