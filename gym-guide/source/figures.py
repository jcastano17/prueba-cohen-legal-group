"""Stick-figure drawing helpers for the gym infographics.

World coordinates: x to the right, y UP, ground at y = 0, units ~ cm for a
~175 cm person. Every limb has a fixed length, and knees/elbows are placed by
two-bone inverse kinematics, so every pose keeps the same anatomy.
"""
import math

# ---- body segment lengths (fixed for every pose) ----
TORSO = 52      # hip joint -> shoulder joint
NECK = 16       # shoulder joint -> head centre
HEAD_R = 10.5
UARM = 31       # shoulder -> elbow
FARM = 27       # elbow -> wrist
THIGH = 44      # hip -> knee
SHIN = 43       # knee -> ankle
ANKLE_H = 7     # ankle joint height above the sole

NEAR = "#24324A"
FAR = "#9AA6BC"
EQUIP = "#7C8796"
EQUIP_DARK = "#4B5563"
EQUIP_LIGHT = "#D5DBE3"
MOTION = "#E8590C"
CALM = "#2F855A"


# ---------- vector helpers ----------
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, k): return (a[0] * k, a[1] * k)
def length(a): return math.hypot(a[0], a[1])
def unit(a):
    l = length(a)
    return (a[0] / l, a[1] / l)
