"""Start/finish poses for every exercise and the active-recovery moves."""
from figures import *


def fk_leg(hip, thigh_deg, shin_deg, phi, far=False):
    knee = add(hip, mul(dirv(thigh_deg), THIGH))
    ankle = add(knee, mul(dirv(shin_deg), SHIN))
    return {"knee": knee, "ankle": ankle, "phi": phi, "far": far}


def plate(s, c, r=21, z=3):
    s.circle(c, r, PLATE, stroke=PLATE_EDGE, sw=2.2, z=z)
    s.circle(c, r * 0.62, "none", stroke=PLATE_EDGE, sw=1.4, z=z)
    s.circle(c, 3.2, EQUIP_DARK, z=z + 1)


def dumbbell(s, hand, z=9):
    s.line(add(hand, (-9, 0)), add(hand, (9, 0)), 2.6, EQUIP_DARK, z=z)
    for dx in (-9, 9):
        s.rect(hand[0] + dx - 3.5, hand[1] - 6.5, 7, 13, EQUIP_DARK, z=z, r=2)


def hand_of(a):
    return add(a["wrist"], mul(unit(sub(a["wrist"], a["elbow"])), 3.0))


# ------------------------------------------------------------------ squat
def squat(phase):
    s = Scene()
    ground(s, -48, 52)
    if phase == "start":
        hip, L, nd = (-3, 92.5), 4, lean(2)
    else:
        hip, L, nd = (-20, 44), 42, lean(24)
    td = lean(L)
    sh = shoulder_of(hip, td)
    bar = add(add(sh, mul(perp(td), 11)), mul(td, 1))
    legs = [leg(hip, (-3, ANKLE_H), far=True), leg(hip, (0, ANKLE_H))]
    arms = [arm(sh, add(bar, (-1, 1)), far=True, prefer="down", k=0.8),
            arm(sh, add(bar, (1, -1.5)), prefer="down", k=0.8)]
    draw_body(s, hip, td, legs, arms, neck_dir=nd, head_offset=2)
    plate(s, bar)
    if phase == "finish":
        s.arrow([(-44, 98), (-44, 50)], both=True)
    return s


# ------------------------------------------------------------- RDL
def rdl(phase):
    s = Scene()
    ground(s, -45, 50)
    if phase == "start":
        hip, L, nd = (-3, 92), 3, lean(3)
        sh = shoulder_of(hip, lean(L))
        grip = (6.5, 84.5)
    else:
        hip, L, nd = (-22, 86), 72, lean(62)
        sh = shoulder_of(hip, lean(L))
        grip = (9.5, 46)
    td = lean(L)
    wrist = add(grip, mul(unit(sub(sh, grip)), 3.0))
    legs = [leg(hip, (-3, ANKLE_H), far=True), leg(hip, (0, ANKLE_H))]
    arms = [arm(sh, add(wrist, (-2, 0.5)), far=True), arm(sh, wrist)]
    draw_body(s, hip, td, legs, arms, neck_dir=nd, head_offset=1)
    plate(s, grip)
    if phase == "finish":
        s.arrow([(hip[0] + 4, hip[1] + 20), (hip[0] - 20, hip[1] + 20)])
        s.arrow([(37, 80), (37, 52)])
    return s


# ------------------------------------------------- Bulgarian split squat
BENCH_TOP = 46
REAR_PHI = -159.1                       # foot laces-down, flat on the bench
REAR_ANKLE = (-62, BENCH_TOP + 4.1)


def bench(s, x0, x1, top, z=0):
    s.rect(x0, top - 7, x1 - x0, 7, EQUIP, z=z, r=2.5)
    for x in (x0 + 5, x1 - 8):
        s.rect(x, 0, 3.5, top - 7, EQUIP_DARK, z=z)


def bss(phase):
    s = Scene()
    ground(s, -98, 40)
    bench(s, -96, -54, BENCH_TOP)
    if phase == "start":
        hip, L = (-10, 88), 5
    else:
        hip, L = (-30, 50), 12
    td = lean(L)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, REAR_ANKLE, phi=REAR_PHI, far=True, prefer="down"),
            leg(hip, (0, ANKLE_H))]
    a_far = arm(sh, add(sh, (0, -57)), far=True)
    a_near = arm(sh, add(sh, (2, -57)))
    draw_body(s, hip, td, legs, [a_far, a_near], neck_dir=lean(2), head_offset=2)
    dumbbell(s, hand_of(a_near))
    if phase == "finish":
        s.arrow([(-46, 98), (-46, 60)], both=True)
    return s


