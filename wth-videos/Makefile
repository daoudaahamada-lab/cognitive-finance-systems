# Pipeline vidéo WealthTech Horizon — chaque cible est relançable vidéo par vidéo.
#   make video ID=V07        voix -> mots -> sous-titres -> montage -> contrôle qualité
#   make upload ID=V07       upload Cloudinary (refusé si le contrôle qualité échoue)
#   make lock ID=V07         verrouille la voix validée (plus jamais régénérée)
#   make motion ID=V01       rendu motion design (Remotion, plan scripts/shotlists/V01.json) -> contrôle qualité

PY ?= python3
ID ?=
FORCE ?=
IDS ?= V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V11 V12 V13 V14 V15

.NOTPARALLEL:

.PHONY: help setup extract lint revue assets voices import video tts words subs render qa upload lock planning all publish check-id motion motion-setup motion-props motion-review

help:
	@sed -n '1,6p' Makefile

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

subs: check-id
	$(PY) -m pipeline.subs $(ID)

# Refuse d'écraser un rendu motion (Remotion) par le montage classique, sauf FORCE=1.
render: check-id
	WTH_FORCE=$(FORCE) $(PY) -m pipeline.render $(ID)

qa: check-id
	$(PY) -m pipeline.qa $(ID)

# Motion design : illustrations en verre + sous-titres karaoké, rendu Remotion (motion/), voix existante.
motion: check-id
	$(PY) -m pipeline.motion $(ID)
	$(PY) -m pipeline.qa $(ID)

motion-setup:
	cd motion && npm ci

motion-props: check-id
	$(PY) -m pipeline.motion $(ID) --props

motion-review: check-id
	$(PY) -m pipeline.motion $(ID) --review

upload: check-id
	$(PY) -m pipeline.upload $(ID)

lock: check-id
	$(PY) -m pipeline.tts lock $(ID)

planning:
	$(PY) -m pipeline.planning

# Une vidéo qui a un plan de tournage motion (scripts/shotlists/Vxx.json) passe par le rendu motion,
# les autres par le montage classique (qui n'écrase jamais un rendu motion, voir render).
all:
	@for id in $(IDS); do \
	  if [ -f scripts/shotlists/$$id.json ]; then $(MAKE) --no-print-directory tts words motion ID=$$id || exit 1; \
	  else $(MAKE) --no-print-directory video ID=$$id || exit 1; fi; \
	done

publish:
	@for id in $(IDS); do $(MAKE) --no-print-directory upload ID=$$id || exit 1; done
	$(MAKE) --no-print-directory planning

check-id:
	@test -n "$(ID)" || (echo "Précise la vidéo : make $(MAKECMDGOALS) ID=V01" && exit 1)
