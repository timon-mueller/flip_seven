import random

from src.engine.card_types import CardType
from .base_agent import BaseAgent

class HeuristicAgent(BaseAgent):
    def decide(self, pid ,game_state):
        own_state = game_state['players'][pid]
        # In der decide-Methode des HeuristicAgent:
        own_numbers = {c['value'] for c in own_state['cards'] if c['type'] == CardType.NUMBER}
        
        # Heuristik: Wenn wir schon 6 verschiedene Zahlen haben, 
        # riskieren wir alles für den Flip 7 (15 Extrapunkte!)[cite: 6, 80].
        if len(own_numbers) == 6:
            return True
            
        # Risiko-Einschätzung: Wie viele der 13 möglichen Zahlen (0-12) haben wir schon?
        # Da höhere Zahlen öfter vorkommen, ist das Risiko bei 4+ Karten meist hoch[cite: 5, 23].
        if len(own_numbers) >= 4:
            return False 
            
        return True

    def choose_target(self, players, action_type):
        # Die KI wählt einfach zufällig einen Gegner[cite: 162, 178].
        targets = [p_id for p_id in players if p_id != self.id]
        return random.choice(targets) if targets else self.id