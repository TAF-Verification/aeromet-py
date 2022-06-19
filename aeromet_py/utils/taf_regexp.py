class TafRegExp:

    AMD_COR = r"^(?P<mod>COR|AMD)$"

    NIL = r"^NIL$"

    VALID = (
        r"^(?P<fmday>0[1-9]|[12][0-9]|3[01])"
        r"(?P<fmhour>[0-1]\d|2[0-3])/"
        r"(?P<tlday>0[1-9]|[12][0-9]|3[01])"
        r"(?P<tlhour>[0-1]\d|2[0-4])$"
    )

    CANCELLED = r"^CNL$"

    WIND = (
        r"^(?P<dir>([0-2][0-9]|3[0-6])0|VRB)"
        r"P?(?P<speed>\d{2,3})"
        r"(G(P)?(?P<gust>\d{2,3}))?"
        r"(?P<units>KT|MPS)$"
    )

    VISIBILITY = (
        r"^(?P<vis>\d{4})"
        r"(?P<dir>[NSEW]([EW])?)?|"
        r"(M|P)?(?P<integer>\d{1,2})?_?"
        r"(?P<fraction>\d/\d)?"
        r"(?P<units>SM|KM|M|U)|"
        r"(?P<cavok>CAVOK)$"
    )

    TEMPERATURE = (
        r"T(?P<type>N|X)"
        r"(?P<sign>M)?"
        r"(?P<temp>\d{2})/"
        r"(?P<day>0[1-9]|[12][0-9]|3[01])"
        r"(?P<hour>[0-1]\d|2[0-3])Z"
    )

    CHANGE_INDICATOR = (
        r"^TEMPO|BECMG"
        r"|FM(?P<day>0[1-9]|[12][0-9]|3[01])"
        r"(?P<hour>[0-1]\d|2[0-3])"
        r"(?P<minute>[0-5]\d)"
        r"|PROB[34]0(_TEMPO)?$"
    )
