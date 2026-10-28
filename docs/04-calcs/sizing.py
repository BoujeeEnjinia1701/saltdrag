"""SaltDrag sizing calculations (SDG-CAL-001). First-order estimates for TRL 3.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every result with its label ([A1], [B2] ...) used in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv. Geometry and masses come from cad/src/model.py (PARAMS, derived(),
masses()), so a change to the model flows into the numbers. Every input that is not geometry is an
assumption listed in ASSUME, with its source or the reason for the value.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, masses, rake_components, mass  # noqa: E402

G = 9.81
ASSUME = {
    # salt bed and heap (estimates; the drag per metre of rake is measured at TRL 4)
    "bulk_density": 1200.0,      # kg/m3, loose crystallised salt (typical 1,100 to 1,300)
    "repose_deg": 35.0,          # angle of repose of the heap in front of the blade
    "mu_heap": 0.70,             # heap sliding on the salt bed, tan(35 deg)
    "cut_n_per_m": 300.0,        # N per metre of blade to loosen and lift the harvest layer (estimate)
    "mu_skid": 0.30,             # UHMW-PE skids on wet salt
    "back_tension": 200.0,       # N held by the far capstan's brake to keep the rake straight
    "eta_roller": 0.98,          # rope over the bund roller
    "eta_gear": 0.96,            # one spur stage, greased, with dust
    "eta_brg": 0.98,             # four flange bearings
    # people
    "crank_force_max": 120.0,    # N per handle (R2)
    "crankers": 2,
    "crank_rpm": 23.0,           # steady cranking rate under load (SDG-DEC-001 D17: 23, was 30, so each cranker
                                 # stays within 75 W sustained even with the rope on its third layer, STM S15)
    "return_rpm": 50.0,          # cranking rate on the light return pass
    "shift_min": 8.0,            # moving both capstans and rollers 3 m along the bunds and re-anchoring
    "crew": 4,                   # 2 cranking near, 1 at the far capstan, 1 moving rollers and ropes
    # materials and bought parts (catalogue-class values, confirmed when parts are bought)
    "rope_mbs": 27000.0,         # N, 12 mm polyester double braid, minimum breaking strength
    "splice_eff": 0.85,          # eye splice efficiency
    "yield_c45": 305.0,          # MPa, C45+N (EN 10083-2), 16 to 100 mm (340 applies only up to 16 mm; review)
    "yield_c45qt": 430.0,        # MPa, C45+QT (EN 10083-2), 16 to 40 mm: drum shaft, crank shaft, gear (D24)
    "uts_c45qt": 650.0,          # MPa, C45+QT lower bound, 16 to 40 mm
    "corr_exposed": 0.5,         # fatigue strength factor for bare steel in salt air (corrosion fatigue, estimate)
    "kf_step": 1.6,              # fatigue notch factor at the crank shaft step, 1.5 mm fillet (estimate)
    "n_fatigue": 1.5,            # Goodman safety factor sought on the crank shaft (design target)
    "sigma_h_pinion": 1000.0,    # MPa, allowable contact stress, induction-hardened C45 pinion teeth (D24, estimate)
    "k_appl": 1.25,              # application factor for hand cranking (ISO 6336 practice, light shocks)
    "share": 0.70,               # share of the rope pull on the more heavily loaded chain (review: unequal tension)
    "yield_s275": 275.0,         # MPa, S275 structural steel
    "frp_flex": 200.0,           # MPa, pultruded FRP square tube, flexural strength (lower bound)
    "frp_E": 23000.0,            # MPa
    "chain_wll": 11800.0,        # N, 10 mm grade 30 galvanised chain, working load limit 2,650 lb (D22; was 8 mm)
    "su_clay": 50.0,             # kPa, undrained shear strength of firm clay behind the bund (to confirm)
    "nc_helix": 9.0,             # bearing factor for a deep helix
    "mu_band": 0.20,             # woven brake lining on steel, wet with brine (design value, D21; 0.30 dry)
    "lewis_y14": 0.277,          # Lewis form factor, 14 teeth, 20 deg full depth
    "lewis_y84": 0.45,
    "yield_barrel": 310.0,       # MPa, drum barrel tube YSt 310 (IS 4923) or S355J2H (EN 10210), SDG-DEC-001 D18
    "layer_factor": 1.8,         # drum barrel pressure factor for three layers wound under load (multi-layer
                                 # winding practice for wire rope, conservative for a polyester rope; to confirm)
    "harvest_days": 61.0,        # March and April (PRB)
    "work_h_per_day": 6.0,       # cooler hours of the day in the harvest season (assumption)
    "pan_output_t": 550.0,       # t a year from one family pan, middle of 500 to 600 (Business Standard, 2009)
}
A = ASSUME
D = derived(P)
R = {}          # label -> (value, unit, text)


def put(label, value, unit, text):
    R[label] = (value, unit, text)
    v = f"{value:,.2f}" if isinstance(value, float) else f"{value}"
    print(f"[{label}] {text}: {v} {unit}")
    return value


# ------------------------------------------------------------------ A. Drag on the rake
L_blade = P["blade"][3] / 1000
h = P["blade"][1] / 1000
A_heap = h ** 2 / (2 * math.tan(math.radians(A["repose_deg"])))
V_heap = put("A1", A_heap * L_blade, "m3", "heap held in front of the blade when full")
m_heap = put("A2", V_heap * A["bulk_density"], "kg", "salt in a full heap")
F_heap = put("A3", A["mu_heap"] * m_heap * G, "N", "force to slide the full heap over the bed")
F_cut = put("A4", A["cut_n_per_m"] * L_blade, "N", "allowance to loosen and lift the harvest layer")
M = masses(P)
m_rake = sum(m for (grp, k), (_, _, m) in M.items() if grp == "rake" and k != "ballast")
m_ball = sum(m for (grp, k), (_, _, m) in M.items() if grp == "rake" and k == "ballast")
put("A5", m_rake, "kg", "rake mass without ballast (model)")
put("A5b", m_ball, "kg", "two ballast bags filled with salt on site (model)")
F_skid = put("A6", A["mu_skid"] * (m_rake + m_ball) * G, "N", "skid friction")
F_drag = put("A7", F_heap + F_cut + F_skid, "N", "design drag on the rake with a full heap")
F_rope = put("A8", F_drag / A["eta_roller"] + A["back_tension"], "N", "rope pull at the drum")
rated = 3000.0
for lab, k in (("A9", 0.5), ("A10", 1.5), ("A11", 2.0)):
    Fk = (F_heap + F_cut) * k + F_skid
    put(lab, (Fk / A["eta_roller"] + A["back_tension"]) / F_rope, "", f"rope pull if the heap and layer drag is {k:g} times the estimate, over the design pull")

# ------------------------------------------------------------------ B. Capstan: crank force, pull, speed
eta = A["eta_gear"] * A["eta_brg"]
i_g = D["ratio"]
r_end = D["layers"][2][1] / 1000          # layer 3: rope on the drum when the rake reaches the near bund
r_full = D["layers"][3][1] / 1000         # layer 4: a 45 m rope fully wound
put("B1", i_g, "", "gear ratio (84 to 14 teeth)")
put("B2", r_end * 1000, "mm", "rope radius on the drum at the end of a 30 m pass (layer 3)")
Tc = F_rope * r_end / (i_g * eta)
f_crank = put("B3", Tc / (A["crankers"] * P["crank_r"] / 1000), "N", "force on each crank handle at the design drag")
T_in = A["crank_force_max"] * A["crankers"] * P["crank_r"] / 1000
pull_end = put("B4", T_in * i_g * eta / r_end, "N", "rope pull with two people at 120 N, layer 3")
pull_full = put("B5", T_in * i_g * eta / r_full, "N", "rope pull with two people at 120 N, layer 4 (full drum)")
r_mean = (D["layers"][0][1] + D["layers"][2][1]) / 2000
v_rope = put("B6", 2 * math.pi * r_mean * A["crank_rpm"] / i_g / 60, "m/s", "rope speed at 23 crank turns a minute")
P_each = put("B7", F_rope * v_rope / eta / A["crankers"], "W", "work rate of each cranker, mean over a pass")
v3 = 2 * math.pi * r_end * A["crank_rpm"] / i_g / 60
put("B7b", F_rope * v3 / eta / A["crankers"], "W", "work rate of each cranker with the rope on its third layer (end of a pass)")
# rope stored
put("B8", D["layers"][3][2], "m", "rope the drum holds in four layers")
put("B9", D["freeboard"], "mm", "flange freeboard above the fourth layer")

# ------------------------------------------------------------------ C. Strength at twice the rated pull (6 kN)
Fd = 2 * rated
Td = Fd * r_full
span = 2 * (D["cheek_out"] + P["brg_drum"][2] / 2)
d = P["dshaft"][0] / 1000
# drum shaft between bearings A (-span/2) and B (+span/2): rope load at the barrel centre (toward the pan, -Y),
# gear tooth force at the overhung gear (+Y tangential, radial down) (independent review: gear reaction added)
xa, xb = -span / 2, span / 2
x_rope = (D["barrel_x"][0] + D["barrel_x"][1]) / 2
x_gear = P["gear_x0"] + P["gear_face"] / 2
Ftg = Td / (D["rg"] / 1000)
Frg = Ftg * math.tan(math.radians(20))
def _reac(loads):
    rb = -sum(f * (x - xa) for f, x in loads) / (xb - xa)
    return -sum(f for f, _ in loads) - rb, rb
ray, _ = _reac([(-Fd, x_rope), (Ftg, x_gear)])
raz, _ = _reac([(-Frg, x_gear)])
My = ray * (x_rope - xa) / 1000
Mz = raz * (x_rope - xa) / 1000
Mb = math.hypot(My, Mz)
sb = 32 * Mb / (math.pi * d ** 3) / 1e6
tau = 16 * Td / (math.pi * d ** 3) / 1e6
svm = put("C1", math.sqrt(sb ** 2 + 3 * tau ** 2), "MPa", "drum shaft, 40 mm, combined stress at 6 kN with the gear reaction")
put("C1b", A["yield_c45qt"] / svm, "", "drum shaft margin to yield at 6 kN (C45+QT)")
Tp = Td / i_g / eta
Ft = Tp / (D["rp"] / 1000)
Fmesh = Ft / math.cos(math.radians(20))
x_pin = P["pinion_x0"] + P["pinion_face"] / 2
over = x_pin - (D["cheek_out"] + P["brg_pin"][2] / 2)
dp = P["pshaft_brg"] / 1000
sbp = 32 * Fmesh * over / 1000 / (math.pi * dp ** 3) / 1e6
taup = 16 * Tp / (math.pi * dp ** 3) / 1e6
svp = put("C2", math.sqrt(sbp ** 2 + 3 * taup ** 2), "MPa", "crank shaft, 30 mm at the bearing, at 6 kN")
put("C2b", A["yield_c45qt"] / svp, "", "crank shaft margin to yield at 6 kN (C45+QT)")
d25 = P["pshaft"][0] / 1000
arm_s = x_pin - P["pshaft_step"]
s_step = math.sqrt((32 * Fmesh * arm_s / 1000 / (math.pi * d25 ** 3) / 1e6) ** 2 + 3 * (16 * Tp / (math.pi * d25 ** 3) / 1e6) ** 2)
put("C2c", A["yield_c45qt"] / s_step, "", "crank shaft margin to yield at the 25 mm step, 6 kN")
# fatigue of the crank shaft at the rated pull (rotating bending, steady torque), Goodman, corrosion-derated
Tr, Ftr = Tp / 2, Fmesh / 2
def _goodman(dd, arm, kf, corr):
    sa = kf * 32 * Ftr * arm / 1000 / (math.pi * dd ** 3) / 1e6
    sm = math.sqrt(3) * 16 * Tr / (math.pi * dd ** 3) / 1e6
    ka = 4.51 * A["uts_c45qt"] ** -0.265
    kb = 1.24 * (dd * 1000) ** -0.107
    se = 0.5 * A["uts_c45qt"] * ka * kb * corr
    return 1 / (sa / se + sm / A["uts_c45qt"])
put("C16", _goodman(d25, arm_s, A["kf_step"], A["corr_exposed"]), "", "crank shaft fatigue safety factor at the 25 mm step, rated pull (Goodman, corroded)")
put("C16b", _goodman(dp, over * 0.92, 1.0, A["corr_exposed"]), "", "crank shaft fatigue safety factor at the cheek, 30 mm, rated pull (Goodman, corroded)")
s_pin = put("C3", Ft / (P["gear_face"] * P["module"] * A["lewis_y14"]), "MPa", "pinion tooth bending (Lewis) at 6 kN")
put("C3b", A["yield_c45"] / s_pin, "", "pinion tooth margin to yield at 6 kN")
Ftr_t = Tp / 2 / (D["rp"] / 1000)
sH = 189.8 * 2.495 * math.sqrt(A["k_appl"] * Ftr_t / (P["gear_face"] * 2 * D["rp"]) * (i_g + 1) / i_g)
put("C3c", sH, "MPa", "pinion contact stress (Hertz) at the rated pull, application factor 1.25")
put("C3d", A["sigma_h_pinion"] / sH, "", "pinion contact margin, induction-hardened teeth")
r_tooth = (P["ratchet"][0] / 2 - 7) / 1000
F_pawl = put("C4", Td / r_tooth, "N", "pawl tip force at 6 kN")
cant = (abs(P["ratchet"][3]) - P["ratchet"][2] / 2) - D["cheek_out"]
bo = P["pawl"][4]
bi = P["pawl"][3] + 1.0
Zb = math.pi * (bo ** 4 - bi ** 4) / (32 * bo)
s_boss = put("C5", F_pawl * cant / Zb, "MPa", "pawl boss bending (40 mm boss welded to the cheek) at 6 kN")
put("C5b", A["yield_s275"] / s_boss, "", "pawl boss margin to yield (S275 tube)")
theta = math.radians(360 - 2 * math.degrees(math.acos((P["flange"][0] / 2 + P["band"][1] / 2) / math.hypot(P["lever_pivot"][0], P["lever_pivot"][1] - P["drum_z"]))))
ratio_b = math.exp(A["mu_band"] * theta)
put("C6", math.degrees(theta), "deg", "brake band wrap")
T_brake = rated * r_full
dT = T_brake / ((P["flange"][0] / 2) / 1000)
T2 = dT / (ratio_b - 1)
put("C7", T2 * 50 / P["lever_len"], "N", "hand force on the brake lever to hold the rated pull (50 mm inner arm)")
put("C8", A["rope_mbs"] * A["splice_eff"] / rated, "", "rope working-load factor at the rated pull, after splices")
# anchors and chains
ey, ez = P["ear"][0], P["ear"][1]
aey = P["anchor_eye"][0]
ang = math.atan2(ez - 25, aey - ey)
T_chain = put("C9", A["share"] * Fd / math.cos(ang), "N", "more loaded chain at 6 kN, 70 % of the pull")
put("C9b", A["chain_wll"] / T_chain, "", "chain working load limit over the 6 kN chain force (10 mm grade 30)")
Q = A["nc_helix"] * A["su_clay"] * 1000 * math.pi * (P["helix"][0] / 2000) ** 2
put("C10", Q, "N", "holding of one 150 mm helix in firm clay (estimate)")
put("C10b", Q / T_chain, "", "anchor holding over the 6 kN chain force (70 % share)")
put("C10c", A["share"] * rated / math.cos(ang) * 1.5, "N", "proof pull for each anchor on site (1.5 times its 70 % share of the rated pull)")
# tipping of the capstan at the rated pull (about the front tips of the runners)
m_cap = sum(m for (grp, k), (_, _, m) in M.items() if grp == "capstan" and k != "anchors")
z_rope = P["drum_z"] + D["layers"][2][1] + P["rope_d"] / 2
y_front = abs(P["runner"][2])
M_tip = rated * z_rope / 1000
M_res = rated * ez / 1000 + rated * math.tan(ang) * (ey + y_front) / 1000 + m_cap * G * y_front / 1000
put("C11", m_cap, "kg", "capstan mass without anchors (model)")
put("C12", M_res / M_tip, "", "capstan resistance to tipping over the rated pull")
M_tip6 = Fd * z_rope / 1000
M_res6 = Fd * ez / 1000 + Fd * math.tan(ang) * (ey + y_front) / 1000 + m_cap * G * y_front / 1000
put("C12b", M_res6 / M_tip6, "", "capstan resistance to tipping at 6 kN")
# rake beam (pulled at both ends; heap and cutting load spread along the blade, at 6 kN)
w = 2 * (F_heap + F_cut) / P["beam"][2]
bs, bw = P["beam"][0], P["beam"][1]
I = (bs ** 4 - (bs - 2 * bw) ** 4) / 12
Z = I / (bs / 2)
Mbeam = w * P["beam"][2] ** 2 / 8
put("C13", Mbeam / Z, "MPa", "rake beam bending at 6 kN")
put("C13b", A["frp_flex"] / (Mbeam / Z), "", "rake beam margin to FRP flexural strength")
dl = 5 * (w / 2) * P["beam"][2] ** 4 / (384 * A["frp_E"] * I)
put("C14", dl, "mm", "rake beam bow at the rated load")
# drum barrel crushed by the rope wound on under load (hoop stress of a ring under the rope pressure,
# sigma = T / (t s) for one layer, times the multi-layer factor for three loaded layers), at 6 kN
s_bar = put("C15", A["layer_factor"] * Fd / (P["barrel"][1] * P["rope_d"]), "MPa",
            "drum barrel hoop stress under three layers of rope wound at 6 kN")
put("C15b", A["yield_barrel"] / s_bar, "", "drum barrel margin to yield (168.3 x 6.3 YSt 310)")
# keys 12 x 8 on the 40 mm drum shaft, bearing on half the key height (D24)
Lg = P["gear_hub"][2] - P["gear_hub"][1]
put("C17", A["yield_c45qt"] / (2 * Td / (d * 0.004 * Lg / 1000) / 1e6), "", "gear key and hub bearing margin at 6 kN (44 mm hub, C45+QT)")
Lr = P["ratchet"][2] + P["ratchet_hub"][1]
put("C18", A["yield_c45"] / (2 * Td / (d * 0.004 * Lr / 1000) / 1e6), "", "ratchet key and hub bearing margin at 6 kN (64 mm, C45+N)")
# roller axle: rope deflected over the roller up to the lift-off angle, at 6 kN
th_in = math.atan2((D["roller_top"] + P["rope_d"] / 2) - (P["drum_z"] + D["layers"][2][1]), P["capstan_back"])
th_out = math.asin(min(1.0, (m_rake + m_ball) * G / F_rope))
Fr_roll = 2 * Fd * math.sin((th_out - th_in) / 2)
span_ax = 2 * (P["saddle_x"] - P["saddle"][0] / 2)
put("C19", 205.0 / (32 * Fr_roll * span_ax / 4 / 1000 / (math.pi * (P["axle"][1] / 1000) ** 3) / 1e6), "", "roller axle margin at 6 kN (316, yield 205 MPa)")

# ------------------------------------------------------------------ D. Floor, lift-off near the bund, rate, set-up
A_sk = len(P["skid_x"]) * P["skid"][0] * P["skid"][2] / 1e6
put("D1", (m_rake + m_ball) * G / A_sk / 1000, "kPa", "skid pressure on the floor with ballast")
put("D2", P["blade"][2], "mm", "blade edge above the floor, set by the skids")
dz_r = (D["roller_top"] + P["rope_d"] / 2) - P["bridle"][2]
for lab, mm, txt in (("D3", m_rake, "without ballast"), ("D4", m_rake + m_ball, "with ballast")):
    s_ = (mm * G) / F_rope
    th = math.asin(min(1.0, s_))
    dist = dz_r / math.tan(th) / 1000
    blade_from_toe = dist + (P["bridle"][0] + 110) / 1000 - P["bund"][2] / 2000
    put(lab, blade_from_toe, "m", f"blade distance from the bund toe where the rope starts to lift the rake, {txt}")
# rake pitching about the front tips of the skids: pull at the bridle height against the heap (at a third of
# the blade height), the layer (at the edge) and skid friction (at the floor) (independent review; D23)
Rk = rake_components(P)
y_cg = sum(c.shape.center().Y * mass(c) for c in Rk.values()) / sum(mass(c) for c in Rk.values())
M_pitch = (F_drag * P["bridle"][2] - F_heap * (P["blade"][2] + h * 1000 / 3) - F_cut * P["blade"][2]) / 1000
M_rest = (m_rake + m_ball) * G * (y_cg - P["skid"][3]) / 1000
put("D13", M_rest / max(M_pitch, 1e-6), "", "rake resistance to pitching nose-down over the pitching moment, full heap")
pan = P["pan_design"] / 1000
t_pull = put("D5", pan / v_rope / 60, "min", "winding a 30 m pass")
v_ret = 2 * math.pi * r_mean * A["return_rpm"] / i_g / 60
t_ret = put("D6", pan / v_ret / 60, "min", "winding the empty rake back")
cyc = put("D7", t_pull + t_ret + A["shift_min"], "min", "one strip: pull, return and move 3 m")
rate = put("D8", m_heap / cyc * 60, "kg/h", "salt gathered to the windrow per hour (one full heap per strip)")
put("D9", rate / A["crew"], "kg per worker-hour", "gathering rate per worker, crew of four")
setup = {"carry capstan into place": 5.0, "two ground anchors": 6.0, "chains and turnbuckles": 2.0,
         "bund roller on the crest": 1.0, "rope round the pan to the rake": 5.0}
put("D10", sum(setup.values()), "min", "set-up time per crew (two crews work at once)")
season = put("D11", rate * A["harvest_days"] * A["work_h_per_day"] / 1000, "t",
             "salt one set gathers in a 61-day harvest at 6 h a day")
put("D12", season / A["pan_output_t"], "", "share of a 550 t family pan output one set gathers in the harvest")

# ------------------------------------------------------------------ E. Mass and cost
import re  # noqa: E402


def each(name, m):
    """Mass of one piece: a component named 'Skids (3)' is three pieces."""
    k = re.search(r"\((\d+)\)", name)
    return m / int(k.group(1)) if k else m


heavy = max(((n, each(n, m)) for (_, _), (n, _, m) in M.items()), key=lambda t: t[1])
put("E1", heavy[1], "kg", f"heaviest single part ({heavy[0]})")
bom = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
put("E2", cost, "USD", "estimated parts cost of the full set (bom/bom.csv)")
target = 4000.0
put("E3", cost - target, "USD", "over (+) or under (-) the value-engineering target of USD 4,000")

with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["label", "value", "unit", "description"])
    for k, (v, u, t) in R.items():
        wr.writerow([k, f"{v:.3f}" if isinstance(v, float) else v, u, t])
