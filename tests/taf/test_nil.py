from aeromet_py import Taf


def test_nil_taf():
    code = """TAF LFBE 231700Z NIL"""
    taf = Taf(code)
    missing = taf.missing

    assert missing.code == "NIL"
    assert missing.is_missing == True
    assert missing.modifier == "Missing report"
    assert str(missing) == "missing report"


def test_no_nil_taf():
    code = """
    TAF LFBE 231700Z 2318/2418 VRB03KT CAVOK
        PROB40
        TEMPO 2402/2407 3000 BR NSC
        BECMG 2412/2414 BKN020
        PROB30
        TEMPO 2414/2416 4000 -SHRA BKN020TCU
    """
    taf = Taf(code)
    missing = taf.missing

    assert missing.code == None
    assert missing.is_missing == False
    assert missing.modifier == None
    assert str(missing) == ""
