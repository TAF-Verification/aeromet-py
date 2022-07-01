from pytest import approx

from aeromet_py import Taf


def test_visibility_from_sea_miles():
    code = """
    KATL 282202Z 2822/0124 04006KT P6SM SKC
        FM010100 00000KT P6SM SKC
        FM010800 33003KT P6SM BKN250
        FM011700 29005KT P6SM SKC
    """
    taf = Taf(code)
    visibility = taf.prevailing_visibility

    assert visibility.code == "P6SM"
    assert visibility.in_meters == 11_112.0
    assert visibility.in_kilometers == 11.112
    assert visibility.in_sea_miles == approx(6.0)
    assert visibility.in_feet == approx(36_456.7)
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "11.1 km"
    assert visibility.as_dict() == {
        "cavok": False,
        "code": "P6SM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 11112.0, "units": "meters"},
    }
