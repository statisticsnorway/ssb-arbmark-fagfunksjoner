import pandas as pd
import pytest

from arbmark.functions.memory import list_dataframes


def test_list_dataframes_basic():
    df1 = pd.DataFrame({"a": [1, 2, 3]})
    df2 = pd.DataFrame({"b": [4, 5]})

    namespace = {
        "df1": df1,
        "df2": df2,
        "not_df": [1, 2, 3],
    }

    result = list_dataframes(namespace)

    assert len(result) == 2
    assert "df1" in result["navn"].values
    assert "df2" in result["navn"].values


def test_empty_namespace():
    result = list_dataframes({})

    assert result.empty
    assert list(result.columns) == ["navn", "shape", "minne_MB"]


def _call_list_dataframes():
    return list_dataframes()


def test_list_dataframes_auto_namespace():
    global df_test_auto
    df_test_auto = pd.DataFrame({"a": [1, 2, 3]})

    result = _call_list_dataframes()

    assert "df_test_auto" in result["navn"].values


def test_list_dataframes_raises_valueerror_when_frame_is_none(monkeypatch):
    monkeypatch.setattr("arbmark.functions.memory.inspect.currentframe", lambda: None)

    with pytest.raises(ValueError, match="Klarte ikke finne namespace automatisk"):
        list_dataframes()


class MockFrame:
    f_back = None


def test_list_dataframes_raises_valueerror_when_f_back_is_none(monkeypatch):
    monkeypatch.setattr(
        "arbmark.functions.memory.inspect.currentframe",
        lambda: MockFrame(),
    )

    with pytest.raises(ValueError, match="Klarte ikke finne namespace automatisk"):
        list_dataframes()
