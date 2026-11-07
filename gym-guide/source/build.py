"""Build the two leg-day infographics (HTML -> PNG via render.js).

The routine below is the single source of truth. It is checked against the
agreed plan before anything is drawn, so a drawing fix can never silently
change an exercise, set, rep, rest time or active-recovery move.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from exercises import pair_fit, mini_svg, art_svg  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..")

# ------------------------------------------------------------ agreed plan
AGREED_MAIN = [
    ("Barbell squat", 3, "8–10", "Shoulder circles"),
    ("Romanian deadlift", 3, "8–10", "Gentle wrist mobility"),
    ("Bulgarian split squat", 3, "8–10 per leg", "Gentle thoracic rotations"),
    ("Leg press", 3, "10–12", "Shoulder/scapular mobility"),
    ("Hamstring curl", 3, "10–12", "Gentle wrist mobility"),
]
AGREED_CALF = [
    ("Standing calf raises", "2–3", "12–15"),
    ("Seated calf raises", "2–3", "12–15"),
    ("Tibialis raises", "2–3", "15–20"),
]
MAIN_REST, CALF_REST, AR_TIME = "2–3 min", "45–75 s", "20–30 s"

OVERVIEW = [("Warm-up", "10 min"), ("Primary exercises", "≈ 45–55 min"),
            ("Calves & ankles", "≈ 15 min"), ("Cardio", "7–10 min"),
            ("Cooldown", "3–5 min")]

# ------------------------------------------------------------ card content
MAIN = [
    dict(key="squat", plan="Barbell squat", name="Barbell<br>Squat", sets=3, reps="8–10",
         ar="Shoulder circles", ar_plan="Shoulder circles", ar_how="slow rolls, arms relaxed",
         mini="shoulder_circles"),
    dict(key="rdl", plan="Romanian deadlift", name="Romanian<br>Deadlift<br><small>(RDL)</small>",
         sets=3, reps="8–10", ar="Wrist mobility", ar_plan="Gentle wrist mobility",
         ar_how="gentle circles, no forced stretch", mini="wrist"),
    dict(key="bss", plan="Bulgarian split squat", name="Bulgarian<br>Split<br>Squat", sets=3,
         reps="8–10", reps_note="(per leg)", reps_plan="8–10 per leg",
         ar="Thoracic rotations", ar_plan="Gentle thoracic rotations",
         ar_how="seated, gentle", mini="thoracic"),
    dict(key="leg_press", plan="Leg press", name="Leg<br>Press", sets=3, reps="10–12",
         ar="Shoulder / scapular mobility", ar_plan="Shoulder/scapular mobility",
         ar_how="reach &amp; squeeze, no load", mini="scapular"),
    dict(key="ham_curl", plan="Hamstring curl", name="Hamstring<br>Curl<br><small>(lying machine)</small>",
         sets=3, reps="10–12", ar="Wrist mobility", ar_plan="Gentle wrist mobility",
         ar_how="gentle circles, no forced stretch", mini="wrist"),
]
CALF = [
    dict(key="standing_calf", plan="Standing calf raises", name="Standing<br>Calf Raise",
         sets="2–3", reps="12–15",
         tips=["Knees straight", "Heels drop below the step", "Rise high, brief pause"]),
    dict(key="seated_calf", plan="Seated calf raises", name="Seated<br>Calf Raise",
         sets="2–3", reps="12–15",
         tips=["Knees ≈ 90°, pad on lower thighs", "Heels all the way down, then up",
               "Brief pause at the top"]),
    dict(key="tibialis", plan="Tibialis raises", name="Tibialis<br>Raise",
         sets="2–3", reps="15–20",
         tips=["Back &amp; hips on the wall, heels down", "Lift toes toward the shins",
               "Feet farther from wall = harder"]),
]


def check_against_plan():
    assert len(MAIN) == len(AGREED_MAIN), "main exercise count changed"
    for card, (plan, sets, reps, ar) in zip(MAIN, AGREED_MAIN):
        assert card["plan"] == plan, (card["plan"], plan)
        assert card["sets"] == sets, (plan, "sets")
        assert card.get("reps_plan", card["reps"]) == reps, (plan, "reps")
        assert card["ar_plan"] == ar, (plan, "active recovery")
    assert len(CALF) == len(AGREED_CALF), "calf exercise count changed"
    for card, (plan, sets, reps) in zip(CALF, AGREED_CALF):
        assert card["plan"] == plan and card["sets"] == sets and card["reps"] == reps, plan
    print("Plan check passed:")
    for plan, sets, reps, ar in AGREED_MAIN:
        print(f"  {plan:<24} {sets} x {reps:<14} rest {MAIN_REST:<8} AR {AR_TIME}: {ar}")
    for plan, sets, reps in AGREED_CALF:
        print(f"  {plan:<24} {sets} x {reps:<14} rest {CALF_REST}")


# ------------------------------------------------------------ HTML
CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F3F6FA;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#1A2233;width:1080px}
.page{padding:0 0 22px}
.band{background:linear-gradient(180deg,#183C6B,#14325A);color:#fff;padding:30px 36px 28px;display:flex;align-items:center;gap:24px}
.band h1{margin:0;font-size:46px;line-height:1.08;font-weight:800;letter-spacing:-.01em}
.band p{margin:8px 0 0;font-size:29px;font-weight:500;color:#D6E3F5}
.wrap{padding:0 22px}
.box{background:#fff;border:2px solid #D3DEEC;border-radius:20px;margin-top:20px;overflow:hidden}
.box-title{background:#DCE9FA;padding:12px 22px;font-size:30px;font-weight:800;color:#14325A;display:flex;align-items:center;gap:12px}
.box-title span{font-weight:500}
.ov{display:grid;grid-template-columns:repeat(5,1fr);padding:14px 6px 16px}
.ov div{text-align:center;border-left:2px solid #DCE3EC;padding:2px 6px}
.ov div:first-child{border-left:0}
.ov b{display:block;font-size:24px;font-weight:700}
.ov i{display:block;font-style:normal;font-size:24px;color:#3E4A5E;margin-top:2px}
.ov .dim b,.ov .dim i{color:#A3ADBD}
.ov .hl b{color:#0E6E8C}
.warm .box-title{background:#FFF0C7;color:#5C3D00}
.warm-grid{display:grid;grid-template-columns:150px 1fr 40px 150px 1fr;align-items:center;padding:10px 18px 14px;gap:8px}
.warm-grid .plus{font-size:52px;font-weight:300;color:#183C6B;text-align:center}
.wt b{display:block;font-size:28px;font-weight:800}
.wt i{display:block;font-style:normal;font-size:24px;color:#3E4A5E;line-height:1.25;margin-top:2px}
.bar{background:#183C6B;color:#fff;border-radius:16px;margin-top:22px;padding:14px 22px;font-size:32px;font-weight:800;display:flex;align-items:center;gap:12px}
.bar span{font-weight:500;color:#D6E3F5}
.rule{margin-top:12px;background:#fff;border:2px dashed #BFD0E6;border-radius:16px;padding:12px 18px;font-size:23px;line-height:1.35;color:#2A3446}
.rule .g{color:#1F6B3A;font-weight:800}
.rule .k{font-weight:800}
.rows{background:#fff;border:2px solid #D3DEEC;border-radius:20px;margin-top:12px;overflow:hidden}
.row{display:grid;grid-template-columns:176px 360px 186px 246px;gap:12px;align-items:center;padding:12px 14px;border-top:2px solid #E3E9F1}
.row:first-child{border-top:0}
.ex{display:flex;gap:12px;align-items:center}
.num{flex:0 0 46px;height:46px;border-radius:50%;background:#183C6B;color:#fff;font-size:28px;font-weight:800;display:grid;place-items:center}
.ex-name{font-size:28px;font-weight:800;line-height:1.1}
.ex-name small{font-size:21px;font-weight:600;color:#4A5568}
.illus{display:grid;grid-template-columns:166px 28px 166px;align-items:center}
.teal .row{grid-template-columns:170px 412px 186px 200px}
.teal .illus{grid-template-columns:190px 32px 190px}
.teal .fr{height:262px}
.teal .fr svg{max-width:190px;max-height:236px}
.fr{height:212px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}
.fr svg{max-width:166px;max-height:186px}
.cap{font-size:17px;font-weight:800;letter-spacing:.1em;color:#7A8597;text-transform:uppercase;margin-top:4px}
.arr{font-size:34px;color:#183C6B;text-align:center;font-weight:700}
.srr{background:#E8F0FA;border-radius:14px;padding:14px 12px;font-size:22px;line-height:1.6;white-space:nowrap}
.srr b{font-weight:800}
.srr small{display:block;font-size:19px;color:#4A5568;line-height:1.1;margin:-4px 0 4px 62px}
.ar{background:#EAF6EC;border:2px solid #BFE0C6;border-radius:14px;padding:10px 8px 10px 14px;display:grid;grid-template-columns:1fr 84px;align-items:center;gap:4px;min-height:186px}
.ar-h{font-size:18px;font-weight:800;color:#1F6B3A;line-height:1.2}
.ar-h span{font-weight:600}
.ar-move{font-size:24px;font-weight:800;color:#123D22;line-height:1.12;margin-top:6px}
.ar-how{font-size:18px;color:#2C5A3B;margin-top:5px;line-height:1.2}
.ar-art{display:flex;justify-content:center}
.tips{background:#EEF3F9;border:2px solid #D3DEEC;border-radius:14px;padding:12px 12px;font-size:20px;line-height:1.28;min-height:150px}
.tips .h{font-size:18px;font-weight:800;color:#0E6E8C;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}
.tips div.t{padding-left:18px;position:relative;margin-top:4px}
.tips div.t:before{content:'';position:absolute;left:2px;top:11px;width:8px;height:8px;border-radius:50%;background:#0E6E8C}
.finish{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px}
.fbox{background:#fff;border:2px solid #D3DEEC;border-radius:20px;padding:14px 16px;display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:center}
.fbox b{display:block;font-size:30px;font-weight:800}
.fbox .t{font-size:26px;font-weight:700;color:#0E6E8C}
.fbox i{display:block;font-style:normal;font-size:22px;color:#3E4A5E;line-height:1.3;margin-top:6px}
.note{margin-top:16px;font-size:20px;color:#5A6578;text-align:center}
.note b{color:#E8590C}
.teal .band{background:linear-gradient(180deg,#0F5E78,#0B4A60)}
.teal .bar{background:#0F5E78}
.teal .num{background:#0F5E78}
"""

