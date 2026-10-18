"""Mots horodatés -> sous-titres .ass (1 à 3 mots à la fois, mot prononcé mis en évidence)."""
import argparse
import math

from PIL import ImageFont
from fontTools.ttLib import TTFont

from .common import build_dir, hex_to_ass, load_config, read_json

BREAK_AFTER = tuple(".,;:!?…»")
# Mots qu'on évite de laisser seuls en fin de groupe (« le | prix »).
WEAK = {"le", "la", "les", "l’", "un", "une", "des", "de", "du", "d’", "à", "au", "aux", "en", "et", "ou", "ton",
        "ta", "tes", "ce", "cette", "ces", "que", "qui", "sur", "pour", "par", "pas", "ne", "n’", "se", "s’", "c’",
        "qu’", "j’", "tu", "il", "on", "y", "son", "sa", "ses", "mon", "ma", "mes", "avec", "sans", "dans"}

ACTIVE_TAG = "{\\1c%s&\\3c%s&%s}"


def ass_time(t):
    cs = max(0, int(round(t * 100)))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


class Measure:
    """Largeur d'un texte en pixels, à l'échelle utilisée par libass (taille = ascendante + descendante)."""

    def __init__(self, font_file, ass_size):
        f = TTFont(font_file, lazy=True)
        upm = f["head"].unitsPerEm
        os2 = f["OS/2"]
        ratio = (os2.usWinAscent + os2.usWinDescent) / upm
        self.font = ImageFont.truetype(font_file, max(1, round(ass_size / ratio)))
        self.cmap = f.getBestCmap()

    def width(self, text):
        return self.font.getlength(text)

    def missing_glyphs(self, text):
        return sorted({c for c in text if not c.isspace() and ord(c) not in self.cmap})


def phrases(words, pause):
    """Coupe aux ponctuations, aux pauses et aux changements de segment."""
    out, cur = [], []
    for i, w in enumerate(words):
        if cur:
            prev = cur[-1]
            if prev["w"].endswith(BREAK_AFTER) or w["start"] - prev["end"] > pause or w["segment"] != prev["segment"]:
                out.append(cur)
                cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def balanced(phrase, max_words):
    """Répartit une phrase en groupes de taille équilibrée (4 -> 2+2 plutôt que 3+1)."""
    n = len(phrase)
    k = math.ceil(n / max_words)
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    groups, pos = [], 0
    for size in sizes:
        groups.append(phrase[pos:pos + size])
        pos += size
    # Évite qu'un article ou une préposition termine un groupe.
    for i in range(len(groups) - 1):
        last = groups[i][-1]["w"].lower()
        if last in WEAK and len(groups[i]) > 1 and len(groups[i + 1]) < max_words:
            groups[i + 1].insert(0, groups[i].pop())
    return [g for g in groups if g]


def fit(group, measure, max_chars, max_width):
    """Redécoupe un groupe trop long (caractères ou pixels)."""
    text = " ".join(w["w"] for w in group)
    if len(group) == 1 or (len(text) <= max_chars and measure.width(text) <= max_width):
        return [group]
    mid = len(group) // 2
    return fit(group[:mid], measure, max_chars, max_width) + fit(group[mid:], measure, max_chars, max_width)


def chunks(words, cfg, measure):
    sc = cfg["subtitles"]
    out = []
    for ph in phrases(words, sc["pause_break"]):
        for g in balanced(ph, sc["max_words"]):
            out.extend(fit(g, measure, sc["max_chars"], sc["max_width_px"]))
    return out


def build_ass(words, cfg, title=""):
    sc, brand, video = cfg["subtitles"], cfg["brand"], cfg["video"]
    measure = Measure(brand["font_bold_file"], sc["font_size"])
    groups = chunks(words, cfg, measure)
    base_fill = hex_to_ass(brand[sc["palette"]["base_fill"]])
    base_line = hex_to_ass(brand[sc["palette"]["base_outline"]])
    act_fill = hex_to_ass(brand[sc["palette"]["active_fill"]])
    act_line = hex_to_ass(brand[sc["palette"]["active_outline"]])
    shadow = hex_to_ass(brand[sc["palette"]["base_outline"]], "80")
    scale = sc.get("active_scale", 100)
    scale_tag = f"\\fscx{scale}\\fscy{scale}" if scale != 100 else ""
    x, y = video["width"] // 2, sc["center_y"]

    lines = [
        "[Script Info]",
        f"Title: {title}",
        "ScriptType: v4.00+",
        f"PlayResX: {video['width']}",
        f"PlayResY: {video['height']}",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Sub,{brand['font_bold']},{sc['font_size']},{base_fill},{base_fill},{base_line},{shadow},0,0,0,0,"
        f"100,100,0,0,1,{sc['outline']},{sc.get('shadow', 0)},5,40,40,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    events = []
    for gi, group in enumerate(groups):
        nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else None
        last_end = group[-1]["end"]
        if nxt is not None and nxt - last_end < 0.6:
            group_end = nxt
        else:
            group_end = last_end + 0.3
        for wi, w in enumerate(group):
            start = w["start"]
            end = group[wi + 1]["start"] if wi + 1 < len(group) else group_end
            end = max(end, start + 0.04)
            parts = []
            for k, other in enumerate(group):
                if k == wi:
                    parts.append(ACTIVE_TAG % (act_fill, act_line, scale_tag) + other["w"] + "{\\r}")
                else:
                    parts.append(other["w"])
            text = f"{{\\an5\\pos({x},{y})}}" + " ".join(parts)
            events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Sub,,0,0,0,,{text}")
    return "\n".join(lines + events) + "\n", groups, measure


def subs_for(video_id):
    cfg = load_config()
    from .common import script
    s = script(video_id)
    data = read_json(build_dir(video_id) / "words.json")
    ass, groups, _ = build_ass(data["words"], cfg, s["titre"])
    out = build_dir(video_id) / "subs.ass"
    out.write_text(ass, encoding="utf-8")
    print(f"{video_id} : {len(groups)} groupes de sous-titres -> {out}")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("id")
    subs_for(p.parse_args().id)


if __name__ == "__main__":
    main()
