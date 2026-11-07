"""Alternative body renderers. Same joints and limb lengths as the flat style;
only the way the body is painted changes (outline, person, sketch, mannequin)."""
import figures as F
from figures import add, sub, mul, unit, perp, length, rot, foot_pts

# tapered segment profiles: (t along segment, width) or (t, back/left w, front/right w)
THIGH_P = [(0, 15), (0.45, 13), (1, 10)]
SHIN_P = [(0, 10), (0.3, 11.5), (0.8, 7.5), (1, 6.5)]
UARM_P = [(0, 9.5), (1, 7.2)]
FARM_P = [(0, 7.2), (0.35, 7.8), (1, 5.2)]
TORSO_P = [(0, 23, 21), (0.35, 19, 20), (0.7, 21, 26), (0.92, 20, 22), (1, 18, 16)]

LIGHT = unit((-0.55, 0.83))

# ---- palettes per style ----
OUTLINE = dict(out="#1E293B", fill="#FFFFFF", fill_f="#E2E8F0", hl="#FF7A59",
               hl_f="#FFB4A1", ow=1.35)
SKETCH = dict(out="#3A3A3A", fill="#FBF7EE", fill_f="#E9E2D2", hl="#F4A261",
              hl_f="#F7C59F", ow=0.85)
PERSON = dict(skin="#E2A57F", skin_f="#C4875F", shirt="#2F6FDB", shirt_f="#2457B0",
              shorts="#1F2937", shorts_f="#0B1220", shoe="#2B3340", shoe_f="#4B5563",
              sole="#F25C05", sock="#FFFFFF", sock_f="#E5E7EB", hair="#2B211B")
REF = dict(skin="#E3AC88", skin_f="#C48D69", shirt="#1E1F23", shirt_f="#0E0F11",
           shorts="#3A3F47", shorts_f="#22252A", shoe="#1C1E22", shoe_f="#3A3D43",
           sole="#F4F4F4", sock="#FFFFFF", sock_f="#D9DCE0", hair="#251B16",
           out="#14161A", ow=0.7, hl="#E53935")


def is_ref():
    return F.STYLE.startswith("ref")


def is_person():
    return F.STYLE == "person" or is_ref()


def pp():
    return REF if is_ref() else PERSON


def _mix(hexc, other, t):
    a = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def tri(f):
    return (_mix(f, "#FFFFFF", 0.22), f, _mix(f, "#000000", 0.32))


MANNEQUIN = dict(c=("#F7F8FA", "#C6CDD5", "#7D8795"), c_f=("#E6E9ED", "#BAC2CB", "#8F99A5"),
                 edge="#6B7583")


def taper(a, b, prof):
    d = unit(sub(b, a))
    n = perp(d)
    L = length(sub(b, a))
    s1, s2 = [], []
    for item in prof:
        t, w1 = item[0], item[1] / 2
        w2 = (item[2] if len(item) > 2 else item[1]) / 2
        c = add(a, mul(d, t * L))
        s1.append(add(c, mul(n, w1)))
        s2.append(add(c, mul(n, -w2)))
    return s1 + s2[::-1]


def half(a, b, prof, side):
    """One half (side=+1 -> +n side) of a tapered segment."""
    d = unit(sub(b, a))
    n = mul(perp(d), side)
    L = length(sub(b, a))
    edge, mid = [], []
    for t, w in prof:
        c = add(a, mul(d, t * L))
        edge.append(add(c, mul(n, w / 2 - 0.3)))
        mid.append(add(c, mul(n, 0.6)))
    return edge + mid[::-1]


# ---- shape primitives -----------------------------------------------------
def P(pts, fill, grad=None, op=1.0):
    return ("poly", pts, fill, grad, op)


def C(c, r, fill, rgrad=False):
    return ("circle", c, r, fill, rgrad)


def Ln(a, b, w, color):
    return ("line", a, b, w, color)


def seg_grad(a, b, w):
    d = unit(sub(b, a))
    n = perp(d)
    if n[0] * LIGHT[0] + n[1] * LIGHT[1] < 0:
        n = mul(n, -1)
    m = mul(add(a, b), 0.5)
    return (add(m, mul(n, w / 2)), add(m, mul(n, -w / 2)))


