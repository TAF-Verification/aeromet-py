class RegularExpresions:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    STATION = r"^(?P<station>[A-Z][A-Z0-9]{3})$"

    MODIFIER = r"^(?P<mod>COR(R)?|AMD|NIL|TEST|FINO|AUTO)$"

    TIME = r"^(?P<day>\d{2})(?P<hour>\d{2})(?P<min>\d{2})Z$"

    WIND = r"^(?P<dir>[0-3]\d{2}|///|MMM|VRB|P)(?P<speed>[\d]{2}|[/M]{2})(G(?P<gust>\d{2}|[/M{2}]))?(?P<units>KT|MPS)$"

    WIND_VARIATION = r"^(?P<from>\d{3})V(?P<to>\d{3})$"
