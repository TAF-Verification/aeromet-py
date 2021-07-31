class RegularExpresions:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    STATION = r"^(?P<station>[A-Z][A-Z0-9]{3})$"

    MODIFIER = r"^(?P<mod>COR(R)?|AMD|NIL|TEST|FINO|AUTO)$"

    TIME = r"^(?P<day>\d{2})" r"(?P<hour>\d{2})" r"(?P<min>\d{2})Z$"

    WIND = (
        r"^(?P<dir>[0-3]\d{2}|///|MMM|VRB|P)"
        r"(?P<speed>[\d]{2}|[/M]{2})"
        r"(G(?P<gust>\d{2}|[/M{2}]))?"
        r"(?P<units>KT|MPS)$"
    )

    WIND_VARIATION = r"^(?P<from>\d{3})V(?P<to>\d{3})$"

    VISIBILITY = (
        r"^(?P<vis>\d{4}|\//\//)"
        r"(?P<dir>[NSEW]([EW])?)?|"
        r"((?P<opt>\d)_)?(M|P)?"
        r"(?P<visextreme>\d{1,2}|\d/\d)"
        r"(?P<units>SM|KM|M|U)|"
        r"(?P<cavok>CAVOK)$"
    )

    MINIMUM_VISIBILITY = r"^(?P<vis>\d{4})" r"(?P<dir>[NSEW]([EW])?)?$"

    RUNWAY_RANGE = (
        r"^R(?P<name>\d{2}([RLC])?)/"
        r"(?P<rvrlow>[MP])?"
        r"(?P<low>\d{2,4})"
        r"(V(?P<rvrhigh>[MP])?"
        r"(?P<high>\d{2,4}))?"
        r"(?P<units>FT)?"
        r"(?P<trend>[NDU])?$"
    )

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
