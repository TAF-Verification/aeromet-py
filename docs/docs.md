# Aeromet-Py Documentation

## Introduction

Aeromet-Py is a package for Python programming language designed for parsing aerinautical and
meteorological information from land stations (airports and meteorological offices).

It is strongly influenced by [Python-Metar][python-metar] package, authored by [Tom Pollard][tom-pollard]. 
But, this package is designed to go further in parsing more than METAR reports.

[python-metar]: https://github.com/python-metar/python-metar
[tom-pollard]: https://github.com/tomp

Going through this documentation will take you about an hour, and by the end of it you will have pretty much 
learned the entire API provided to interact with the objects and its methods and properties.

## Installing

The best way of installing the latest version of `Aeromet-Py` is via `pip`:

```
pip install aeromet-py
```

## Upgrade to the latest version

If you have an old version of `Aeromet-Py` consider the following command:

```
pip install --upgrade aeromet-py
```

# Table of contents

<table>
<tr><td width=50% valign=top>

- [Aeromet-Py Documentation](#aeromet-py-documentation)
  - [Introduction](#introduction)
  - [Installing](#installing)
  - [Upgrade to the latest version](#upgrade-to-the-latest-version)
- [Table of contents](#table-of-contents)
- [Metar](#metar)
  - [Raw Code](#raw-code)
  - [Sections](#sections)
  - [Unparsed Groups](#unparsed-groups)
  - [Methods as_dict() and to_json()](#methods-as_dict()-and-to_json())
  - [The `GroupList` object](#the-grouplist-object)
  - [Type](#type)
  - [Station](#station)
  - [Time](#time)
  - [Modifier](#modifier)
  - [Wind](#wind)
  - [Wind Variation](#wind-variation)
  - [Prevailing Visibility](#prevailing-visibility)
  - [Minimum Visibility](#minimum-visibility)
  - [Runway Ranges](#runway-ranges)
    - [Runway Range](#runway-range)
  - [Weathers](#weathers)
    - [Weather](#weather)
  - [Clouds](#clouds)
    - [Cloud](#cloud)
  - [Temperatures](#temperatures)
  - [Pressure](#pressure)
  - [Recent Weather](#recent-weather)
  - [Windshears](#windshears)
    - [Windshear](#windshear)
  - [Sea State](#sea-state)
  - [Runway State](#runway-state)
  - [Weather Trend](#weather-trend)
    - [Change Period](#change-period)
      - [Trend Indicator](#trend-indicator)
  - [Remark](#remark)

</td>
<td valign=top>

- [Taf](#taf)
  - [Missing](#missing)
  - [Valid](#valid)
  - [Cancelled](#cancelled)
  - [Max and Min Temperatures](#max-and-min-temperatures)
    - [TAF Temperature](#taf-temperature)

</td>
<!-- <td valign=top>
</td> -->
</tr>
</table>

# Metar

All features of the `Metar` report are represented as objects in the package. So, these objects have inside
of them another objects as fields, properties and methods. In the next sections you have a tour across all of 
that characteristics. 

Import the `Metar` object and instantiate it with the following syntax:

```python
from aeromet_py import Metar

code = "KMIA 130053Z 25005KT 250V140 10SM FEW030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233"
metar = Metar(code)
```

Because of the codification of the reports doesn't have the month and year, you can give it to the instance
as shown in the following example:

```python
metar = Metar(code, year=2022, month=3)
```

If you do not give this arguments, `Metar` object is instantiated with the current year and month.

By default the parser do not raise any error when find a group that can't be parsed. For anulate this
behavior provide the argument `truncate`, so it can raises a `ParserError` showing the unparsed groups
as follows:

```python
code_with_bad_group = "KMIA 130053Z 00000KT 10SM FEWT030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233"
metar = Metar(code_with_bad_group, truncate=True)

# Raises the following error
# ParserError: failed while processing FEWT030 from: KMIA 130053Z 00000KT 10SM FEWT030 FEW045 BKN250 29/23
# A2994 RMK AO2 SLP140 T02940233
```

Now that you have a `Metar` object, you can extract all the relevant information.

## Raw Code

Get the raw code as its received in the instance. TypeStation`str`station

```python
print(metar.raw_code)

# prints...
# KMIA 130053Z 00000KT 10SM FEWT030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233
```

## Sections

Get the `Metar` separated in its sections. Type `List[str]`.

```python
print(metar.sections)

# prints...
# ['KMIA 130053Z 00000KT 10SM FEW030 FEW045 BKN250 29/23 A2994', '', 'RMK AO2 SLP140 T02940233']
```

Where the first element is the body, the second is the trend and the last one is the remark.

## Unparsed Groups

Get the unparsed groups of the report. Type `List[str]`.

```python
code_with_bad_group = "KMIA 130053Z COR 00000KT 10SM FEWT030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233"
metar = Metar(code_with_bad_group)
print(metar.unparsed_groups)

# prints...
# ['FEWT030']
```

As you can see, the parser is very strict. This is because we can't take in count every case of bad 
digitation in land station where the work is completely manual. Human errors are inevitable. Try to
parse bad groups may incur us to have bad data to make calculations, we don't want this in our
climatology.

## Methods as_dict() and to_json()

Starting from here, all the properties contains this list of methods:

* as_dict() -> `Dict[str, Any]`: Returns the object data as a dictionary like `Dict[str, Any]`. In some
  cases the `Any` type is replaced by a especific type.
* to_json() -> `str`: Returns the object data as a string in JSON format.

Of course, the `Metar` object also containes this same methods.

## The `GroupList` object

Some groups may appear several times in the `METAR` report, but representing different data.
For example, the weather or the cloud layers. So, we can group these in one object to manipulate
them more easily.

The `GroupList` object is a class that contains other objects of the same type like a list.
This is iterable, so, you can use it in a `for` loop:

```python
for group in group_list_instance:
  print(group.some_property)

# Can be indexed too
group = group_list_instance[0]
print(group.some_property)
```

We will use the `GroupList` object for the first time in [Runway Ranges](#runway-ranges)
section.

Fields:
* codes `List[str]`: The codes of every group found in report as a List[str].
* items `List[T]`: The groups found in report.

## Type

Get the type of the report. Type `ReportType`.

Fields:
* code `str`: The code present in the `Metar`. Defaults to `METAR`.
* type_ `str`: The report type name, e.g. `Meteorological Aerodrome Report`.

```python
print(metar.type_.code)
print(metar.type_.type_)

# prints...
# METAR
# Meteorological Aerodrome Report
```

## Station

Get the station information of the report. Type `Station`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `KJFK`.
* name `str | None`: The name of the land station.
* country `str | None`: The country to which the land station belongs.
* elevation `str | None`: The elevation in meters above sea level of the station.
* longitude `str | None`: The longitude of the station.
* latitude `str | None`: The latitude of the station.
* icao `str | None`: The ICAO code of the station.
* iata `str | None`: The IATA code of the station.
* synop `str | None`: The SYNOP code of the station.

```python
print("Code:", metar.station.code)
print("Name:", metar.station.name)
print("Country:", metar.station.country)
print("Elevation:", metar.station.elevation)
print("Longitude:", metar.station.longitude)
print("Latitude:", metar.station.latitude)
print("ICAO:", metar.station.icao)
print("IATA:", metar.station.iata)
print("SYNOP:", metar.station.synop)

# prints...
# Code: KJFK
# Name: NY NYC/JFK ARPT
# Country: United States of America (the)
# Elevation: 9
# Longitude: 073.46W
# Latitude: 40.38N
# ICAO: KJFK
# IATA: JFK
# SYNOP: 74486
```

## Time

Get the date and time of the report. Type `Time`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `130053Z`.
* time `datetime`: The time of the report as a `datetime` object.
* year `int`: The year of the report. Defaults to current year if not provided in the
  `Metar` instance.
* month `int`: The month of the report. Defaults to current month if not provided in the
  `Metar` instance.
* day `int`: The day of the report.
* hour `int`: The hour of the report.
* minute `int`: The minute of the report.

```python
print(metar.time.code)
print(metar.time.day)
print(metar.time.hour)
print(metar.time.minute)

# prints...
# 130053Z
# 13
# 0
# 53
```

## Modifier

Get the modifier description of the report. Type `Modifier`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `AUTO`.
* description `str | None`: The description of the modifier code.

Supported codes are:
* `COR`: Correction
* `CORR`: Correction
* `AMD`: Amendment
* `NIL`: Missing report
* `AUTO`: Automatic report
* `TEST`: Testing report
* `FINO`: Missing report

```python
print(metar.modifier.code)
print(metar.modifier.description)

# prints...
# COR
# Correction
```

## Wind

Get the wind data of the report. Type `MetarWind`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `25005KT`.
* cardinal_direction `str | None`: The cardinal direction associated to the wind direction,
  e.g. "NW" (north west).
* variable `bool`: Represents if the wind direction is variable (VRB).
* direction_in_degrees `float | None`: The wind direction in degrees.
* direction_in_radians `float | None`: The wind direction in radians.
* direction_in_gradians `float | None`: The wind direction in gradians.
* speed_in_knot `float | None`: The wind speed in knot.
* speed_in_mps `float | None`: The wind speed in meters per second.
* speed_in_kph `float | None`: The wind speed in kilometers per hour.
* speed_in_miph `float | None`: The wind speed in miles per hour.
* gust_in_knot `float | None`: The wind gust in knot.
* gust_in_mps `float | None`: The wind gust in meters per second.
* gust_in_kph `float | None`: The wind gust in kilometers per hour.
* gust_in_miph `float | None`: The wind gust in miles per hour.

```python
print(metar.wind.code)
print(metar.wind.cardinal_direction)
print(metar.wind.variable)
print(metar.wind.direction_in_degrees)
print(metar.wind.speed_in_miph)
print(metar.wind.gust_in_kph)

# prints...
# 25005KT
# WSW
# False
# 250.0
# 5.7539
# None
```

## Wind Variation

Get the wind variation directions from the report. Type `MetarWindVariation`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `250V140`.
* from_cardinal_direction `str | None`: The `from` cardinal direction, e.g. "NW" (north west).
* from_in_degrees `float | None`: The `from` direction in degrees.
* from_in_radians `float | None`: The `from` direction in radians.
* from_in_gradians `float | None`: The `from` direction in gradians.
* to_cardinal_direction `str | None`: The `to` cardinal direction, e.g. "SE" (south est).
* to_in_degrees `float | None`: The `to` direction in degrees.
* to_in_radians `float | None`: The `to` direction in radians.
* to_in_gradians `float | None`: The `to` direction in gradians.

```python
print(metar.wind_variation.code)
print(metar.wind_variation.from_cardinal_direction)
print(metar.wind_variation.from_in_degrees)
print(metar.wind_variation.to_cardinal_direction)
print(metar.wind_variation.to_in_degrees)

# prints...
# 250V140
# WSW
# 250.0
# SE
# 140.0
```

## Prevailing Visibility

Get the prevailing visibility of the report. Type `MetarPrevailingVisibility`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `9999`.
* in_meters `float | None`: The prevailing visibility in meters.
* in_kilometers `float | None`: The prevailing visibility in kilometers.
* in_feet `float | None`: The prevailing visibility in feet.
* in_sea_miles `float | None`: The prevailing visibility in sea miles.
* cardinal_direction `str | None`: The cardinal direction associated to the visibility,
  e.g. "NW" (north west).
* direction_in_degrees `float | None`: The direction of the prevailing visibility in degrees.
* direction_in_radians `float | None`: The direction of the prevailing visibility in radians.
* direction_in_gradians `float | None`: The direction of the prevailing visibility in gradians.
* cavok `bool`: True if CAVOK, False if not.

```python
print(metar.prevailing_visibility.code)
print(metar.prevailing_visibility.in_meters)
print(metar.prevailing_visibility.cavok)

# prints...
# 10SM
# 18520.0
# False
```

## Minimum Visibility

Get the minimum visibility of the report. Type `MetarMinimumVisibility`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `3000W`.
* in_meters `float | None`: The minimum visibility in meters.
* in_kilometers `float | None`: The minimum visibility in kilometers.
* in_feet `float | None`: The minimum visibility in feet.
* in_sea_miles `float | None`: The minimum visibility in sea miles.
* cardinal_direction `str | None`: The cardinal direction associated to the minimum visibility,
  e.g. "NW" (north west).
* direction_in_degrees `float | None`: The direction of the minimum visibility in degrees.
* direction_in_radians `float | None`: The direction of the minimum visibility in radians.
* direction_in_gradians `float | None`: The direction of the minimum visibility in gradians.

```python
# New METAR code for this example
code = "MROC 160700Z 09003KT 3000 1000SW BR SCT005 BKN015 19/19 A3007 NOSIG"
metar = Metar(code)

print(metar.minimum_visibility.code)
print(metar.minimum_visibility.in_meters)
print(metar.minimum_visibility.cardinal_direction)
print(metar.minimum_visibility.direction_in_degrees)

# prints...
# 1000SW
# 1000.0
# SW
# 225.0
```

## Runway Ranges

Get the runway ranges data of the report. Type `GroupList[MetarRunwayRange]`.

### Runway Range

The individual runway range data by group provided in the report. Type `MetarRunwayRange`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `R07L/M0150V0600U`.
* name `str | None`: The runway name.
* low_range `str | None`: The runway low range as a string.
* low_in_meters `float | None`: The runway low range in meters.
* low_in_kilometers `float | None`: The runway low range in kilometers.
* low_in_feet `float | None`: The runway low range in feet.
* low_in_sea_miles `float | None`: The runway low range in sea miles.
* high_range `str | None`: The runway high range as a string.
* high_in_meters `float | None`: The runway high range in meters.
* high_in_kilometers `float | None`: The runway high range in kilometers.
* high_in_feet `float | None`: The runway high range in feet.
* high_in_sea_miles `float | None`: The runway high range in sea miles.
* trend `str | None`: The trend of the runway range.

```python
# New METAR code for this example
code = "METAR SCFA 121300Z 21008KT 9999 3000W R07L/M0150V0600U TSRA FEW020 20/13 Q1014 NOSIG"
metar = Metar(code)

print(metar.runway_ranges.codes)

for runway_range in metar.runway_ranges:
    print(runway_range.name)
    print(runway_range.low_range)
    print(runway_range.high_in_sea_miles)

# prints...
# ['R07L/M0150V0600U']
# 07 left
# below of 150.0 m
# 0.3239740820734341
```

## Weathers

Get the weathers data of the report. Type `GroupList[MetarWeather]`.

### Weather

The individual weather data by group provided in the report. Type `MetarWeather`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `+TSRA`.
* intensity `str | None`: The intensity translation of the weather, e.g. `+ -> heavy`.
* description `str | None`: The description translation of the weather, e.g. `TS -> thunder storm`.
* precipitation `str | None`: The precipitation translation of the weather, e.g. `RA -> rain`.
* obscuration `str | None`: The obscuration translation of the weather, e.g. `BR -> mist`.
* other `str | None`: The other translation of the weather, e.g. `FC -> funnel cloud`.

```python
# New METAR code for this example
metar_code = "METAR BIBD 191100Z 03002KT 5000 +RA BR VCTS SCT008CB OVC020 04/03 Q1013"
metar = Metar(code)

code = f"{'code':>13}"
intensity = f"{'intensity':>13}"
description = f"{'description':>13}"
precipitation = f"{'precipitation':>13}"
obscuration = f"{'obscuration':>13}"
other = f"{'other':>13}"

for weather in metar.weathers:
    code += f"{weather.code:>14}"
    intensity += f"{str(weather.intensity):>14}"
    description += f"{str(weather.description):>14}"
    precipitation += f"{str(weather.precipitation):>14}"
    obscuration += f"{str(weather.obscuration):>14}"
    other += f"{str(weather.other):>14}"

print(code)
print(intensity)
print(description)
print(precipitation)
print(obscuration)
print(other)

# prints...
#          code           +RA            BR          VCTS
#     intensity         heavy          None        nearby
#   description          None          None  thunderstorm
# precipitation          rain          None          None
#   obscuration          None          mist          None
#         other          None          None          None
```

## Clouds

Get the clouds data of the report. Type `CloudList` which extends `GroupList[Cloud]`.

Fields:
* ceiling `bool`: True if there is ceiling, False if not. If the cover of someone of the
  cloud layers is broken (BKN) or overcast (OVC) and its height is less than or equal to
  1500.0 feet, there is ceiling; there isn't otherwise.

### Cloud

The individual cloud data by group provided in the report. Type `Cloud`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `SCT015CB`.
* cover `str | None`: The cover translation of the cloud layer, e.g. `SCT -> scattered`.
* cloud_type `str | None`: The type of cloud translation of the cloud layer, e.g. `CB -> cumulonimbus`.
* oktas `str`: The oktas amount of the cloud layer, e.g. `SCT -> 3-4`.
* height_in_meters `float | None`: The height of the cloud base in meters.
* height_in_kilometers `float | None`: The height of the cloud base in kilometers.
* height_in_sea_miles `float | None`: The height of the cloud base in sea miles.
* height_in_feet `float | None`: The height of the cloud base in feet.

```python
# New METAR code for this example
metar_code = (
    "METAR BIBD 191100Z 03002KT 5000 +RA BR VCTS FEW010CB SCT020 BKN120 04/03 Q1013"
)
metar = Metar(metar_code)

print(metar.clouds.codes)
print(metar.clouds.ceiling)

# prints...
# ['FEW010CB', 'SCT020', 'BKN120']
# False

code = f"{'code':>13}"
cover = f"{'cover':>13}"
oktas = f"{'oktas':>13}"
cloud_type = f"{'cloud_type':>13}"
height = f"{'height (ft)':>13}"

for cloud in metar.clouds:
    code += f"{cloud.code:>14}"
    cover += f"{str(cloud.cover):>14}"
    oktas += f"{str(cloud.oktas):>14}"
    cloud_type += f"{str(cloud.cloud_type):>14}"
    height += f"{f'{cloud.height_in_feet:.1f}':>14}"

print(code)
print(cover)
print(oktas)
print(cloud_type)
print(height)

# prints...
#         code      FEW010CB        SCT020        BKN120
#        cover         a few     scattered        broken
#        oktas           1-2           3-4           5-7
#   cloud_type  cumulonimbus          None          None
#  height (ft)        1000.0        2000.0       12000.0
```

## Temperatures

Get the temperatures of the report. Type `MetarTemperatures`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `29/23`.
* temperature_in_celsius `float | None`: The temperature in °Celsius.
* temperature_in_kelvin `float | None`: The temperature in °Kelvin.
* temperature_in_fahrenheit `float | None`: The temperature in °Fahrenheit.
* temperature_in_rankine `float | None`: The temperature in Rankine.
* dewpoint_in_celsius `float | None`: The dewpoint in °Celsius.
* dewpoint_in_kelvin `float | None`: The dewpoint in °Kelvin.
* dewpoint_in_fahrenheit `float | None`: The dewpoint in °Fahrenheit.
* dewpoint_in_rankine `float | None`: The dewpoint in Rankine.

```python
print(metar.temperatures.temperature_in_celsius)
print(metar.temperatures.temperature_in_fahrenheit)
print(metar.temperatures.dewpoint_in_celsius)
print(metar.temperatures.dewpoint_in_fahrenheit)

# prints...
# 29.0
# 84.2
# 23.0
# 73.4
```

## Pressure

Get the pressure of the report. Type `MetarPressure`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `A2994`.
* in_atm `float | None`: The pressure in atmospheres.
* in_bar `float | None`: The pressure in bars.
* in_mbar `float | None`: The pressure in millibars.
* in_hPa `float | None`: The pressure in hecto pascals.
* in_inHg `float | None`: The pressure in mercury inches.
* value `float | None`: The default stored value of the pressure in hecto pascals.

```python
print(metar.pressure.code)
print(f"{metar.pressure.in_atm:.6f}")
print(f"{metar.pressure.in_hPa:.6f}")
print(f"{metar.pressure.in_inHg:.6f}")

# prints...
# A2994
# 1.000626
# 1013.884186
# 29.940000
```

## Recent Weather

Get the recent weather data of the report. Type `MetarRecentWeather`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `RERA`.
* description `str | None`: The description translation of the recent weather, e.g. `TS -> thunder storm`.
* precipitation `str | None`: The precipitation translation of the recent weather, e.g. `RA -> rain`.
* obscuration `str | None`: The obscuration translation of the recent weather, e.g. `FG -> fog`.
* other `str | None`: The other translation of the recent weather, e.g. `FC -> funnel cloud`.

```python
# New METAR code for this example
metar_code = (
    "METAR BIBD 191100Z 03002KT 9999 VCTS FEW010CB SCT020 BKN120 04/03 Q1013 RETSRA NOSIG"
)
metar = Metar(metar_code)

print(metar.recent_weather.code)
print(metar.recent_weather.description)
print(metar.recent_weather.precipitation)
print(metar.recent_weather.obscuration)
print(metar.recent_weather.other)

# prints...
# RETSRA
# thunderstorm
# rain
# None
# None
```

## Windshears

Get the windshear data of the report. Type `MetarWindshearList` which
extends `GroupList[MetarWindshearRunway]`.

Fields:
* names `List[str]`: The names of runways with windshear reported.
* all_runways `bool`: True if all runways have windshear, False if not.

### Windshear

The individual windshear data by group provided in the report. Type `MetarWindshearRunway`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `WS R07`.
* all_ `bool`: True if `ALL` is found in the group, False if not, e.g. `WS ALL RWY`.
* name `str | None`: The name of the runway that has being reported with windshear.

```python
# New METAR code for this example
metar_code = (
    "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07L WS R25C NOSIG"
)
metar = Metar(metar_code)

print(metar.windshears.codes)
print(metar.windshears.names)
print(metar.windshears.all_runways)

# prints...
# ['WS R07L', 'WS R25C']
# ['07 left', '25 center']
# False

code = f"{'code':>5}"
all_ = f"{'all_':>5}"
name = f"{'name':>5}"

for ws in metar.windshears:
    code += f"{ws.code:>11}"
    all_ += f"{str(ws.all_):>11}"
    name += f"{ws.name:>11}"

print(code)
print(all_)
print(name)

# prints...
# code    WS R07L    WS R25C
# all_      False      False
# name    07 left  25 center
```

## Sea State

Get the sea state data of the report. Type `MetarSeaState`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `W20/S5`.
* state `str | None`: The sea state if provided.
* temperature_in_celsius `float | None`: The temperature of the sea in Celsius.
* temperature_in_kelvin `float | None`: The temperature of the sea in Kelvin.
* temperature_in_fahrenheit `float | None`: The temperature of the sea in Fahrenheit.
* temperature_in_rankine `float | None`: The temperature of the sea in Rankine.
* height_in_meters `float | None`: The height of the significant wave in meters.
* height_in_centimeters `float | None`: The height of the significant wave in centimeters.
* height_in_decimeters `float | None`: The height of the significant wave in decimeters.
* height_in_feet `float | None`: The height of the significant wave in feet.
* height_in_inches `float | None`: The height of the significant wave in inches.

```python
# New METAR code for this example
metar_code = "METAR LXGB 201950Z AUTO 09012KT 9999 BKN080/// 14/07 Q1016 RERA W20/S5"
metar = Metar(metar_code)

print(metar.sea_state.code)
print(metar.sea_state.state)
print(metar.sea_state.temperature_in_celsius)
print(metar.sea_state.temperature_in_kelvin)
print(metar.sea_state.temperature_in_fahrenheit)
print(metar.sea_state.height_in_inches)

# prints...
# W20/S5
# rough
# 20.0
# 293.15
# 68.0
# None
```

## Runway State

Get the runway state data of the report. Type `MetarRunwayState`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `R10R/527650`.
* name `str | None`: The name of the runway that has being reported.
* deposits `str | None`: The deposits type on the runway.
* contamination `str | None`: The contamination quantity of the deposits.
* deposits_depth `str | None`: The deposits depth.
* surface_friction `str | None`: The surface friction index of the runway.
* snoclo `bool`: True: aerodrome is closed due to extreme deposit of snow.
  False: aerodrome is open.
* clrd `str | None`: Get if contamination have ceased to exists in some runway.

```python
# New METAR code for this example
metar_code = (
    "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R10R/527650"
)
metar = Metar(metar_code)

print(f"{f'Code:':>18} {metar.runway_state.code}")
print(f"{f'Name:':>18} {metar.runway_state.name}")
print(f"{f'Deposits:':>18} {metar.runway_state.deposits}")
print(f"{f'Deposits depth:':>18} {metar.runway_state.deposits_depth}")
print(f"{f'Contamination:':>18} {metar.runway_state.contamination}")
print(f"{f'Surface friction:':>18} {metar.runway_state.surface_friction}")
print(f"{f'SNOCLO:':>18} {str(metar.runway_state.snoclo)}")
print(f"{f'CLRD:':>18} {str(metar.runway_state.clrd)}")

# prints...
#             Code: R10R/527650
#             Name: 10 right
#         Deposits: wet snow
#   Deposits depth: 76 mm
#    Contamination: 11%-25% of runway
# Surface friction: 0.50
#           SNOCLO: False
#             CLRD: None
```

## Weather Trend

Get the weather trends of the report if provided. Type `MetarWeatherTrends`
which extends `GroupList[ChangePeriods]`.

The weather trends are change periods forecasted for the next two hours from the
report. May be one or two, and they can have wind, prevailing visibility, weather and
clouds, but not all are strictly required. All of this fields are the same
as in the [Metar](#metar) object, so, you can access them as in the previous examples
for every change period.

### Change Period

The change period forecasted for the next two hours. Type `ChangePeriod`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `BECMG 25005KT 5000 RA`.
* wind `MetarWind`: The wind forecasted, see [Wind](#wind) for more details.
* prevailing_visibility `MetarPrevailingVisibility`: The prevailing visibility
  forecasted, see [Prevailing Visibility](#prevailing-visibility) for more details.
* weathers `GroupList[MetarWeather]`: the weather forecasted, see [Weathers](#weathers)
  for more details.
* clouds `CloudList`: the clouds forecasted, see [Clouds](#clouds) for more details.

#### Trend Indicator

Get the trend indicator features of the report. Type `MetarTrendIndicator`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `BECMG FM0500 TL0700`.
* forecast_period `Tuple[Time, Time]`: The forcast period, i.e. the initial forecast
  time and the end forecast time.
* period_from `Time`: The `from` forecast period.
* period_until `Time`: The `until` forecast period.
* period_at `Time | None`: The `at` forecast period.

```python
# New METAR code for this example
metar_code = (
    "METAR BIAR 190800Z 20015KT 9999 FEW049 BKN056 10/03 Q1016 BECMG 25010G20KT 5000 RA SCT010 BKN015"
)
metar = Metar(metar_code)
weather_trends = metar.weather_trends

print(weather_trends.codes)

# prints...
# ['BECMG 25010G20KT 5000 RA SCT010 BKN015']

for change_period in weather_trends:
    print(f"Trend indicator: {change_period.trend_indicator}")
    print(f"Wind: {change_period.wind}")
    print(f"Prevailing visibility: {change_period.prevailing_visibility}")
    print(f"Weather: {change_period.weathers}")
    print(f"Clouds: {change_period.clouds}")

# prints...
# Trend indicator: becoming from 2022-09-19 08:00:00 until 2022-09-19 10:00:00
# Wind: WSW (250.0°) 10.0 kt gust of 20.0 kt
# Prevailing visibility: 5.0 km
# Weather: rain
# Clouds: scattered at 1000.0 feet | broken at 1500.0 feet
```

## Remark

There is no support for remark at this time, but we hope add it soon. Sorry.

# Taf

All features of the `Taf` report are represented as objects in the package as like the `Metar`.
So, in the same way as the `Metar`, the `Taf` object can be intantiated as follows: 

```python
from aeromet_py import Taf

code = (
  """KATL 251958Z 2520/2624 27009KT P6SM VCSH FEW040 BKN120
  FM260100 28005KT P6SM SCT060 SCT120
  FM260800 32004KT P6SM FEW150
  FM261500 32011G18KT P6SM SKC"""
)
taf = Taf(code)
```

Because of the codification of the reports doesn't have the month and year, you can give it to the instance
as shown in the following example:

```python
taf = Taf(code, year=2022, month=3)
```

If you do not give this arguments, `Taf` object is instantiated with the current year and month.

By default the parser do not raise any error when find a group that can't be parsed. For anulate this
behavior provide the argument `truncate`, so it can raises a `ParserError` showing the unparsed groups
as follows:

```python
code_with_bad_groups = (
  """KATL 251958Z 2520/2624 27009KT P6SM VCHS FEW040 BKN120
  FM260100 28005KT P6SM SCT060 SCT120
  FM260800 32004KT P6SM FEW150
  FM261500 32011G18KT P6SM SKC"""
)
taf = Taf(code_with_bad_groups, truncate=True)

# Raises the following error
# ParserError: failed while processing VCHS, SKC from: KATL 251958Z 2520/2624 27009KT P6SM VCHS FEW040 BKN120 
# FM260100 28005KT P6SM SCT060 SCT120 FM260800 32004KT P6SM FEW150 FM261500 32011G18KT P6SM SKC
```

As you can see, the parser is very strict. This is because we can't take in count every case of bad 
digitation in land station where the work is completely manual. Human errors are inevitable. Try to
parse bad groups may incur us to have bad data to make TAF verification, we don't want this in our
analysis.

The `Taf` and `Metar` objects share some of its properties and methods. So, the use of these fields
is the same.

Fields:
* raw_code `str`: See [Raw Code](#raw-code) for more details.
* sections `List[str]`: See [Sections](#sections) for more details. In the case of `Taf`, the
  `sections` field returns a list of two elements, the first one is the body and the second one
  the change periods if provided.
* unparsed_groups `List[str]`: See [Unparsed Groups](#unparsed-groups) for more details.
* as_dict() and to_json(): See [Methods as_dict() and to_json()](#methods-as_dict-and-to_json) for
  more details.
* type_ `ReportType`: See [Type](#type) for more details.
* station `Station`: See [Station](#station) for more details.
* time `Time`: See [Time](#time) for more details.
* modifier `Modifier`: See [Modifier](#modifier) for more details.
* wind `MetarWind`: See [Wind](#wind) for more details.
* prevailing_visibility `MetarPrevailingVisibility`: See
  [Prevailing Visibility](#prevailing-visibility) for more details.
* weathers `GroupList[MetarWeather]`: See [Weathers](#weathers) for more details.
* clouds `CloudList`: See [Clouds](#clouds) for more details.

## Missing

Get the missing information of the report if provided. Type `Missing`.

Fields:
* code `str | None`: The code present in the `Taf`, which is `NIL`.
* description `str | None`: The description of the missing code.
* is_missing `bool`: True if `NIL` group is found, False if not.

```python
# New TAF code for this example
code = "TAF SKBO 261630Z NIL"
taf = Taf(code)

print(taf.missing.code)
print(taf.missing.description)
print(taf.missing.is_missing)

# prints...
# NIL
# Missing report
# True
```

## Valid

Get the dates of valid period of the report. Type `Valid`.

Fields:
* code `str | None`: The code present in the `Taf`, e.g. `2518/2618`.
* period_from `Time`: The time period `from` of the forecast. If group is not found, defaults to
  current machine date at 00:00Z. See [Time](#time) for more details.
* period_until `Time`: The time period `until` of the forecast. If group is not found, defaults to
  current machine date at 00:00Z + 24 hours. See [Time](#time) for more details.
* duration `timedelta`: The validity of the forecast.

```python
# Use this TAF instance for this example
taf = Taf(code, year=2022, month=3)

print(taf.valid.period_from)
print(taf.valid.period_until)
print(f"Hours of validity: {taf.valid.duration.total_seconds() / 60 / 60}")

# prints...
# 2022-03-25 20:00:00
# 2022-03-27 00:00:00
# Hours of validity: 28.0
```

## Cancelled

Get the cancelled group data of the report. Type `Cancelled`.

Fields:
* code `str | None`: The code present in the `Taf`, e.g. `CNL`.
* is_cancelled `bool`: True if `TAF` is cancelled, False if not.

```python
# New TAF for this example
code = "KATL 251958Z 2520/2624 CNL"
taf = Taf(code)

print(taf.cancelled.code)
print(taf.cancelled.is_cancelled)

# prints...
# CNL
# True
```

## Max and Min Temperatures

Get the maximum and minimum temperatures expected to happen if provided. Remember you can
add two maximum and two minimum temperatures in the TAF body. Type `TafTemperatureList`
which extends `GroupList[TafTemperature]`.

### TAF Temperature

The temperature data provided in the report. Type `TafTemperature`.

Fields:
* code `str | None`: The code present in the `Taf`, e.g. `TX07/0305Z`.
* in_celsius `float | None`: The temperature in Celsius.
* in_kelvin `float | None`: The temperature in Kelvin.
* in_fahrenheit `float | None`: The temperature in Fahrenheit.
* in_rankine `float | None`: The temperature in Rankine.
* time `Time`: The datetime the temperature is expected to happen.

```python
# New TAF code for this example
code = """TAF AMD RKNY 021725Z 0218/0324 26017G35KT CAVOK TX07/0305Z TNM03/0321Z
        BECMG 0223/0224 27010KT
        BECMG 0302/0303 03006KT
        BECMG 0308/0309 23006KT"""
taf = Taf(code, year=2022, month=9)

print(taf.max_temperatures.codes)
print(taf.min_temperatures.codes)

# prints...
# ['TX07/0305Z']
# ['TNM03/0321Z']

max_temp = taf.max_temperatures[0]
print(max_temp.code)
print(max_temp.in_celsius)
print(max_temp.in_kelvin)
print(max_temp.time)

# prints...
# TX07/0305Z
# 7.0
# 280.15
# 2022-09-03 05:00:00

min_temp = taf.min_temperatures[0]
print(min_temp.code)
print(min_temp.in_celsius)
print(min_temp.in_kelvin)
print(min_temp.time)

# prints...
# TNM03/0321Z
# -3.0
# 270.15
# 2022-09-03 21:00:00
```