from aeromet_py import Metar


def test_code():
    metar = Metar(
        "SPECI UUDD 212130Z COR 35003MPS 320V020 CAVOK 18/12 Q1008 R88/60D NOSIG",
        year=2021,
        month=7,
    )
    time = metar.time

    assert time.code == "212130Z"
    assert time.year == 2021
    assert time.month == 7
    assert time.day == 21
    assert time.hour == 21
    assert time.minute == 30
    assert str(time) == "2021-07-21 21:30:00"