def perp(a): return (-a[1], a[0])
def rot(v, deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)
def dirv(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))
def lean(deg):
    """Unit vector tilted `deg` degrees forward (+x) from vertical."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


def ik(a, c, l1, l2, prefer):
    """Place the middle joint of a two-bone chain a->b->c.

    `prefer` picks between the two solutions: 'up', 'down', 'front' (+x),
    'back' (-x). Raises if the target is out of reach, so a pose can never
    silently stretch a limb.
    """
    d = length(sub(c, a))
    if d > l1 + l2 + 1e-6:
        raise ValueError(f"target out of reach: {d:.2f} > {l1 + l2}")
    if d < abs(l1 - l2):
        raise ValueError("target too close")
    u = unit(sub(c, a))
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - x * x, 0.0))
    base = add(a, mul(u, x))
    s1 = add(base, mul(perp(u), h))
    s2 = add(base, mul(perp(u), -h))
    key = {"up": lambda p: p[1], "down": lambda p: -p[1],
           "front": lambda p: p[0], "back": lambda p: -p[0]}[prefer]
    return s1 if key(s1) >= key(s2) else s2


def foot_pts(ankle, phi):
    """Foot polygon. phi = rotation of the foot frame (0 = standing flat,
    toes to +x). Positive phi = toes up (dorsiflexion) for a figure facing +x."""
    local = [(0, 3), (-5, 0), (-6.5, -4), (-5, -7), (19, -7), (21, -5),
             (17, -2.5), (6, 1.5)]
    return [add(ankle, rot(p, phi)) for p in local]


def ankle_from_ball(ball, phi):
    """Ankle position when the ball of the foot is fixed at `ball`."""
    return sub(ball, rot((14, -7), phi))


def ankle_from_heel(heel, phi):
    return sub(heel, rot((-5, -7), phi))


# ---------- scene ----------
class Scene:
    def __init__(self):
        self.items = []  # (z, svg_fn, points_for_bbox, margin)

    def _add(self, z, fn, pts, margin):
        self.items.append((z, fn, pts, margin))

    def line(self, a, b, w, color, z=0, opacity=1.0, cap="round", dash=None):
        def fn(T):
            (x1, y1), (x2, y2) = T(a), T(b)
            d = f' stroke-dasharray="{dash}"' if dash else ""
            return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{color}" stroke-width="{w * T.s:.1f}" stroke-linecap="{cap}" '
                    f'stroke-opacity="{opacity}"{d}/>')
        self._add(z, fn, [a, b], w / 2)

    def polyline(self, pts, w, color, z=0, opacity=1.0, dash=None):
        def fn(T):
            p = " ".join(f"{T(q)[0]:.1f},{T(q)[1]:.1f}" for q in pts)
            d = f' stroke-dasharray="{dash}"' if dash else ""
            return (f'<polyline points="{p}" fill="none" stroke="{color}" '
                    f'stroke-width="{w * T.s:.1f}" stroke-linecap="round" '
                    f'stroke-linejoin="round" stroke-opacity="{opacity}"{d}/>')
        self._add(z, fn, pts, w / 2)

    def circle(self, c, r, fill, stroke=None, sw=0, z=0, opacity=1.0):
        def fn(T):
            x, y = T(c)
            st = f' stroke="{stroke}" stroke-width="{sw * T.s:.1f}"' if stroke else ""
            return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * T.s:.1f}" fill="{fill}" '
                    f'fill-opacity="{opacity}"{st}/>')
        self._add(z, fn, [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)], sw / 2)

    def poly(self, pts, fill, stroke=None, sw=0, z=0, opacity=1.0):
        def fn(T):
            p = " ".join(f"{T(q)[0]:.1f},{T(q)[1]:.1f}" for q in pts)
            st = (f' stroke="{stroke}" stroke-width="{sw * T.s:.1f}" stroke-linejoin="round"'
                  if stroke else "")
            return f'<polygon points="{p}" fill="{fill}" fill-opacity="{opacity}"{st}/>'
        self._add(z, fn, pts, sw / 2)

    def rect(self, x, y, w, h, fill, stroke=None, sw=0, z=0, r=0, opacity=1.0):
        """Axis-aligned rect, (x, y) = bottom-left corner in world coords."""
        def fn(T):
            X, Y = T((x, y + h))
            st = f' stroke="{stroke}" stroke-width="{sw * T.s:.1f}"' if stroke else ""
            return (f'<rect x="{X:.1f}" y="{Y:.1f}" width="{w * T.s:.1f}" height="{h * T.s:.1f}" '
                    f'rx="{r * T.s:.1f}" fill="{fill}" fill-opacity="{opacity}"{st}/>')
        self._add(z, fn, [(x, y), (x + w, y + h)], sw / 2)

    def capsule(self, a, b, w, fill, z=0, stroke=None, sw=0):
        """Thick rounded bar (pads, benches at an angle)."""
        if stroke:
            self.line(a, b, w + 2 * sw, stroke, z=z)
        self.line(a, b, w, fill, z=z)

    def arrow(self, pts, color=MOTION, w=3.2, z=20, both=False, head=7.5):
        self.polyline(pts, w, color, z=z)
        self._head(pts[-2], pts[-1], color, z, head)
        if both:
            self._head(pts[1], pts[0], color, z, head)

    def _head(self, p_from, p_to, color, z, size):
        d = unit(sub(p_to, p_from))
        n = perp(d)
        tip = add(p_to, mul(d, size * 0.55))
        b1 = add(sub(p_to, mul(d, size * 0.45)), mul(n, size * 0.6))
        b2 = add(sub(p_to, mul(d, size * 0.45)), mul(n, -size * 0.6))
        self.poly([tip, b1, b2], color, stroke=color, sw=1.2, z=z)

    def arc_arrow(self, c, r, a0, a1, color=MOTION, w=3.2, z=20, both=False,
                  ry=None, head=7.5):
        ry = r if ry is None else ry
        n = max(int(abs(a1 - a0) / 6), 4)
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((c[0] + r * math.cos(a), c[1] + ry * math.sin(a)))
        self.arrow(pts, color=color, w=w, z=z, both=both, head=head)

    def bbox(self):
        xs, ys = [], []
        for _, _, pts, m in self.items:
            for p in pts:
                xs += [p[0] - m, p[0] + m]
                ys += [p[1] - m, p[1] + m]
        return min(xs), min(ys), max(xs), max(ys)

    def svg(self, box, scale, pad=8, ground=None):
        x0, y0, x1, y1 = box
        W = (x1 - x0) * scale + 2 * pad
        H = (y1 - y0) * scale + 2 * pad

        class T:
            s = scale
            def __call__(self, p):
                return (pad + (p[0] - x0) * scale, pad + (y1 - p[1]) * scale)
        t = T()
        body = [fn(t) for z, fn, _, _ in sorted(self.items, key=lambda i: i[0])]
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
                f'width="{W:.0f}" height="{H:.0f}">' + "".join(body) + "</svg>")


def union(*boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


# ---------- body ----------
def draw_body(s, hip, torso_dir, legs, arms, neck_dir=None, head_offset=0.0,
              torso_w=21):
    """legs: list of dicts {knee, ankle, phi, far} ; arms: {elbow, wrist, far}.
    Returns the shoulder point."""
    sh = add(hip, mul(torso_dir, TORSO))
    nd = neck_dir or torso_dir
    head = add(add(sh, mul(nd, NECK)), mul((nd[1], -nd[0]), head_offset))

    for i, L in enumerate(legs):
        col, z = (FAR, 2) if L.get("far") else (NEAR, 6)
        s.line(hip, L["knee"], 12, col, z=z)
        s.line(L["knee"], L["ankle"], 10, col, z=z)
        s.poly(L.get("foot") or foot_pts(L["ankle"], L.get("phi", 0)), col,
               stroke=col, sw=2.5, z=z)
    for A in arms:
        col, z = (FAR, 1) if A.get("far") else (NEAR, 8)
        s.line(sh, A["elbow"], 8.5, col, z=z)
        s.line(A["elbow"], A["wrist"], 7.5, col, z=z)
        fd = unit(sub(A["wrist"], A["elbow"]))
        s.circle(add(A["wrist"], mul(fd, 3.0)), 4.6, col, z=z)
    s.line(hip, sh, torso_w, NEAR, z=4)
    s.line(sh, add(sh, mul(nd, 8)), 9, NEAR, z=4)
    s.circle(head, HEAD_R, NEAR, z=5)
    return sh, head


def leg(hip, ankle, phi=0.0, far=False, prefer="front", foot=None):
    return {"knee": ik(hip, ankle, THIGH, SHIN, prefer), "ankle": ankle,
            "phi": phi, "far": far, "foot": foot}


def arm(sh, wrist, far=False, prefer="back", k=1.0):
    return {"elbow": ik(sh, wrist, UARM * k, FARM * k, prefer), "wrist": wrist,
            "far": far}


def shoulder_of(hip, torso_dir):
    return add(hip, mul(torso_dir, TORSO))


def ground(s, x0, x1, z=-5):
    s.line((x0, -1.5), (x1, -1.5), 3, "#C7CDD6", z=z, cap="butt")
