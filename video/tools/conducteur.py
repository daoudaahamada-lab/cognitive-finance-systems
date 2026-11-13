# -*- coding: utf-8 -*-
"""Génère dist/conducteur.md : conducteur scène par scène avec les durées réelles mesurées sur la timeline."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "script"))
from script import SCENES  # noqa: E402

DESC = {
    "hook": dict(
        visuel="Bureau saturé : messagerie (23 non lus), agenda du lundi, fiche CRM, documents, post-it, tâches. À droite, compteurs chiffrés.",
        animation="Fenêtres qui s'ouvrent en cascade ; compteur 0 → 24 h ; 10 cases sur 24 passent en violet ; calcul 10 h × 46 = 460 h ; « chiffre d'affaires promis » barré ; trois cartes « données sensibles » ; chatbot barré ; frise de mission en 4 étapes.",
        ecran="24 h / semaine · 10 h à récupérer ? (hypothèse à tester) · 10 h × 46 semaines = 460 h · chiffre d'affaires promis (barré) · si les mesures du pilote le confirment · Une condition · Diagnostic → Note sur 100 → 3 agents → Décision · Le CGP garde la main à chaque étape",
        transition="Fondu enchaîné 0,6 s vers le titre."),
    "title": dict(
        visuel="Carton titre sur fond bleu nuit, wordmark texte « Agentic Wealth » (pas de logo inventé), trois étiquettes à droite.",
        animation="Apparitions décalées du titre, du sous-titre et des étiquettes ; bandeau simulation.",
        ecran="On audite un cabinet de gestion de patrimoine · Une mission, du premier diagnostic à la décision · L'agent prépare / Le CGP valide / Le CGP décide · Simulation pédagogique : cabinet, personnes, dossiers et chiffres fictifs",
        transition="Fondu enchaîné."),
    "cabinet": dict(
        visuel="Fiche « Horizon Patrimoine (fictif) » ; cartes Sophie, Karim, Léa (avatars à initiales) ; puis carte des 5 outils reliés par les trajets de Sophie.",
        animation="Cartes qui glissent ; responsabilités cochées une à une ; tracé progressif du trajet avant rendez-vous (bleu) puis après (ambre) ; outils surlignés au mot « passages de relais ».",
        ecran="Aix-en-Provence · 3 personnes · ~180 foyers clients (simulation) · Statuts réglementaires : non supposés ici · Les outils existent. Les passages, moins. · 1. Note dans le CRM … 6. Suite à organiser · Périmètre de l'audit : les passages de relais",
        transition="Fondu enchaîné."),
    "audit": dict(
        visuel="Entretiens (3 avatars), questions de diagnostic, grille Déclaré / Observé / À mesurer ; barre 8 h / 9 h / 7 h ; grille de notation sur 5 critères ; carte des 5 domaines métier Agentic Wealth.",
        animation="Questions synchronisées sur la voix ; blocs d'heures qui apparaissent ; équation 8 + 9 + 7 = 24 h ; barres de score animées avec compteurs ; total 0 → 45/100 ; domaines révélés un à un puis étiquetés Agent 1 / 2 / 3.",
        ecran="Hypothèses de départ · 8 + 9 + 7 = 24 h · À chronométrer sur un échantillon réel · Processus 13/20 · Interconnexion 6/20 · Accès et données 7/20 · Appropriation 9/20 · Validations et traçabilité 10/20 · 45/100 note illustrative · Acquisition et conversion · Conseil et préparation · Conformité et traçabilité · Service et relation client · Pilotage du cabinet",
        transition="Fondu enchaîné."),
    "agent1": dict(
        visuel="Agenda de Sophie (mardi, 14:00 à 15:10, Camille R. cliente fictive) ; frise des 11 étapes ; écrans : sources avec interrupteurs, journal de collecte S1 à S4, écart 12/03 ≠ 14/03, manques, brief sourcé, rendez-vous sans écran, brouillon de compte rendu en 4 colonnes, tâches et brouillon de message ; horloge Mardi 08:35 → 09:02 → 14:00 → 15:10.",
        animation="Curseur de Sophie : clic « Préparer », activation des 4 sources, archive et messagerie grisées, clic « Autoriser » ; frappe du journal ; question barrée, date corrigée, tampon « Brief v2 validé par Sophie · 09:02 » ; phrase ambiguë surlignée puis précisée ; tampon « Compte rendu validé par Sophie · 15:31 » ; « à confirmer » → « confirmé » ; bouton d'envoi réservé à Sophie.",
        ecran="11 étapes, dont 3 validations humaines · Ce dossier. Ces sources. Rien d'autre. · Écart signalé, non tranché · Absent / À vérifier / Ancien · Faits sourcés · Points à vérifier · Questions proposées · Pas d'écran d'IA pendant le rendez-vous · Ambigu : quoi ? avec qui ? quand ? · Brouillon · non envoyé · Rien ne part sans le clic de Sophie · 8 h → 4 h visées · gain cible, pas un résultat · 3 briefs → Continuer / Ajuster / Retirer l'accès",
        transition="Fondu enchaîné."),
    "agent2": dict(
        visuel="Espace documentaire de Léa (mercredi 10:20) ; cartes « règles de contrôle » et « cadre d'accès aux données » ; tableau en 4 colonnes Présent / Absent / Ambigu / Non vérifié ; aperçu d'un justificatif à date floutée ; comparaison de revue ; repères connaissance client et vigilance ; journal horodaté ; bilan du bloc.",
        animation="Colonnes et cartes qui tombent dans leur statut ; clic sur la carte ambiguë ; ouverture de l'aperçu ; clic de Léa « Demander une meilleure version » ; badge « Dossier conforme » barré ; lignes du journal successives.",
        ecran="L'agent n'invente pas les règles · Validée par la personne compétente · Quelles sources / personnes habilitées / finalité / sous-traitant éventuel / conservation · liste fictive de démonstration, non réglementaire · Date illisible : ni « valide », ni « périmé » · Décision humaine requise · Dossier conforme (barré) : jamais attribué par l'agent seul · Repère AMF · approche fondée sur les risques · Un journal technique n'est pas, à lui seul, la preuve … · 9 h → 6 h visées",
        transition="Fondu enchaîné."),
    "agent3": dict(
        visuel="Messagerie (jeudi 16:40, Mme D. cliente fictive) ; recherche de Léa ; fiche engagement / source / état connu / inconnu ; brouillon de réponse ; boutons de l'agent vs de Karim ; fiche prospect ; cockpit du lundi 09:00 en 4 listes ; bilan du bloc.",
        animation="Frappe du message entrant ; sources qui se rassemblent ; lignes de fiche synchronisées sur « Voici… » ; phrase incertaine remplacée par Karim ; clic de Karim « Vérifier et envoyer » ; score de valeur barré ; raisons puis arbitrages de Sophie ; « client négligé » barré.",
        ecran="Demande : rappel d'un engagement · seuls éléments autorisés · statut non renseigné · Statut non fiable : le brouillon n'affirme pas que c'est fait · Boutons de l'agent : Préparer · Envoi décidé par Karim · Aucun score automatique · règle du cabinet : sans action depuis 90 jours (paramètre) · Sophie : Attend volontairement une date / Mérite un appel / Donnée CRM incorrecte · 7 h → 4 h visées · Un cockpit que personne n'ouvre n'est pas un gain",
        transition="Fondu enchaîné."),
    "data": dict(
        visuel="Question de Sophie en bulle ; « Non. » ; chemin autorisé des données en 5 nœuds avec trois chemins interdits ; points d'examen du cabinet ; auto-hébergement ≠ conformité ; trois cas d'arrêt ; cinq interdits ; déploiement progressif.",
        animation="Nœuds et flèches révélés au rythme de l'énumération ; puces d'examen une à une ; cartes d'arrêt glissantes ; interdits synchronisés phrase par phrase.",
        ecran="Source autorisée → Accès limité → Préparation → Validation humaine → Destination autorisée · Toute la messagerie / Envoi direct au client / Outil non approuvé (interdits) · Modèle auto-hébergé ou open source ≠ Traitement conforme · Points d'attention rappelés par la CNIL · « Information non vérifiée » · Transmis au CGP · Données de démonstration → Accès limité → Revue du cadre et autorisation → Données réelles",
        transition="Fondu enchaîné."),
    "bilan": dict(
        visuel="Tableau avant / après visé / gain cible ; bandeau récapitulatif ; deux calculs ; trois cases à ne pas confondre ; déductions.",
        animation="Lignes révélées sur la voix ; total 8 + 9 + 7 = 24 h puis 4 + 6 + 4 = 14 h ; compteur 0 → 27 600 € ; signes ≠ entre les trois notions.",
        ecran="simulation · gains cibles · 24 h → 14 h / semaine · Gain cible : 10 h · Mesure réelle : à établir · 10 h × 46 semaines = 460 h · 460 h × 60 € = 27 600 € (valorisation interne illustrative, capacité théorique annuelle) · Capacité théorique ≠ Économies encaissées ≠ Chiffre d'affaires additionnel · À déduire : contrôle humain, outils, maintenance, erreurs",
        transition="Fondu enchaîné."),
    "deploy": dict(
        visuel="Ordre de déploiement en 4 cartes ; planning de mission S1-2 / S3-5 / S6-8 ; fenêtres qui se ferment pour laisser un brief sourcé ; appel à l'action ; carton final bleu nuit.",
        animation="Cartes révélées sur la voix ; puces du planning ; fenêtres qui disparaissent une à une ; « L'IA parle à la place du conseiller » barré ; carton final en fondu.",
        ecran="Quel agent en premier ? · Périmètre étroit / Compréhensible par Sophie / Mesurable · planning proposé · 8 semaines ≠ 3 agents achevés dans tous les cabinets · Retrouve le contexte / Voit les manques / Décide · Montrez-nous un dossier et une semaine réelle. · Agentic Wealth · L'agent prépare. Le CGP valide et décide.",
        transition="Fondu au noir (fin de la nappe sur 4 s)."),
}


def fmt(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def main():
    tl = json.load(open(os.path.join(ROOT, "build", "timeline.json")))
    out = ["# Conducteur : « On audite un cabinet de gestion de patrimoine »", "",
           "Simulation pédagogique Agentic Wealth. Cabinet, personnes, dossiers et chiffres fictifs.",
           f"Durée totale mesurée sur la piste voix : {fmt(tl['duration'])} ({tl['duration']:.1f} s).", ""]
    for sc_def, sc in zip(SCENES, tl["scenes"]):
        d = DESC[sc["id"]]
        out += [f"## {fmt(sc['start'])} à {fmt(sc['end'])} · {sc_def['title']} ({sc['end'] - sc['start']:.1f} s)", "",
                f"**Visuel.** {d['visuel']}", "", f"**Animation.** {d['animation']}", "",
                f"**Texte à l'écran.** {d['ecran']}", "", f"**Transition.** {d['transition']}", "", "**Texte prononcé.**", ""]
        for (bid, text, _), b in zip(sc_def["beats"], sc["beats"]):
            out.append(f"- `{fmt(b['start'])}` {text}")
        out.append("")
    with open(os.path.join(ROOT, "dist", "conducteur.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("conducteur ok")


if __name__ == "__main__":
    main()
