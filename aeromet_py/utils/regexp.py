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

    SKY = (
        r"^(?P<cover>VV|CLR|SCK|SCK|NSC|NCD|BKN|SCT|FEW|[O0]VC|///)"
        r"(?P<height>\d{3}|///)?"
        r"(?P<cloud>TCU|CB|///)?$"
    )

    TEMPERATURES = (
        r"^(?P<tsign>M|-)?"
        r"(?P<temp>\d{2}|//|XX|MM)/"
        r"(?P<dsign>M|-)?"
        r"(?P<dewpt>\d{2}|//|XX|MM)$"
    )

    PRESSURE = r"^(?P<units>A|Q|QNH)?" r"(?P<press>\d{4}|\//\//)" r"(?P<units2>INS)?$"

    RECENT_WEATHER = (
        r"^RE(?P<descrip>MI|PR|BC|DR|BL|SH|TS|FZ)?"
        r"(?P<precip>DZ|RA|SN|SG|IC|PL|GR|GS|UP)?"
        r"(?P<obsc>BR|FG|VA|DU|SA|HZ|PY)?"
        r"(?P<other>PO|SQ|FC|SS|DS)?$"
    )

    WINDSHEAR = r"^WS(?P<all>_ALL)?" r"_(RWY|R(?P<name>\d{2}[RCL]?))$"

    SEA_STATE = r"^W(?P<sign>M)?" r"(?P<temp>\d{2})/S" r"(?P<state>\d)$"

    TREND = r"^(?P<trend>TEMPO|BECMG|NOSIG|FM\d+|PROB\d{2})$"

    REMARK = r"^(?P<rmk>RMK(S)?)$"