# -------------------------------------------------------------- leg press
LP_HIP = (0, 30)
LP_TORSO = dirv(140)
LP_N = unit((1, 1))          # sled travel direction (45 degrees)
LP_ALONG = unit((-1, 1))     # along the platform face (toes direction)
LP_ANKLE_F = (55.4, 56.6)
LP_TRAVEL = 23


def leg_press(phase):
    s = Scene()
    ground(s, -66, 112)
    ankle = LP_ANKLE_F if phase == "finish" else add(LP_ANKLE_F, mul(LP_N, LP_TRAVEL))
    hip, td = LP_HIP, LP_TORSO
    sh = shoulder_of(hip, td)
    bn = perp(td)  # behind the back
    if bn[1] > 0:
        bn = mul(bn, -1)
    # frame
    s.rect(-62, 0, 172, 5, EQUIP_DARK, z=-1, r=2)
    corner = add(hip, mul(bn, 13))
    s.capsule(add(corner, mul(td, -2)), add(sh, add(mul(bn, 13), mul(td, 14))), 9, EQUIP, z=0)
    s.capsule(add(corner, mul(dirv(25), -4)), add(corner, mul(dirv(25), 22)), 9, EQUIP, z=0)
    s.line(add(corner, (4, -2)), (add(corner, (4, -2))[0], 3), 5, EQUIP_DARK, z=-1)
    s.line(add(add(sh, mul(bn, 13)), mul(td, -10)), (-58, 3), 5, EQUIP_DARK, z=-1)
    # rail (under the sled)
    m = (LP_N[1], -LP_N[0])
    plat_c_f = add(add(LP_ANKLE_F, mul(LP_N, 11.5)), mul(LP_ALONG, 8))
    r0 = add(plat_c_f, mul(m, 17))
    rail_a = add(r0, mul(LP_N, -(r0[1] - 4) / LP_N[1]))
    rail_b = add(r0, mul(LP_N, 44))
    s.line(rail_a, rail_b, 5, EQUIP_DARK, z=-1)
    # platform + sled
    pc = add(add(ankle, mul(LP_N, 11.5)), mul(LP_ALONG, 8))
    s.capsule(add(pc, mul(LP_ALONG, -22)), add(pc, mul(LP_ALONG, 24)), 7, EQUIP_DARK, z=9)
    s.capsule(add(pc, mul(LP_N, 4)), add(add(pc, mul(LP_N, 4)), mul(m, 14)), 6, EQUIP, z=-1)
    # handles beside the seat
    handle = (-2, 33)
    s.line(add(handle, (-2, -10)), handle, 4, EQUIP_DARK, z=7)
    legs = [leg(hip, add(ankle, (-1.5, 1.5)), phi=135, far=True, prefer="up"),
            leg(hip, ankle, phi=135, prefer="up")]
    arms = [arm(sh, add(handle, (-2, 0)), far=True, prefer="down"),
            arm(sh, handle, prefer="down")]
    draw_body(s, hip, td, legs, arms, neck_dir=dirv(128), head_offset=1.5)
    if phase == "finish":
        a = add(add(LP_ANKLE_F, mul(LP_ALONG, -26)), mul(LP_N, 6))
        s.arrow([add(a, mul(LP_N, LP_TRAVEL + 6)), a], both=True)
    return s


# ---------------------------------------------------- lying hamstring curl
HC_HIP = (0, 60)
PAD_TOP = 50


