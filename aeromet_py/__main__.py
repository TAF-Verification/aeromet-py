from .metar import Metar

metar = Metar(
    "SPECI MROC 220000Z COR 34012G22KT 310V150 CAVOK 24/22 A2995 RMK VEL MAX VTO 25KT BECMG 08015G25KT",
    truncate=False,
    # truncate=True,
)

print(metar.code)
print(metar.sections)
print(metar.type, metar.type.code, metar.type.type)
print(
    metar.station.name,
    metar.station.icao,
    metar.station.country,
    metar.station.synop,
    metar.station,
)
print(metar.modifier, metar.modifier.code, metar.modifier.modifier)
print(metar.time.time.year, metar.time)
print(
    metar.wind,
    metar.wind.direction_in_degrees,
    metar.wind.direction_in_radians,
    metar.wind.cardinal_direction,
    metar.wind.speed_in_knot,
    metar.wind.speed_in_kph,
    metar.wind.gust_in_mps,
    metar.wind.gust_in_kph,
    metar.wind.gust_in_miph,
    metar.wind.code,
)
print(
    metar.wind_variation,
    metar.wind_variation.code,
    metar.wind_variation.from_cardinal_direction,
    metar.wind_variation.to_cardinal_direction,
    metar.wind_variation.from_in_degrees,
    metar.wind_variation.to_in_degrees,
    metar.wind_variation.from_in_gradians,
    metar.wind_variation.to_in_gradians,
)
print(
    metar.visibility.code,
    metar.visibility.in_meters,
    metar.visibility.in_kilometers,
    metar.visibility.in_sea_miles,
    metar.visibility.cavok,
)

metar.visibility.cavok = True

# metar.sections = "other"
# print(metar.sections)
# print(metar.__dict__)
