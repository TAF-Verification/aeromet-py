from aeromet_py import Metar


def test_visibility_from_meters():
    metar = Metar("METAR SBBV 170400Z 08004KT 9999 SCT030 FEW035TCU BKN070 26/23 Q1012")
    visibility = metar.prevailing_visibility

    assert visibility.code == "9999"
    assert visibility.in_meters == 10_000.0
    assert visibility.in_kilometers == 10.0
    assert visibility.in_sea_miles == 5.399568034557235
    assert visibility.in_feet == 32_808.39895013123
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "10.0 km"
    assert visibility.as_dict() == {
        "cavok": False,
        "code": "9999",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 10000.0, "units": "meters"},
    }


def test_visibility_from_seamiles():
    metar = Metar(
        "METAR PALH 170933Z 00000KT 1 1/4SM BR FEW002 M14/M16 A2980 RMK AO2 T11441156"
    )
    visibility = metar.prevailing_visibility

    assert visibility.code == "1 1/4SM"
    assert visibility.in_meters == 2315.0
    assert visibility.in_kilometers == 2.315
    assert visibility.in_sea_miles == 1.2499999999999998
    assert visibility.in_feet == 7_595.144356955379
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "2.3 km"
    assert visibility.as_dict() == {
        "cavok": False,
        "code": "1 1/4SM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 2315.0, "units": "meters"},
    }


def test_visibility_from_seamiles_only_fraction():
    metar = Metar(
        "METAR PALH 170933Z 00000KT 1/2SM BR FEW002 M14/M16 A2980 RMK AO2 T11441156"
    )
    visibility = metar.prevailing_visibility

    assert visibility.code == "1/2SM"
    assert visibility.in_meters == 926.0
    assert visibility.in_kilometers == 0.926
    assert visibility.in_sea_miles == 0.49999999999999994
    assert visibility.in_feet == 3038.0577427821518
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "0.9 km"
    assert visibility.as_dict() == {
        "cavok": False,
        "code": "1/2SM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 926.0, "units": "meters"},
    }


def test_visibility_from_kilometers():
    metar = Metar("METAR SCAT 210900Z AUTO 18005KT 5KM OVC027/// 16/12 Q1013")
    visibility = metar.prevailing_visibility

    assert visibility.code == "5KM"
    assert visibility.in_meters == 5_000.0
    assert visibility.in_kilometers == 5.0
    assert visibility.in_sea_miles == 2.6997840172786174
    assert visibility.in_feet == 16_404.199475065616
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "5.0 km"
    assert visibility.as_dict() == {
        "cavok": False,
        "code": "5KM",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 5000.0, "units": "meters"},
    }


def test_visibility_from_cavok():
    metar = Metar("METAR SAAR 222000Z 13011KT 100V160 CAVOK 32/15 Q1012 RMK PP000")
    visibility = metar.prevailing_visibility

    assert visibility.code == "CAVOK"
    assert visibility.in_meters == 10_000.0
    assert visibility.in_kilometers == 10.0
    assert visibility.in_sea_miles == 5.399568034557235
    assert visibility.in_feet == 32808.39895013123
    assert visibility.cavok == True
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "Ceiling and Visibility OK"
    assert visibility.as_dict() == {
        "cavok": True,
        "code": "CAVOK",
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 10000.0, "units": "meters"},
    }


def test_no_visibility():
    metar = Metar(
        "METAR PALH 170933Z 00000KT BR FEW002 M14/M16 A2980 RMK AO2 T11441156"
    )
    visibility = metar.prevailing_visibility

    assert visibility.code == None
    assert visibility.in_meters == None
    assert visibility.in_kilometers == None
    assert visibility.in_sea_miles == None
    assert visibility.in_feet == None
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == ""
    assert visibility.as_dict() == {
        "cavok": False,
        "code": None,
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": None, "units": "meters"},
    }


def test_minimum_visibility():
    metar = Metar(
        "METAR UUDD 180100Z 00000MPS 4800 2100NW -SN BR SCT025 M02/M03 Q1007 R32L/290042 NOSIG"
    )
    min_vis = metar.minimum_visibility

    assert min_vis.code == "2100NW"
    assert min_vis.in_meters == 2100.0
    assert min_vis.in_kilometers == 2.1
    assert min_vis.in_sea_miles == 1.1339092872570193
    assert min_vis.in_feet == 6889.763779527559
    assert min_vis.cardinal_direction == "NW"
    assert min_vis.direction_in_degrees == 315.0
    assert min_vis.direction_in_radians == 5.497787143782138
    assert str(min_vis) == "2.1 km to NW (315.0°)"
    assert min_vis.as_dict() == {
        "code": "2100NW",
        "direction": {
            "cardinal": "NW",
            "direction": 315.0,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": 2100.0, "units": "meters"},
    }


def test_no_minimum_visibility():
    metar = Metar(
        "METAR UUDD 180100Z 25005MPS 4800 -SN BR SCT025 M02/M03 Q1007 R32L/290042 NOSIG"
    )
    min_vis = metar.minimum_visibility

    assert min_vis.code == None
    assert min_vis.in_meters == None
    assert min_vis.in_kilometers == None
    assert min_vis.in_sea_miles == None
    assert min_vis.in_feet == None
    assert min_vis.cardinal_direction == None
    assert min_vis.direction_in_degrees == None
    assert min_vis.direction_in_radians == None
    assert str(min_vis) == ""
    assert min_vis.as_dict() == {
        "code": None,
        "direction": {
            "cardinal": None,
            "direction": None,
            "units": "degrees",
            "variable": False,
        },
        "visibility": {"distance": None, "units": "meters"},
    }
