from aeromet_py import Metar

def test_code():
    metar = Metar("SPECI UUDD 212130Z 35003MPS 320V020 CAVOK 18/12 Q1008 R88/60D NOSIG", year=2021, month=7)
    time = metar.time.time
    time_code = metar.time.code
    time_year = time.year
    time_month = time.month
    time_day = time.day
    time_hour = time.hour
    time_minute = time.minute
    
    assert time_code == "212130Z"
    assert time_year == 2021
    assert time_month == 7
    assert time_day == 21
    assert time_hour == 21
    assert time_minute == 30