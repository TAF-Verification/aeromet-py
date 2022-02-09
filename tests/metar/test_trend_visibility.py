from aeromet_py import Metar


def test_trend_visibility_from_meters():
    metar = Metar(
        "METAR SBBV 170400Z 08004KT 9999 SCT030 FEW035TCU BKN070 26/23 Q1012 BECMG 5000 +RA"
    )
    visibility = metar.trend_prevailing_visibility

    assert visibility.code == "5000"
    assert visibility.in_meters == 5_000.0
    assert visibility.in_kilometers == 5.0
    assert visibility.in_sea_miles == 2.6997840172786174
    assert visibility.in_feet == 16_404.199475065616
    assert visibility.cavok == False
    assert visibility.cardinal_direction == None
    assert visibility.direction_in_degrees == None
    assert visibility.direction_in_radians == None
    assert str(visibility) == "5.0 km"


def test_trend_visibility_from_seamiles():
    metar = Metar(
        "SPECI PALH 170933Z 00000KT 10SM FEW020 M14/M16 A2980 TEMPO FM1000 TL1100 1 1/4SM BR BKN002 RMK AO2 T11441156"
    )
    visibility = metar.trend_prevailing_visibility

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


def test_trend_visibility_from_seamiles_only_fraction():
    metar = Metar(
        "METAR PALH 170933Z 00000KT 2SM BR FEW002 M14/M16 A2980 BECMG AT1000 1/2SM RMK AO2 T11441156"
    )
    visibility = metar.trend_prevailing_visibility

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


def test_trend_visibility_from_kilometers():
    metar = Metar("METAR SCAT 210900Z 18005KT 10KM OVC027/// 16/12 Q1013 BECMG 5KM")
    visibility = metar.trend_prevailing_visibility

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


def test_trend_visibility_from_cavok():
    metar = Metar(
        "METAR SAAR 222000Z 13011KT 100V160 9999 FEW030 32/15 Q1012 BECMG AT2100 CAVOK RMK PP000"
    )
    visibility = metar.trend_prevailing_visibility

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


def test_no_trend_visibility():
    metar = Metar(
        "METAR PALH 170933Z 00000KT BR FEW002 M14/M16 A2980 NOSIG RMK AO2 T11441156"
    )
    visibility = metar.trend_prevailing_visibility

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
