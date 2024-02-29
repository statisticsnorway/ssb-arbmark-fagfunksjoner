import numpy as np
import pandas as pd
import pytest

from arbmark import alder_5grp
from arbmark import alder_grp
from arbmark import landbakgrunn_grp
from arbmark import nace_sn07_47grp
from arbmark import nace_to_17_groups
from arbmark import sektor2_grp
from arbmark import virk_str_8grp


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
