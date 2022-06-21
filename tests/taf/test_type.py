from aeromet_py import Taf


def test_taf_type_first_sample():
    code = """
    TAF UUDD 221352Z 2215/2321 22007MPS 9999 BKN016 TX04/2215Z TNM03/2321Z
        TEMPO 2215/2221 22012G17MPS 2000 SHSNRA FEW007 BKN016CB
        BECMG 2306/2308 28007MPS
        BECMG 2315/2317 28002MPS
    """
    taf = Taf(code)
    assert taf.type_.code == "TAF"
    assert taf.type_.type == "Terminal Aerodrome Forecast"
    assert str(taf.type_) == "Terminal Aerodrome Forecast (TAF)"


def test_taf_type_second_sample():
    code = """
    TAF MMPQ 221654Z 2218/2318 10015KT P6SM SCT020
        FM230300 13010KT P6SM BKN010
        TEMPO 2308/2312 3SM -RA BKN005
        FM231500 12010KT 4SM HZ SCT010
    """
    taf = Taf(code)
    assert taf.type_.code == "TAF"
    assert taf.type_.type == "Terminal Aerodrome Forecast"
    assert str(taf.type_) == "Terminal Aerodrome Forecast (TAF)"


def test_no_taf_type():
    code = """
    MRLM 221100Z 2212/2312 24005KT 9999 FEW025 TX30/2221Z TN19/2311Z
        BECMG 2215/2217 07006KT
        BECMG 2300/2303 25004KT
    """
    taf = Taf(code)
    assert taf.type_.code == "TAF"
    assert taf.type_.type == "Terminal Aerodrome Forecast"
    assert str(taf.type_) == "Terminal Aerodrome Forecast (TAF)"
