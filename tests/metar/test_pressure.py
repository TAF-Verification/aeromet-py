from aeromet_py import Metar
from pytest import approx


def test_from_hpa():
    metar = Metar("METAR OESH 201700Z 06004KT CAVOK 31/00 Q1013 NOSIG")
    pressure = metar.pressure

    assert pressure.in_hecto_pascals == 1013.0
    assert pressure.in_mercury_inches == approx(29.91, rel=9.0e-04)
    assert pressure.in_milli_bars == 1013.0
    assert pressure.in_bars == approx(1.013)
    assert pressure.in_atmospheres == approx(0.999753269183321)
    assert str(pressure) == "1013.00 hPa"


def test_from_inhg():
    metar = Metar("METAR MMGL 201721Z 00000KT 7SM NSC 26/M07 A3025 RMK HZY CI")
    pressure = metar.pressure

    assert pressure.in_hecto_pascals == approx(1024.38, rel=1.0e-03)
    assert pressure.in_mercury_inches == approx(30.25)
    assert pressure.in_milli_bars == approx(1024.38, rel=1.0e-03)
    assert pressure.in_bars == approx(1.02438, rel=2.0e-06)
    assert pressure.in_atmospheres == approx(1.0109864144314047)
    assert str(pressure) == "1024.38 hPa"


def test_no_pressure():
    metar = Metar(
        "SPECI KMIA 152353Z 00000KT 10SM FEW024 BKN150 BKN250 27/23 A//// RMK AO2 RAB2254E04 SLP127 P0000 60029 T02670233 10317 20256 50004 $"
    )
    pressure = metar.pressure

    assert pressure.in_hecto_pascals == None
    assert pressure.in_mercury_inches == None
    assert pressure.in_milli_bars == None
    assert pressure.in_bars == None
    assert pressure.in_atmospheres == None
    assert str(pressure) == "////"
