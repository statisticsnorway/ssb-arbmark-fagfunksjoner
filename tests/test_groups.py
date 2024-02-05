import numpy as np
import pandas as pd
import pytest

from ssb_arbmark_fagfunksjoner.groups import alder_5grp
from ssb_arbmark_fagfunksjoner.groups import alder_grp
from ssb_arbmark_fagfunksjoner.groups import landbakgrunn_grp
from ssb_arbmark_fagfunksjoner.groups import nace_sn07_17grp
from ssb_arbmark_fagfunksjoner.groups import nace_sn07_47grp
from ssb_arbmark_fagfunksjoner.groups import sektor2_grp
from ssb_arbmark_fagfunksjoner.groups import virk_str_8grp


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "alder_all": np.random.randint(0, 75, size=100),
            "alder": np.random.randint(15, 70, size=100),
            "nace_sn07": np.random.choice(
                ["49.100", "56.101", "84.110", "93.130", "95.110"], size=100
            ),
            "sektor": np.random.choice(["6100", "6500", "1510", "1520"], size=100),
            "undersektor": np.random.choice(["007", "008", "009"], size=100),
            "ansatte": np.random.randint(0, 300, size=100),
            "landbakgrunn": np.char.zfill(
                np.random.randint(0, 799, size=100).astype(str), 3
            ),
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


def test_nace_sn07_17grp(sample_df):
    df = sample_df
    df["nace_sn07_17grp"] = nace_sn07_17grp(df["nace_sn07"]).astype(str)
    assert (
        not df["nace_sn07_17grp"].isnull().any()
    ), "NACE SN07 17 group contains null values"


def test_nace_sn07_17grp_number(sample_df):
    df = sample_df
    df["nace_sn07_17grp"] = nace_sn07_17grp(df["nace_sn07"], display="number").astype(
        str
    )
    assert (
        not df["nace_sn07_17grp"].isnull().any()
    ), "NACE SN07 17 group contains null values"


def test_nace_sn07_17grp_combined(sample_df):
    df = sample_df
    df["nace_sn07_47grp"] = nace_sn07_47grp(df["nace_sn07"], display="combined").astype(
        str
    )
    df["nace_sn07_17grp"] = nace_sn07_17grp(
        df["nace_sn07_47grp"], display="combined"
    ).astype(str)
    assert (
        not df["nace_sn07_17grp"].isnull().any()
    ), "NACE SN07 17 group contains null values"


def test_sektor2_grp(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(df["sektor"], df["undersektor"]).astype(str)
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"


def test_sektor2_grp_number(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(
        df["sektor"], df["undersektor"], display="number"
    ).astype(str)
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"


def test_sektor2_grp_combined(sample_df):
    df = sample_df
    df["sektor2_grp"] = sektor2_grp(
        df["sektor"], df["undersektor"], display="combined"
    ).astype(str)
    assert not df["sektor2_grp"].isnull().any(), "Sector 2 group contains null values"


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
