import numpy as np
import pandas as pd
import pytest

import arbmark.groups.country_origin as klb
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


class FakeKlass:
    """Minimal fake for KlassClassification used in tests.

    It returns a .data DataFrame with columns ['code', 'parentCode'].
    We parametrize the mapping via the constructor.
    """

    def __init__(self, klass_id: int, mapping: dict[str, str] | None = None):
        """klass_id is ignored by the fake, but kept for signature compatibility."""
        self.klass_id = klass_id
        self._mapping = mapping or {
            # country -> parentCode (string so slicing works)
            "NOR": "EU1",
            "SWE": "EU1",
            "USA": "NA1",
            "JPN": "AS1",
        }

    def get_codes(self, select_level: str):
        # Return self with a .data attribute that looks like the real object
        # The functions only use .data[["code","parentCode"]]
        codes = []
        parents = []
        for code, parent in self._mapping.items():
            codes.append(code)
            parents.append(parent)
        self.data = pd.DataFrame({"code": codes, "parentCode": parents})
        return self


@pytest.fixture
def patch_klass_546(monkeypatch):
    """Monkeypatch KlassClassification used by koble_landbakgrunn_546."""

    def _factory(klass_id: int):
        # Ensure we were called with the expected classification id
        assert klass_id == 546
        return FakeKlass(klass_id)

    monkeypatch.setattr(klb, "KlassClassification", _factory)
    return _factory


@pytest.fixture
def patch_klass_545(monkeypatch):
    """Monkeypatch KlassClassification used by koble_landbakgrunn_545."""

    def _factory(klass_id: int):
        assert klass_id == 545
        return FakeKlass(klass_id)

    monkeypatch.setattr(klb, "KlassClassification", _factory)
    return _factory


@pytest.mark.parametrize(
    "func_name,fixture_name",
    [
        ("koble_landbakgrunn_546", "patch_klass_546"),
        ("koble_landbakgrunn_545", "patch_klass_545"),
    ],
)
def test_raises_when_land_col_missing(func_name, fixture_name, request):
    # Activate the right Klass patch
    request.getfixturevalue(fixture_name)

    func = getattr(klb, func_name)
    df = pd.DataFrame({"landkode": ["NOR", "USA"]})

    with pytest.raises(ValueError):
        func(df)  # land_col omitted / None

    with pytest.raises(ValueError):
        func(df, land_col="")  # falsy value should also raise


def test_koble_landbakgrunn_546_basic_mapping(patch_klass_546):
    df = pd.DataFrame({"landkode": ["NOR", "USA", "UNK"]})

    # Call function
    ret = klb.koble_landbakgrunn_546(df, land_col="landkode")

    # Same object returned (in-place mutation)
    assert ret is df

    # For 546: verdensdel == parentCode; landegruppe == verdensdel[:2]
    # Using FakeKlass mapping: NOR->EU1, USA->NA1, UNK unmapped
    expected_verdensdel = ["EU1", "NA1", np.nan]
    expected_landegruppe = ["EU", "NA", np.nan]

    assert ret["verdensdel"].tolist() == expected_verdensdel
    assert ret["landegruppe"].tolist() == expected_landegruppe

    # Column presence
    assert set(["verdensdel", "landegruppe"]).issubset(ret.columns)


def test_koble_landbakgrunn_545_basic_mapping(patch_klass_545):
    df = pd.DataFrame({"landkode": ["NOR", "USA", "UNK"]})

    # Call function
    ret = klb.koble_landbakgrunn_545(df, land_col="landkode")

    # Same object returned (in-place mutation)
    assert ret is df

    # For 545: verdensdel == parentCode[:2]; landegruppe == parentCode[:3]
    expected_verdensdel = ["EU", "NA", np.nan]
    expected_landegruppe = ["EU1", "NA1", np.nan]

    assert ret["verdensdel"].tolist() == expected_verdensdel
    assert ret["landegruppe"].tolist() == expected_landegruppe

    # Column presence
    assert set(["verdensdel", "landegruppe"]).issubset(ret.columns)


def test_koble_landbakgrunn_handles_various_codes(patch_klass_546):
    """Extra check with an augmented mapping to ensure slicing is robust."""
    # Override the default mapping with a custom one
    custom_mapping = {
        "NOR": "EU2",
        "USA": "NA3",
        "JPN": "AS9",
    }

    def factory(_klass_id: int):
        return FakeKlass(_klass_id, mapping=custom_mapping)

    # Replace the patched factory with our custom one for this test
    klb.KlassClassification = factory  # type: ignore

    df = pd.DataFrame({"landkode": ["NOR", "JPN", "USA", "UNK"]})
    ret = klb.koble_landbakgrunn_546(df, land_col="landkode")

    assert ret["verdensdel"].tolist() == ["EU2", "AS9", "NA3", np.nan]
    assert ret["landegruppe"].tolist() == ["EU", "AS", "NA", np.nan]