def shadow(a, b, prof):
    d = unit(sub(b, a))
    n = perp(d)
    side = -1 if n[0] * LIGHT[0] + n[1] * LIGHT[1] > 0 else 1
    return P(half(a, b, prof, side), "#000000", None, 0.17)


def segment(a, b, prof, fill, mannequin=False, caps=True):
    if F.STYLE == "ref2":
        mannequin = True
    w0, w1 = prof[0][1], prof[-1][1]
    g = seg_grad(a, b, max(p[1] for p in prof)) if mannequin else None
    out = [C(a, w0 / 2, fill, mannequin), C(b, w1 / 2, fill, mannequin)] if caps else []
    out.append(P(taper(a, b, prof), fill, g))
    if F.STYLE in ("ref1", "ref3"):
        out.append(shadow(a, b, prof))
    return out


def cloth(a, b, prof, fill):
    """Clothing panel (no round caps) with the style's shading."""
    return segment(a, b, prof, fill, caps=False)


# ---- emit -----------------------------------------------------------------
def _emit(s, z, shape, fill=None, stroke=None, sw=0.0, pal=None):
    kind = shape[0]
    if kind == "line":
        _, a, b, w, color = shape
        s.line(a, b, w + (sw if stroke else 0), stroke or color, z=z)
        return
    if kind == "circle":
        _, c, r, f, rg = shape
        f = fill or f
        if rg and not stroke:
            cols = pal or tri(f)

            def fn(T, c=c, r=r, cols=cols):
                gid = f"rg{next(F._IDS)}"
                x, y = T(c)
                return (f'<radialGradient id="{gid}" cx=".5" cy=".5" r=".55" fx=".32" fy=".28">'
                        f'<stop offset="0" stop-color="{cols[0]}"/><stop offset=".6" stop-color="{cols[1]}"/>'
                        f'<stop offset="1" stop-color="{cols[2]}"/></radialGradient>'
                        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * T.s:.1f}" fill="url(#{gid})"/>')
            s._add(z, fn, [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)], 0)
        else:
            s.circle(c, r, f, stroke=stroke, sw=sw, z=z)
        return
    _, pts, f, g, op = shape
    if stroke and op < 1:
        return
    f = fill or f
    if g and not stroke:
        cols = pal or tri(f)

        def fn(T, pts=pts, g=g, cols=cols):
            gid = f"lg{next(F._IDS)}"
            (x1, y1), (x2, y2) = T(g[0]), T(g[1])
            p = " ".join(f"{T(q)[0]:.1f},{T(q)[1]:.1f}" for q in pts)
            return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" '
                    f'y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"><stop offset="0" stop-color="{cols[0]}"/>'
                    f'<stop offset=".55" stop-color="{cols[1]}"/><stop offset="1" stop-color="{cols[2]}"/>'
                    f'</linearGradient><polygon points="{p}" fill="url(#{gid})"/>')
        s._add(z, fn, pts, 0)
    else:
        s.poly(pts, f, stroke=stroke, sw=sw, z=z, opacity=op)


def emit_group(s, z, shapes, far=False):
    st = F.STYLE
    if st in ("outline", "sketch"):
        pal = OUTLINE if st == "outline" else SKETCH
        for sh in shapes:
            _emit(s, z, sh, fill=pal["out"], stroke=pal["out"], sw=2 * pal["ow"])
        for sh in shapes:
            _emit(s, z + 0.5, sh)
    elif st in ("ref1", "ref3"):
        for sh in shapes:
            _emit(s, z, sh, fill=REF["out"], stroke=REF["out"], sw=2 * REF["ow"])
        for sh in shapes:
            _emit(s, z + 0.5, sh)
    elif st == "mannequin":
        cols = MANNEQUIN["c_f"] if far else MANNEQUIN["c"]
        for sh in shapes:
            _emit(s, z, sh, fill=MANNEQUIN["edge"], stroke=MANNEQUIN["edge"], sw=1.0)
        for sh in shapes:
            _emit(s, z + 0.5, sh, pal=cols)
    else:
        for sh in shapes:
            _emit(s, z, sh)


