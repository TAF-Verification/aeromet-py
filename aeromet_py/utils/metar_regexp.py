class MetarRegExp:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    STATION = r"^(?P<station>[A-Z][A-Z0-9]{3})$"

    TIME = (
        r"^(?P<day>0[1-9]|[12][0-9]|3[01])"
        r"(?P<hour>[0-1]\d|2[0-4])"
        r"(?P<min>[0-5]\d)Z$"
    )

    MODIFIER = r"^(?P<mod>COR(R)?|AMD|NIL|TEST|FINO|AUTO)$"

    WIND = (
        r"^(?P<dir>([0-2][0-9]|3[0-6])0|///|VRB)"
        r"P?(?P<speed>\d{2,3}|//|///)"
        r"(G(P)?(?P<gust>\d{2,3}))?"
        r"(?P<units>KT|MPS)$"
    )

    WIND_VARIATION = (
        r"^(?P<from>(0[1-9]|[12][0-9]|3[0-6])0)" r"V(?P<to>(0[1-9]|[12][0-9]|3[0-6])0)$"
    )

    VISIBILITY = (
        r"^((?P<vis>\d{4}|////)"
        r"(?P<dir>[NSEW]([EW])?)?|"
        r"(M|P)?(?P<integer>\d{1,2})?_?"
        r"(?P<fraction>\d/\d)?"
        r"(?P<units>SM|KM|M|U)|"
        r"(?P<cavok>CAVOK))$"
    )

    MINIMUM_VISIBILITY = r"^(?P<vis>\d{4}|////)" r"(?P<dir>[NSEW]([EW])?)?$"

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

    CLOUD = (
        r"^(?P<cover>VV|CLR|SKC|NSC|NCD|BKN|SCT|FEW|[O0]VC|///)"
        r"(?P<height>\d{3}|///)?"
        r"(?P<type>TCU|CB|///)?$"
    )

    TEMPERATURES = (
        r"^(?P<tsign>M|-)?"
        r"(?P<temp>\d{2}|//|XX|MM)/"
        r"(?P<dsign>M|-)?"
        r"(?P<dewpt>\d{2}|//|XX|MM)$"
    )

    PRESSURE = r"^(?P<units>A|Q|QNH)?" r"(?P<press>\d{4}|\//\//)" r"(?P<units2>INS)?$"

    RECENT_WEATHER = (
        r"^RE(?P<desc>MI|PR|BC|DR|BL|SH|TS|FZ)?"
        r"(?P<prec>DZ|RA|SN|SG|IC|PL|GR|GS|UP)?"
        r"(?P<obsc>BR|FG|VA|DU|SA|HZ|PY)?"
        r"(?P<other>PO|SQ|FC|SS|DS)?$"
    )

    WINDSHEAR = r"^WS(?P<all>_ALL)?" r"_(RWY|R(?P<name>\d{2}[RCL]?))$"

    SEA_STATE = (
        r"^W(?P<sign>M)?"
        r"(?P<temp>\d{2})"
        r"/(S(?P<state>\d)"
        r"|H(?P<height>\d{3}))$"
    )

    RUNWAY_STATE = (
        r"^R(?P<name>\d{2}([RLC])?)?/("
        r"(?P<deposit>\d|/)"
        r"(?P<cont>\d|/)"
        r"(?P<depth>\d\d|//)"
        r"(?P<fric>\d\d|//)|"
        r"(?P<snoclo>SNOCLO)|"
        r"(?P<clrd>CLRD//))$"
    )

    CHANGE_INDICATOR = r"^TEMPO|BECMG|NOSIG$"

    TREND_TIME_PERIOD = (
        r"^(?P<prefix>FM|TL|AT)" r"(?P<hour>[01]\d|2[0-4])" r"(?P<min>[0-5]\d)$"
    )

    REMARK = r"^(?P<rmk>RMK(S)?)$"
