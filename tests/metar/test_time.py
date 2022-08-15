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
    assert time.as_dict() == {"code": "212130Z", "datetime": "2021-07-21 21:30:00"}


def test_no_code():
    metar = Metar(
        "METAR UUDD NIL",
        year=2021,
        month=7,
    )
    date2str = f"2021-07-01 00:00:00"
    time = metar.time

    assert time.code == None
    assert time.year == 2021
    assert time.month == 7
    assert time.day == 1
    assert time.hour == 0
    assert time.minute == 0
    assert str(time) == date2str
    assert time.as_dict() == {"code": None, "datetime": date2str}
