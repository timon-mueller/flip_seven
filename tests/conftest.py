import pytest
from unittest.mock import MagicMock
from src.engine.card_types import CardType
from src.engine.deck import Card    
from src.engine.game import Game

@pytest.fixture
def game_config():
    """Gibt eine Standard-Konfiguration basierend auf dem Handbuch zurück."""
    return {
        'game': {
            'target_points': 200,    # Zielpunktzahl laut Anleitung [cite: 2]
            'flip7_bonus': 15,       # Bonus für 7 verschiedene Karten [cite: 7, 80]
            'seed': 42
        }
    }

@pytest.fixture
def mock_card_factory():
    """Hilfsfunktion, um schnell Test-Karten zu erzeugen."""
    def _make_card(name, c_type, value):
        return Card(name=name, type=c_type, value=value)
    return _make_card

@pytest.fixture
def sample_flip7_hand(mock_card_factory):
    """Erzeugt eine Hand, die genau einen Flip 7 erfüllt (7 verschiedene Zahlen)[cite: 6, 78]."""
    return [mock_card_factory(str(i), CardType.NUMBER, i) for i in range(1, 8)]

@pytest.fixture
def sample_multiplier_hand(mock_card_factory):
    """Erzeugt eine Hand mit Zahlen, x2 und Boni zum Testen der Scoring-Hierarchie[cite: 130, 190]."""
    return [
        mock_card_factory("10", CardType.NUMBER, 10),
        mock_card_factory("x2", CardType.BONUS_MULT, 2),
        mock_card_factory("+6", CardType.BONUS_ADD, 6)
    ]

@pytest.fixture
def game_engine(game_config):
    """Initialisiert eine Game-Engine mit einem Mock-Spieler."""
    player = MagicMock()
    player.id = 0
    player.name = "TestPlayer"
    
    engine = Game([player], game_config)
    # Initialisiere den player_states für Unittests manuell
    engine.player_states = {
        player.id: {
            'name': player.name,
            'cards': [],
            'busted': False,
            'frozen': False,
            'done': False,
            'has_second_chance': False
        }
    }
    return engine