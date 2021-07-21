from aeromet_py import Metar


def test_auto_modifier():
    metar = Metar("METAR KJST 060154Z AUTO 05007KT 10SM OVC085 13/01 A3004 RMK AO2 SLP174 T01280006")
    assert metar.modifier == "Automatic report"


def test_nil_modifier():
    metar = Metar("METAR KJST 060100Z NIL")
    assert metar.modifier == "Missing report"


def test_cor_modifier():
    metar = Metar("METAR MROC 202200Z COR 08011KT 9999 FEW045 SCT200 29/17 A2989 NOSIG")
    assert metar.modifier == "Correction"