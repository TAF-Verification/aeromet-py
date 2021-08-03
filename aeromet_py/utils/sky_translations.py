class SkyTranslations:
    SKY_COVER = {
        "SKC": "clear",
        "CLR": "clear",
        "NSC": "clear",
        "NCD": "clear",
        "FEW": "a few",
        "SCT": "scattered",
        "BKN": "broken",
        "OVC": "overcast",
        "///": "",
        "VV": "indefinite ceiling",
    }

    CLOUD_TYPE = {
        "AC": "altocumulus",
        "ACC": "altocumulus castellanus",
        "ACSL": "standing lenticulas altocumulus",
        "AS": "altostratus",
        "CB": "cumulonimbus",
        "CBMAM": "cumulonimbus mammatus",
        "CCSL": "standing lenticular cirrocumulus",
        "CC": "cirrocumulus",
        "CI": "cirrus",
        "CS": "cirrostratus",
        "CU": "cumulus",
        "NS": "nimbostratus",
        "SC": "stratocumulus",
        "ST": "stratus",
        "SCSL": "standing lenticular stratocumulus",
        "TCU": "towering cumulus",
    }

    # Translation of the present-weather codes into english

    WEATHER_INT = {
        "-": "light",
        "+": "heavy",
        "-VC": "nearby light",
        "+VC": "nearby heavy",
        "VC": "nearby",
    }

    WEATHER_DESC = {
        "MI": "shallow",
        "PR": "partial",
        "BC": "patches of",
        "DR": "low drifting",
        "BL": "blowing",
        "SH": "showers",
        "TS": "thunderstorm",
        "FZ": "freezing",
    }

    WEATHER_PREC = {
        "DZ": "drizzle",
        "RA": "rain",
        "SN": "snow",
        "SG": "snow grains",
        "IC": "ice crystals",
        "PL": "ice pellets",
        "GR": "hail",
        "GS": "snow pellets",
        "UP": "unknown precipitation",
        "//": "",
    }

    WEATHER_OBSC = {
        "BR": "mist",
        "FG": "fog",
        "FU": "smoke",
        "VA": "volcanic ash",
        "DU": "dust",
        "SA": "sand",
        "HZ": "haze",
        "PY": "spray",
    }

    WEATHER_OTHER = {
        "PO": "sand whirls",
        "SQ": "squalls",
        "FC": "funnel cloud",
        "SS": "sandstorm",
        "DS": "dust storm",
    }

    WEATHER_SPECIAL = {
        "+FC": "tornado",
    }

    COLOR = {
        "BLU": "blue",
        "GRN": "green",
        "WHT": "white",
    }

    # table 3700
    SEA_STATE = {
        "0": "calm (glassy)",
        "1": "calm (rippled)",
        "2": "smooth (wavelets)",
        "3": "slight",
        "4": "moderate",
        "5": "rough",
        "6": "very rough",
        "7": "high",
        "8": "very high",
        "9": "phenomenal",
    }

    # table 0919
    RUNWAY_DEPOSITS = {
        "0": "clear and dry",
        "1": "damp",
        "2": "wet and water patches",
        "3": "rime and frost covered (depth normally less than 1 mm)",
        "4": "dry snow",
        "5": "wet snow",
        "6": "slush",
        "7": "ice",
        "8": "compacted or rolled snow",
        "9": "frozen ruts or ridges",
        "/": "type of deposit not reported (e.g. due to runway clearance in progress),",
    }

    # table 0519
    RUNWAY_CONTAMINATION = {
        "1": "less than 10%",
        "2": "11%-25%",
        "3": "reserved",
        "4": "reserved",
        "5": "26%-50%",
        "6": "reserved",
        "7": "reserved",
        "8": "reserved",
        "9": "51%-100%",
        "/": "not reported",
    }

    # table 1079
    DEPOSIT_DEPTH = {
        "00": "less than 1 mm",
        "91": "reserved",
        "92": "10 cm",
        "93": "15 cm",
        "94": "20 cm",
        "95": "25 cm",
        "96": "30 cm",
        "97": "35 cm",
        "98": "40 cm or more",
        "99": "runway(s) non-operational due to snow, slush, ice, large drifts or runway clearance, but depth not reported",
        "//": "depth of deposit operationally not significant or not measurable",
    }

    # table 0366
    SURFACE_FRICTION = {
        "91": "breaking action poor",
        "92": "breaking action medium/poor",
        "93": "breaking action medium",
        "94": "breaking action medium/good",
        "95": "breaking action good",
        "96": "reserved",
        "97": "reserved",
        "98": "reserved",
        "99": "unreliable",
        "//": "breaking conditions not reported and/or runway not operational",
    }

    # Translation of various remark codes into english

    PRESSURE_TENDENCY = {
        "0": "increasing, then decreasing",
        "1": "increasing more slowly",
        "2": "increasing",
        "3": "increasing more quickly",
        "4": "steady",
        "5": "decreasing, then increasing",
        "6": "decreasing more slowly",
        "7": "decreasing",
        "8": "decreasing more quickly",
    }

    LIGHTNING_FREQUENCY = {
        "OCNL": "occasional",
        "FRQ": "frequent",
        "CONS": "constant",
    }

    LIGHTNING_TYPE = {
        "IC": "intracloud",
        "CC": "cloud-to-cloud",
        "CG": "cloud-to-ground",
        "CA": "cloud-to-air",
    }
