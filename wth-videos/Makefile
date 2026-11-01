# Pipeline vidéo WealthTech Horizon — chaque cible est relançable vidéo par vidéo.
#   make video ID=V07        voix -> mots -> sous-titres -> montage -> contrôle qualité
#   make upload ID=V07       upload Cloudinary (refusé si le contrôle qualité échoue)
#   make lock ID=V07         verrouille la voix validée (plus jamais régénérée)
#   make motion ID=V01       rendu motion design (Remotion, plan scripts/shotlists/V01.json) -> contrôle qualité
# Story (méthode validée sur V01 : storyboard scripts/storyboards/Vxx.json + mise en scène scripts/story/Vxx(.py|/)) :
#   make voice ID=V07                    voix en cache -> tts.json, words.json, audio.wav (aucun appel si en cache)
#   make storyboard-check ID=V07         contrôle du storyboard (scènes, débuts de mot, temps forts, texte, idées-clés)
#   make story-props ID=V07              props du film sans rendu (FROM=… TO=… : un extrait ; ALLOW_PARTIAL=1 : film incomplet admis)
#   make story-staging ID=V07            film entier rendable ? (mise en scène complète : code 0, sinon 1 ; sans rendu)
#   make story-stills ID=V07 FRAMES="0 120"   images fixes PNG (images de la vidéo rendue) -> build/V07/story/stills/
#   make story ID=V07                    film entier -> output/WTH-V07.mp4 + version sans sous-titres -> contrôle qualité
#   make story ID=V07 ALLOW_PARTIAL=1    film incomplet (rendu de travail) -> build/V07/story/film_partiel*.mp4, sans QA
#   make story ID=V01 FROM=25.612 TO=41.309   extrait -> output/extraits/ (pas de contrôle qualité)
#   make review-sheets ID=V07            planches de revue -> build/V07/review/film/ (REVIEW="--nocap --sheets" pour choisir ;
#                                        film incomplet : REVIEW="--src build/V07/story/film_partiel.mp4")
#   make story-check                     parité Python / TypeScript (tests.story_parity) + tsc
#   make films                           make story pour chaque vidéo de IDS dont la mise en scène est complète (les autres sont sautées)
#   make shorts [SHORTS="S01 S03"]      vidéos courtes sans voix (shorts/shorts.json, composition Short) -> output/shorts/WTH-Sxx.mp4
#                                        + contrôles (ffprobe, zones réservées) + planches build/shorts/Sxx_sheet.jpg
#   make shorts-stills FRAMES="0 75 400" [SHORTS=…]   images fixes PNG -> build/shorts/stills/
#   make clean-tmp [ID=V07]              dossiers temporaires de Remotion (sous le verrou de rendu) ; avec ID : images de revue
#                                        de cette vidéo (garde les planches)

PY ?= python3
ID ?=
FORCE ?=
FROM ?=
TO ?=
FRAMES ?=
ALLOW_PARTIAL ?=
REVIEW ?=
SHORTS ?=
IDS ?= V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V11 V12 V13 V14 V15

.NOTPARALLEL:

.PHONY: help setup extract lint revue assets voices import video tts words subs render qa upload lock planning all publish check-id motion motion-setup motion-props motion-review story story-window voice storyboard-check story-props story-staging story-stills story-check review-sheets films clean-tmp shorts shorts-stills shorts-check

help:
	@sed -n '/^#/!q;p' Makefile

setup:
	$(PY) -m pip install -r requirements.txt

extract:
	$(PY) -m pipeline.extract

revue:
	$(PY) -m pipeline.review

lint:
	$(PY) -m pipeline.lint $(ID)

assets:
	$(PY) -m pipeline.assets $(ID)

voices:
	$(PY) -m pipeline.tts voices

# Voix générée par le connecteur ElevenLabs (API injoignable) : make import ID=V01 AUDIO=prise.mp3 WORDS=mots.json GEN=<generation_id>
import: check-id
	$(PY) -m pipeline.connector $(ID) --audio $(AUDIO) --words $(WORDS) --generation-id $(GEN)

