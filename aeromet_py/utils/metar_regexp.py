class MetarRegExp:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
