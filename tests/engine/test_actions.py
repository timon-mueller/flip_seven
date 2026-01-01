from src.engine.card_types import CardType


def test_second_chance_prevents_bust(game_engine, mock_card_factory):
    """Testet, ob die Second Chance Karte eine Dublette neutralisiert[cite: 168]."""
    p_id = 0
    state = game_engine.player_states[p_id]
    
    # 1. Vorbereitung: Spieler hat bereits eine 6 und eine Second Chance
    state['cards'].append(mock_card_factory("6", CardType.NUMBER, 6))
    state['has_second_chance'] = True
    
    # 2. Aktion: Spieler zieht erneut eine 6 (Dublette) [cite: 71]
    duplicate_card = mock_card_factory("6", CardType.NUMBER, 6)
    game_engine._process_drawn_card(p_id, duplicate_card, game_engine.player_states)
    
    # 3. Überprüfung: Spieler ist nicht 'busted', aber Second Chance ist verbraucht
    assert state['busted'] is False
    assert state['has_second_chance'] is False
    assert len(state['cards']) == 2