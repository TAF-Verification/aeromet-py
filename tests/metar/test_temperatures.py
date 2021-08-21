from aeromet_py import Metar
from pytest import approx

def test_positive_temperatures():
    metar = Metar("METAR LHBP 191530Z 17007KT 9999 VCSH FEW018CB SCT029 04/02 Q1015 NOSIG")
    temperatures = metar.temperatures
    
    assert temperatures.code == '04/02'
    assert temperatures.temperature_in_celsius == 4.0
    assert temperatures.temperature_in_kelvin == 277.15
    assert temperatures.temperature_in_fahrenheit == approx(39.2)
    assert temperatures.temperature_in_rankine == approx(498.87)
    assert temperatures.dewpoint_in_celsius == 2.0
    assert temperatures.dewpoint_in_kelvin == 275.15
    assert temperatures.dewpoint_in_fahrenheit == approx(35.6)
    assert temperatures.dewpoint_in_rankine == approx(495.27)


def test_negative_temperatures():
    metar = Metar("METAR LHBP 191530Z 17007KT 9999 VCSH FEW018CB SCT029 M01/M04 Q1015 NOSIG")
    temperatures = metar.temperatures
    
    assert temperatures.code == 'M01/M04'
    assert temperatures.temperature_in_celsius == -1.0
    assert temperatures.temperature_in_kelvin == 272.15
    assert temperatures.temperature_in_fahrenheit == approx(30.2)
    assert temperatures.temperature_in_rankine == approx(489.87)
    assert temperatures.dewpoint_in_celsius == -4.0
    assert temperatures.dewpoint_in_kelvin == 269.15
    assert temperatures.dewpoint_in_fahrenheit == approx(24.8)
    assert temperatures.dewpoint_in_rankine == approx(484.47)


def test_none_temperatures():
    metar = Metar("METAR MSSS 182050Z 17011KT 130V220 9999 FEW060 ///// Q1012 A2990")
    temperatures = metar.temperatures
    
    assert temperatures.code == '/////'
    assert temperatures.temperature_in_celsius == None
    assert temperatures.temperature_in_kelvin == None
    assert temperatures.temperature_in_fahrenheit == None
    assert temperatures.temperature_in_rankine == None
    assert temperatures.dewpoint_in_celsius == None
    assert temperatures.dewpoint_in_kelvin == None
    assert temperatures.dewpoint_in_fahrenheit == None
    assert temperatures.dewpoint_in_rankine == None