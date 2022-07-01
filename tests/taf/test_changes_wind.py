from pytest import raises, approx

from aeromet_py import Taf


def test_three_wind_changes():
    code = """
    TAF OPRK 262145Z 2700/2718 23005KT 3000 FU NSC TN18/2701Z TX40/2710Z
        FM270700 23010KT 5000 HZ NSC
        FM271200 11005KT 9999 SCT020
        PROB30 RA
    """
    taf = Taf(code)
    changes = taf.change_periods

    wind0 = changes[0].wind
    assert wind0.code == "23010KT"
    assert wind0.cardinal_direction == "SW"
    assert wind0.direction_in_degrees == 230.0
    assert wind0.direction_in_radians == 4.014257279586958
    assert wind0.variable == False
    assert wind0.speed_in_knot == 10.0
    assert wind0.speed_in_mps == 5.1444444
    assert wind0.speed_in_kph == 18.52
    assert wind0.gust_in_knot == None
    assert wind0.gust_in_mps == None
    assert wind0.gust_in_miph == None
    assert str(wind0) == "SW (230.0°) 10.0 kt"
    assert wind0.as_dict() == {
        "code": "23010KT",
        "direction": {
            "cardinal": "SW",
            "direction": 230.0,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": None, "units": "knot"},
        "speed": {"speed": 10.0, "units": "knot"},
    }

    wind1 = changes[1].wind
    assert wind1.code == "11005KT"
    assert wind1.cardinal_direction == "ESE"
    assert wind1.direction_in_degrees == 110.0
    assert wind1.direction_in_radians == 1.9198621771937625
    assert wind1.variable == False
    assert wind1.speed_in_knot == 5.0
    assert wind1.speed_in_mps == 2.5722222
    assert wind1.speed_in_kph == 9.26
    assert wind1.gust_in_knot == None
    assert wind1.gust_in_mps == None
    assert wind1.gust_in_miph == None
    assert str(wind1) == "ESE (110.0°) 5.0 kt"
    assert wind1.as_dict() == {
        "code": "11005KT",
        "direction": {
            "cardinal": "ESE",
            "direction": 110.0,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": None, "units": "knot"},
        "speed": {"speed": 5.0, "units": "knot"},
    }

    wind2 = changes[2].wind
    assert wind2.code == None
    assert wind2.cardinal_direction == None
    assert wind2.direction_in_degrees == None
    assert wind2.direction_in_radians == None
    assert wind2.variable == False
    assert wind2.speed_in_knot == None
    assert wind2.speed_in_mps == None
    assert wind2.speed_in_kph == None
    assert wind2.gust_in_knot == None
    assert wind2.gust_in_mps == None
    assert wind2.gust_in_miph == None
    assert str(wind2) == ""
    assert wind2.as_dict() == {
        "code": None,
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "gust": {"speed": None, "units": "knot"},
        "speed": {"speed": None, "units": "knot"},
    }