def ham_curl(phase):
    s = Scene()
    ground(s, -100, 92)
    # machine: pad, frame, legs
    s.rect(-36, PAD_TOP - 8, 120, 8, EQUIP, z=0, r=3)
    s.rect(-30, PAD_TOP - 13, 104, 5, EQUIP_DARK, z=-1)
    for x in (-26, 66):
        s.rect(x, 0, 4, PAD_TOP - 13, EQUIP_DARK, z=-1)
    s.line((78, 46), (80, 34), 4, EQUIP_DARK, z=-1)  # hand grip
    hip, td = HC_HIP, dirv(4)
    sh = shoulder_of(hip, td)
    shin_deg = 181 if phase == "start" else 78
    near = fk_leg(hip, 185, shin_deg, -90 if phase == "start" else 168)
    far = fk_leg(add(hip, (0, 0.5)), 185.5, shin_deg + 2,
                 -90 if phase == "start" else 170, far=True)
    knee, ankle = near["knee"], near["ankle"]
    up = unit(sub(knee, ankle))
    n_back = (-up[1], up[0])
    if phase == "start":
        n_back = (0, 1)
    else:
        n_back = (abs(n_back[0]), n_back[1]) if n_back[0] > 0 else mul(n_back, -1)
    roller = add(add(ankle, mul(up, 7)), mul(n_back, 10.5))
    s.line(knee, roller, 4, EQUIP_DARK, z=3)
    s.circle(knee, 4.5, EQUIP_DARK, z=3)
    s.circle(roller, 6.5, EQUIP, stroke=EQUIP_DARK, sw=1.6, z=9)
    arms = [arm(sh, (79, 41), far=True, prefer="up"),
            arm(sh, (80, 40), prefer="up")]
    draw_body(s, hip, td, [far, near], arms, neck_dir=dirv(12), head_offset=2.5)
    if phase == "finish":
        s.arc_arrow(knee, 58, 172, 100)
    return s


# ------------------------------------------------------ standing calf raise
STEP_BALL = (2, 25.2)


def standing_calf(phase):
    s = Scene()
    ground(s, -40, 60)
    s.rect(-6, 0, 48, 24, EQUIP_LIGHT, stroke=EQUIP_DARK, sw=1.6, z=0, r=2)
    phi = 24 if phase == "start" else -35
    ankle = ankle_from_ball(STEP_BALL, phi)
    hip = add(ankle, (-0.8, 86.6))
    td = lean(1)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, add(ankle, (-2, 0.3)), phi=phi, far=True), leg(hip, ankle, phi=phi)]
    arms = [arm(sh, add(sh, (0, -57)), far=True), arm(sh, add(sh, (2, -57)))]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(1), head_offset=2)
    if phase == "finish":
        s.arrow([(-26, 12), (-26, 50)], both=True)
    return s


# -------------------------------------------------------- seated calf raise
SC_HIP = (-38, 54)
SC_BALL = (20, 11.2)


def seated_calf(phase):
    s = Scene()
    ground(s, -64, 56)
    bench(s, -62, -18, 46)
    s.rect(18, 0, 28, 10, EQUIP_LIGHT, stroke=EQUIP_DARK, sw=1.6, z=0, r=2)
    phi = 15 if phase == "start" else -30
    ankle = ankle_from_ball(SC_BALL, phi)
    hip = SC_HIP
    knee = ik(hip, ankle, THIGH, SHIN, "up")
    # knee pad on the lower thighs + machine column
    tdir = unit(sub(knee, hip))
    tn = perp(tdir)
    pad = add(add(knee, mul(tdir, -9)), mul(tn, 10.5))
    s.capsule(add(pad, mul(tdir, -11)), add(pad, mul(tdir, 9)), 8, EQUIP, z=9)
    s.line((44, 9), (44, pad[1]), 5, EQUIP_DARK, z=-1)
    s.line((44, pad[1]), add(pad, mul(tdir, 9)), 5, EQUIP_DARK, z=-1)
    td = lean(2)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, add(ankle, (-2, 0.4)), phi=phi, far=True, prefer="up"),
            {"knee": knee, "ankle": ankle, "phi": phi}]
    grip = add(pad, (-2, 6))
    arms = [arm(sh, add(grip, (-3, 1)), far=True, prefer="down"),
            arm(sh, grip, prefer="down")]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(4), head_offset=2)
    if phase == "finish":
        s.arrow([(-10, 4), (-10, 32)], both=True)
    return s


# ------------------------------------------------------------ tibialis raise
WALL_X = -48.5
TIB_HEEL = (5, 1.25)
TIB_HIP_X = -36


