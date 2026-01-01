class BaseAgent:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name

    def decide(self, pid ,game_state):
        """Gibt True für 'Noch eine' oder False für 'Stopp' zurück."""
        raise NotImplementedError

    def choose_target(self, players, action_type):
        """Wählt eine Zielperson für Aktionen wie 'Freeze'."""
        raise NotImplementedError