video: check-id tts words subs render qa

tts: check-id
	$(PY) -m pipeline.tts video $(ID)

words: check-id
	$(PY) -m pipeline.words $(ID)

# Voix prête pour la mise en scène : tts.json (voix en cache), words.json, puis build/Vxx/audio.wav normalisé.
voice: check-id tts words
	$(PY) -m pipeline.story $(ID) --audio

subs: check-id
	$(PY) -m pipeline.subs $(ID)

# Refuse d'écraser un rendu motion (Remotion) ou un film Story par le montage classique, sauf FORCE=1.
render: check-id
	WTH_FORCE=$(FORCE) $(PY) -m pipeline.render $(ID)

qa: check-id
	$(PY) -m pipeline.qa $(ID)

# Motion design : illustrations en verre + sous-titres karaoké, rendu Remotion (motion/), voix existante.
# N'écrase pas un film Story (output/WTH-Vxx.mp4, wth_mode=story), sauf FORCE=1.
motion: check-id
	WTH_FORCE=$(FORCE) $(PY) -m pipeline.motion $(ID)
	$(PY) -m pipeline.qa $(ID)

motion-setup:
	cd motion && npm ci

motion-props: check-id
	$(PY) -m pipeline.motion $(ID) --props

motion-review: check-id
	$(PY) -m pipeline.motion $(ID) --review

# ---------- Story ----------
# Fenêtre : FROM et TO (s) ensemble pour un extrait, aucun des deux pour le film entier.
STORY_WINDOW = $(if $(strip $(FROM)$(TO)),--from $(FROM) --to $(TO),--full)
STORY_PARTIAL = $(if $(filter 1,$(ALLOW_PARTIAL)),--allow-partial)
STORY_WINDOW_ERR = FROM et TO vont ensemble (ex. FROM=25.612 TO=41.309), ou aucun des deux pour le film entier.
HAS_SPEC = [ -f scripts/story/$$id.py ] || [ -f scripts/story/$$id/__init__.py ]
# Mise en scène complète (toutes les scènes, tous les temps forts) : seul cas où make all / make films rendent le film Story.
STORY_READY = $(PY) -m pipeline.story $$id --staging

story-window:
	@$(if $(and $(strip $(FROM)),$(strip $(TO))),true,$(if $(strip $(FROM)$(TO)),echo "$(STORY_WINDOW_ERR)" && exit 2,true))

# Film entier : toutes les scènes mises en scène (sinon arrêt), puis QA (--qa : seulement si output/WTH-Vxx.mp4 a été
# rendu). ALLOW_PARTIAL=1 : film incomplet admis, rendu de travail dans build/Vxx/story/film_partiel*.mp4, sans QA ;
# output/WTH-Vxx.mp4 et build/Vxx/story_render.json ne changent pas.
# Extrait (FROM/TO) : output/extraits/WTH-Vxx_extrait_Sa-Sb.mp4 + build/Vxx/story/extrait_sans_sous_titres.mp4.
story: check-id story-window
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) $(STORY_PARTIAL) $(if $(strip $(FROM)$(TO)),,--qa)

story-props: check-id story-window
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) --props $(STORY_PARTIAL)

story-stills: check-id story-window
	@test -n "$(strip $(FRAMES))" || (echo 'Précise les images : make story-stills ID=$(ID) FRAMES="0 120 480"' && exit 1)
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) --stills $(FRAMES) $(STORY_PARTIAL)

storyboard-check: check-id
	$(PY) -m pipeline.story $(ID) --check

story-staging: check-id
	$(PY) -m pipeline.story $(ID) --staging

story-check:
	$(PY) -m tests.story_parity
	cd motion && npx tsc --noEmit

review-sheets: check-id
	$(PY) -m pipeline.story_review $(ID) $(REVIEW)

# ---------- Shorts (14 s, sans voix, piste AAC muette) ----------
shorts:
	$(PY) -m pipeline.shorts $(SHORTS)

