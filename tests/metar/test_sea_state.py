from aeromet_py import Metar
from pytest import approx


def test_sea_state_positive_temperature():
    metar = Metar(
        "METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA W20/S5"
    )
    sea_state = metar.sea_state

    assert sea_state.code == "W20/S5"
    assert sea_state.temperature_in_celsius == 20.0
    assert sea_state.temperature_in_fahrenheit == approx(68.0)
    assert sea_state.temperature_in_kelvin == 293.15
    assert sea_state.temperature_in_rankine == approx(527.67)
    assert sea_state.state == "rough"


def test_sea_state_negative_temperature():
    metar = Metar(
        "METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA WM01/S8"
    )
    sea_state = metar.sea_state

    assert sea_state.code == "WM01/S8"
    assert sea_state.temperature_in_celsius == -1.0
    assert sea_state.temperature_in_fahrenheit == approx(30.2)
    assert sea_state.temperature_in_kelvin == 272.15
    assert sea_state.temperature_in_rankine == approx(489.87)
    assert sea_state.state == "very high"