DUMBBELL = ('<svg width="86" height="86" viewBox="0 0 86 86"><g transform="rotate(-35 43 43)" fill="#fff">'
            '<rect x="6" y="28" width="12" height="30" rx="4"/><rect x="18" y="22" width="12" height="42" rx="4"/>'
            '<rect x="30" y="38" width="26" height="10" rx="3"/><rect x="56" y="22" width="12" height="42" rx="4"/>'
            '<rect x="68" y="28" width="12" height="30" rx="4"/></g></svg>')
TIMER = ('<svg width="36" height="36" viewBox="0 0 36 36" fill="none" stroke="#14325A" stroke-width="3">'
         '<circle cx="18" cy="20" r="13"/><path d="M18 20V12M14 3h8M28 8l2-2" stroke-linecap="round"/></svg>')


def overview(highlight):
    cells = []
    for i, (label, t) in enumerate(OVERVIEW):
        cls = "hl" if i in highlight else ("dim" if highlight else "")
        cells.append(f'<div class="{cls}"><b>{label}</b><i>{t}</i></div>')
    return (f'<section class="box"><div class="box-title">{TIMER} Session Overview '
            f'<span>(≈ 90 min)</span></div><div class="ov">{"".join(cells)}</div></section>')


def page(title, sub, body, theme=""):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{theme}"><div class="page"><header class="band">{DUMBBELL}'
            f'<div><h1>{title}</h1><p>{sub}</p></div></header><div class="wrap">{body}</div>'
            f'</div></body></html>')


