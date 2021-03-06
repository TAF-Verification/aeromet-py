from aeromet_py import Metar


def test_snoclo():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R09L/SNOCLO"
    )
    state = metar.runway_state

    assert state.code == "R09L/SNOCLO"
    assert state.name == "09 left"
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == True
    assert state.clrd == None
    assert str(state) == "aerodrome is closed due to extreme deposit of snow"
    assert state.as_dict() == {
        "clrd": None,
        "code": "R09L/SNOCLO",
        "contamination": None,
        "deposits": None,
        "deposits_depth": None,
        "name": "09 left",
        "snoclo": True,
        "surface_friction": None,
    }


def test_clrd():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R25C/CLRD//"
    )
    state = metar.runway_state

    assert state.code == "R25C/CLRD//"
    assert state.name == "25 center"
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == False
    assert state.clrd == "contaminations have ceased to exists on runway 25 center"
    assert str(state) == "contaminations have ceased to exists on runway 25 center"
    assert state.as_dict() == {
        "clrd": "contaminations have ceased to exists on runway 25 center",
        "code": "R25C/CLRD//",
        "contamination": None,
        "deposits": None,
        "deposits_depth": None,
        "name": "25 center",
        "snoclo": False,
        "surface_friction": None,
    }


def test_runway_state():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R10R/527650"
    )
    state = metar.runway_state

    assert state.code == "R10R/527650"
    assert state.name == "10 right"
    assert state.deposits == "wet snow"
    assert state.contamination == "11%-25% of runway"
    assert state.deposits_depth == "76 mm"
    assert state.surface_friction == "0.50"
    assert state.snoclo == False
    assert state.clrd == None
    assert (
        str(state)
        == "10 right, deposits of 76 mm of wet snow, contamination 11%-25% of runway, estimated surface friction 0.50"
    )
    assert state.as_dict() == {
        "clrd": None,
        "code": "R10R/527650",
        "contamination": "11%-25% of runway",
        "deposits": "wet snow",
        "deposits_depth": "76 mm",
        "name": "10 right",
        "snoclo": False,
        "surface_friction": "0.50",
    }


def test_no_runway_state():
    metar = Metar("METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965")
    state = metar.runway_state

    assert state.code == None
    assert state.name == None
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == False
    assert state.clrd == None
    assert str(state) == ""
    assert state.as_dict() == {
        "clrd": None,
        "code": None,
        "contamination": None,
        "deposits": None,
        "deposits_depth": None,
        "name": None,
        "snoclo": False,
        "surface_friction": None,
    }
