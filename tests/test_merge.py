import numpy as np
import pandas as pd

from arbmark import indicate_merge


def test_indicate_merge() -> None:
    dfa = pd.DataFrame(
        {
            "id": [i for i in np.random.randint(0, 1000, size=100)],
            "a": [i for i in np.random.randint(0, 10, size=100)],
        }
    )
    dfb = pd.DataFrame(
        {
            "id": [i for i in np.random.randint(0, 1000, size=100)],
            "b": [i for i in np.random.randint(0, 10, size=100)],
        }
    )
    result = indicate_merge(dfa, dfb, on="id", how="outer")
    expected = pd.merge(dfa, dfb, on="id", how="outer")
    assert result.equals(
        expected
    ), "Function indicate_merge did not return an exact merge."
