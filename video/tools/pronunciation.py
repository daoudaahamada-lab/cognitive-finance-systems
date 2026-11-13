# -*- coding: utf-8 -*-
"""Ajustements de prononciation appliqués UNIQUEMENT au texte envoyé au moteur TTS.
Le texte des sous-titres reste celui de script/script.py."""
import re

# (motif regex, remplacement). Ordre significatif.
RULES = [
    (r"Agentic Wealth", "Adjènntik Ouèlse"),
    (r"\bCGP\b", "cé-gé-pé"),
    (r"\bCRM\b", "cé-erre-aime"),
    (r"\bAMF\b", "a-aime-èf"),
    (r"\bCNIL\b", "Cnil"),
    (r"\bIA\b", "I.A."),
    (r"\bLéa\b", "Léïa"),
    (r"\bmails\b", "mèles"),
    (r"\bchatbot\b", "tchatbotte"),
    (r"open source", "opène source"),
    (r"\bbriefs?\b", "brif"),
    (r"\bcockpit\b", "coque-pitte"),
    (r"[«»]", ""),
    (r"\s+", " "),
]


def tts_text(text: str) -> str:
    out = text
    for pat, rep in RULES:
        out = re.sub(pat, rep, out)
    return out.strip()
