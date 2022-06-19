from aeromet_py import Taf


def test_code():
    code = """
    TAF GCTS 232000Z 2321/2421 33005KT 9999 FEW030 TX22/2414Z TN14/2406Z
        TEMPO 2321/2324 03010KT
        BECMG 2411/2413 20010KT
        BECMG 2416/2417 10007KT
    """
    taf = Taf(code, year=2022, month=1)
    time = taf.time

    assert time.code == "232000Z"
    assert time.year == 2022
    assert time.month == 1
    assert time.day == 23
    assert time.hour == 20
    assert time.minute == 0
    assert str(time) == "2022-01-23 20:00:00"
