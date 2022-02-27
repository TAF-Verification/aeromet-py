from aeromet_py import Taf


def test_cancelled_taf():
    code = "TAF FKKD 271700Z 2718/2824 CNL"
    taf = Taf(code)

    assert taf.cancelled.code == "CNL"
    assert taf.cancelled.is_cancelled == True
    assert str(taf.cancelled) == "cancelled"


def test_no_cancelled_taf():
    code = """
    TAF FKKD 271700Z 2718/2824 VRB03KT 9999 SCT016 FEW020CB
        PROB30 2718/2720 TS
        TEMPO 2722/2807 BKN013 FEW016CB
        TEMPO 2805/2807 2000 BR
    """
    taf = Taf(code)

    assert taf.cancelled.code == None
    assert taf.cancelled.is_cancelled == False
    assert str(taf.cancelled) == ""
