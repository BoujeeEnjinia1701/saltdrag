"""SaltDrag concept media (TRL 3, constructable design SDG-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py   (after docs/04-calcs/sizing.py)
Takes the working layout from cad/src/model.py and renders the media set with .kit/concept.py:
hero.png (the layout on a pan shortened to 7 m, with the 1.75 m figure), concept-blueprint.*
(SDG-DWG-010), model.glb and viewer.html, exploded.png (the set pulled apart, numbers matching
bom/bom.csv), cutaway.png (one capstan with its left half removed) and flow.png (work per pass).
Every coloured part carries its BOM line number; grey parts (bunds, ground, the far-side set in
the hero) are context. Figures come from docs/04-calcs/results.csv (SDG-CAL-001).
CONCEPT, NOT FOR FABRICATION.
"""
import copy
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import matplotlib.colors as mc  # noqa: E402
from build123d import Compound, Color, Pos, Rot, export_gltf  # noqa: E402
from concept import Part, render_all, _render, cutaway_parts, human_figure  # noqa: E402
from model import (PARAMS as P, capstan_components, rake_components, roller_components, layout,  # noqa: E402
                   context, derived, xcyl)

R = {r["label"]: float(r["value"]) for r in csv.DictReader((ROOT / "docs" / "04-calcs" / "results.csv").open())}
D = derived(P)
COL = {1: "#4B5563", 2: "#6B7280", 3: "#C2410C", 4: "#B45309", 5: "#92400E", 6: "#1D4ED8", 7: "#7C3AED",
       8: "#9333EA", 9: "#374151", 10: "#EAB308", 11: "#78716C", 12: "#0E7490", 13: "#0F766E", 14: "#E5E7EB",
       15: "#14B8A6", 16: "#94A3B8", 17: "#2563EB", 18: "#1E40AF", 19: "#111827", 22: "#D6CFC0"}
NAMES = {1: "Capstan side frames", 2: "Cross tubes", 3: "Drum", 4: "Spur gear", 5: "Crank shaft and pinion",
         6: "Flange bearings", 7: "Ratchet and pawl", 8: "Brake band and lever", 9: "Crank handles",
         10: "Gear guard", 11: "Anchors and chains", 12: "Bund roller", 13: "Rake beam", 14: "Rake blade",
         15: "Skids", 16: "End caps", 17: "Bridles", 18: "Pull ropes", 19: "Bolts", 22: "Ballast bags"}


def group(items):
    """Fuse the shapes of each BOM line into one Part."""
    by = {}
    for comp, shape in items:
        by.setdefault(comp.bom, []).append(shape)
    out = []
    for bom, shapes in sorted(by.items()):
        s = shapes[0]
        for t in shapes[1:]:
            s = s + t
        out.append(Part(NAMES[bom], s, COL[bom], bom))
    return out


# ------------------------------------------------------------------ hero layout: near set coloured, far set grey
L = layout(P)
near = [(c, s) for k, (c, s) in L.items() if not k.startswith("far_") and k != "ropes"]
parts = group(near)
parts.append(Part(NAMES[18], L["ropes"][1], COL[18], 18))
far = [s for k, (c, s) in L.items() if k.startswith("far_")]
far_shape = far[0]
for s in far[1:]:
    far_shape = far_shape + s
bund_n, bund_f, ground = context(P, length=5000.0)
ppl = human_figure(1750.0, x=-760.0, y=D["drum_y"], z=0.0).shape + human_figure(1750.0, x=760.0, y=D["drum_y"], z=0.0).shape
ctx = [Part("bunds and ground", bund_n + bund_f + ground, "#C9BFA8"), Part("far-side capstan and roller", far_shape, "#BFC5CC"),
       Part("two 1.75 m people at the cranks", ppl, "#9CA3AF")]

md = ROOT / "media"
md.mkdir(exist_ok=True)

flow = {"title": "work in one 30 m pass with a full heap, kJ (SDG-CAL-001 estimates)", "unit": "kJ"}
pass_m = P["pan_design"] / 1000
w_rope = R["A8"] * pass_m / 1000
w_crank = w_rope / (0.96 * 0.98)
w_rake = (R["A7"]) * pass_m / 1000
w_salt = (R["A3"] + R["A4"]) * pass_m / 1000
flow["stages"] = [("Two people cranking", round(w_crank, 1)), ("Rope leaving the drum", round(w_rope, 1)),
                  ("Pull at the rake", round(w_rake, 1)), ("Sliding and lifting salt", round(w_salt, 1))]
flow["losses"] = [(0, "Gears and bearings", round(w_crank - w_rope, 1)),
                  (1, "Roller and far-side hold-back", round(w_rope - w_rake, 1)),
                  (2, "Skid friction", round(w_rake - w_salt, 1))]

