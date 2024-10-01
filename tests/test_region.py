from arbmark import get_valid_county_codes

def test_region() -> None:
    year = 2023
    test1_result = sort(get_valid_county_codes(year))
    test1_result_first = test1_result[0]
    
    test1_expected = "03"

    assert (
        test1_result_first == test1_expected
    ), f"Expected {test1_expected}, but got {test1_result_first}"
    
