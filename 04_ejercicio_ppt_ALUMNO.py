def generar_features_basicas(self, hist_j2, hist_j1, ronda):
    features = {}

    # RONDA AL PRINCIPIO
    features["Ronda"] = ronda

    # Frecuencias totales del Jugador2
    if hist_j2:
        tot = len(hist_j2)
        c = Counter(hist_j2)
        features["freq_piedra"] = c.get("piedra", 0) / tot
        features["freq_papel"] = c.get("papel", 0) / tot
        features["freq_tijera"] = c.get("tijera", 0) / tot
    else:
        features["freq_piedra"] = features["freq_papel"] = features["freq_tijera"] = 1/3

    # Frecuencias últimas 5
    rec = hist_j2[-5:]
    if rec:
        c5 = Counter(rec)
        d5 = len(rec)
        features["freq_5_piedra"] = c5.get("piedra", 0) / d5
        features["freq_5_papel"] = c5.get("papel", 0) / d5
        features["freq_5_tijera"] = c5.get("tijera", 0) / d5
    else:
        features["freq_5_piedra"] = features["freq_5_papel"] = features["freq_5_tijera"] = 1/3

    # Lags Jugador2
    lag1 = hist_j2[-1] if len(hist_j2) >= 1 else None
    lag2 = hist_j2[-2] if len(hist_j2) >= 2 else None

    for jug in ["piedra", "papel", "tijera"]:
        features[f"lag_1_{jug}"] = 1 if lag1 == jug else 0
        features[f"lag_2_{jug}"] = 1 if lag2 == jug else 0

    # Rachas Jugador1
    rv, rd = 0, 0
    if hist_j1 and len(hist_j1) == len(hist_j2):
        for i in range(len(hist_j1)-1, -1, -1):
            res = self.calcular_resultado(hist_j1[i], hist_j2[i])
            if res == "victoria":
                if rd == 0: rv += 1
                else: break
            elif res == "derrota":
                if rv == 0: rd += 1
                else: break
            else:
                break

    features["racha_victorias"] = rv
    features["racha_derrotas"] = rd

    # Fases
    if self.total_rounds:
        if ronda <= self.total_rounds / 3:
            fase = "inicio"
        elif ronda <= 2 * self.total_rounds / 3:
            fase = "medio"
        else:
            fase = "final"
    else:
        fase = "inicio" if ronda <= 3 else "medio" if ronda <= 6 else "final"

    features["fase_inicio"] = 1 if fase == "inicio" else 0
    features["fase_medio"] = 1 if fase == "medio" else 0
    features["fase_final"] = 1 if fase == "final" else 0

    return features
