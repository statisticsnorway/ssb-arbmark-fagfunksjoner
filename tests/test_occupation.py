from arbmark import nyk08yrkeregsys1


def test_nyk08yrkeregsys1() -> None:
    occupation_codes = pd.Series(["24", "5421", "9999", "0111101"])
    
    test1_result = nyk08yrkeregsys1()

    expected_output = np.array(["2", "5", "0b", "3_01-03"])
    
    output = nyk08yrkeregsys1(occupation_codes)
    
    assert np.array_equal(output, expected_output), f"Expected {expected_output}, but got {output}"