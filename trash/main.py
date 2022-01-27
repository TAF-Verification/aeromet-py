from aeromet_py import Metar

metars = [
    "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R09L/SNOCLO",
    "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R88/CLRD//",
    "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R10R//57665",
    "METAR PANC 210353Z 01006KT 10SM FEW045 BKN070 OVC100 M05/M17 A2965 R25//266//",
]

metar = Metar(
    "METAR MROC 202000Z 12013G23KT 9999 FEW040 SCT100 27/16 A2997 WS R07L WS R25C NOSIG"
)

print(metar.pressure.in_atmospheres)

for code in metars:
    metar = Metar(code)
    print(metar.runway_state)
    # print(metar.sea_state)
    print("#" * 20)