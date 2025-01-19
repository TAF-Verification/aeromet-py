import pytest

from typing import Dict, Any, Optional

from aeromet_py import Metar

modifier_metars: Dict[Optional[str], Dict[str, Any]] = {
    "AUTO": {
        "code": "METAR KJST 060154Z AUTO 05007KT 10SM OVC085 13/01 A3004 RMK AO2 SLP174 T01280006",
        "desc": "Automatic report",
        "dict": {"code": "AUTO", "modifier": "Automatic report"},
    },
    "NIL": {
        "code": "METAR KJST 060100Z NIL",
        "desc": "Missing report",
        "dict": {"code": "NIL", "modifier": "Missing report"},
    },
    "COR": {
        "code": "METAR MROC 202200Z COR 08011KT 9999 FEW045 SCT200 29/17 A2989 NOSIG",
        "desc": "Correction",
        "dict": {"code": "COR", "modifier": "Correction"},
    },
    None: {
        "code": "SPECI UUDD 152330Z 29005MPS 9999 SCT019 07/04 Q1014 R32L/290042 NOSIG",
        "desc": None,
        "dict": {"code": None, "modifier": None},
    },
}


@pytest.mark.parametrize("mod,d", [(mod, d) for mod, d in modifier_metars.items()])
def test_modifier(mod, d):
    metar = Metar(d.get("code"))

    assert metar.modifier.code == mod
    assert metar.modifier.description == d.get("desc")

    mod_as_string = d.get("desc").lower() if mod else ""
    assert str(metar.modifier) == mod_as_string

    assert metar.modifier.as_dict() == d.get("dict")
