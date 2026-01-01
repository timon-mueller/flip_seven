import yaml
from src.engine.game import Game
from src.agents.human_agent import HumanAgent
from src.agents.heuristic_agent import HeuristicAgent

def main():
    # 1. Konfiguration laden
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 2. Spieler erstellen
    p1 = HumanAgent(player_id=0, name="Du")
    p2 = HeuristicAgent(player_id=1, name="Computer 1")
    p3 = HeuristicAgent(player_id=2, name="Computer 2")
    
    # Als Dictionary an die Engine geben, damit der Zugriff per ID klappt
    players_dict = {p.id: p for p in [p1, p2, p3]}

    game = Game(list(players_dict.values()), config)
    
    print("=== FLIP7 START ===")
    while max(game.scores.values()) < config['game']['target_points']: 
        game.play_round() 
        print("\nAktuelle Punkte:")
        for p in players_dict.values():
            print(f"{p.name}: {game.scores[p.id]}")

if __name__ == "__main__":
    main()