shorts-stills:
	@test -n "$(strip $(FRAMES))" || (echo 'Précise les images : make shorts-stills FRAMES="0 75 400"' && exit 1)
	$(PY) -m pipeline.shorts $(SHORTS) --stills "$(FRAMES)"

shorts-check:
	$(PY) -m pipeline.shorts $(SHORTS) --check

# Une vidéo dont la mise en scène est incomplète ou en cours d'écriture (paquet scripts/story/Vxx/ sans toutes ses
# parties) est sautée avec la raison, sans arrêter les suivantes ; un rendu ou une QA en échec arrête la série.
films:
	@for id in $(IDS); do \
	  $(HAS_SPEC) || continue; \
	  if $(STORY_READY); then $(MAKE) --no-print-directory story ID=$$id || exit 1; \
	  else echo "$$id : film Story sauté (mise en scène pas prête)"; fi; \
	done

# Dossiers temporaires de Remotion (bundles, profils Chrome, TMPDIR d'un rendu tué) : supprimés EN TENANT le verrou de
# rendu (aucun rendu ne peut démarrer pendant la suppression), et seulement si aucun rendu hors verrou ne tourne.
# Avec ID=Vxx : images de travail de revue de cette vidéo (bandes de temps forts, téléphone, images extraites) ; les
# planches et les rapports restent. Sans ID, aucune image de revue n'est touchée (une revue peut être en cours).
CLEAN_TMP = t=$${TMPDIR:-/tmp}; rm -rf $$t/remotion-webpack-bundle-* $$t/wth-render-* $$t/react-motion-render* \
	$$t/puppeteer_dev_chrome_profile-* $$t/remotion-v4*-assets*; echo "Dossiers temporaires de Remotion supprimés ($$t)"
clean-tmp:
	@mkdir -p build
	@if pgrep -f "[r]emotion render|[s]tills.mjs|[r]emotion studio" >/dev/null; then \
	  echo "Rendu Remotion en cours (hors verrou) : dossiers temporaires laissés"; \
	elif ! flock -n build/.render.lock sh -c '$(CLEAN_TMP)'; then \
	  echo "Rendu Remotion en cours (verrou build/.render.lock pris) : dossiers temporaires laissés"; \
	fi
	@$(if $(strip $(ID)),$(PY) -m pipeline.story_review $(ID) --clean,echo "Images de revue : make clean-tmp ID=Vxx (vidéo terminée)")
	@df -h . | tail -1

upload: check-id
	$(PY) -m pipeline.upload $(ID)

lock: check-id
	$(PY) -m pipeline.tts lock $(ID)

planning:
	$(PY) -m pipeline.planning

# Une vidéo dont la mise en scène Story (scripts/story/Vxx.py ou scripts/story/Vxx/) est complète passe par la méthode
# Story ; sinon (pas de mise en scène, ou mise en scène incomplète : la raison est affichée), avec un plan de tournage
# motion (scripts/shotlists/Vxx.json), par le rendu motion ; les autres par le montage classique (qui n'écrase jamais un
# rendu Remotion, voir render ; make motion n'écrase pas un film Story).
all:
	@for id in $(IDS); do \
	  if $(HAS_SPEC) && $(MAKE) --no-print-directory voice ID=$$id && $(STORY_READY); then \
	    $(MAKE) --no-print-directory story ID=$$id || exit 1; \
	  else \
	    if $(HAS_SPEC); then echo "$$id : mise en scène Story pas prête, rendu motion ou montage classique"; fi; \
	    if [ -f scripts/shotlists/$$id.json ]; then $(MAKE) --no-print-directory tts words motion ID=$$id || exit 1; \
	    else $(MAKE) --no-print-directory video ID=$$id || exit 1; fi; \
	  fi; \
	done

publish:
	@for id in $(IDS); do $(MAKE) --no-print-directory upload ID=$$id || exit 1; done
	$(MAKE) --no-print-directory planning

check-id:
	@test -n "$(ID)" || (echo "Précise la vidéo : make $(MAKECMDGOALS) ID=V01" && exit 1)
