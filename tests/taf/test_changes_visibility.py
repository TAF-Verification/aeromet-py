from pytest import approx

from aeromet_py import Taf


def test_changes_visibility_from_sea_miles():
    code = """
    TAF KATL 282202Z 2822/0124 04006KT P6SM SKC
        FM010100 00000KT P6SM SKC
        TEMPO 0106/0112 33003KT 1 1/4SM BKN020
        BECMG 0117/0119 29005KT 1/2SM SN BKN010
    """
    taf = Taf(code)
    changes = taf.change_periods

    visibility0 = changes[0].prevailing_visibility
    assert visibility0.code == "P6SM"
    assert visibility0.in_meters == 11_112.0
    assert visibility0.in_kilometers == 11.112
    assert visibility0.in_sea_miles == approx(6.0)
    assert visibility0.in_feet == approx(36_456.7)
    assert visibility0.cavok == False
    assert visibility0.cardinal_direction == None
    assert visibility0.direction_in_degrees == None
    assert visibility0.direction_in_radians == None
    assert str(visibility0) == "11.1 km"

    visibility1 = changes[1].prevailing_visibility
    assert visibility1.code == "1 1/4SM"
    assert visibility1.in_meters == 2_315.0
    assert visibility1.in_kilometers == 2.315
    assert visibility1.in_sea_miles == approx(1.25)
    assert visibility1.in_feet == 7595.144356955379
    assert visibility1.cavok == False
    assert visibility1.cardinal_direction == None
    assert visibility1.direction_in_degrees == None
    assert visibility1.direction_in_radians == None
    assert str(visibility1) == "2.3 km"

    visibility2 = changes[2].prevailing_visibility
    assert visibility2.code == "1/2SM"
    assert visibility2.in_meters == 926.0
    assert visibility2.in_kilometers == 0.926
    assert visibility2.in_sea_miles == approx(0.5)
    assert visibility2.in_feet == 3038.0577427821518
    assert visibility2.cavok == False
    assert visibility2.cardinal_direction == None
    assert visibility2.direction_in_degrees == None
    assert visibility2.direction_in_radians == None
    assert str(visibility2) == "0.9 km"
