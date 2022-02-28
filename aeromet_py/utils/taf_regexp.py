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
        r"^(?P<dir>[0-2][0-9]0|3[0-6]0)"
        r"P?(?P<speed>\d{2,3})"
        r"(G(P)?(?P<gust>\d{2,3}))?"
        r"(?P<units>KT|MPS)$"
    )
