from aeromet_py import Metar


def test_auto_modifier():
    metar = Metar(
        "METAR KJST 060154Z AUTO 05007KT 10SM OVC085 13/01 A3004 RMK AO2 SLP174 T01280006"
    )

    assert metar.modifier.code == "AUTO"
    assert metar.modifier.modifier == "Automatic report"
    assert str(metar.modifier) == "automatic report"
    assert metar.modifier.as_dict() == {"code": "AUTO", "modifier": "Automatic report"}


def test_nil_modifier():
    metar = Metar("METAR KJST 060100Z NIL")

    assert metar.modifier.code == "NIL"
    assert metar.modifier.modifier == "Missing report"
    assert str(metar.modifier) == "missing report"
    assert metar.modifier.as_dict() == {"code": "NIL", "modifier": "Missing report"}


def test_cor_modifier():
    metar = Metar("METAR MROC 202200Z COR 08011KT 9999 FEW045 SCT200 29/17 A2989 NOSIG")

    assert metar.modifier.code == "COR"
    assert metar.modifier.modifier == "Correction"
    assert str(metar.modifier) == "correction"
    assert metar.modifier.as_dict() == {"code": "COR", "modifier": "Correction"}


def test_no_modifier():
    metar = Metar(
        "SPECI UUDD 152330Z 29005MPS 9999 SCT019 07/04 Q1014 R32L/290042 NOSIG"
    )

    assert metar.modifier.code == None
    assert metar.modifier.modifier == None
    assert str(metar.modifier) == ""
    assert metar.modifier.as_dict() == {"code": None, "modifier": None}
