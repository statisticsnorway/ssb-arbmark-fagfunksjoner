from arbmark import first_last_date_quarter


def test_first_last_date_quarter() -> None:
    test_cases = [
        ("2023", "1", ("2023-01-01", "2023-03-31")),
        ("2023", "2", ("2023-04-01", "2023-06-30")),
        ("2023", "3", ("2023-07-01", "2023-09-30")),
        ("2023", "4", ("2023-10-01", "2023-12-31")),
        # Add more test cases if necessary
    ]

    for year, quarter, expected in test_cases:
        result = first_last_date_quarter(year, quarter)
        assert (
            result == expected
        ), f"For {year} Q{quarter}, expected {expected}, but got {result}"
