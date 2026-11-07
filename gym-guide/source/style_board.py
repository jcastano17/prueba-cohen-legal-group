"""Style options board: same squat / RDL / active-recovery move in each style."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "style-options")

STYLES = [
    ("A", "outline", "Line art + muscle focus",
     "Clean outlines like a fitness app. The muscles each lift works are highlighted in coral.",
     "#FFFFFF"),
    ("B", "person", "Illustrated athlete",
     "A flat-colour person in shirt, shorts and trainers, closest in feel to your reference image.",
     "#FFFFFF"),
    ("C", "sketch", "Coach's notebook sketch",
     "Hand-drawn pencil look on paper. Informal and friendly.",
     "#FBF7EE"),
    ("D", "mannequin", "3D mannequin",
     "Shaded wooden-mannequin figure with visible joints, so you can see the angles clearly.",
     "#FFFFFF"),
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#EEF2F7;font-family:Inter,Arial,sans-serif;color:#1A2233;width:1080px}
.band{background:#183C6B;color:#fff;padding:30px 36px}
.band h1{margin:0;font-size:46px;font-weight:800}
.band p{margin:8px 0 0;font-size:26px;color:#D6E3F5}
.wrap{padding:6px 22px 26px}
.card{border:2px solid #D3DEEC;border-radius:22px;margin-top:20px;padding:18px 20px 14px}
.head{display:flex;align-items:center;gap:16px}
.letter{flex:0 0 58px;width:58px;height:58px;border-radius:14px;background:#183C6B;color:#fff;font-size:34px;font-weight:800;display:grid;place-items:center}
.t{font-size:32px;font-weight:800}
.d{font-size:22px;color:#4A5568;margin-top:3px}
.figs{display:flex;align-items:flex-end;justify-content:space-between;margin-top:12px}
.pair{display:flex;align-items:center;gap:4px}
.f{display:flex;flex-direction:column;align-items:center}
.f svg{max-height:236px}
.cap{font-size:15px;font-weight:800;letter-spacing:.1em;color:#7A8597;margin-top:4px}
.arr{font-size:28px;color:#183C6B;font-weight:700;padding-bottom:40px}
.mini{background:#EAF6EC;border-radius:14px;padding:6px 8px 4px;display:flex;flex-direction:column;align-items:center}
.mini .cap{color:#1F6B3A}
.ai{background:#FFF8E6;border-color:#F0D58C}
.ai .letter{background:#B7791F}
.foot{margin-top:18px;font-size:21px;color:#4A5568;text-align:center}
"""


def card(letter, title, desc, data, bg):
    def pair(key, label):
        a, b = data[key]
        return (f'<div class="pair"><div class="f">{a}<div class="cap">{label} · START</div></div>'
                f'<div class="arr">→</div><div class="f">{b}<div class="cap">FINISH</div></div></div>')
    return (f'<div class="card" style="background:{bg}"><div class="head"><div class="letter">{letter}</div>'
            f'<div><div class="t">{title}</div><div class="d">{desc}</div></div></div>'
            f'<div class="figs">{pair("squat", "SQUAT")}{pair("rdl", "RDL")}'
            f'<div class="mini">{data["mini"]}<div class="cap">ACTIVE RECOVERY</div></div></div></div>')


def main():
    cards = []
    for letter, key, title, desc, bg in STYLES:
        env = dict(os.environ, GYM_STYLE=key)
        js = subprocess.run([sys.executable, os.path.join(HERE, "style_worker.py")], env=env,
                            capture_output=True, text=True, check=True).stdout
        cards.append(card(letter, title, desc, json.loads(js), bg))
    ai = ('<div class="card ai"><div class="head"><div class="letter">E</div><div>'
          '<div class="t">AI-rendered realistic people</div><div class="d">Like the ChatGPT reference. '
          'The most lifelike, but the AI chooses the poses, which is how the earlier errors crept in. '
          'I would make each exercise separately and check every pose. No sample shown: '
          'it needs an image-generation tool that uses paid credits.</div></div></div></div>')
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            '<div class="band"><h1>Choose a drawing style</h1><p>Same exercises and same layout. '
            'Only the drawings change.</p></div>'
            f'<div class="wrap">{"".join(cards)}{ai}'
            '<div class="foot">Reply with a letter, or mix them, e.g. "B with the muscle highlights from A".</div>'
            '</div></body></html>')
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "style-options.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