# ---- body builders ---------------------------------------------------------
def _limb_fill(far, part="body"):
    st = F.STYLE
    if st in ("outline", "sketch"):
        pal = OUTLINE if st == "outline" else SKETCH
        if part == "hl":
            return pal["hl_f"] if far else pal["hl"]
        return pal["fill_f"] if far else pal["fill"]
    if is_person():
        return pp()[part + ("_f" if far else "")]
    return "#C6CDD5"


def leg_shapes(hip, L, far):
    st = F.STYLE
    knee, ankle = L["knee"], L["ankle"]
    foot = L.get("foot") or foot_pts(ankle, L.get("phi", 0))
    man = st == "mannequin"
    sh = []
    if is_person():
        sh += segment(knee, ankle, SHIN_P, _limb_fill(far, "skin"))
        sh += segment(hip, knee, THIGH_P, _limb_fill(far, "skin"))
        mid = add(hip, mul(sub(knee, hip), 0.62))
        sh += [C(hip, 9, _limb_fill(far, "shorts"))]
        sh += cloth(hip, mid, [(0, 16.6), (1, 14.6)], _limb_fill(far, "shorts"))
        sock0 = add(ankle, mul(sub(knee, ankle), 0.2))
        sh += [P(taper(sock0, ankle, [(0, 7.8), (1, 7.2)]), _limb_fill(far, "sock")),
               C(ankle, 3.6, _limb_fill(far, "sock"))]
        sh += [P(foot, _limb_fill(far, "shoe"))]
        phi = L.get("phi", 0)
        if not L.get("foot"):
            sh += [Ln(add(ankle, rot((-5.5, -6.6), phi)), add(ankle, rot((20, -6.6), phi)), 2.4,
                      pp()["sole"])]
        if st == "ref3" and not far:
            hl = REF["hl"]
            if "quads" in F.HIGHLIGHT:
                sh.append(P(half(hip, knee, THIGH_P, +1), hl, None, 0.55))
            if "hamstrings" in F.HIGHLIGHT:
                sh.append(P(half(hip, knee, THIGH_P, -1), hl, None, 0.55))
        return sh
    fill = _limb_fill(far)
    thigh_fill = fill
    sh += segment(knee, ankle, SHIN_P, fill, man)
    sh += segment(hip, knee, THIGH_P, thigh_fill, man)
    if st in ("outline", "sketch"):
        hl = _limb_fill(far, "hl")
        if "glutes" in F.HIGHLIGHT:
            pass  # drawn with the torso group (behind the hip)
        if "quads" in F.HIGHLIGHT:
            sh.append(P(half(hip, knee, THIGH_P, +1), hl))
        if "hamstrings" in F.HIGHLIGHT:
            sh.append(P(half(hip, knee, THIGH_P, -1), hl))
        if "calves" in F.HIGHLIGHT:
            sh.append(P(half(knee, ankle, SHIN_P, -1), hl))
        if "shins" in F.HIGHLIGHT:
            sh.append(P(half(knee, ankle, SHIN_P, +1), hl))
    sh.append(P(foot, fill))
    if man:
        for j, r in ((knee, 5.6), (ankle, 3.9)):
            sh.append(C(j, r, fill, True))
    return sh


def arm_shapes(shp, A, far):
    st = F.STYLE
    el, wr = A["elbow"], A["wrist"]
    hand = add(wr, mul(unit(sub(wr, el)), 3.0))
    man = st == "mannequin"
    if is_person():
        skin = _limb_fill(far, "skin")
        sh = segment(el, wr, FARM_P, skin) + segment(shp, el, UARM_P, skin)
        mid = add(shp, mul(sub(el, shp), 0.5))
        sh += [C(shp, 6.2, _limb_fill(far, "shirt"))]
        sh += cloth(shp, mid, [(0, 12), (1, 10.2)], _limb_fill(far, "shirt"))
        sh += [C(hand, 4.6, skin)]
        return sh
    fill = _limb_fill(far)
    sh = segment(el, wr, FARM_P, fill, man) + segment(shp, el, UARM_P, fill, man)
    sh.append(C(hand, 4.6, fill, man))
    if man:
        sh += [C(el, 4.6, fill, True), C(wr, 3.2, fill, True)]
    return sh


