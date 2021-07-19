# AeroMet-Py

A library for Python developers.

This library will parse meteorological information of aeronautical land stations.

## Current METAR reports

The current report for a station is available at the URL

```
http://tgftp.nws.noaa.gov/data/observations/metar/stations/<station>.TXT
```

where `station` is the ICAO station code of the airport. This is a four-letter code.
For all stations at any cycle (i.e., hour) in the last  hours the reports are available
at the URL

```
http://tgftp.nws.noaa.gov/data/observations/metar/cycles/<cycle>Z.TXT
```

where `cycle` is the 2-digit cycle number (`00` to `23`).

## Usage

A simple usage example:

```Python
from aeromet_py import Metar

metar = Metar(
    "METAR MROC 161900Z 09014KT 070V130 CAVOK 29/16 A2999 RMK VEL MAX VTO 25KT BECMG 08015G25KT"
)

print(metar.sections)

# prints a list like this...
# [
#   "METAR MROC 181500Z 09012G23KT 050V110 9999 FEW035 SCT130 BKN200 27/18 A3004",
#   "NOSIG",
#   "RMK TS TO S"
# ]
```

## Features and bugs

Please file feature requests and bugs at the [issue tracker][tracker].

[tracker]: https://github.com/TAF-Verification/aeromet-py/issues

## Current Sources

The most recent version of this package is always available via git, only run the
following command on your terminal:

```
git clone https://github.com/TAF-Verification/aeromet-py.git
```

## Authors

The `python-metar` library was originaly authored by [Tom Pollard][TomPollard] in january 2005.
This package `aeromet-py` for is inspired from his work in 2021 by [Diego Garro][DiegoGarro].

[TomPollard]: https://github.com/tomp
[DiegoGarro]: https://github.com/diego-garro

## Versioning

This project uses [Bump2version][bumpversion] tool for versioning, so, if you fork this
repository remember install it in your environment.

[bumpversion]: https://pypi.org/project/bump2version/

```
pip install bump2version
```