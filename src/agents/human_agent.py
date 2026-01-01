from .base_agent import BaseAgent
from src.graphics.visualize import Visualizer

class HumanAgent(BaseAgent):
    def decide(self, pid, game_state):
        own_state = game_state['players'][pid]
        
        # Visuelle Aufbereitung nur für den Menschen
        Visualizer.visualize_game_state(game_state, self.id)
        print(f"\n--- {self.name}, du bist am Zug ---")
        choice = input("Möchtest du (n)och eine Karte oder (s)toppen? [n/s]: ").lower()
        return choice == 'n'

    def choose_target(self, players, action_type):
        print(f"Aktion {action_type}! Wähle ein Ziel:")
        valid_targets = [p_id for p_id in players]
        for p_id in valid_targets:
            print(f"ID: {p_id}")
        target = input("Ziel-ID eingeben: ")
        return int(target) if target.isdigit() else valid_targets[0]