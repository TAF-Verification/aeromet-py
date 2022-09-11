# Aeromet-Py

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![codecov][coverage-shield]][coverage-url]
[![MIT License][license-shield]][license-url]

[coverage-shield]: https://codecov.io/gh/TAF-Verification/aeromet-py/branch/main/graph/badge.svg?token=1MUT17FQZY
[coverage-url]: https://codecov.io/gh/TAF-Verification/aeromet-py
[contributors-shield]: https://img.shields.io/github/contributors/TAF-Verification/aeromet-py.svg
[contributors-url]: https://github.com/TAF-Verification/aeromet-py/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TAF-Verification/aeromet-py.svg
[forks-url]: https://github.com/TAF-Verification/aeromet-py/network/members
[stars-shield]: https://img.shields.io/github/stars/TAF-Verification/aeromet-py.svg
[stars-url]: https://github.com/TAF-Verification/aeromet-py/stargazers
[issues-shield]: https://img.shields.io/github/issues/TAF-Verification/aeromet-py.svg
[issues-url]: https://github.com/TAF-Verification/aeromet-py/issues
[license-shield]: https://img.shields.io/github/license/TAF-Verification/aeromet-py.svg
[license-url]: https://github.com/TAF-Verification/aeromet-py/blob/master/LICENSE

Inspired from python-metar, a library writed in Python language to parse Meteorological Aviation Weather Reports (METAR and SPECI).

This library will parse meteorological information of aeronautical land stations.
Supported report types:
* METAR
* SPECI
* TAF

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

```python
from aeromet_py import Metar

code = 'METAR MROC 071200Z 10018KT 3000 R07/P2000N BR VV003 17/09 A2994 RESHRA NOSIG'
metar = Metar(code)

# Get the type of the report
print(f"{metar.type}")  # Meteorological Aerodrome Report

# Get the wind speed in knots and direction in degrees
print(f"{metar.wind.speed_in_knot} kt")       # 18.0 kt 
print(f"{metar.wind.direction_in_degrees}°")  # 100.0°

# Get the pressure in hecto pascals
print(f"{metar.pressure.in_hPa} hPa")  # 1014.0 hPa

# Get the temperature in Celsius
print(f"{metar.temperatures.temperature_in_celsius}°C")  # 17.0°C
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create.
Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.
You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [x] Add parsers for TAF and METAR reports
- [ ] Add functions to verificate the TAF with the observations
- [ ] Add a CLI API to interact with the verification functions
- [ ] Add parser for SYNOPTIC reports
- [ ] Add functions to verificate reports with rules of [Annex 3][annex3]
- [ ] Multi-language Support
    - [ ] Portuguese
    - [ ] Spanish

[annex3]: https://www.icao.int/airnavigation/IMP/Documents/Annex%203%20-%2075.pdf

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

## License

Distributed under the MIT License. See `LICENSE` for more information.