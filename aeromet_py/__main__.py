from .metar import Metar

metar = Metar(
    "SPECI MROC 220000Z 34012G22KT 310V150 3500 2100NW R07C/P1000VM2500FTU RA BCFG VCTS BKN015 24/22 A2995 RMK VEL MAX VTO 25KT BECMG 08015G25KT",
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
    metar.visibility.cardinal_direction,
    metar.visibility.direction_in_degrees,
    metar.visibility,
)

metar.visibility.cavok = True

print(
    metar.minimum_visibility.code,
    metar.minimum_visibility.in_kilometers,
    metar.minimum_visibility.in_sea_miles,
    metar.minimum_visibility.direction_in_degrees,
    metar.minimum_visibility.cardinal_direction,
    metar.minimum_visibility,
)
print(
    metar.runway_range,
    metar.runway_range.code,
    metar.runway_range.name,
    metar.runway_range.low_in_kilometers,
    metar.runway_range.high_in_kilometers,
    metar.runway_range.low_range,
    metar.runway_range.high_range,
)
print(
    metar.weathers,
    metar.weathers.to_list,
    metar.weathers.first,
    metar.weathers.second,
    metar.weathers.thrid.code,
    metar.weathers.thrid.intensity,
    metar.weathers.thrid.description,
    metar.weathers.thrid.precipitation,
    metar.weathers.thrid.obscuration,
    metar.weathers.thrid.other,
    metar.weathers.codes,
)

for weather in metar.weathers:
    print(
        weather.code,
        "|",
        weather.intensity,
        "|",
        weather.description,
        "|",
        weather.obscuration,
        "|",
        weather.precipitation,
    )

# metar.sections = "other"
# print(metar.sections)
# print(metar.__dict__)
