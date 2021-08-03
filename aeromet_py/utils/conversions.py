from math import pi

class Conversions:

    # Distance conversions
    SMI_TO_KM = 1.852
    KM_TO_SMI = 1 / SMI_TO_KM
    KM_TO_M = 1000
    M_TO_KM = 1 / KM_TO_M
    M_TO_SMI = M_TO_KM * KM_TO_SMI
    FT_TO_M = 0.3048
    M_TO_FT = 1 / FT_TO_M

    # Direction conversions
    DEGREES_TO_RADIANS = pi / 180
    DEGREES_TO_GRADIANS = 1.11111111

    # Speed conversions
    KNOT_TO_MPS = 0.51444444
    KNOT_TO_MIPH = 1.15078
    KNOT_TO_KPH = 1.852
    MPS_TO_KNOT = 1 / KNOT_TO_MPS
