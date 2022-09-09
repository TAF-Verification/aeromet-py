from aeromet_py import Metar
from pytest import approx


def test_from_hpa():
    metar = Metar("METAR OESH 201700Z 06004KT CAVOK 31/00 Q1013 NOSIG")
    pressure = metar.pressure

    assert pressure.code == "Q1013"
    assert pressure.in_hPa == 1013.0
    assert pressure.in_inHg == approx(29.91, rel=9.0e-04)
    assert pressure.in_mbar == 1013.0
    assert pressure.in_bar == approx(1.013)
    assert pressure.in_atm == approx(0.999753269183321)
    assert str(pressure) == "1013.0 hPa"
    assert pressure.as_dict() == {"pressure": 1013.0, "units": "hectopascals"}


def test_from_inhg():
    metar = Metar("METAR MMGL 201721Z 00000KT 7SM NSC 26/M07 A3025 RMK HZY CI")
    pressure = metar.pressure

    assert pressure.code == "A3025"
    assert pressure.in_hPa == approx(1024.38, rel=1.0e-03)
    assert pressure.in_inHg == approx(30.25)
    assert pressure.in_mbar == approx(1024.38, rel=1.0e-03)
    assert pressure.in_bar == approx(1.02438, rel=2.0e-06)
    assert pressure.in_atm == approx(1.0109864144314047)
    assert str(pressure) == "1024.4 hPa"
    assert pressure.as_dict() == {"pressure": 1024.3819844226, "units": "hectopascals"}


def test_two_pressures_from_hPa_and_inHg():
    metar = Metar("METAR MSSS 091250Z 00000KT 5000 BR FEW040CB 22/21 Q1013 A2993")
    pressure = metar.pressure

    assert pressure.code == "A2993"
    assert pressure.in_hPa == approx(1013.54, rel=5.0e-2)
    assert pressure.in_inHg == approx(29.91, rel=9.0e-04)
    assert pressure.in_mbar == approx(1013.54, rel=5.0e-2)
    assert pressure.in_bar == approx(1.013, rel=5.0e-3)
    assert pressure.in_atm == approx(1.00029, rel=1.0e-5)
    assert str(pressure) == "1013.5 hPa"
    assert pressure.as_dict() == {"pressure": 1013.5455469015, "units": "hectopascals"}


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
