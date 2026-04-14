from enum import Enum


class SexsEnum(str, Enum):
    """Enums for sexs"""

    L = "L"
    P = "P"


class ReligionsEnum(str, Enum):
    """Enums for recognized religions in Indonesia"""

    islam = "Islam"
    kristen = "Kristen"
    katolik = "Katolik"
    buddha = "Buddha"
    hindu = "Hindu"
    konghucu = "Konghucu"