def frames(key, size=(166, 186)):
    a, b = pair_fit(key, *size)
    return (f'<div class="illus"><div class="fr">{a}<div class="cap">Start</div></div>'
            f'<div class="arr">→</div><div class="fr">{b}<div class="cap">Finish</div></div></div>')


def image1():
    warm = (
        '<section class="box warm"><div class="box-title">Warm-up <span>(10 minutes)</span></div>'
        '<div class="warm-grid">'
        f'<div>{art_svg("treadmill", 150, 160)}</div>'
        '<div class="wt"><b>Light cardio</b><i>(≈ 5 min)<br>Treadmill, bike<br>or elliptical</i></div>'
        '<div class="plus">+</div>'
        f'<div>{art_svg("lunge", 150, 160)}</div>'
        '<div class="wt"><b>Dynamic mobility</b><i>(≈ 5 min)<br>Leg swings, hip circles,<br>bodyweight lunges</i></div>'
        '</div></section>')
    rows = []
    for i, c in enumerate(MAIN, 1):
        note = f'<small>{c["reps_note"]}</small>' if c.get("reps_note") else ""
        rows.append(
            f'<div class="row"><div class="ex"><div class="num">{i}</div>'
            f'<div class="ex-name">{c["name"]}</div></div>{frames(c["key"])}'
            f'<div class="srr"><div><b>Sets:</b> {c["sets"]}</div><div><b>Reps:</b> {c["reps"]}</div>'
            f'{note}<div><b>Rest:</b> {MAIN_REST}</div></div>'
            f'<div class="ar"><div><div class="ar-h">Active recovery<br><span>({AR_TIME})</span></div>'
            f'<div class="ar-move">{c["ar"]}</div><div class="ar-how">{c["ar_how"]}</div></div>'
            f'<div class="ar-art">{mini_svg(c["mini"], 84, 160)}</div></div></div>')
    body = (overview(set()) + warm +
            '<div class="bar">Primary Leg Exercises <span>(5 exercises)</span></div>'
            '<div class="rule">Between sets (2–3 min): <span class="g">20–30 s gentle active recovery</span>'
            ' → <span class="k">then genuine rest</span>. Active recovery never tires or strongly '
            'stretches the muscles needed for the next set.</div>'
            f'<div class="rows">{"".join(rows)}</div>'
            '<div class="note"><b>Orange arrows</b> show the movement — return the same way, under control.</div>')
    return page("Gym Track | Leg Day – Leg Strength", "Primary Exercises + Active Recovery", body)


