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
from model import PARAMS as P, derived, masses  # noqa: E402

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
    "crank_rpm": 30.0,           # steady cranking rate under load
    "return_rpm": 50.0,          # cranking rate on the light return pass
    "shift_min": 8.0,            # moving both capstans and rollers 3 m along the bunds and re-anchoring
    "crew": 4,                   # 2 cranking near, 1 at the far capstan, 1 moving rollers and ropes
    # materials and bought parts (catalogue-class values, confirmed when parts are bought)
    "rope_mbs": 27000.0,         # N, 12 mm polyester double braid, minimum breaking strength
    "splice_eff": 0.85,          # eye splice efficiency
    "yield_c45": 340.0,          # MPa, C45 (EN8) bright bar, normalised
    "yield_s275": 275.0,         # MPa, S275 structural steel
    "frp_flex": 200.0,           # MPa, pultruded FRP square tube, flexural strength (lower bound)
    "frp_E": 23000.0,            # MPa
    "chain_wll": 7800.0,         # N, 8 mm grade 30 galvanised chain, working load limit
    "su_clay": 50.0,             # kPa, undrained shear strength of firm clay behind the bund (to confirm)
    "nc_helix": 9.0,             # bearing factor for a deep helix
    "mu_band": 0.30,             # woven brake lining on steel, dusty
    "lewis_y14": 0.277,          # Lewis form factor, 14 teeth, 20 deg full depth
    "lewis_y84": 0.45,
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
v_rope = put("B6", 2 * math.pi * r_mean * A["crank_rpm"] / i_g / 60, "m/s", "rope speed at 30 crank turns a minute")
P_each = put("B7", F_rope * v_rope / eta / A["crankers"], "W", "work rate of each cranker")
# rope stored
put("B8", D["layers"][3][2], "m", "rope the drum holds in four layers")
put("B9", D["freeboard"], "mm", "flange freeboard above the fourth layer")

# ------------------------------------------------------------------ C. Strength at twice the rated pull (6 kN)
Fd = 2 * rated
Td = Fd * r_full
span = 2 * (D["cheek_out"] + P["brg_drum"][2] / 2)
Mb = Fd * span / 4 / 1000            # N m, rope load mid-span
d = P["dshaft"][0] / 1000
sb = 32 * Mb / (math.pi * d ** 3) / 1e6
tau = 16 * Td / (math.pi * d ** 3) / 1e6
svm = put("C1", math.sqrt(sb ** 2 + 3 * tau ** 2), "MPa", "drum shaft, 40 mm, combined stress at 6 kN")
put("C1b", A["yield_c45"] / svm, "", "drum shaft margin to yield at 6 kN")
Tp = Td / i_g / eta
Ft = Tp / (D["rp"] / 1000)
over = (P["pinion_x0"] + P["pinion_face"] / 2) - (D["cheek_out"] + P["brg_pin"][2] / 2)
dp = P["pshaft"][0] / 1000
sbp = 32 * Ft * over / 1000 / (math.pi * dp ** 3) / 1e6
taup = 16 * Tp / (math.pi * dp ** 3) / 1e6
svp = put("C2", math.sqrt(sbp ** 2 + 3 * taup ** 2), "MPa", "crank shaft, 25 mm, at the overhung pinion, 6 kN")
put("C2b", A["yield_c45"] / svp, "", "crank shaft margin to yield at 6 kN")
s_pin = put("C3", Ft / (P["gear_face"] * P["module"] * A["lewis_y14"]), "MPa", "pinion tooth bending (Lewis) at 6 kN")
put("C3b", A["yield_c45"] / s_pin, "", "pinion tooth margin to yield at 6 kN")
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
T_chain = put("C9", Fd / 2 / math.cos(ang), "N", "each chain at 6 kN (two chains)")
put("C9b", A["chain_wll"] / T_chain, "", "chain working load limit over the 6 kN chain force")
Q = A["nc_helix"] * A["su_clay"] * 1000 * math.pi * (P["helix"][0] / 2000) ** 2
put("C10", Q, "N", "holding of one 150 mm helix in firm clay (estimate)")
put("C10b", Q / T_chain, "", "anchor holding over the 6 kN chain force")
# tipping of the capstan at the rated pull (about the front tips of the runners)
m_cap = sum(m for (grp, k), (_, _, m) in M.items() if grp == "capstan" and k != "anchors")
z_rope = P["drum_z"] + D["layers"][2][1] + P["rope_d"] / 2
y_front = abs(P["runner"][2])
M_tip = rated * z_rope / 1000
M_res = rated * ez / 1000 + rated * math.tan(ang) * (ey + y_front) / 1000 + m_cap * G * y_front / 1000
put("C11", m_cap, "kg", "capstan mass without anchors (model)")
put("C12", M_res / M_tip, "", "capstan resistance to tipping over the rated pull")
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
