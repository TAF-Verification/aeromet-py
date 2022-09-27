from aeromet_py import Taf

_year: int = 2019
_month: int = 3


def test_0606_valid_period():
    code = """
    TAF KATL 250357Z 2506/2606 21006KT P6SM FEW045
        FM251000 23008KT P6SM BKN020
        FM251300 27009KT P6SM VCSH SCT010 BKN015
        FM251800 31011G18KT P6SM BKN025
        FM252100 31012G18KT P6SM FEW035 FEW150
        FM260000 32009KT P6SM FEW060
    """
    taf = Taf(code, year=_year, month=_month)
    valid = taf.valid

    assert valid.code == "2506/2606"
    assert valid.duration.total_seconds() / 60 / 60 == 24.0
    assert str(valid) == "from 2019-03-25 06:00:00 until 2019-03-26 06:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 3
    assert valid.period_from.day == 25
    assert valid.period_from.hour == 6
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2019
    assert valid.period_until.month == 3
    assert valid.period_until.day == 26
    assert valid.period_until.hour == 6
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "2506/2606",
        "from_": {"code": None, "datetime": "2019-03-25 06:00:00"},
        "until": {"code": None, "datetime": "2019-03-26 06:00:00"},
    }


def test_0024_valid_period():
    code = """
    TAF MROC 302300Z 3100/3124 09015KT CAVOK TX29/2519Z TN19/2511Z
        TEMPO 3112/3120 08015G28KT
    """
    taf = Taf(code, year=_year, month=_month)
    valid = taf.valid

    assert valid.code == "3100/3124"
    assert valid.duration.total_seconds() / 60 / 60 == 24.0
    assert str(valid) == "from 2019-03-31 00:00:00 until 2019-04-01 00:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 3
    assert valid.period_from.day == 31
    assert valid.period_from.hour == 0
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2019
    assert valid.period_until.month == 4
    assert valid.period_until.day == 1
    assert valid.period_until.hour == 0
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "3100/3124",
        "from_": {"code": None, "datetime": "2019-03-31 00:00:00"},
        "until": {"code": None, "datetime": "2019-04-01 00:00:00"},
    }


def test_0306_valid_period():
    code = """
    KBWI 250258Z 2503/2606 08006KT 2SM -RA BR OVC008
        TEMPO 2503/2507 2SM -FZRA BKN005
        FM250700 10005KT 2SM RA BR OVC008
        FM250900 00000KT 1SM -RA BR OVC005
        FM251300 00000KT 3SM -RA BR OVC015
        FM251600 27013G25KT 6SM BR FEW015 SCT250
        FM252200 31016G25KT P6SM FEW250
    """
    taf = Taf(code, year=_year, month=_month)
    valid = taf.valid

    assert valid.code == "2503/2606"
    assert valid.duration.total_seconds() / 60 / 60 == 27.0
    assert str(valid) == "from 2019-03-25 03:00:00 until 2019-03-26 06:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 3
    assert valid.period_from.day == 25
    assert valid.period_from.hour == 3
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2019
    assert valid.period_until.month == 3
    assert valid.period_until.day == 26
    assert valid.period_until.hour == 6
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "2503/2606",
        "from_": {"code": None, "datetime": "2019-03-25 03:00:00"},
        "until": {"code": None, "datetime": "2019-03-26 06:00:00"},
    }


def test_1806_valid_period():
    code = """
    KSEA 021730Z 0218/0306 VRB03KT P6SM SKC
        FM022000 35006KT P6SM SKC
    """
    taf = Taf(code, year=_year, month=_month)
    valid = taf.valid

    assert valid.code == "0218/0306"
    assert valid.duration.total_seconds() / 60 / 60 == 12.0
    assert str(valid) == "from 2019-03-02 18:00:00 until 2019-03-03 06:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 3
    assert valid.period_from.day == 2
    assert valid.period_from.hour == 18
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2019
    assert valid.period_until.month == 3
    assert valid.period_until.day == 3
    assert valid.period_until.hour == 6
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "0218/0306",
        "from_": {"code": None, "datetime": "2019-03-02 18:00:00"},
        "until": {"code": None, "datetime": "2019-03-03 06:00:00"},
    }


def test_0012_valid_period():
    code = """
    KFLL 052312Z 0600/0612 10009KT P6SM FEW025
        FM060800 10011KT P6SM FEW025 SCT050
    """
    taf = Taf(code, year=_year, month=_month)
    valid = taf.valid

    assert valid.code == "0600/0612"
    assert valid.duration.total_seconds() / 60 / 60 == 12.0
    assert str(valid) == "from 2019-03-06 00:00:00 until 2019-03-06 12:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 3
    assert valid.period_from.day == 6
    assert valid.period_from.hour == 0
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2019
    assert valid.period_until.month == 3
    assert valid.period_until.day == 6
    assert valid.period_until.hour == 12
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "0600/0612",
        "from_": {"code": None, "datetime": "2019-03-06 00:00:00"},
        "until": {"code": None, "datetime": "2019-03-06 12:00:00"},
    }


def test_0024_with_year_change_valid_period():
    code = """
    TAF FKKD 302300Z 3100/3124 VRB05KT 8000 BKN013 FEW016CB
        TEMPO 3105/3107 2000 BR
        BECMG 3106/3108 BKN016 FEW020CB
    """
    taf = Taf(code, year=_year, month=12)
    valid = taf.valid

    assert valid.code == "3100/3124"
    assert valid.duration.total_seconds() / 60 / 60 == 24.0
    assert str(valid) == "from 2019-12-31 00:00:00 until 2020-01-01 00:00:00"
    assert valid.period_from.year == 2019
    assert valid.period_from.month == 12
    assert valid.period_from.day == 31
    assert valid.period_from.hour == 0
    assert valid.period_from.minute == 0
    assert valid.period_until.year == 2020
    assert valid.period_until.month == 1
    assert valid.period_until.day == 1
    assert valid.period_until.hour == 0
    assert valid.period_until.minute == 0
    assert valid.as_dict() == {
        "code": "3100/3124",
        "from_": {"code": None, "datetime": "2019-12-31 00:00:00"},
        "until": {"code": None, "datetime": "2020-01-01 00:00:00"},
    }
