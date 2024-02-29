from arbmark import pinterval


def test_pinterval_q() -> None:
    test_cases = [
        ("2022k3", "2022k4", ["2022k3", "2022k4"]),
        ("2022k2", "2023k1", ["2022k2", "2022k3", "2022k4", "2023k1"]),
        (
            "2021k3",
            "2023k2",
            [
                "2021k3",
                "2021k4",
                "2022k1",
                "2022k2",
                "2022k3",
                "2022k4",
                "2023k1",
                "2023k2",
            ],
        ),
    ]

    for start_p, slutt_p, expected in test_cases:
        result = pinterval(start_p, slutt_p, sep="k", freq="quarterly")
        assert (
            result == expected
        ), f"For {start_p} to {slutt_p}, expected {expected}, but got {result}"


def test_pinterval_m() -> None:
    test_cases = [
        ("202203", "202204", ["202203", "202204"]),
        (
            "202108",
            "202202",
            [
                "202108",
                "202109",
                "202110",
                "202111",
                "202112",
                "202201",
                "202202",
            ],
        ),
    ]

    for start_p, slutt_p, expected in test_cases:
        result = pinterval(start_p, slutt_p)
        assert (
            result == expected
        ), f"For {start_p} to {slutt_p}, expected {expected}, but got {result}"