def tibialis(phase):
    s = Scene()
    ground(s, -58, 40)
    s.rect(WALL_X - 8, 0, 8, 168, EQUIP_LIGHT, stroke=EQUIP, sw=1.5, z=-2)
    a0 = ankle_from_heel(TIB_HEEL, 0)
    d0 = 86.6
    hip0 = (TIB_HIP_X, a0[1] + math.sqrt(d0 ** 2 - (a0[0] - TIB_HIP_X) ** 2))
    phi = 0 if phase == "start" else 28
    ankle = ankle_from_heel(TIB_HEEL, phi)
    # legs stay straight: the hips slide a hair along the wall
    hip = (TIB_HIP_X, ankle[1] + math.sqrt(d0 ** 2 - (ankle[0] - TIB_HIP_X) ** 2))
    td = lean(-2)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, add(ankle, (-2, 0.3)), phi=phi, far=True), leg(hip, ankle, phi=phi)]
    arms = [arm(sh, add(sh, (1, -56)), far=True), arm(sh, add(sh, (3, -56)))]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(4), head_offset=2)
    if phase == "finish":
        s.arc_arrow(TIB_HEEL, 30, 4, 34)
    return s


# =================================================== active-recovery minis
def _stand(s, arms_fn, torso=lean(0)):
    ground(s, -30, 40)
    hip = (-1.5, 93.5)
    sh = shoulder_of(hip, torso)
    legs = [leg(hip, (-3, ANKLE_H), far=True), leg(hip, (0, ANKLE_H))]
    arms = arms_fn(sh)
    draw_body(s, hip, torso, legs, arms, neck_dir=lean(2), head_offset=2)
    return sh


def ar_shoulder_circles():
    """Front view: both shoulders roll in slow circles, arms hang relaxed."""
    s = Scene()
    ground(s, -38, 38)
    for side in (-1, 1):
        hipj, sh = (side * 9, 93), (side * 19, 142)
        knee, ankle = (side * 9.5, 50), (side * 10, ANKLE_H)
        s.line(hipj, knee, 12, NEAR, z=4)
        s.line(knee, ankle, 10, NEAR, z=4)
        s.poly([add(ankle, (side * -3, 2)), add(ankle, (side * 9, -2)),
                add(ankle, (side * 9, -6.5)), add(ankle, (side * -4, -6.5))],
               NEAR, stroke=NEAR, sw=2.5, z=4)
        el, wr = (side * 22.5, 111.5), (side * 24, 84.5)
        s.line(sh, el, 8.5, NEAR, z=6)
        s.line(el, wr, 7.5, NEAR, z=6)
        s.circle(add(wr, (0, -3)), 4.6, NEAR, z=6)
        a0, a1 = (110, 400) if side < 0 else (70, -220)
        s.arc_arrow((side * 21, 147), 11.5, a0, a1, color=CALM, w=3.2, head=7.5)
    s.poly([(-21, 146), (21, 146), (13, 92), (-13, 92)], NEAR, stroke=NEAR, sw=6, z=5)
    s.line((0, 146), (0, 153), 8, NEAR, z=5)
    s.circle((0, 160), HEAD_R, NEAR, z=5)
    return s


def ar_wrist():
    s = Scene()

    def arms(sh):
        out = []
        for far, dx, dy in ((True, -1.5, 1.5), (False, 0, 0)):
            el = add(sh, (dx + 3, -UARM + 0.15))
            out.append({"elbow": el, "wrist": add(el, (FARM, dy)), "far": far})
        return out
    sh = _stand(s, arms)
    hand = add(sh, (3 + FARM + 3, -UARM))
    s.arc_arrow(hand, 13, 100, 400, color=CALM, w=3.4, head=8)
    return s


def ar_thoracic():
    s = Scene()
    ground(s, -26, 56)
    bench(s, -22, 26, 42)
    hip, td = (0, 50), lean(0)
    sh = shoulder_of(hip, td)
    legs = [fk_leg(add(hip, (-2, 0.5)), 1, -90, 0, far=True), fk_leg(hip, 0, -90, 0)]
    arms = [{"elbow": add(sh, (12, -18)), "wrist": add(sh, (11, -2)), "far": True},
            {"elbow": add(sh, (14, -20)), "wrist": add(sh, (8, -3))}]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(2), head_offset=2)
    s.arc_arrow(add(sh, (0, -14)), 27, 200, 340, ry=8, color=CALM, w=3.4, both=True, head=8)
    return s


