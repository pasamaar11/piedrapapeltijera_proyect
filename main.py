import time
import keyboard
import csv
import os

# Piedra Papel Tijera: Jugador vs Jugador

opciones_j1 = {"a": "piedra", "s": "papel", "d": "tijera"}
opciones_j2 = {"4": "piedra", "5": "papel", "6": "tijera"}

# Contadores de victorias
puntos_j1 = 0
puntos_j2 = 0
empates = 0

# Archivo CSV
archivo_csv = "jugadas.csv"

# Crear el archivo CSV con encabezados si no existe
if not os.path.exists(archivo_csv):
    with open(archivo_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ronda", "Jugador 1", "Jugador 2", "Resultado"])


print("¿Cuántas rondas se quieren jugar?")
rondas = int(input())

for i in range(rondas):
    print(f"\n--- Ronda {i + 1} de {rondas} ---")
    print("Preparados...")

    # Cuenta regresiva
    for n in range(3, 0, -1):
        print(n)
        time.sleep(1)

    print("¡YA!\n")

    j1jugada = False
    j2jugada = False
    j1eleccion = None
    j2eleccion = None

    # Bucle para detectar teclas de ambos jugadores
    while not j1jugada or not j2jugada:
        # Jugador 1
        if not j1jugada:
            if keyboard.is_pressed("a"):
                j1eleccion = "piedra"
                j1jugada = True
            elif keyboard.is_pressed("s"):
                j1eleccion = "papel"
                j1jugada = True
            elif keyboard.is_pressed("d"):
                j1eleccion = "tijera"
                j1jugada = True
            elif keyboard.is_pressed("q"):
                print("Jugador 1 ha salido del juego.")
                exit()

        # Jugador 2
        if not j2jugada:
            if keyboard.is_pressed("4"):
                j2eleccion = "piedra"
                j2jugada = True
            elif keyboard.is_pressed("5"):
                j2eleccion = "papel"
                j2jugada = True
            elif keyboard.is_pressed("6"):
                j2eleccion = "tijera"
                j2jugada = True
            elif keyboard.is_pressed("q"):
                print("Jugador 2 ha salido del juego.")
                exit()

    print(f"Jugador 1 eligió {j1eleccion} | Jugador 2 eligió {j2eleccion}")

    # Determinar el ganador
    if j1eleccion == j2eleccion:
        resultado = "Empate"
        empates += 1
    elif (j1eleccion == "piedra" and j2eleccion == "tijera") or \
            (j1eleccion == "papel" and j2eleccion == "piedra") or \
            (j1eleccion == "tijera" and j2eleccion == "papel"):
        resultado = "Jugador 1 gana"
        puntos_j1 += 1
    else:
        resultado = "Jugador 2 gana"
        puntos_j2 += 1

    print(resultado)
    print(f"Marcador -> J1: {puntos_j1} | J2: {puntos_j2} | Empates: {empates}")

    # Guardar en CSV
    with open(archivo_csv, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([i + 1, j1eleccion, j2eleccion, resultado])

# Resultado final
print("\n=== Resultado Final ===")
print(f"Jugador 1: {puntos_j1} victorias")
print(f"Jugador 2: {puntos_j2} victorias")
print(f"Empates: {empates}")
print(f"\nLas jugadas se han guardado en '{archivo_csv}'.")
print("Gracias por jugar.")
