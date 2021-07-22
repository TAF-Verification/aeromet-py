from .metar import Metar

metar = Metar(
    "SPECI MROC 220000Z COR VRB02KT 9999 SCT030 24/22 A2995 RMK VEL MAX VTO 25KT BECMG 08015G25KT",
    truncate=False,
    # truncate=True,
)

print(metar.code)
print(metar.sections)
print(metar.type, metar.type.code, metar.type.type)
print(metar.modifier, metar.modifier.code, metar.modifier.modifier)
print(metar.time.time.year, metar.time)

# metar.sections = "other"
# print(metar.sections)
# print(metar.__dict__)
