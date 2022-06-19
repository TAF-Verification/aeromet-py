from aeromet_py import Taf


def test_AMD_modifier():
    code = """
    TAF AMD MGPB 231700Z 2318/2418 07008KT 9999 SCT018 TX30/2320Z TN21/2412Z
        PROB40
        TEMPO 2322/2412 8000 VCSH BKN016
        BECMG 2400/2402 00000KT SCT016
        BECMG 2416/2418 06008KT SCT018
    """
    taf = Taf(code)

    assert taf.modifier.code == "AMD"
    assert taf.modifier.modifier == "Amendment"
    assert str(taf.modifier) == "amendment"


def test_COR_modifier():
    code = """
    TAF COR SKBO 231630Z 2318/2418 28010KT 9999 SCT023
        TEMPO 2319/2323 5000 TSRA SCT018CB
        BECMG 2400/2402 VRB02KT
        PROB40
        TEMPO 2410/2412 5000 BCFG SCT010 TX21/2318Z TN09/2410Z
    """
    taf = Taf(code)

    assert taf.modifier.code == "COR"
    assert taf.modifier.modifier == "Correction"
    assert str(taf.modifier) == "correction"


def test_no_modifier():
    code = """
    TAF SKCG 231630Z 2318/2418 35015KT 9999 FEW020
        TX33/2319Z TN23/2410Z
        BECMG 2402/2404 VRB02KT
    """
    taf = Taf(code)

    assert taf.modifier.code == None
    assert taf.modifier.modifier == None
    assert str(taf.modifier) == ""
