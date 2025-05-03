from geolysis.utils.exceptions import ErrorMsg


def test_error_msg():
    error_msg = ErrorMsg(msg="testing")

    print(repr(error_msg))
    assert error_msg.msg == "testing"

    mod_msg = error_msg + "001"
    assert mod_msg == "testing001"

    mod_msg = "001" + error_msg
    assert mod_msg == "001testing"

    mod_msg = error_msg + 1
    assert mod_msg == "testing1"


def test_to_dict_default_message():
    err = ErrorMsg(param_name="limit",
                   param_value=150,
                   symbol="<=",
                   param_value_bound=100)

    expected = {
        "param_name": "limit",
        "param_value": 150,
        "symbol": "<=",
        "param_value_bound": 100,
        "message": "limit: 150 must be <= 100"
    }

    assert err.to_dict() == expected


def test_to_dict_with_custom_message():
    custom_msg = "Custom error message"
    err = ErrorMsg(param_name="threshold",
                   param_value=50,
                   symbol=">",
                   param_value_bound=20,
                   msg=custom_msg)

    expected = {
        "param_name": "threshold",
        "param_value": 50,
        "symbol": ">",
        "param_value_bound": 20,
        "message": custom_msg
    }

    assert err.to_dict() == expected
