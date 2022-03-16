from aeromet_py import Taf


def test_sections_variated():
    code: str = """
    TAF OEDF 182100Z 1900/2006 16007KT 5000 BR NSC
        PROB30
        TEMPO 1902/1904 2000
        BECMG 1907/1909 13018KT 8000
        TEMPO 1918/2006 5000 BLDU SCT040 BKN080
        PROB30
        TEMPO 2000/2005 VRB25KT 3000 TSRA FEW030CB
    """
    taf = Taf(code)
    sections = [
        "TAF OEDF 182100Z 1900/2006 16007KT 5000 BR NSC",
        (
            "PROB30 TEMPO 1902/1904 2000"
            " BECMG 1907/1909 13018KT 8000"
            " TEMPO 1918/2006 5000 BLDU SCT040 BKN080"
            " PROB30 TEMPO 2000/2005 VRB25KT 3000 TSRA FEW030CB"
        ),
    ]

    assert taf.sections == sections
    assert taf.body == sections[0]
    assert taf.weather_changes == sections[1]


def test_sections_with_from():
    code: str = """
    TAF OKBK 190445Z 1906/2012 15015G25KT 6000 SCT040 BKN080
        PROB30
        TEMPO 1906/1915 2000 BLDU
        FM190900 0800 DS
    """
    taf = Taf(code)
    sections = [
        "TAF OKBK 190445Z 1906/2012 15015G25KT 6000 SCT040 BKN080",
        ("PROB30 TEMPO 1906/1915 2000 BLDU" " FM190900 0800 DS"),
    ]

    assert taf.sections == sections
    assert taf.body == sections[0]
    assert taf.weather_changes == sections[1]


def test_sections_no_weather_changes():
    code: str = "TAF MRPV 190500Z 1906/2006 10017G28KT CAVOK TX27/1919Z TN18/1911Z"
    taf = Taf(code)
    sections = [
        "TAF MRPV 190500Z 1906/2006 10017G28KT CAVOK TX27/1919Z TN18/1911Z",
        "",
    ]

    assert taf.sections == sections
    assert taf.body == sections[0]
    assert taf.weather_changes == sections[1]
