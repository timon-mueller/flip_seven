from enum import Enum, auto

class CardType(Enum):
    NUMBER = auto()      # Karten 0-12 [cite: 27, 28]
    ACTION = auto()      # Freeze, Second Chance, Flip Three [cite: 25, 43]
    BONUS_ADD = auto()   # +2, +4, +6, +8, +10 [cite: 38, 42, 50]
    BONUS_MULT = auto()  # x2 [cite: 39, 122, 188]