import pandas as pd
import pytest


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


class FakeKlass:
    """Minimal fake for KlassClassification used in tests.

    It returns a .data DataFrame with columns ['code', 'parentCode'].
    We parametrize the mapping via the constructor.
    """

    def __init__(self, klass_id: int, mapping: dict[str, str] | None = None):
        """klass_id is ignored by the fake, but kept for signature compatibility."""
        self.klass_id = klass_id
        self._mapping = mapping or {
            # country -> parentCode (string so slicing works)
            "NOR": "EU1",
            "SWE": "EU1",
            "USA": "NA1",
            "JPN": "AS1",
        }

    def get_codes(self, select_level: str):
        # Return self with a .data attribute that looks like the real object
        # The functions only use .data[["code","parentCode"]]
        codes = []
        parents = []
        for code, parent in self._mapping.items():
            codes.append(code)
            parents.append(parent)
        self.data = pd.DataFrame({"code": codes, "parentCode": parents})
        return self


@pytest.fixture
def patch_klass_546(monkeypatch):
    """Monkeypatch KlassClassification used by koble_landbakgrunn_546."""

    def _factory(klass_id: int):
        # Ensure we were called with the expected classification id
        assert klass_id == 546
        return FakeKlass(klass_id)

    monkeypatch.setattr(klb, "KlassClassification", _factory)
    return _factory


@pytest.fixture
def patch_klass_545(monkeypatch):
    """Monkeypatch KlassClassification used by koble_landbakgrunn_545."""

    def _factory(klass_id: int):
        assert klass_id == 545
        return FakeKlass(klass_id)

    monkeypatch.setattr(klb, "KlassClassification", _factory)
    return _factory


@pytest.mark.parametrize(
    "func_name,fixture_name",
    [
        ("koble_landbakgrunn_546", "patch_klass_546"),
        ("koble_landbakgrunn_545", "patch_klass_545"),
    ],
)
def test_raises_when_land_col_missing(func_name, fixture_name, request):
    # Activate the right Klass patch
    request.getfixturevalue(fixture_name)

    func = getattr(klb, func_name)
    df = pd.DataFrame({"landkode": ["NOR", "USA"]})

    with pytest.raises(ValueError):
        func(df)  # land_col omitted / None

    with pytest.raises(ValueError):
        func(df, land_col="")  # falsy value should also raise


def test_koble_landbakgrunn_546_basic_mapping(patch_klass_546):
    df = pd.DataFrame({"landkode": ["NOR", "USA", "UNK"]})

    # Call function
    ret = klb.koble_landbakgrunn_546(df, land_col="landkode")

    # Same object returned (in-place mutation)
    assert ret is df

    # For 546: verdensdel == parentCode; landegruppe == verdensdel[:2]
    # Using FakeKlass mapping: NOR->EU1, USA->NA1, UNK unmapped
    expected_verdensdel = ["EU1", "NA1", np.nan]
    expected_landegruppe = ["EU", "NA", np.nan]

    assert ret["verdensdel"].tolist() == expected_verdensdel
    assert ret["landegruppe"].tolist() == expected_landegruppe

    # Column presence
    assert set(["verdensdel", "landegruppe"]).issubset(ret.columns)


def test_koble_landbakgrunn_545_basic_mapping(patch_klass_545):
    df = pd.DataFrame({"landkode": ["NOR", "USA", "UNK"]})

    # Call function
    ret = klb.koble_landbakgrunn_545(df, land_col="landkode")

    # Same object returned (in-place mutation)
    assert ret is df

    # For 545: verdensdel == parentCode[:2]; landegruppe == parentCode[:3]
    expected_verdensdel = ["EU", "NA", np.nan]
    expected_landegruppe = ["EU1", "NA1", np.nan]

    assert ret["verdensdel"].tolist() == expected_verdensdel
    assert ret["landegruppe"].tolist() == expected_landegruppe

    # Column presence
    assert set(["verdensdel", "landegruppe"]).issubset(ret.columns)


def test_koble_landbakgrunn_handles_various_codes(patch_klass_546):
    """Extra check with an augmented mapping to ensure slicing is robust."""
    # Override the default mapping with a custom one
    custom_mapping = {
        "NOR": "EU2",
        "USA": "NA3",
        "JPN": "AS9",
    }

    def factory(_klass_id: int):
        return FakeKlass(_klass_id, mapping=custom_mapping)

    # Replace the patched factory with our custom one for this test
    klb.KlassClassification = factory  # type: ignore

    df = pd.DataFrame({"landkode": ["NOR", "JPN", "USA", "UNK"]})
    ret = klb.koble_landbakgrunn_546(df, land_col="landkode")

    assert ret["verdensdel"].tolist() == ["EU2", "AS9", "NA3", np.nan]
    assert ret["landegruppe"].tolist() == ["EU", "AS", "NA", np.nan]
