import pytest

from aeromet_py import Taf
from aeromet_py.models import RangeError


def test_two_taf_weathers():
    code = """
    TAF RKNY 282300Z 0100/0206 27010KT 5000 +RA BR BKN015 TX11/0105Z TN01/0121Z
        BECMG 0101/0102 28015G30KT SCT030
        BECMG 0105/0106 34010KT
        BECMG 0111/0112 27012KT
        BECMG 0123/0124 27015G25KT
        BECMG 0202/0203 27017G35KT
    """
    taf = Taf(code)
    weathers = taf.weathers

    assert weathers.codes == ["+RA", "BR"]
    assert str(weathers) == "heavy rain | mist"

    assert weathers[0].intensity == "heavy"
    assert weathers[0].description == None
    assert weathers[0].precipitation == "rain"
    assert weathers[0].obscuration == None
    assert weathers[0].other == None

    assert weathers[1].intensity == None
    assert weathers[1].description == None
    assert weathers[1].precipitation == None
    assert weathers[1].obscuration == "mist"
    assert weathers[1].other == None

    with pytest.raises(IndexError):
        weathers[2].code = None
