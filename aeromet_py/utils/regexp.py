class RegularExpresions:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    STATION = r"^(?P<station>[A-Z][A-Z0-9]{3})$"

    TIME = r"^(?P<day>\d{2})" r"(?P<hour>\d{2})" r"(?P<min>\d{2})Z$"

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
