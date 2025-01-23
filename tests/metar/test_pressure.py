from typing import List

import pytest
from pytest import approx

from aeromet_py import Metar

from . import ureg, PyMetar


class PythonMetarPressure:
    def __init__(self, code: str) -> None:
        metar = PyMetar.Metar(code)
        self.value = metar.press.value("IN") * ureg.inHg

    def convert(self, unit: str):
        value = self.value.to(unit)
        return value.magnitude


codes: List[str] = [
    ["METAR OESH 201700Z 06004KT CAVOK 31/00 Q1013 NOSIG", "Q1013"],
    ["METAR MMGL 201721Z 00000KT 7SM NSC 26/M07 A3025 RMK HZY CI", "A3025"],
    ["METAR MSSS 091250Z 00000KT 5000 BR FEW040CB 22/21 Q1013 A2993", "A2993"],
]


@pytest.mark.parametrize(
    "press,code,qnh",
    [(PythonMetarPressure(code[0]), code[0], code[1]) for code in codes],
)
def test_pressure_qnh(press, code, qnh):
    metar = Metar(code=code)
    pressure = metar.pressure

    assert pressure.code == qnh
    assert pressure.in_hPa == approx(press.convert("hPa"), rel=1e-3)
    assert pressure.in_inHg == approx(press.value.magnitude, rel=1e-3)
    assert pressure.in_mbar == approx(press.convert("mbar"), rel=1e-3)
    assert pressure.in_bar == approx(press.convert("bar"), rel=1e-3)
    assert pressure.in_atm == approx(press.convert("atm"), rel=1e-3)

    press_str_in_hPa = f"{press.convert('hPa'):.1f}"
    assert str(pressure) == f"{press_str_in_hPa} hPa"
    assert pressure.as_dict() == {
        "pressure": approx(float(press_str_in_hPa), rel=1e-3),
        "units": "hectopascals",
    }


def test_no_pressure():
    metar = Metar(
        "SPECI KMIA 152353Z 00000KT 10SM FEW024 BKN150 BKN250 27/23 A//// RMK AO2 RAB2254E04 SLP127 P0000 60029 T02670233 10317 20256 50004 $"
    )
    pressure = metar.pressure

    assert pressure.code == "A////"
    assert pressure.in_hPa == None
    assert pressure.in_inHg == None
    assert pressure.in_mbar == None
    assert pressure.in_bar == None
    assert pressure.in_atm == None
    assert str(pressure) == ""
    assert pressure.as_dict() == {"pressure": None, "units": "hectopascals"}
