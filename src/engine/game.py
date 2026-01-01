import random
from src.engine.deck import Deck
from src.engine.scoring import calculate_score
from src.engine.card_types import CardType


class Game:
    def __init__(self, players, config):
        self.players = players  # Liste von Agent-Objekten
        self.config = config
        self.scores = {p.id: 0 for p in players}
        self.deck = Deck(config)

    def play_round(self):
        """
         Führt eine komplette Runde FLIP7 nach offiziellen Regeln aus.
        """
        self.round_ended_by_flip7 = False

        # 1. Initialisierung des Runden-Status für alle Spieler 
        # Wir nutzen ein lokales Dictionary für den flüchtigen Status dieser Runde
        self.player_states = {
            p.id: {
                'name': p.name,
                'cards': [],           # Liste der Card-Objekte [cite: 85]
                'busted': False,       # Hat sich verzockt? [cite: 4, 71]
                'frozen': False,       # Durch Freeze-Karte blockiert? [cite: 162]
                'done': False,         # Hat freiwillig STOPP gesagt? [cite: 59, 63]
                'has_second_chance': False # Schutz aktiv? [cite: 168]
            } for p in self.players
        }

        players_dict = {p.id: p for p in self.players}

        # 2. Die Startkarten verteilen 
        # Jede Person erhält reihum eine Karte offen ausgelegt.
        for p_id in players_dict:
            if not self.round_ended_by_flip7:
                # Falls hier eine Aktionskarte kommt, wird das Austeilen kurz unterbrochen [cite: 55]
                self._draw_card_for_player(p_id, self.player_states, players_dict)

        # 3. Die Hauptrunde (Entscheidungsphase) [cite: 59]
        # Es wird so lange reihum gefragt, bis die Runde beendet ist[cite: 60].
        while not self.round_ended_by_flip7:
            any_player_acted = False
            
            for p_id in list(players_dict.keys()):
                state = self.player_states[p_id]
                
                # Nur Spieler fragen, die noch im Spiel sind [cite: 67, 72, 162]
                if state['busted'] or state['done'] or state['frozen']:
                    continue
                
                any_player_acted = True
                
                # Agenten-Entscheidung: (pid, gamestate) [cite: 59, 65]
                current_state = self._get_complete_state(p_id, self.player_states)
                decision = players_dict[p_id].decide(p_id, current_state)
                
                if decision: # "NOCH EINE" [cite: 65]
                    self._draw_card_for_player(p_id, self.player_states, players_dict)
                    # Sofortiger Abbruch der Schleife bei Flip 7 [cite: 7, 78, 113]
                    if self.round_ended_by_flip7:
                        break
                else: # "STOPP" [cite: 61, 63]
                    state['done'] = True

            # Die Runde endet, wenn niemand mehr im Spiel ist oder ein Flip 7 gelang[cite: 111, 113].
            if not any_player_acted or self.round_ended_by_flip7:
                break

        # 4. Punkteabrechnung am Rundenende [cite: 114]
        self._finalize_scores(player_states=self.player_states)
     

    def _draw_card_for_player(self, p_id, player_states, active_players):
        """Standard-Zug: Zieht eine Karte und führt sie sofort aus."""
        card = self.deck.draw()
        
        if card.type == CardType.ACTION:
            # Im normalen Zug werden Aktionen sofort ausgeführt
            self._handle_action(card, p_id, player_states, active_players)
        else:
            # Zahlen und Boni werden normal verarbeitet
            self._process_drawn_card(p_id, card, player_states)

    def _process_drawn_card(self, p_id, card, player_states):
        """Verarbeitet Karten und speichert das Objekt (nicht das Dict)."""
        state = player_states[p_id]

        match card.type:
            case CardType.NUMBER:
                # Dubletten-Check: Wir prüfen gegen die .value Attribute der Objekte
                has_duplicate = any(c.value == card.value for c in state['cards'] if c.type == CardType.NUMBER)
                
                if has_duplicate:
                    if state.get('has_second_chance'): 
                        state['has_second_chance'] = False
                        # Karte wird trotzdem behalten (wichtig für die Endabrechnung) [cite: 168, 169]
                        state['cards'].append(card)
                    else:
                        state['busted'] = True 
                else:
                    state['cards'].append(card)

            case CardType.BONUS_ADD | CardType.BONUS_MULT:
                # Bonuskarten können sich nicht verzocken [cite: 95]
                state['cards'].append(card)
        
        # Sofortige Prüfung: Hat dieser Zug die Runde beendet?
        if self._has_flip7(state['cards']): 
            self.round_ended_by_flip7 = True

    def _handle_action(self, card, p_id, player_states, players_dict):
            """
            logic for action cards (freeze, second chance, flip three)
            """
            if card.name == "FREEZE":
                target_id = players_dict[p_id].choose_target(players_dict, "FREEZE")
                if target_id in player_states:
                    player_states[target_id]['frozen'] = True 
            
            elif card.name == "SECOND CHANCE":
                player_states[p_id]['has_second_chance'] = True 
                
            elif card.name == "FLIP THREE":
                # draw three cards one by one
                action_queue = []
                for _ in range(3):
                    if player_states[p_id]['busted'] or self._has_flip7(player_states[p_id]['cards']):
                        break
                    
                    drawn_card = self.deck.draw()
                    
                    # play action cards after all cards drawn
                    if drawn_card.type == CardType.ACTION:
                        action_queue.append(drawn_card)
                    else:
                        self._process_drawn_card(p_id, drawn_card, player_states)
                
                # process additional action cards
                for action_card in action_queue:
                    self._handle_action(action_card, p_id, player_states, players_dict)
                
    def _has_flip7(self, cards):
        """
        check if the player has a flip7.
        """
        numbers = {c.value for c in cards if c.type == CardType.NUMBER}
        return len(numbers) >= 7

    def _finalize_scores(self, player_states):
        """Verteilt die berechneten Punkte an die Spieler-Konten."""
        for p_id, state in player_states.items():
            # Wer sich verzockt hat, erhält keine Punkte für die Runde [cite: 4, 71]
            if state['busted']:
                continue

            # Berechnung via Untermethode
            round_score = calculate_score(state['cards'])
            
            # Addition zum Gesamtkonto aus vorherigen Runden [cite: 64, 115]
            self.scores[p_id] += round_score

    def _get_view_for_player(self, p_id, player_states):
        """
        creates information for agent.
        """
        return {
            'own_cards': player_states[p_id]['cards'],
            'others_cards': {pid: state['cards'] for pid, state in player_states.items() if pid != p_id},
            'scores': self.scores.copy()
        }
    
    def _get_complete_state(self, current_p_id, player_states):
        """Erzeugt ein vollständiges Dictionary des aktuellen Spielzustands."""
        return {
            'meta': {
                'target_points': self.config['game']['target_points'], 
                'cards_in_deck': len(self.deck.cards),
                'current_player_id': current_p_id
            },
            'players': {
                pid: {
                    'name': state['name'],
                    'cards': [c.to_dict() for c in state['cards']],
                    'busted': state['busted'], 
                    'done': state['done'], 
                    'frozen': state['frozen'],
                    'has_second_chance': state['has_second_chance'],
                    'total_score': self.scores[pid]
                } for pid, state in player_states.items()
            },
            'discard_pile': [c.to_dict() for c in self.deck.discard_pile]
        
        }