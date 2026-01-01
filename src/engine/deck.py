from dataclasses import dataclass
from enum import Enum
import random

from src.engine.card_types import CardType

@dataclass
class Card:
    __slots__ = ['name', 'type', 'value']
    name: str
    type: CardType
    value: int

    def to_dict(self):
        """Manuelle Serialisierung, da __slots__ kein __dict__ erlaubt."""
        return {
            'name': self.name,
            'type': self.type, # Das Enum-Objekt selbst für Logik-Checks
            'type_name': self.type.name, # String-Name für Visualisierung/KI
            'value': self.value
        }

class Deck:
    def __init__(self, config):
        # Seed aus der Config laden
        self.seed = config['game'].get('seed')
        # Eigene Random-Instanz für Kapselung und Reproduzierbarkeit
        self._rng = random.Random(self.seed)
        
        self.cards = self._build_deck(config)
        self.discard_pile = []
        # Nutze die Instanz-Methode zum Mischen
        self._rng.shuffle(self.cards)

    def _build_deck(self, config):
        """
        Erstellt das Deck basierend auf den offiziellen FLIP7-Frequenzen.
        """
        deck = []

        # 1. Zahlenkarten (79 Karten insgesamt) [cite: 27, 28]
        # Zahlen 1-12: Häufigkeit entspricht dem Wert 
        for num in range(1, 13):
            for _ in range(num):
                deck.append(Card(name=str(num), type=CardType.NUMBER, value=num))
        
        # Die "0" ist genau einmal im Stapel 
        deck.append(Card(name="0", type=CardType.NUMBER, value=0))

        # 2. Aktionskarten (9 Karten insgesamt) 
        # Es gibt 3 Typen: Freeze, Second Chance, Flip Three [cite: 25]
        # Jeder Typ ist genau 3-mal vorhanden [cite: 49]
        actions = [
            ("FREEZE", CardType.ACTION),
            ("SECOND CHANCE", CardType.ACTION),
            ("FLIP THREE", CardType.ACTION)
        ]
        for name, c_type in actions:
            for _ in range(3):
                deck.append(Card(name=name, type=c_type, value=0))

        # 3. Bonuskarten (6 Karten insgesamt) [cite: 25, 38]
        # Plus-Karten: +2, +4, +6, +8, +10 [cite: 39, 40, 41, 42, 50]
        for bonus_val in [2, 4, 6, 8, 10]:
            deck.append(Card(name=f"+{bonus_val}", type=CardType.BONUS_ADD, value=bonus_val))
        
        # Multiplikator-Karte: x2 [cite: 39, 122, 188]
        deck.append(Card(name="x2", type=CardType.BONUS_MULT, value=2))

        return deck

    def draw(self):
        if not self.cards:
            self._reshuffle() # [cite: 154]
        return self.cards.pop()