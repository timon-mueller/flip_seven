import pytest
from src.engine.deck import Deck

def test_deck_reshuffle_logic(game_config):
    """
    Testet, ob das Reshuffle die Karten korrekt vom Ablagestapel 
    in den Hauptstapel verschiebt und mischt.
    """
    deck = Deck(game_config)
    total_cards_init = len(deck.cards) # Sollte 94 sein
    
    # 1. Simuliere das Leeren des Decks durch Ziehen von Karten
    drawn_cards = []
    for _ in range(total_cards_init):
        card = deck.draw()
        drawn_cards.append(card)
        # Wir legen die Karten manuell in den Ablagestapel
        deck.discard_pile.append(card)
    
    assert len(deck.cards) == 0
    assert len(deck.discard_pile) == total_cards_init
    
    # 2. Die nächste Ziehung muss ein automatisches Reshuffle auslösen 
    next_card = deck.draw()
    
    # 3. Überprüfungen (Assertions)
    # - Der Stapel muss jetzt wieder voll sein (minus die eine gezogene Karte)
    assert len(deck.cards) == total_cards_init - 1
    
    # - Der Ablagestapel muss geleert worden sein 
    assert len(deck.discard_pile) == 0
    
    # - Die Gesamtzahl der Karten im System muss gleich bleiben (94)
    all_current_cards = deck.cards + [next_card]
    assert len(all_current_cards) == total_cards_init
    
    # - Optional: Prüfen, ob die Reihenfolge anders ist als die ursprüngliche Liste 
    # (Sehr hohe Wahrscheinlichkeit bei 94 Karten)
    # Da wir Card-Objekte haben, vergleichen wir die Namen-Sequenz
    current_names = [c.name for c in deck.cards]
    original_names_reversed = [c.name for c in reversed(drawn_cards[:-1])]
    assert current_names != original_names_reversed