render_all(
    parts, project="SaltDrag", title="Hand capstans and rake for salt pans", dwg_no="SDG-DWG-010",
    key_figures=[f"Rake 3.0 m, blade 300 mm; full heap about {R['A2']:.0f} kg (estimate)",
                 f"Design drag {R['A7'] / 1000:.2f} kN; rope pull {R['A8'] / 1000:.1f} kN at the drum",
                 f"Gear 6:1, crank 330 mm: {R['B3']:.0f} N per handle, two people",
                 f"About {R['D9']:.0f} kg per worker-hour (estimate); nobody in the pan",
                 f"Heaviest part {R['E1']:.0f} kg; set about USD {R['E2']:,.0f} (target USD 4,000)"],
    cut=False, scale_figure=False, web_model=False, context=ctx, flow=flow,
)

# ------------------------------------------------------------------ exploded: one capstan, a roller and the rake
cap = capstan_components(P)
ex_cap = {"frame_r": (260, 0, 0), "frame_l": (-260, 0, 0), "xtube_front": (0, -380, -120), "xtube_rear": (0, 380, -120),
          "xtube_top": (0, 0, 380), "drum": (0, -520, 0), "bearings": (0, 0, 0), "gear": (560, -300, 0),
          "pinion": (0, -300, 520), "ratchet": (-520, -300, 0), "pawl": (-640, 0, 260), "brake": (-420, 300, -260),
          "cranks": (0, 0, 760), "guard": (760, 0, 0), "anchors": (0, 0, 0)}
ex = []
for k, c in cap.items():
    if k == "anchors":
        continue
    sh = c.shape
    if k == "bearings":
        sh = sh
    ex.append(Part(NAMES[c.bom], sh, COL[c.bom], c.bom, ex_cap[k]))
rk = rake_components(P)
shift = Pos(-300, -2300, 0)
ex_rk = {"beam": (0, 0, 0), "blade": (0, -550, 0), "skids": (0, 350, -300), "hangers": (0, 350, -140),
         "caps": (0, 0, 0), "rake_bolts": (0, 0, 0), "bridles": (0, 0, 0), "ballast": (0, 0, 380)}
for k, c in rk.items():
    if k in ("rake_bolts", "bridles"):
        continue
    ex.append(Part(NAMES[c.bom], shift * c.shape, COL[c.bom], c.bom, ex_rk[k]))
ro = roller_components(P)
rshift = Pos(1500, 700, 0)
roll = ro["saddle"].shape + ro["roller"].shape + ro["axle"].shape
ex.append(Part(NAMES[12], rshift * roll, COL[12], 12, (0, 0, 0)))
_render(ex, md / "exploded.png", offsets=True, labels=True, title="SaltDrag: exploded view",
        note="One capstan (two are built), the rake (front) and a bund roller (right), pulled apart; seen from the front right "
             "and above, 24 deg elevation; numbers match bom/bom.csv", size=(10, 7.5))

# ------------------------------------------------------------------ cutaway: one capstan, left half removed
rope_on = xcyl(D["barrel_x"][0], D["barrel_x"][1], 0, P["drum_z"], D["layers"][2][1] + P["rope_d"] / 2) - \
    xcyl(D["barrel_x"][0] - 1, D["barrel_x"][1] + 1, 0, P["drum_z"], P["barrel"][0] / 2)
cps = [Part(NAMES[c.bom], Rot(0, 0, 90) * c.shape, COL[c.bom], c.bom) for k, c in cap.items() if k != "anchors"]
cps.append(Part("Rope on the drum, three layers", Rot(0, 0, 90) * rope_on, COL[18], 18))
_render(cutaway_parts(cps, keep="+Y"), md / "cutaway.png", azim=-90, elev=18, title="SaltDrag: capstan cutaway",
        note="Capstan turned so the drum axis runs away from the viewer; the near half (ratchet and brake side) removed; "
             "seen from the front and above, 18 deg elevation; rope shown three layers deep")
# glTF last, with a coarse mesh (a few MB), from deep copies of the shapes
kids = []
for p in parts + ctx:
    sh = copy.deepcopy(p.shape)
    sh.color = Color(*mc.to_rgb(p.color))
    sh.label = p.name
    kids.append(sh)
export_gltf(Compound(kids), str(md / "model.glb"), binary=True, linear_deflection=1.0, angular_deflection=0.35)
(md / "viewer.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SaltDrag: hand capstans and rake</title>
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3/dist/model-viewer.min.js"></script>
<style>body{margin:0;font-family:system-ui,sans-serif;background:#F9FAFB}model-viewer{width:100vw;height:100vh}
.tag{position:fixed;left:12px;top:10px;font-size:12px;color:#B45309;letter-spacing:.06em}</style></head>
<body><div class="tag">CONCEPT, NOT FOR FABRICATION</div>
<model-viewer src="model.glb" poster="hero.png" alt="SaltDrag: hand capstans and rake on a salt pan shortened to 7 m" camera-controls auto-rotate shadow-intensity="0.6"
  exposure="1.0" camera-orbit="-35deg 70deg auto" interaction-prompt="auto"></model-viewer></body></html>
""")

import shutil  # noqa: E402
for d_ in ("_views", "_views_fig"):
    shutil.rmtree(md / d_, ignore_errors=True)
print("concept media written")
