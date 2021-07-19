from .metar import Metar

metar = Metar(
    "METAR MROC 161900Z 09014KT 070V130 CAVOK 29/16 A2999 RMK VEL MAX VTO 25KT BECMG 08015G25KT"
)

print(metar.raw_code)
print(metar.sections)
print(metar.__dict__)

# metar.sections = "other"
# print(metar.sections)
# print(metar.__dict__)