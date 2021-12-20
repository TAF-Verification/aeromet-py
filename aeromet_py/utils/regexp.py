class RegularExpresions:

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

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
