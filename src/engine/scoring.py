from src.engine.card_types import CardType


def calculate_score(cards):
        """
        Berechnet die Punkte für eine gegebene Liste von Karten nach den offiziellen Regeln.
        Input: Liste von Card-Objekten.
        """
        # 1. Zahlenwerte zusammenzählen [cite: 116]
        # Die Karte "0" wird mit 0 Punkten gewertet [cite: 37]
        num_sum = sum(c.value for c in cards if c.type == CardType.NUMBER)

        # 2. Multiplikator prüfen [cite: 122]
        # Die x2-Karte verdoppelt ausschließlich die Summe der Zahlenkarten [cite: 190]
        if any(c.type == CardType.BONUS_MULT for c in cards):
            num_sum *= 2 # Verdopplung erfolgt vor der Addition der Boni [cite: 130]

        # 3. Bonuskarten (+2, +4, +6, +8, +10) summieren [cite: 131, 187]
        bonus_sum = sum(c.value for c in cards if c.type == CardType.BONUS_ADD)

        # 4. Gesamtsumme aus verdoppelten Zahlen und Boni bilden [cite: 133]
        total = num_sum + bonus_sum

        # 5. Flip 7 Bonus prüfen [cite: 6, 78]
        # Bei 7 verschiedenen Zahlenkarten gibt es 15 Extrapunkte [cite: 7, 80, 137]
        # Dieser Bonus wird nicht durch die x2-Karte verdoppelt [cite: 190]
        has_flip7 = True if len(set(c.value for c in cards if c.type == CardType.NUMBER)) == 7 else False
        if has_flip7:
            total += 15

        return total
