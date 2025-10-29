
#!/usr/bin/env python3
"""
rps_ai.py

Juego de Piedra, Papel o Tijera (Rock-Paper-Scissors) contra una IA que aprende
del comportamiento del jugador. La IA usa un modelo de Markov de orden 1:
estima la probabilidad de la siguiente jugada del jugador condicional a la
última jugada del jugador, y juega la contraria más probable.

Cómo usar:
    python3 /path/to/rps_ai.py

Controles en consola:
    1 = Piedra
    2 = Papel
    3 = Tijera
    q = salir

Características:
 - Aprendizaje en línea (actualiza el modelo tras cada jugada del jugador).
 - Fallback a frecuencias globales si no hay historial previo.
 - Exploración ε-greedy (la IA a veces elige aleatoriamente para evitar sobreajuste).
 - Guardado/recarga opcional del modelo en formato JSON (por defecto no se guarda).
"""

import json
import random
import os
from collections import defaultdict, Counter

MOVES = {
    "1": "Piedra",
    "2": "Papel",
    "3": "Tijera"
}

# Map a move to the move that beats it
BEATS = {
    "Piedra": "Papel",
    "Papel": "Tijera",
    "Tijera": "Piedra"
}

MODEL_PATH = "rps_model.json"

class MarkovRPS:
    def __init__(self, epsilon=0.05):
        # counts[prev_move][next_move] = count
        self.counts = defaultdict(Counter)
        # global frequency of next moves
        self.global_counts = Counter()
        self.epsilon = epsilon  # exploration probability

    def predict_next(self, prev_move):
        """Predict the player's next move string ('Piedra'|'Papel'|'Tijera')."""
        # Exploration: sometimes choose uniformly at random
        if random.random() < self.epsilon:
            return random.choice(list(BEATS.keys()))

        # If we have data for prev_move use conditional distribution
        if prev_move and sum(self.counts[prev_move].values()) > 0:
            counter = self.counts[prev_move]
        else:
            counter = self.global_counts

        if not counter:
            # No data at all, random guess
            return random.choice(list(BEATS.keys()))

        # Return the most common move (break ties randomly)
        max_count = max(counter.values())
        candidates = [m for m, c in counter.items() if c == max_count]
        return random.choice(candidates)

    def update(self, prev_move, next_move):
        """Update model with an observed transition prev_move -> next_move."""
        if prev_move:
            self.counts[prev_move][next_move] += 1
        self.global_counts[next_move] += 1

    def save(self, path=MODEL_PATH):
        data = {
            "counts": {pm: dict(cnt) for pm, cnt in self.counts.items()},
            "global_counts": dict(self.global_counts),
            "epsilon": self.epsilon
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path=MODEL_PATH):
        m = cls()
        if not os.path.exists(path):
            return m
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for pm, cnt in data.get("counts", {}).items():
            m.counts[pm] = Counter(cnt)
        m.global_counts = Counter(data.get("global_counts", {}))
        m.epsilon = data.get("epsilon", m.epsilon)
        return m

def get_player_move():
    prompt = "Elige (1)Piedra (2)Papel (3)Tijera, o 'q' para salir: "
    while True:
        choice = input(prompt).strip()
        if choice == "q":
            return "q"
        if choice in MOVES:
            return MOVES[choice]
        print("Entrada no válida. Intenta de nuevo.")

def decide_ai_move(ai_model, prev_player_move):
    """AI predicts the player's next move and selects the counter to it."""
    predicted_player_move = ai_model.predict_next(prev_player_move)
    # AI plays the move that beats the predicted player's move
    ai_move = BEATS[predicted_player_move]
    return ai_move, predicted_player_move

def resolve_round(player, ai):
    if player == ai:
        return "Empate"
    elif BEATS[player] == ai:
        # player's move is beaten by ai -> AI wins
        return "IA"
    else:
        return "Jugador"

def pretty_stats(stats):
    lines = [
        f"Rondas jugadas: {stats['rounds']}",
        f"Victorias jugador: {stats['player_wins']}",
        f"Victorias IA: {stats['ai_wins']}",
        f"Empates: {stats['ties']}",
        f"Frecuencia jugador: Piedra={stats['freq'].get('Piedra',0)}, Papel={stats['freq'].get('Papel',0)}, Tijera={stats['freq'].get('Tijera',0)}"
    ]
    return "\n".join(lines)

def main():
    print("=== Piedra, Papel o Tijera — IA que aprende ===")
    print("Controles: 1=Piedra, 2=Papel, 3=Tijera, q=salir")
    # Ask user if they want to load an existing model
    model = None
    if os.path.exists(MODEL_PATH):
        ans = input(f"Se encontró un modelo previo en '{MODEL_PATH}'. ¿Cargarlo? (s/n): ").strip().lower()
        if ans == "s":
            model = MarkovRPS.load(MODEL_PATH)
            print("Modelo cargado.")
    if model is None:
        # set epsilon exploration; user can tweak it
        eps = input("Tasa de exploración ε (valor entre 0 y 1, enter para 0.05): ").strip()
        try:
            eps_val = float(eps) if eps != "" else 0.05
            model = MarkovRPS(epsilon=max(0.0, min(1.0, eps_val)))
        except Exception:
            model = MarkovRPS(epsilon=0.05)

    stats = {"rounds": 0, "player_wins": 0, "ai_wins": 0, "ties": 0, "freq": Counter()}
    prev_player_move = None

    while True:
        player_move = get_player_move()
        if player_move == "q":
            break

        ai_move, predicted = decide_ai_move(model, prev_player_move)

        # Show choices
        print(f"Jugador: {player_move}  |  IA: {ai_move}  (IA predijo: {predicted})")

        # Resolve
        winner = resolve_round(player_move, ai_move)
        if winner == "Empate":
            print("Resultado: Empate.")
            stats["ties"] += 1
        elif winner == "IA":
            print("Resultado: Gana la IA.")
            stats["ai_wins"] += 1
        else:
            print("Resultado: Gana el Jugador.")
            stats["player_wins"] += 1

        stats["rounds"] += 1
        stats["freq"][player_move] += 1

        # Update model with observed transition (prev -> current)
        model.update(prev_player_move, player_move)
        prev_player_move = player_move

        # After each round show short stats
        print(pretty_stats(stats))
        print("-" * 40)

    # End of game
    print("\nPartida finalizada.")
    print(pretty_stats(stats))

    # Offer to save model
    save_ans = input(f"¿Guardar modelo actual en '{MODEL_PATH}' para futuras partidas? (s/n): ").strip().lower()
    if save_ans == "s":
        model.save(MODEL_PATH)
        print(f"Modelo guardado en {MODEL_PATH}.")

if __name__ == "__main__":
    main()
