# Pipeline vidéo WealthTech Horizon — chaque cible est relançable vidéo par vidéo.
#   make video ID=V07        voix -> mots -> sous-titres -> montage -> contrôle qualité
#   make upload ID=V07       upload Cloudinary (refusé si le contrôle qualité échoue)
#   make lock ID=V07         verrouille la voix validée (plus jamais régénérée)
#   make motion ID=V01       rendu motion design (Remotion, plan scripts/shotlists/V01.json) -> contrôle qualité
# Story (méthode validée sur V01 : storyboard scripts/storyboards/Vxx.json + mise en scène scripts/story/Vxx(.py|/)) :
#   make voice ID=V07                    voix en cache -> tts.json, words.json, audio.wav (aucun appel si en cache)
#   make storyboard-check ID=V07         contrôle du storyboard (scènes, débuts de mot, temps forts, texte, idées-clés)
#   make story-props ID=V07              props du film sans rendu (FROM=… TO=… : un extrait ; ALLOW_PARTIAL=1 : film incomplet admis)
#   make story-stills ID=V07 FRAMES="0 120"   images fixes PNG (images de la vidéo rendue) -> build/V07/story/stills/
#   make story ID=V07                    film entier -> output/WTH-V07.mp4 + version sans sous-titres -> contrôle qualité
#   make story ID=V01 FROM=25.612 TO=41.309   extrait -> output/extraits/ (pas de contrôle qualité)
#   make review-sheets ID=V07            planches de revue -> build/V07/review/film/ (REVIEW="--nocap --sheets" pour choisir)
#   make story-check                     parité Python / TypeScript (tests.story_parity) + tsc
#   make films                           make story pour chaque vidéo de IDS qui a une mise en scène
#   make clean-tmp                       dossiers temporaires de Remotion et images de revue (garde les planches)

PY ?= python3
ID ?=
FORCE ?=
FROM ?=
TO ?=
FRAMES ?=
ALLOW_PARTIAL ?=
REVIEW ?=
IDS ?= V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V11 V12 V13 V14 V15

.NOTPARALLEL:

.PHONY: help setup extract lint revue assets voices import video tts words subs render qa upload lock planning all publish check-id motion motion-setup motion-props motion-review story story-window voice storyboard-check story-props story-stills story-check review-sheets films clean-tmp

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

story-window:
	@$(if $(and $(strip $(FROM)),$(strip $(TO))),true,$(if $(strip $(FROM)$(TO)),echo "$(STORY_WINDOW_ERR)" && exit 2,true))

# Film entier : toutes les scènes mises en scène (sinon arrêt, ALLOW_PARTIAL=1 pour un rendu de travail), puis QA.
# Extrait (FROM/TO) : output/extraits/WTH-Vxx_extrait_Sa-Sb.mp4 + build/Vxx/story/extrait_sans_sous_titres.mp4.
story: check-id story-window
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) $(STORY_PARTIAL)
	$(if $(strip $(FROM)$(TO)),,$(PY) -m pipeline.qa $(ID))

story-props: check-id story-window
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) --props $(STORY_PARTIAL)

story-stills: check-id story-window
	@test -n "$(strip $(FRAMES))" || (echo 'Précise les images : make story-stills ID=$(ID) FRAMES="0 120 480"' && exit 1)
	$(PY) -m pipeline.story $(ID) $(STORY_WINDOW) --stills $(FRAMES) $(STORY_PARTIAL)

storyboard-check: check-id
	$(PY) -m pipeline.story $(ID) --check

story-check:
	$(PY) -m tests.story_parity
	cd motion && npx tsc --noEmit

review-sheets: check-id
	$(PY) -m pipeline.story_review $(ID) $(REVIEW)

films:
	@for id in $(IDS); do \
	  if $(HAS_SPEC); then $(MAKE) --no-print-directory story ID=$$id || exit 1; fi; \
	done

# Dossiers temporaires de Remotion (bundles, profils Chrome) seulement si aucun rendu ne tourne ; images de revue
# (bandes de temps forts, téléphone, images extraites) de chaque vidéo : les planches et les rapports restent.
clean-tmp:
	@mkdir -p build
	@if pgrep -f "[r]emotion render|[s]tills.mjs" >/dev/null || ! flock -n build/.render.lock true; then \
	  echo "Rendu Remotion en cours : dossiers temporaires laissés"; \
	else \
	  t=$${TMPDIR:-/tmp}; rm -rf $$t/remotion-webpack-bundle-* $$t/wth-render-* $$t/react-motion-render* \
	    $$t/puppeteer_dev_chrome_profile-* $$t/remotion-v4*-assets* $$t/wth-phone-*; echo "Dossiers temporaires de Remotion supprimés ($$t)"; \
	fi
	@for d in build/V*/review; do [ -d "$$d" ] && $(PY) -m pipeline.story_review $$(basename $$(dirname $$d)) --clean; done; true
	@rm -rf build/V*/story/frames
	@df -h . | tail -1

upload: check-id
	$(PY) -m pipeline.upload $(ID)

lock: check-id
	$(PY) -m pipeline.tts lock $(ID)

planning:
	$(PY) -m pipeline.planning

# Une vidéo qui a une mise en scène Story (scripts/story/Vxx.py ou scripts/story/Vxx/) passe par la méthode Story ;
# sinon, avec un plan de tournage motion (scripts/shotlists/Vxx.json), par le rendu motion ; les autres par le montage
# classique (qui n'écrase jamais un rendu Remotion, voir render).
all:
	@for id in $(IDS); do \
	  if $(HAS_SPEC); then $(MAKE) --no-print-directory voice story ID=$$id || exit 1; \
	  elif [ -f scripts/shotlists/$$id.json ]; then $(MAKE) --no-print-directory tts words motion ID=$$id || exit 1; \
	  else $(MAKE) --no-print-directory video ID=$$id || exit 1; fi; \
	done

publish:
	@for id in $(IDS); do $(MAKE) --no-print-directory upload ID=$$id || exit 1; done
	$(MAKE) --no-print-directory planning

check-id:
	@test -n "$(ID)" || (echo "Précise la vidéo : make $(MAKECMDGOALS) ID=V01" && exit 1)
