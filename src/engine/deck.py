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
        """
        Manuelle Serialisierung, da __slots__ kein __dict__ erlaubt.
        """
        return {
            'name': self.name,
            'type': self.type,              # Types: NUMBER, ACTION...
            'type_name': self.type.name,    # string name for visualization
            'value': self.value             # value of the card (relevant for NUMBER cards)
        }

class Deck:
    def __init__(self, config):
        # load seed from config for reproducability
        self.seed = config['game'].get('seed')
        self._rng = random.Random(self.seed)
        
        # build deck & discard pile
        self.cards = self._build_deck()
        self.discard_pile = []

        # shuffle based on the seed
        self._rng.shuffle(self.cards)

    def _build_deck(self):
        """
        Creates a deck, based on the flip7 rules.
        """
        deck = []

        # add NUMBER cards
        for num in range(1, 13):
            for _ in range(num):
                deck.append(Card(name=str(num), type=CardType.NUMBER, value=num))
        deck.append(Card(name="0", type=CardType.NUMBER, value=0))

        # add ACTION cards
        actions = [
            ("FREEZE", CardType.ACTION),
            ("SECOND CHANCE", CardType.ACTION),
            ("FLIP THREE", CardType.ACTION)
        ]
        for name, c_type in actions:
            for _ in range(3):
                deck.append(Card(name=name, type=c_type, value=0))

        # add BONUS_ADD cards
        for bonus_val in [2, 4, 6, 8, 10]:
            deck.append(Card(name=f"+{bonus_val}", type=CardType.BONUS_ADD, value=bonus_val))
        
        # add BONUS_MULT card
        deck.append(Card(name="x2", type=CardType.BONUS_MULT, value=2))

        return deck

    def draw(self):
        if not self.cards:
            self._reshuffle() # [cite: 154]
        return self.cards.pop()
    
    def _reshuffle(self):
        """
        Reshuffles the cards from discard pile if deck is empty.
        """
        if not self.discard_pile:
            raise RuntimeError("Keine Karten mehr im Stapel und im Ablagestapel vorhanden!")
 
        self.cards = self.discard_pile[:]
        self.discard_pile = []
        self._rng.shuffle(self.cards)