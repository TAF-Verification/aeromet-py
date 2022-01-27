class MetarRegExp:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    STATION = r"^(?P<station>[A-Z][A-Z0-9]{3})$"

    TIME = r"^(?P<day>\d{2})" r"(?P<hour>\d{2})" r"(?P<min>\d{2})Z$"

    MODIFIER = r"^(?P<mod>COR(R)?|AMD|NIL|TEST|FINO|AUTO)$"

    WIND = (
        r"^(?P<dir>[0-3]\d{2}|///|VRB)"
        r"P?(?P<speed>\d{2,3}|//)"
        r"(G(P)?(?P<gust>\d{2,3}))?"
        r"(?P<units>KT|MPS)$"
    )

    WIND_VARIATION = r"^(?P<from>\d{3})V(?P<to>\d{3})$"

    VISIBILITY = (
        r"^(?P<vis>\d{4}|////)"
        r"(?P<dir>[NSEW]([EW])?)?|"
        r"(?P<integer>\d{1,2})?_?(M|P)?"
        r"(?P<fraction>\d/\d)?"
        r"(?P<units>SM|KM|M|U)|"
        r"(?P<cavok>CAVOK)$"
    )

    RUNWAY_RANGE = (
        r"^R(?P<name>\d{2}[RLC]?)/"
        r"(?P<rvrlow>[MP])?"
        r"(?P<low>\d{2,4})"
        r"(V(?P<rvrhigh>[MP])?"
        r"(?P<high>\d{2,4}))?"
        r"(?P<units>FT)?"
        r"(?P<trend>[NDU])?$"
    )

    WEATHER = (
        r"^(?P<int>(-|\+)VC|(-|\+)|VC)?"
        r"(?P<desc>MI|PR|BC|DR|BL|SH|TS|FZ)?"
        r"((?P<prec>DZ|RA|SN|SG|IC|PL|GR|GS|UP)|"
        r"(?P<obsc>BR|FG|FU|VA|DU|SA|HZ|PY)|"
        r"(?P<other>PO|SQ|FC|SS|DS|NSW|/))?$"
    )

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
