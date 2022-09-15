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

</td>
<td width=33% valign=top>
</td>
<td valign=top>
</td>
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

Get the raw code as its received in the instance. Type `str`.

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
code_with_bad_group = "KMIA 130053Z 00000KT 10SM FEWT030 FEW045 BKN250 29/23 A2994 RMK AO2 SLP140 T02940233"
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

* to_dict() -> `Dict[str, Any]`: Returns the object data as a dictionary like `Dict[str, Any]`. In some
  cases the `Any` type is replaced by a especific type.
* to_json() -> `str`: Returns the object data as a string in JSON format.

Of course, the `Metar` object also containes this same methods.

### Type

Get the type of the Metar. Type `Type`.

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