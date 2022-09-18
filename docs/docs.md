# Aeromet-Py Documentation

## Introduction

Aeromet-Py is a package for Python programming language designed for parsing aerinautical and
meteorological information from land stations (airports and meteorological offices).

It is strongly influenced by [Python-Metar][python-metar] package, authored by [Tom Pollard][tom-pollard]. 
But, this package is designed to go further in parsing more than METAR reports.

[python-metar]: https://github.com/python-metar/python-metar
[tom-pollard]: https://github.com/tomp

Going through this documentation will take you about an hour, and by the end of it you will have pretty much 
learned the entire API provided to interact with the objects ands its methods and properties.

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
<tr><td width=33% valign=top>

- [Aeromet-Py Documentation](#aeromet-py-documentation)
  - [Introduction](#introduction)
  - [Installing](#installing)
  - [Upgrade to the latest version](#upgrade-to-the-latest-version)
- [Table of contents](#table-of-contents)
  - [Metar](#metar)
    - [Raw Code](#raw-code)
    - [Sections](#sections)
    - [Unparsed Groups](#unparsed-groups)
    - [Type](#type)
    - [Station](#station)
    - [Time](#time)
    - [Modifier](#modifier)

</td>
<!-- <td width=33% valign=top>
</td>
<td valign=top>
</td> -->
</tr>
</table>

## Metar

All features of the `Metar` report are represented as objects in the package. So, these objects have inside
of them another objects as fields, properties and methods. In the next sections you have a tour across all of 
that characteristics. 

Import the `Metar` object and instantiate it with the following syntax:

```python
from aeromet_py import Metar

code = "KMIA 130053Z 00000KT 10SM FEW030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233"
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

### Raw Code

Get the raw code as its received in the instance. TypeStation`str`station

```python
print(metar.raw_code)

# prints...
# KMIA 130053Z 00000KT 10SM FEWT030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233
```

### Sections

Get the `Metar` separated in its sections. Type `List[str]`.

```python
print(metar.sections)

# prints...
# ['KMIA 130053Z 00000KT 10SM FEW030 FEW045 BKN250 29/23 A2994', '', 'RMK AO2 SLP140 T02940233']
```

Where the first element is the body, the second is the trend and the last one is the remark.

### Unparsed Groups

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

Starting from here, all the properties contains this list of methods:

* as_dict() -> `Dict[str, Any]`: Returns the object data as a dictionary like `Dict[str, Any]`. In some
  cases the `Any` type is replaced by a especific type.
* to_json() -> `str`: Returns the object data as a string in JSON format.

Of course, the `Metar` object also containes this same methods.

### Type

Get the type of the Metar. Type `ReportType`.

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

### Station

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

### Time

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

### Modifier

Get the modifier description of the report. Type `Modifier`.

Fields:
* code `str | None`: The code present in the `Metar`, e.g. `AUTO`.
* description `str | None`: The description of the modifier code.

Supported codes are:
* COR: Correction
* CORR: Correction
* AMD: Amendment
* NIL: Missing report
* AUTO: Automatic report
* TEST: Testing report
* FINO: Missing report

```python
print(metar.modifier.code)
print(metar.modifier.description)

# prints...
# COR
# Correction
```