from aeromet_py import Metar
from pytest import approx


def test_sea_state_with_positive_temperature():
    metar = Metar(
        "METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA W20/S5"
    )
    sea_state = metar.sea_state

    assert sea_state.code == "W20/S5"
    assert sea_state.state == "rough"
    assert str(sea_state) == "temperature 20.0°C, no significant wave height, rough"
    assert sea_state.temperature_in_celsius == 20.0
    assert sea_state.temperature_in_fahrenheit == approx(68.0)
    assert sea_state.temperature_in_kelvin == 293.15
    assert sea_state.temperature_in_rankine == approx(527.67)
    assert sea_state.height_in_meters == None
    assert sea_state.height_in_centimeters == None
    assert sea_state.height_in_decimeters == None
    assert sea_state.height_in_feet == None
    assert sea_state.height_in_inches == None
    assert sea_state.as_dict() == {
        "code": "W20/S5",
        "height": {"distance": None, "units": "meters"},
        "state": "rough",
        "temperature": {"temperature": 20.0, "units": "celsius"},
    }


def test_sea_state_with_negative_temperature():
    metar = Metar(
        "METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA WM01/S8"
    )
    sea_state = metar.sea_state

    assert sea_state.code == "WM01/S8"
    assert sea_state.state == "very high"
    assert str(sea_state) == "temperature -1.0°C, no significant wave height, very high"
    assert sea_state.temperature_in_celsius == -1.0
    assert sea_state.temperature_in_fahrenheit == approx(30.2)
    assert sea_state.temperature_in_kelvin == 272.15
    assert sea_state.temperature_in_rankine == approx(489.87)
    assert sea_state.height_in_meters == None
    assert sea_state.height_in_centimeters == None
    assert sea_state.height_in_decimeters == None
    assert sea_state.height_in_feet == None
    assert sea_state.height_in_inches == None
    assert sea_state.as_dict() == {
        "code": "WM01/S8",
        "height": {"distance": None, "units": "meters"},
        "state": "very high",
        "temperature": {"temperature": -1.0, "units": "celsius"},
    }


def test_sea_state_with_significant_wave_height():
    metar = Metar(
        "METAR LXGB 032250Z 25006KT CAVOK 16/07 Q1022 W15/H008 NOSIG RMK BLU BLU"
    )
    sea_state = metar.sea_state

    assert sea_state.code == "W15/H008"
    assert sea_state.state == None
    assert (
        str(sea_state)
        == "temperature 15.0°C, significant wave height 0.8 m, no sea state"
    )
    assert sea_state.temperature_in_celsius == 15.0
    assert sea_state.temperature_in_fahrenheit == 59.0
    assert sea_state.temperature_in_kelvin == 288.15
    assert sea_state.temperature_in_rankine == approx(518.67)
    assert sea_state.height_in_meters == 0.8
    assert sea_state.height_in_centimeters == 80.0
    assert sea_state.height_in_decimeters == 8.0
    assert sea_state.height_in_feet == approx(2.62467)
    assert sea_state.height_in_inches == approx(31.49608)
    assert sea_state.as_dict() == {
        "code": "W15/H008",
        "height": {"distance": 0.8, "units": "meters"},
        "state": None,
        "temperature": {"temperature": 15.0, "units": "celsius"},
    }


def test_no_sea_state():
    metar = Metar("METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA")
    sea_state = metar.sea_state

    assert sea_state.code == None
    assert sea_state.state == None
    assert str(sea_state) == ""
    assert sea_state.temperature_in_celsius == None
    assert sea_state.temperature_in_fahrenheit == None
    assert sea_state.temperature_in_kelvin == None
    assert sea_state.temperature_in_rankine == None
    assert sea_state.height_in_meters == None
    assert sea_state.height_in_centimeters == None
    assert sea_state.height_in_decimeters == None
    assert sea_state.height_in_feet == None
    assert sea_state.height_in_inches == None
    assert sea_state.as_dict() == {
        "code": None,
        "height": {"distance": None, "units": "meters"},
        "state": None,
        "temperature": {"temperature": None, "units": "celsius"},
    }
