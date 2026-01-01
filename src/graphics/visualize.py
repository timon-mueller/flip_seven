class Visualizer:
    @staticmethod
    def visualize_game_state(state, player_id):
        """Visualisiert den vollständigen Zustand für den menschlichen Spieler."""
        curr_id = state['meta']['current_player_id']
        
        print("\n" + "="*50)
        print(f" SPIELSTAND (Deck: {state['meta']['cards_in_deck']} Karten übrig) ") 
        print("="*50)

        for pid, p in state['players'].items():
            # Marker für den aktiven Spieler
            active_marker = ">> " if pid == curr_id else "   "
            
            # Status ermitteln
            status = ""
            if p['busted']: status = "💥 VERZOCKT" 
            elif p['frozen']: status = "❄️ FROZEN" 
            elif p['done']: status = "🛑 STOPP" 

            print(f"{active_marker}Spieler {pid} ({p['name']}): {p['total_score']} Pkt {status}")
            
            # Karten trennen in Zahlen und Boni
            numbers = [str(c['value']) for c in p['cards'] if c['type'].name == "NUMBER"]
            bonuses = [c['name'] for c in p['cards'] if "BONUS" in c['type'].name]
            
            if bonuses: print(f"      Boni:  [{' | '.join(bonuses)}]") 
            if numbers: print(f"      Reihe: | {' | '.join(numbers)} | ({len(set(numbers))}/7)") 
            if p['has_second_chance']: print("      🛡️ SECOND CHANCE AKTIV") 