def torso_shapes(hip, shp, head, nd):
    st = F.STYLE
    man = st == "mannequin"
    f = (nd[1], -nd[0])          # face direction
    back = mul(f, -1)
    neck_top = add(shp, mul(nd, 9))
    if is_person():
        PAL = pp()
        skin, shirt = PAL["skin"], PAL["shirt"]
        sh = [Ln(shp, neck_top, 8, skin)]
        sh += [C(hip, 11, PAL["shorts"]), C(shp, 9.5, shirt),
               P(taper(hip, shp, TORSO_P), shirt, seg_grad(hip, shp, 24) if st == "ref2" else None)]
        if st in ("ref1", "ref3"):
            sh.append(shadow(hip, shp, [(0, 22), (0.35, 19.5), (0.7, 23.5), (0.92, 21), (1, 17)]))
        # shorts waistband over the lower torso
        wb = add(hip, mul(unit(sub(shp, hip)), 9))
        sh += cloth(hip, wb, [(0, 23), (1, 20)], PAL["shorts"])
        if st == "ref3" and "glutes" in F.HIGHLIGHT:
            bn = perp(unit(sub(shp, hip)))
            sh.append(P(half_disc(add(hip, mul(bn, 2.5)), 10.5, bn), REF["hl"], None, 0.55))
        sh += [C(add(add(head, mul(back, 1.4)), mul(nd, 1.2)), F.HEAD_R + 0.6, PAL["hair"]),
               C(add(head, mul(f, 1.0)), F.HEAD_R - 0.4, skin),
               P([add(head, mul(back, 1.5)), add(add(head, mul(back, 11.5)), mul(nd, 4)),
                  add(add(head, mul(back, 5)), mul(nd, 11.5)), add(head, mul(nd, 11))],
                 PAL["hair"]),
               C(add(head, mul(back, 1.8)), 2.4, "#D0916C"),
               C(add(add(head, mul(f, 9.6)), mul(nd, -0.5)), 1.9, skin)]
        if is_ref():   # eye + brow give the face direction, like the reference
            sh.append(C(add(add(head, mul(f, 6.4)), mul(nd, 1.4)), 0.95, "#1A1A1A"))
            sh.append(Ln(add(add(head, mul(f, 4.8)), mul(nd, 3.6)),
                         add(add(head, mul(f, 7.8)), mul(nd, 3.4)), 1.1, PAL["hair"]))
        return sh
    fill = _limb_fill(False)
    sh = [Ln(shp, neck_top, 8, fill)]
    sh += [C(hip, 11, fill, man), C(shp, 9.5, fill, man)]
    g = seg_grad(hip, shp, 24) if man else None
    sh.append(P(taper(hip, shp, TORSO_P), fill, g))
    if st in ("outline", "sketch") and "glutes" in F.HIGHLIGHT:
        bn = perp(unit(sub(shp, hip)))
        sh.append(P(half_disc(add(hip, mul(bn, 2.5)), 10.5, bn), _limb_fill(False, "hl")))
    sh.append(C(head, F.HEAD_R, fill, man))
    if man:
        sh += [C(hip, 7.5, fill, True), C(shp, 6.5, fill, True)]
    return sh


def half_disc(c, r, n):
    import math
    a0 = math.atan2(n[1], n[0])
    pts = []
    for i in range(13):
        a = a0 - math.pi / 2 + math.pi * i / 12
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    return pts


def draw_styled(s, hip, shp, head, nd, legs, arms):
    for A in arms:
        if A.get("far"):
            emit_group(s, 1, arm_shapes(shp, A, True), far=True)
    for L in legs:
        if L.get("far"):
            emit_group(s, 2, leg_shapes(hip, L, True), far=True)
    emit_group(s, 4, torso_shapes(hip, shp, head, nd))
    for L in legs:
        if not L.get("far"):
            emit_group(s, 6, leg_shapes(hip, L, False))
    for A in arms:
        if not A.get("far"):
            emit_group(s, 8, arm_shapes(shp, A, False))
