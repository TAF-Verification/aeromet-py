from typing import List

from aeromet_py import Metar
from ..mocks import ToVerifyCavok


def test_clear_conditions():
    observations: List[ToVerifyCavok] = [
        ToVerifyCavok(
            "METAR KLAX 302053Z 25009KT 10SM CLR 23/17 A2985 RMK AO2 SLP107 T02330167 58018",
            True,
        ),
        ToVerifyCavok(
            "METAR UUDD 300400Z 15003MPS 5000 BR NSC 05/05 Q1014 R14R/CLRD60 TEMPO 0300 FG",
            False,
        ),
        ToVerifyCavok(
            "METAR MROC 030500Z 07005KT 030V100 9999 SKC 21/18 A3011 NOSIG", True
        ),
    ]

    for obs in observations:
        metar = Metar(obs.code)
        clouds = metar.clouds

        assert clouds[0].cover == "clear"
        assert clouds.ceiling == False
        assert metar.should_be_cavok() == obs.should_be


def test_general_conditions():
    observations: List[ToVerifyCavok] = [
        ToVerifyCavok(
            "KATL 052052Z 33009G16KT 10SM FEW200 FEW250 26/03 A3002 RMK AO2 SLP162 T02560028 56014",
            True,
        ),
        ToVerifyCavok(
            "KBOS 052054Z 01012KT 7SM BKN009 OVC013 14/13 A2991 RMK AO2 DZB18E34 SLP128 P0000 60000 T01440128 50004 $",
            False,
        ),
        ToVerifyCavok(
            "KBWI 052054Z 31005KT 10SM SCT020 BKN035 BKN045 18/13 A2995 RMK AO2 SLP140 T01780128 55001 $",
            False,
        ),
        ToVerifyCavok(
            "KCLE 052051Z 01007KT 10SM FEW250 22/06 A3005 RMK AO2 SLP191 T02170061 56012",
            True,
        ),
        ToVerifyCavok(
            "KCLT 052052Z 32007KT 10SM FEW200 25/09 A2999 RMK SLP149 T02500089 56009",
            True,
        ),
        ToVerifyCavok(
            "KCVG 052052Z 31005KT 10SM BKN300 24/04 A3008 RMK AO2 SLP182 T02390039 56017",
            True,
        ),
        ToVerifyCavok(
            "KDCA 052058Z 35010KT 10SM SCT028 BKN039 OVC046 19/13 A2996 RMK AO2 T01940133",
            False,
        ),
        ToVerifyCavok(
            "KDEN 052053Z 04007KT 10SM SCT045 SCT200 20/06 A3030 RMK AO2 SLP204 T02000056 58012",
            False,
        ),
        ToVerifyCavok(
            "KDFW 052053Z 04004KT 10SM SCT250 31/06 A3004 RMK AO2 SLP164 T03060056 56020",
            True,
        ),
        ToVerifyCavok(
            "KDTW 052053Z 32009KT 10SM FEW130 BKN250 24/08 A3005 RMK AO2 SLP173 T02440083 56016 PNO",
            True,
        ),
        ToVerifyCavok(
            "KEWR 052055Z 02008KT 6SM -RA BR SCT008 BKN013 OVC025 13/13 A2992 RMK AO2 P0000 T01280128",
            False,
        ),
        ToVerifyCavok(
            "KFLL 052053Z 06009KT 10SM SCT040 SCT075 BKN090 28/19 A2995 RMK AO2 SLP140 T02780194 55007",
            False,
        ),
        ToVerifyCavok(
            "KIAD 052052Z 33012KT 10SM FEW037 BKN100 21/12 A2996 RMK AO2 SLP145 T02110117 55006",
            False,
        ),
        ToVerifyCavok(
            "KIAH 052053Z 05005KT 10SM FEW060 30/12 A3002 RMK AO2 SLP164 T03000122 56023",
            True,
        ),
        ToVerifyCavok(
            "KJFK 052102Z 33011KT 10SM -RA FEW006 BKN080 OVC100 13/13 A2989 RMK AO2 VIS 2 1/2 W P0002 T01330133",
            False,
        ),
        ToVerifyCavok(
            "KLAS 052056Z 00000KT 10SM FEW140 31/01 A3002 RMK AO2 SLP141 T03110011 58023",
            True,
        ),
        ToVerifyCavok(
            "KLAX 052053Z 24012KT 8SM FEW009 SCT018 23/18 A2996 RMK AO2 SLP142 T02330178 58013",
            False,
        ),
        ToVerifyCavok(
            "KLGA 052113Z 33010KT 10SM SCT016 OVC065 14/12 A2989 RMK AO2 T01440122",
            False,
        ),
        ToVerifyCavok(
            "KMCO 052053Z 03004KT 10SM SCT055 28/14 A2998 RMK AO2 SLP150 T02780144 55013",
            True,
        ),
        ToVerifyCavok(
            "KMDW 052053Z 24010KT 10SM SCT150 BKN200 BKN250 25/00 A3005 RMK AO2 SLP171 T02500000 56020",
            True,
        ),
        ToVerifyCavok(
            "KMEM 052054Z 35006KT 10SM FEW250 26/04 A3008 RMK AO2 SLP181 T02610044 56018",
            True,
        ),
        ToVerifyCavok(
            "KMIA 052053Z COR 05010KT 10SM -RA BKN035 BKN060 BKN080 28/20 A2995 RMK AO2 RAB41 SLP144 P0000 60000 T02830200 55004",
            False,
        ),
        ToVerifyCavok(
            "KMSP 052053Z 28006KT 10SM FEW030 FEW040 BKN090 21/13 A2999 RMK AO2 SLP152 T02060128 55007",
            False,
        ),
        ToVerifyCavok(
            "KORD 052051Z VRB06KT 10SM SCT170 BKN200 BKN250 24/01 A3004 RMK AO2 SLP172 T02390006 56020",
            True,
        ),
        ToVerifyCavok(
            "KPDX 052118Z 00000KT 10SM BKN017 19/13 A3013 RMK AO2 T01940133", False
        ),
        ToVerifyCavok(
            "KPHL 052054Z 36007G18KT 10SM OVC016 18/13 A2993 RMK AO2 SLP134 T01780133 53004",
            False,
        ),
        ToVerifyCavok(
            "KPHX 052051Z 18004KT 10SM FEW090 FEW250 33/10 A2990 RMK AO2 SLP107 CB DSNT E AND S AND NW T03330100 58028",
            True,
        ),
        ToVerifyCavok(
            "KPIT 052051Z 32007KT 10SM FEW250 21/03 A3005 RMK AO2 SLP183 T02110033 56010",
            True,
        ),
        ToVerifyCavok(
            "KSAN 052102Z 29006KT 10SM OVC009 21/17 A2997 RMK AO2 T02060172", False
        ),
        ToVerifyCavok(
            "KSEA 052053Z 28004KT 3SM BR OVC007 15/13 A3019 RMK AO2 SLP229 T01500128 58007",
            False,
        ),
        ToVerifyCavok(
            "KSFO 052056Z 34008KT 10SM FEW006 22/14 A2999 RMK AO2 SLP155 T02170139 58018",
            False,
        ),
        ToVerifyCavok(
            "KSLC 052054Z 31008KT 10SM FEW100 26/04 A3021 RMK AO2 SLP187 T02560039 58014",
            True,
        ),
        ToVerifyCavok(
            "KSTL 052051Z VRB03KT 10SM BKN140 BKN250 26/03 A3007 RMK AO2 SLP179 T02560033 56021",
            True,
        ),
        ToVerifyCavok(
            "KTPA 052053Z 26007KT 10SM SCT050 SCT250 27/17 A2997 RMK AO2 SLP149 T02720167 56014",
            True,
        ),
    ]

    for obs in observations:
        metar = Metar(obs.code)

        assert metar.should_be_cavok() == obs.should_be
