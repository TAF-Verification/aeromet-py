from aeromet_py import Metar


def test_snoclo():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R09L/SNOCLO"
    )
    state = metar.runway_state

    assert state.name == "09 left"
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == "aerodrome is closed due to extreme deposit of snow"
    assert state.clrd == None
    assert str(state) == "aerodrome is closed due to extreme deposit of snow"


def test_clrd():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R25C/CLRD//"
    )
    state = metar.runway_state

    assert state.name == "25 center"
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == None
    assert state.clrd == "contaminations have ceased to exist on runway 25 center"
    assert str(state) == "contaminations have ceased to exist on runway 25 center"


def test_runway_state():
    metar = Metar(
        "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R10R/527650"
    )
    state = metar.runway_state

    assert state.name == "10 right"
    assert state.deposits == "wet snow"
    assert state.contamination == "11%-25% of runway"
    assert state.deposits_depth == "76 mm"
    assert state.surface_friction == "0.50"
    assert state.snoclo == None
    assert state.clrd == None
    assert (
        str(state)
        == "10 right, deposits of 76 mm of wet snow, contamination 11%-25% of runway, estimated surface friction 0.50"
    )


def test_no_runway_state():
    metar = Metar("METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965")
    state = metar.runway_state

    assert state.name == None
    assert state.deposits == None
    assert state.contamination == None
    assert state.deposits_depth == None
    assert state.surface_friction == None
    assert state.snoclo == None
    assert state.clrd == None
    assert str(state) == ""
