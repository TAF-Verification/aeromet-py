from pytest import raises

from aeromet_py import Taf
from aeromet_py.models import RangeError


_year: int = 2018
_month: int = 10


def test_three_changes():
    code = """
    TAF UNOO 061700Z 0618/0718 22007G13MPS 6000 -SHSN BKN010 BKN025CB
        TEMPO 0618/0706 1000 SHSN BLSN VV004
        BECMG 0700/0702 26006G12MPS
        BECMG 0708/0710 27007G13MPS
    """
    taf = Taf(code)
    changes = taf.change_periods

    assert len(changes) == 3
    assert changes.codes == [
        "TEMPO 0618/0706 1000 SHSN BLSN VV004",
        "BECMG 0700/0702 26006G12MPS",
        "BECMG 0708/0710 27007G13MPS",
    ]

    change0 = changes[0]
    assert change0.code == "TEMPO 0618/0706 1000 SHSN BLSN VV004"
    assert change0.change_indicator.code == "TEMPO 0618/0706"
    assert (
        change0.change_indicator.translation
        == "temporary from 2022-03-06 18:00:00 until 2022-03-07 06:00:00"
    )

    change1 = changes[1]
    assert change1.code == "BECMG 0700/0702 26006G12MPS"
    assert change1.change_indicator.code == "BECMG 0700/0702"
    assert (
        change1.change_indicator.translation
        == "becoming from 2022-03-07 00:00:00 until 2022-03-07 02:00:00"
    )

    change2 = changes[2]
    assert change2.code == "BECMG 0708/0710 27007G13MPS"
    assert change2.change_indicator.code == "BECMG 0708/0710"
    assert (
        change2.change_indicator.translation
        == "becoming from 2022-03-07 08:00:00 until 2022-03-07 10:00:00"
    )

    with raises(IndexError):
        assert changes[3].code == None

    with raises(RangeError):
        assert changes[8].code == None


def test_six_changes():
    code = """
    TAF KATL 062027Z 0620/0724 21010G20KT P6SM BKN050
        FM070000 17005KT P6SM FEW250
        FM070500 20010KT P6SM SCT050
        FM071700 22015G25KT P6SM BKN030
        PROB30 0717/0721 4SM -SHRA BR OVC015
        FM072200 24015G25KT 6SM -SHRA BR BKN035
        PROB30 TEMPO 0722/0724 4SM TSRA BR OVC025CB
    """
    taf = Taf(code, year=_year, month=_month)
    changes = taf.change_periods

    assert len(changes) == 6
    assert changes.codes == [
        "FM070000 17005KT P6SM FEW250",
        "FM070500 20010KT P6SM SCT050",
        "FM071700 22015G25KT P6SM BKN030",
        "PROB30 0717/0721 4SM -SHRA BR OVC015",
        "FM072200 24015G25KT 6SM -SHRA BR BKN035",
        "PROB30 TEMPO 0722/0724 4SM TSRA BR OVC025CB",
    ]

    change0 = changes[0]
    assert change0.code == "FM070000 17005KT P6SM FEW250"
    assert change0.change_indicator.code == "FM070000"
    assert (
        change0.change_indicator.translation
        == "from 2018-10-07 00:00:00 until 2018-10-07 04:00:00"
    )

    change1 = changes[1]
    assert change1.code == "FM070500 20010KT P6SM SCT050"
    assert change1.change_indicator.code == "FM070500"
    assert (
        change1.change_indicator.translation
        == "from 2018-10-07 05:00:00 until 2018-10-07 16:00:00"
    )

    change2 = changes[2]
    assert change2.code == "FM071700 22015G25KT P6SM BKN030"
    assert change2.change_indicator.code == "FM071700"
    assert (
        change2.change_indicator.translation
        == "from 2018-10-07 17:00:00 until 2018-10-07 21:00:00"
    )

    change3 = changes[3]
    assert change3.code == "PROB30 0717/0721 4SM -SHRA BR OVC015"
    assert change3.change_indicator.code == "PROB30 0717/0721"
    assert (
        change3.change_indicator.translation
        == "probability 30% from 2018-10-07 17:00:00 until 2018-10-07 21:00:00"
    )

    change4 = changes[4]
    assert change4.code == "FM072200 24015G25KT 6SM -SHRA BR BKN035"
    assert change4.change_indicator.code == "FM072200"
    assert (
        change4.change_indicator.translation
        == "from 2018-10-07 22:00:00 until 2018-10-08 00:00:00"
    )

    change5 = changes[5]
    assert change5.code == "PROB30 TEMPO 0722/0724 4SM TSRA BR OVC025CB"
    assert change5.change_indicator.code == "PROB30 TEMPO 0722/0724"
    assert (
        change5.change_indicator.translation
        == "probability 30% temporary from 2018-10-07 22:00:00 until 2018-10-08 00:00:00"
    )

    with raises(IndexError):
        assert changes[6].code == None

    with raises(RangeError):
        assert changes[8].code == None


def test_no_changes():
    code = "TAF KPHX 062100Z 0621/0724 27007KT P6SM FEW070"
    taf = Taf(code)
    changes = taf.change_periods

    assert len(changes) == 0
    assert changes.codes == []

    with raises(IndexError):
        assert changes[0].code == None

    with raises(RangeError):
        assert changes[8].code == None
