# Pipeline vidéo WealthTech Horizon — chaque cible est relançable vidéo par vidéo.
#   make video ID=V07        voix -> mots -> sous-titres -> montage -> contrôle qualité
#   make upload ID=V07       upload Cloudinary (refusé si le contrôle qualité échoue)
#   make lock ID=V07         verrouille la voix validée (plus jamais régénérée)

PY ?= python3
ID ?=
IDS ?= V01 V02 V03 V04 V05 V06 V07 V08 V09 V10 V11 V12 V13 V14 V15

.PHONY: help setup extract lint assets voices video tts words subs render qa upload lock planning all publish check-id

help:
	@sed -n '1,5p' Makefile

setup:
	$(PY) -m pip install -r requirements.txt

extract:
	$(PY) -m pipeline.extract

lint:
	$(PY) -m pipeline.lint $(ID)

assets:
	$(PY) -m pipeline.assets $(ID)

voices:
	$(PY) -m pipeline.tts voices

video: check-id tts words subs render qa

tts: check-id
	$(PY) -m pipeline.tts video $(ID)

words: check-id
	$(PY) -m pipeline.words $(ID)

subs: check-id
	$(PY) -m pipeline.subs $(ID)

render: check-id
	$(PY) -m pipeline.render $(ID)

qa: check-id
	$(PY) -m pipeline.qa $(ID)

upload: check-id
	$(PY) -m pipeline.upload $(ID)

lock: check-id
	$(PY) -m pipeline.tts lock $(ID)

planning:
	$(PY) -m pipeline.planning

all:
	@for id in $(IDS); do $(MAKE) --no-print-directory video ID=$$id || exit 1; done

publish:
	@for id in $(IDS); do $(MAKE) --no-print-directory upload ID=$$id || exit 1; done
	$(MAKE) --no-print-directory planning

check-id:
	@test -n "$(ID)" || (echo "Précise la vidéo : make $(MAKECMDGOALS) ID=V01" && exit 1)
