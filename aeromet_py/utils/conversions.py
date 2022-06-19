from math import pi


class Conversions:

    # Distance conversions
    FT_TO_M = 0.3048
    SMI_TO_KM = 1.852
    KM_TO_SMI = 1 / SMI_TO_KM
    KM_TO_M = 1000
    M_TO_KM = 1 / KM_TO_M
    M_TO_SMI = M_TO_KM * KM_TO_SMI
    M_TO_FT = 1 / FT_TO_M
    M_TO_DM = 10.0
    M_TO_CM = 100.0
    M_TO_IN = 39.3701

    # Direction conversions
    DEGREES_TO_RADIANS = pi / 180
    DEGREES_TO_GRADIANS = 1.11111111

    # Speed conversions
    KNOT_TO_MPS = 0.51444444
    KNOT_TO_MIPH = 1.15078
    KNOT_TO_KPH = 1.852
    MPS_TO_KNOT = 1 / KNOT_TO_MPS

    # Pressure conversions
    HPA_TO_INHG = 0.02953
    INHG_TO_HPA = 1 / HPA_TO_INHG
    HPA_TO_BAR = 0.001
    BAR_TO_HPA = 1 / HPA_TO_BAR
    MBAR_TO_HPA = BAR_TO_HPA / 1000
    HPA_TO_MBAR = HPA_TO_BAR * 1000
    HPA_TO_ATM = 1 / 1013.25

    # Temperature conversions
    @staticmethod
    def celsius_to_kelvin(temp: float) -> float:
        return temp + 273.15

    @staticmethod
    def kelvin_to_celsius(temp: float) -> float:
        return temp - 273.15

    @staticmethod
    def celsius_to_fahrenheit(temp: float) -> float:
        return temp * 9 / 5 + 32

    @staticmethod
    def fahrenheit_to_celsius(temp: float) -> float:
        return (temp - 32) * 5 / 9

    @staticmethod
    def celsius_to_rankine(temp: float) -> float:
        return temp * 9 / 5 + 491.67

    @staticmethod
    def rankine_to_celsius(temp: float) -> float:
        return (temp - 491.67) * 5 / 9
