class RegularExpresions:

    TYPE = r"^(?P<type>METAR|SPECI|TAF)$"

    MODIFIER = r"^(?P<mod>COR(R)?|AMD|NIL|TEST|FINO|AUTO)$"
    
    TIME = r"^(?P<day>\d{2})(?P<hour>\d{2})(?P<min>\d{2})Z$"
