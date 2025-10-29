import time
import threading
import csv
import os

# Piedra Papel Tijera: Jugador vs Jugador

opciones_j1 = {"a": "piedra", "s": "papel", "d": "tijera"}
opciones_j2 = {"4": "piedra", "5": "papel", "6": "tijera"}

# Contadores de victorias
puntos_j1 = 0
puntos_j2 = 0
empates = 0

# Variables globales para almacenar las jugadas
jugada_j1 = None
jugada_j2 = None

# Archivo CSV
archivo_csv = "jugadas.csv"

# Crear el archivo CSV con encabezados si no existe
if not os.path.exists(archivo_csv):
    with open(archivo_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ronda", "Jugador 1", "Jugador 2", "Resultado"])


def input_jugador1():
    global jugada_j1
    jugada_j1 = input("Jugador 1 (a=piedra, s=papel, d=tijera, q=salir): ").lower()


def input_jugador2():
    global jugada_j2
    jugada_j2 = input("Jugador 2 (4=piedra, 5=papel, 6=tijera, q=salir): ").lower()


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

    # Reiniciar jugadas
    jugada_j1 = None
    jugada_j2 = None

    # Crear hilos para capturar entradas simultáneamente
    hilo_j1 = threading.Thread(target=input_jugador1)
    hilo_j2 = threading.Thread(target=input_jugador2)

    # Iniciar ambos hilos
    hilo_j1.start()
    hilo_j2.start()

    # Esperar a que ambos hilos terminen
    hilo_j1.join()
    hilo_j2.join()

    # Verificar si algún jugador quiere salir
    if jugada_j1 == "q":
        print("Jugador 1 ha salido del juego.")
        break
    if jugada_j2 == "q":
        print("Jugador 2 ha salido del juego.")
        break

    if jugada_j1 not in opciones_j1 or jugada_j2 not in opciones_j2:
        print("Alguna tecla no es válida, intenta otra vez.")
        continue

    jugada1 = opciones_j1[jugada_j1]
    jugada2 = opciones_j2[jugada_j2]

    print(f"Jugador 1 eligió {jugada1} | Jugador 2 eligió {jugada2}")

    # Determinar el ganador
    if jugada1 == jugada2:
        resultado = "Empate"
        empates += 1
    elif (jugada1 == "piedra" and jugada2 == "tijera") or \
            (jugada1 == "papel" and jugada2 == "piedra") or \
            (jugada1 == "tijera" and jugada2 == "papel"):
        resultado = "Jugador 1 gana"
        puntos_j1 += 1
    else:
        resultado = "Jugador 2 gana"
        puntos_j2 += 1

    print(resultado)
    print(f"Marcador -> J1: {puntos_j1} | J2: {puntos_j2} | Empates: {empates}")

    # Guardar la jugada en el archivo CSV
    with open(archivo_csv, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([i + 1, jugada1, jugada2, resultado])

# Resultado final
print("\n=== Resultado Final ===")
print(f"Jugador 1: {puntos_j1} victorias")
print(f"Jugador 2: {puntos_j2} victorias")
print(f"Empates: {empates}")

print(f"\nLas jugadas se han guardado en '{archivo_csv}'.")
print("Gracias por jugar.")