def ar_scapular():
    s = Scene()

    def arms(sh):
        return [{"elbow": add(sh, (UARM - 0.5, 0.5)), "wrist": add(sh, (UARM + FARM - 1, 1)),
                 "far": True},
                {"elbow": add(sh, (UARM, -1.5)), "wrist": add(sh, (UARM + FARM, -2.5))}]
    sh = _stand(s, arms)
    s.arrow([add(sh, (34, 15)), add(sh, (64, 15))], color=CALM, w=3.4, both=True, head=8)
    return s


# ======================================== warm-up / cardio / cool-down art
def treadmill_walk():
    s = Scene()
    belt = 9
    s.rect(-52, 0, 104, belt, EQUIP_DARK, z=-1, r=3)
    s.line((46, belt), (52, 112), 5, EQUIP, z=-1)
    s.line((52, 112), (30, 104), 5, EQUIP, z=-1)
    s.rect(44, 108, 16, 9, EQUIP_DARK, z=-1, r=2)
    hip, td = (0, belt + 86), lean(5)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, (-22, belt + 9), phi=-25, far=True),
            leg(hip, (22, belt + ANKLE_H + 1.5), phi=12)]
    arms = [arm(sh, add(sh, (16, -50)), far=True, prefer="back"),
            arm(sh, add(sh, (-15, -53)), prefer="back")]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(4), head_offset=2)
    return s


def bw_lunge():
    s = Scene()
    ground(s, -60, 50)
    hip, td = (-6, 50), lean(3)
    sh = shoulder_of(hip, td)
    rear = ankle_from_ball((-42, 1.25), -55)
    legs = [leg(hip, rear, phi=-55, far=True, prefer="down"), leg(hip, (28, ANKLE_H))]
    hips_hand = add(hip, (5, 9))
    arms = [arm(sh, add(hips_hand, (-2, 1)), far=True, prefer="back"),
            arm(sh, hips_hand, prefer="back")]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(3), head_offset=2)
    return s


def wall_calf_stretch():
    s = Scene()
    ground(s, -60, 64)
    s.rect(54, 0, 8, 160, EQUIP_LIGHT, stroke=EQUIP, sw=1.5, z=-2)
    hip, td = (-5, 78), lean(22)
    sh = shoulder_of(hip, td)
    legs = [leg(hip, (-48, ANKLE_H), far=True), leg(hip, (25, ANKLE_H))]
    arms = [arm(sh, (51, 127), far=True, prefer="down"), arm(sh, (52, 126), prefer="down")]
    draw_body(s, hip, td, legs, arms, neck_dir=lean(18), head_offset=2)
    return s


ART = {"treadmill": treadmill_walk, "lunge": bw_lunge, "calf_stretch": wall_calf_stretch}


def art_svg(name, max_w, max_h):
    s = ART[name]()
    box = s.bbox()
    pad = 4
    sc = min((max_w - 2 * pad) / (box[2] - box[0]), (max_h - 2 * pad) / (box[3] - box[1]))
    return s.svg(box, sc, pad)


EXERCISES = {
    "squat": squat, "rdl": rdl, "bss": bss, "leg_press": leg_press,
    "ham_curl": ham_curl, "standing_calf": standing_calf,
    "seated_calf": seated_calf, "tibialis": tibialis,
}
MINIS = {
    "shoulder_circles": ar_shoulder_circles, "wrist": ar_wrist,
    "thoracic": ar_thoracic, "scapular": ar_scapular,
}


def pair_fit(name, max_w, max_h):
    """Start/finish share one bounding box and one scale, fitted to a box."""
    a, b = EXERCISES[name]("start"), EXERCISES[name]("finish")
    box = union(a.bbox(), b.bbox())
    pad = 5
    sc = min((max_w - 2 * pad) / (box[2] - box[0]), (max_h - 2 * pad) / (box[3] - box[1]))
    return a.svg(box, sc, pad), b.svg(box, sc, pad)


def pair_svgs(name, scale):
    """Start/finish share one bounding box and one scale, so they line up."""
    a, b = EXERCISES[name]("start"), EXERCISES[name]("finish")
    box = union(a.bbox(), b.bbox())
    return a.svg(box, scale, 6), b.svg(box, scale, 6)


def mini_svg(name, max_w, max_h):
    s = MINIS[name]()
    box = s.bbox()
    pad = 4
    sc = min((max_w - 2 * pad) / (box[2] - box[0]), (max_h - 2 * pad) / (box[3] - box[1]))
    return s.svg(box, sc, pad)
