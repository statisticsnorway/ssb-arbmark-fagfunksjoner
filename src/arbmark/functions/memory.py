import inspect

import pandas as pd


def list_dataframes(namespace: dict | None = None) -> pd.DataFrame:
    """Returnerer en oversikt over alle pandas-DataFrames i et namespace.

    Hvis namespace ikke er oppgitt, brukes caller sitt globale namespace.
    Bruker trenger kun å skrive ``list_dataframes()``.
    """
    if namespace is None:
        frame = inspect.currentframe()
        if frame is None or frame.f_back is None:
            raise ValueError("Klarte ikke finne namespace automatisk.")
        namespace = frame.f_back.f_globals

    dfs = []

    for name, obj in namespace.items():
        if isinstance(obj, pd.DataFrame):
            size_mb = obj.memory_usage(deep=True).sum() / (1024**2)
            dfs.append((name, obj.shape, size_mb))

    df_summary = pd.DataFrame(dfs, columns=["navn", "shape", "minne_MB"])

    if df_summary.empty:
        return df_summary

    return df_summary.sort_values("minne_MB", ascending=False).reset_index(drop=True)