def image2():
    rows = []
    for i, c in enumerate(CALF, 1):
        tips = "".join(f'<div class="t">{t}</div>' for t in c["tips"])
        rows.append(
            f'<div class="row"><div class="ex"><div class="num">{i}</div>'
            f'<div class="ex-name">{c["name"]}</div></div>{frames(c["key"], (190, 236))}'
            f'<div class="srr"><div><b>Sets:</b> {c["sets"]}</div><div><b>Reps:</b> {c["reps"]}</div>'
            f'<div><b>Rest:</b> {CALF_REST}</div></div>'
            f'<div class="tips"><div class="h">Key points</div>{tips}</div></div>')
    finish = (
        '<div class="finish">'
        f'<div class="fbox"><div>{art_svg("treadmill", 150, 170)}</div><div><b>Cardio</b>'
        '<div class="t">7–10 min</div><i>Steady, moderate pace.<br>Treadmill, bike or elliptical.</i></div></div>'
        f'<div class="fbox"><div>{art_svg("calf_stretch", 150, 170)}</div><div><b>Cooldown</b>'
        '<div class="t">3–5 min</div><i>Easy walk, then gentle stretches: calves, quads, hamstrings, '
        'hips. 20–30 s each, never forced.</i></div></div></div>')
    body = (overview({2, 3, 4}) +
            '<div class="bar">Calves &amp; Ankles <span>(3 exercises)</span></div>'
            '<div class="rule"><span class="k">Dedicated strengthening — not active recovery.</span> '
            'Goal: calf strength, ankle stability and resilience for soccer. '
            'Between sets: <span class="k">rest 45–75 s</span> (breathe, walk). '
            'Save calf and shin stretching for the cooldown.</div>'
            f'<div class="rows">{"".join(rows)}</div>'
            '<div class="bar">Finish the Session</div>' + finish +
            '<div class="note"><b>Orange arrows</b> show the movement — return the same way, under control.</div>')
    return page("Gym Track | Leg Day – Calves &amp; Ankles", "Secondary Exercises + Cardio &amp; Cooldown",
                body, theme="teal")


if __name__ == "__main__":
    check_against_plan()
    os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
    for name, fn in (("1-leg-strength", image1), ("2-calves-ankles", image2)):
        with open(os.path.join(OUT, "html", f"{name}.html"), "w") as f:
            f.write(fn())
    print("HTML written")
