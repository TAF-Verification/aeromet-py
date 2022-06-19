from aeromet_py import Taf


def test_taf_flight_rules():
    code = """
    TAF UUDD 061958Z 0621/0803 22003MPS 9999 SCT016 TX09/0712Z TNM03/0621Z
        BECMG 0703/0704 18008G14MPS 5000 -SNRA
        TEMPO 0704/0709 0700 +SHSN FEW007 BKN016CB
        PROB40
        TEMPO 0704/0709 -FZRA OVC007
    """
    taf = Taf(code)

    assert taf.flight_rules == "VFR"

    changes = taf.change_periods
    assert changes[0].flight_rules == "MVFR"
    assert changes[1].flight_rules == "VLIFR"
    assert changes[2].flight_rules == "IFR"
