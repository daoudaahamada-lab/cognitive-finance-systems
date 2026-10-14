#!/usr/bin/env python3
"""Découpe une prise complète de la voix off (19 phrases séparées par des pauses longues)
en public/voix/L01.wav ... L19.wav, puis lance la mesure des durées.

Usage : python3 outils/decouper-prise.py prise.mp3
Prérequis : ffmpeg. Les coupes se font au milieu des 18 plus longs silences de la prise.
"""
import json, re, subprocess, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
LIGNES = json.load(open(RACINE / 'voix-off' / 'script.json'))
prise = sys.argv[1]

def silences(seuil_db, duree_min):
    sortie = subprocess.run(
        ['ffmpeg', '-nostdin', '-i', prise, '-af', f'silencedetect=noise={seuil_db}dB:d={duree_min}', '-f', 'null', '-'],
        capture_output=True, text=True).stderr
    debuts = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', sortie)]
    fins = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', sortie)]
    return list(zip(debuts, fins))

total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', prise],
                             capture_output=True, text=True).stdout)
blancs = [s for s in silences(-40, 0.2) if s[0] > 0.05 and s[1] < total - 0.05]
attendu = len(LIGNES) - 1
if len(blancs) < attendu:
    sys.exit(f'Seulement {len(blancs)} pauses trouvées, {attendu} attendues : vérifiez la prise.')

# Choix des coupes : longueur des pauses + durée attendue de chaque phrase (proportionnelle au nombre de caractères).
poids = [len(l['prononciation']) for l in LIGNES]
parole = total - sum(b - a for a, b in blancs) * 0.6
attendues = [parole * w / sum(poids) for w in poids]
n = len(blancs)
milieux = [(a + b) / 2 for a, b in blancs]
INF = float('inf')
# meilleur[k][j] : meilleur score en ayant placé k coupes, la dernière sur la pause j
meilleur = [[-INF] * n for _ in range(attendu + 1)]
precedent = [[-1] * n for _ in range(attendu + 1)]
def score(debut, fin, k, j):
    ecart = abs((fin - debut) - attendues[k]) / max(attendues[k], 0.8)
    return 3 * (blancs[j][1] - blancs[j][0]) - 2.5 * ecart
for j in range(n):
    meilleur[1][j] = score(0, milieux[j], 0, j)
for k in range(2, attendu + 1):
    for j in range(n):
        for i in range(j):
            if meilleur[k - 1][i] == -INF:
                continue
            v = meilleur[k - 1][i] + score(milieux[i], milieux[j], k - 1, j)
            if v > meilleur[k][j]:
                meilleur[k][j], precedent[k][j] = v, i
fin_score = lambda j: meilleur[attendu][j] - 2.5 * abs((total - milieux[j]) - attendues[-1]) / attendues[-1]
j = max(range(n), key=fin_score)
choix = []
for k in range(attendu, 0, -1):
    choix.append(j)
    j = precedent[k][j]
coupes = [blancs[j] for j in sorted(choix)]
print('Pauses retenues (s) :', ', '.join(f'{(a + b) / 2:.2f} ({b - a:.2f})' for a, b in coupes))
bornes = [0.0] + [(a + b) / 2 for a, b in coupes] + [total]
dossier = RACINE / 'public' / 'voix'
dossier.mkdir(parents=True, exist_ok=True)
for l, debut, fin in zip(LIGNES, bornes[:-1], bornes[1:]):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', prise, '-ss', f'{debut:.3f}', '-to', f'{fin:.3f}',
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000', '-ac', '1', str(dossier / f"{l['id']}.wav")], check=True)
subprocess.run(['bash', str(RACINE / 'outils' / 'mesurer-voix.sh')], check=True)
