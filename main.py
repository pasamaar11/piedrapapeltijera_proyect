import random
opciones = ["piedra","papel","tijera"]

while True:
    jugador = input("Elige piedra, papel o tijera, o salir: ").lower()
    if jugador == "salir":
        break
    if jugador not in opciones:
        print("ERROR. Opción no válida")
        continue

    ia = random.choice(opciones)
    print(f"La IA elige: {ia}")

    if jugador == ia:
        print("Empate.")
    elif (jugador == "piedra" and ia == "tijera") or \
        (jugador == "papel" and ia == "piedra") or \
            (jugador == "tijera" and ia == "papel"):
        print("Ganas.")
    else:
        print("Pierdes.")