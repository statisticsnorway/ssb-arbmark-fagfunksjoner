import pandas as pd

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
