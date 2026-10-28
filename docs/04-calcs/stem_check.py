"""SaltDrag STEM check calculations (SDG-STM-001, STANDARDS section 20).

Run from the repo root (after docs/04-calcs/sizing.py):  python docs/04-calcs/stem_check.py
Reads the calculation results of SDG-CAL-001 (docs/04-calcs/results.csv, written by sizing.py from the model) and
writes docs/04-calcs/stem_results.csv, which the STM document tabulates. It also prints the first-order numbers
of concept options B and C (SDG-OPT-001), which have no calculation note of their own. Each row is a first-order
screen of one claim; the sizing itself is in SDG-CAL-001.

Rows S7, S9, S11, S15, S17, S22, S24, S26 and S29 record checks that failed on the kit 1.7 design (four found by the
first check, five more by the independent review) and were fixed under Amish's standing instruction of 2026-10-23
(SDG-DEC-001 D17 to D24); the values printed here are on the fixed design, and the failing values are kept in
FAILED_BEFORE_FIX for the record. Rows that rest on the assumed drag of S1 say so in their claim.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from stem_check import Check, G, WITHIN, PLAUSIBLE, limits  # noqa: E402

R = {r["label"]: float(r["value"]) for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open())}
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
CAL = "SDG-CAL-001"

FAILED_BEFORE_FIX = {
    "S7": "168.3 x 4.5 mm pipe barrel: 1.8 x 6 kN / (4.5 mm x 12 mm) = 200 MPa against 105 MPa (half of 210 MPa pipe yield)",
    "S15": "84 W per cranker at 30 turns a minute, against 75 W sustained (77 W at 25 turns on the third layer, review)",
    "S9": "92 N with a dry lining (friction 0.30) on a 450 mm lever; 179 N with a wet lining (0.20), over 150 N",
    "S11": "8 mm chain, WLL 7.8 kN: margin 1.71 when one chain takes 70 % of a 6 kN pull",
    "S17": "25 mm C45+N crank shaft: 1.89 on yield (305 MPa above 16 mm) and a fatigue factor below 1.5",
    "S22": "12 x 8 keys in a 30 mm gear face and a 20 mm ratchet: bearing stress 303 and 455 MPa at 6 kN",
    "S29": "bridles at mid-height (130 mm): pitching moment twice the restoring moment, blade tips onto the floor",
    "S24": "assumption that several families share one set across a harvest: one set gathers about 37 % of one pan",
    "S26": "cross-tube washers 2 mm from the tube wall, guard spacer holes 2.5 mm from the cheek edge, axle split-pin holes inside the saddle plates",
}

# ------------------------------------------------------------------ Physics: mechanics and statics
c.cited("S1", f"A 3 m rake with a full heap of about {R['A2']:.0f} kg needs about {R['A7'] / 1000:.2f} kN to drag (0.9 kN per metre)",
        "Physics", "Mechanics and statics",
        "Coulomb sliding of the heap (friction 0.70, tan of the 35 degree repose angle) plus an assumed 300 N/m to loosen the "
        "harvest layer and skid friction 0.30; granular drag in front of a blade (soil-tool mechanics)",
        f"heap {R['A3']:.0f} N + layer {R['A4']:.0f} N + skids {R['A6']:.0f} N = {R['A7']:.0f} N; the layer term is an "
        "estimate, not a measurement", PLAUSIBLE, f"Open: {CAL} [A7] rests on the assumed 300 N/m; measured on the partner's bed (SDG-DEC-001, to confirm 7)")
c.claim("S2", f"At the design drag of S1, two people at {R['B3']:.0f} N each on 330 mm cranks wind the rake", "Physics", "Mechanics and statics",
        f"Torque balance through a 6 to 1 spur stage, 94 % gear and bearing efficiency, rope on its third layer; if the drag is "
        f"1.5 times the estimate the pull rises {R['A10']:.2f} times and the skids are raised or the rake shortened ({CAL} [A10])",
        round(R["B3"], 1), 120.0, "N", closed_by=f"{CAL} [B3]; PR-002")
c.claim("S3", "Two people at 120 N give at least 3 kN of rope pull, even on a full drum", "Physics", "Mechanics and statics",
        "Torque balance as S2 on the fourth layer (largest radius)", round(R["B5"] / 1000, 2), 3.0, "kN", rule="above",
        closed_by=f"{CAL} [B5]; PR-003")
c.claim("S13", "The anchored capstan does not tip, even at twice the rated pull", "Physics", "Mechanics and statics",
        f"Moments about the front tips of the runners: rope at 677 mm against weight, chain tension and chain line, both chains taut "
        f"(rated pull {R['C12']:.2f}); a slack chain is a hazard controlled by the turnbuckles and the set-up check (SDG-RSK-001 F11)",
        round(R["C12b"], 2), 1.0, "resisting / tipping", rule="above", closed_by=f"{CAL} [C12], [C12b]")
c.claim("S17", "The crank shaft survives a season of rotating bending at the rated pull", "Physics", "Strength of materials",
        "Goodman, fully reversed bending from the tooth force and steady torque at the 25 mm step (notch factor 1.6), C45+QT "
        "(UTS 650 MPa), surface and size factors, endurance halved for bare steel in salt air (corrosion fatigue, estimate)",
        round(R["C16"], 2), 1.5, "safety factor", rule="above", closed_by=f"SDG-DEC-001 D24; {CAL} [C16], [C16b]")
c.claim("S22", "The gear and ratchet keys carry the drum torque at 6 kN with a margin of 2", "Physics", "Strength of materials",
        "Key bearing stress 2 T / (d (h/2) L), 12 x 8 keys on the 40 mm shaft: gear hub 44 mm (C45+QT, 430 MPa), ratchet with its "
        "welded hub 64 mm (C45+N, 305 MPa)",
        round(min(R["C17"], R["C18"]), 2), 2.0, "margin", rule="above", closed_by=f"SDG-DEC-001 D24; {CAL} [C17], [C18]")
c.claim("S28", "The induction-hardened pinion teeth resist pitting at the rated pull", "Physics", "Strength of materials",
        "Hertz contact sigma_H = Z_E Z_H sqrt(K_A F_t (u + 1) / (b d u)), K_A 1.25 for hand cranking; allowable about 1,000 MPa for "
        "induction-hardened C45 teeth (estimate)",
        round(R["C3d"], 2), 1.2, "margin", rule="above", closed_by=f"SDG-DEC-001 D24; {CAL} [C3c], [C3d]")
c.claim("S29", "The rake does not pitch onto its blade edge under the full heap", "Physics", "Mechanics and statics",
        "Moments about the skid tips: the pull at the bridle height (70 mm) against the heap at a third of the blade height, the "
        "layer at the edge and skid friction at the floor; restoring moment of the rake's weight about the skid tips",
        round(R["D13"], 2), 1.5, "restoring / pitching", rule="above", closed_by=f"SDG-DEC-001 D23; {CAL} [D13]")
c.order_of_magnitude("S30", "With two 24 kg ballast bags the blade stays down until about 3.5 m from the bund toe", "Physics",
                     "Mechanics and statics", claimed=3.5, estimate=R["D4"], unit="m",
                     law="Vertical equilibrium of the rake under the rising rope: lift-off when T sin(theta) exceeds the rake's weight",
                     closed_by=f"{CAL} [D4]")
person = 70.0 * G / (2 * 0.025) / 1000          # a 70 kg worker standing on two feet of about 250 cm2 each
c.claim("S31", "The skids press on the pan floor less than a worker standing on it does", "Physics", "Mechanics and statics",
        f"Contact pressure = weight / skid area; the pull's pitching moment is small with the bridles at the skid foot (S29), so the "
        f"pressure stays near the static value; a 70 kg person on two feet (about 0.025 m2 each) presses {person:.1f} kPa",
        round(R["D1"], 1), round(person, 1), "kPa", closed_by=f"{CAL} [D1]; PR-004")

# ------------------------------------------------------------------ Physics: strength of materials (R3: 2 to 1 at 6 kN)
for sid, lab, what, yld, law in (
        ("S4", "C1", "40 mm drum shaft", 430.0, "Bending (rope load and the gear's reaction, both planes) plus torsion, von Mises; C45+QT yield 430 MPa, 16 to 40 mm (EN 10083-2)"),
        ("S5", "C2", "crank shaft at the bearing next to the overhung pinion", 430.0, "Bending from the full tooth force plus torsion, von Mises, 30 mm; C45+QT yield 430 MPa"),
        ("S6", "C3", "module 4 pinion teeth", 305.0, "Lewis bending, form factor 0.277 for 14 teeth; C45+N yield 305 MPa above 16 mm"),
        ("S8", "C5", "pawl boss welded to the cheek", 275.0, "Cantilever bending of the 40 mm boss; S275 yield 275 MPa (EN 10025-2)"),
        ("S14", "C13", "3 m FRP rake beam", 200.0, "Simply supported beam under the heap and layer load; pultruded FRP flexural strength 200 MPa (lower bound)")):
    c.claim(sid, f"The {what} keeps a margin of 2 at twice the rated pull (6 kN)", "Physics", "Strength of materials",
            law, round(R[lab], 1), yld / 2, "MPa", closed_by=f"{CAL} [{lab}]; PR-003")
c.cited("S7", "The drum barrel is not crushed by three layers of rope wound on at 6 kN, with a margin of 2", "Physics", "Strength of materials",
        "Hoop stress of a ring under rope pressure, sigma = k T / (t s); 168.3 x 6.3 YSt 310 tube, yield 310 MPa (IS 4923); the multi-layer "
        "factor k = 1.8 for three loaded layers is taken from wire-rope practice and is not sourced for polyester (independent review); the "
        "margin of 2 holds for k up to 1.95; flange thrust not yet checked",
        f"{R['C15']:.0f} MPa against 155 MPa at k = 1.8 (margin {R['C15b']:.2f}); the 4.5 mm pipe it replaces failed at about 200 MPa",
        PLAUSIBLE, f"Open: sourced layer factor and a CalRig proof load with three layers wound on (TRL 4); SDG-DEC-001 D18")
c.claim("S9", "A hand force of 150 N or less on the band brake holds the rated pull, with the lining wet", "Physics", "Mechanics and statics",
        "Band brake (capstan) equation T1/T2 = exp(mu theta), mu 0.20 for a woven lining wet with brine (0.30 dry), 247 degrees of wrap, "
        "differential lever 600 mm with a 50 mm inner arm",
        round(R["C7"], 1), 150.0, "N", closed_by=f"{CAL} [C7]; PR-011")
c.claim("S11", "The more loaded anchor chain keeps a margin of 2 on its working load limit at 6 kN", "Engineering and technology", "Standards practice",
        "Chain tension from the 23 degree chain line with 70 % of the pull on one chain (unequal tension, independent review); 10 mm "
        "grade 30 chain working load limit 11.8 kN (2,650 lb, catalogue class, to confirm on purchase)",
        round(R["C9b"], 2), 2.0, "WLL / tension", rule="above", closed_by=f"{CAL} [C9b]; PR-003")
c.cited("S12", "Each 150 mm helical anchor holds at least 1.5 times its share of the rated pull in the ground behind the bund",
        "Physics", "Mechanics and statics",
        "Deep helix bearing Q = 9 s_u A in firm clay, s_u 50 kPa assumed; the rod is screwed in at 45 degrees and the chain arrives at 23 "
        "degrees, so the load is 22 degrees off the anchor's axis; at a helix depth of about 0.6 m the bearing factor may be below 9, "
        "and saline silty soil can be softer",
        f"{R['C10'] / 1000:.2f} kN estimated against a proof pull of {R['C10c'] / 1000:.2f} kN (1.5 times a 70 % share); {R['C10b']:.2f} times "
        "the 6 kN chain force at a 70 % share; soil unknown",
        PLAUSIBLE, f"Open: {CAL} [C10]; site pull test before first use (SDG-DEC-001, to confirm 6)")

# ------------------------------------------------------------------ Engineering: rope practice, tolerances
c.claim("S10", "The rope's minimum breaking strength after splices is at least 5 times the rated pull", "Engineering and technology", "Standards practice",
        "Working-load factor of 5 to 12 for fibre rope in general use (rope makers' practice); 12 mm polyester double braid 27 kN class, splices 85 %",
        round(R["C8"], 2), 5.0, "MBS / rated pull", rule="above", closed_by=f"{CAL} [C8]; PR-010")
c.cited("S27", "The rope lasts a season over the 100 mm roller and the 168 mm drum and dragging on the bed",
        "Engineering and technology", "Standards practice",
        "Rope makers give a minimum sheave-to-rope diameter ratio of about 8 for polyester double braid (to confirm on the chosen rope's "
        "datasheet); a bend at D/d 8.3 costs about 15 % of strength (the working-load factor falls from 7.7 to about 6.5, still over 5); "
        "salt crystals abrade the rope where it lies on the bed on the light return",
        "roller 8.3, drum 14.0 against about 8; abrasion life unknown", PLAUSIBLE, "Open: rope datasheet on purchase (SDG-DEC-001, to confirm 10); daily inspection (SDG-RSK-001 F1)")
c.cited("S26", "Every bolted joint can be assembled: washers and nuts clear their neighbours, holes keep at least 1.2 diameters of edge",
        "Engineering and technology", "Manufacturing tolerances",
        "Edge distance e >= 1.2 d0 (EN 1993-1-8 practice); interference check of every part at detail level D3 (.kit/cad_check.py)",
        "cross-tube bolts at 36 mm on 100 x 80 plates (14 mm edge, 1.27 d0), guard spacer holes 73 mm from the cheek edge, axle "
        "split pins outside the plates, gear and ratchet hubs clear of the bearings, guard and crank; cad/fidelity.json: no interference",
        WITHIN, "SDG-DEC-001 D19, D24; cad/fidelity.json")

# ------------------------------------------------------------------ Biology: ergonomics and physiology
c.claim("S15", "At the design drag, each of two crankers works within a sustained rate, even at the end of a pass", "Biology", "Ergonomics",
        f"Rope power over efficiency, shared by two, with the rope on its third layer at 23 turns a minute (mean over a pass "
        f"{R['B7']:.0f} W; pull duty about 45 %); sustained hand-cranking by an average adult about 75 W (.kit/stem_check.py limit)",
        round(R["B7b"], 1), limits.HUMAN_SUSTAINED_W, "W", closed_by=f"SDG-DEC-001 D17; {CAL} [B7b]; PR-018")
c.cited("S16", "Winding at about 70 W is safe in the harvest heat with work planned for the cooler hours",
        "Biology", "Human physiology and biomechanics",
        "Arm cranking is about 15 % efficient, so 64 to 71 W of external work is a metabolic rate of about 450 to 500 W, high work; "
        "ISO 7243 sets a reference WBGT of about 26 C for acclimatised workers at high work (to confirm against the 2017 edition); "
        "afternoon WBGT in the Little Rann in March and April is likely to exceed it, so 6 working hours a day (S24) may be optimistic",
        "safe in the early morning and evening only; a work and rest schedule is needed", PLAUSIBLE,
        "Open: work hours, shade and water agreed with the partner (PRB co-design checklist; RSK H6)")

# ------------------------------------------------------------------ Chemistry: corrosion and materials
c.cited("S18", "Hot-dip galvanised steel on the dry ground lasts more than one season in salt-laden air with a daily rinse",
        "Chemistry", "Electrochemistry and batteries",
        "Zinc corrosion rate about 4.2 to 8.4 um a year in a very high (C5) atmosphere and up to about 25 um a year in an extreme (CX) one "
        "(ISO 9223); minimum mean hot-dip coating 85 um on steel over 6 mm and 55 um on 1.5 to 3 mm (ISO 1461); cut edges and drilled "
        "holes are galvanised after fabrication",
        "at 25 um a year (brine-wetted, CX): 3.4 years on the 6 mm plate, 2.2 years on the 3 mm runners and tubes; more than one season", WITHIN, "BOM 1 to 3, 10 to 12; PR-007")
c.cited("S19", "316 stainless fittings on the rake survive a season wetted by near-saturated brine",
        "Chemistry", "Electrochemistry and batteries",
        "Type 316 suffers pitting and crevice corrosion in warm chloride brines, worst in crevices under bolt heads and washers "
        "(Nickel Institute guidance on stainless steel in seawater); daily freshwater rinse lowers the risk",
        "no calculation possible; crevice corrosion of the blade and hanger bolts is the likely failure", PLAUSIBLE,
        "Open: season trial with inspection (PR-007, TRL 5); duplex 2205 bolts as the fallback (RSK F9)")
c.cited("S20", "UHMW-PE, pultruded FRP and polyester rope keep their strength in brine and sun for a season",
        "Chemistry", "Materials and polymer chemistry",
        "Polyolefins and glass-polyester or vinylester composites are inert to sodium chloride; UV degrades unstabilised "
        "UHMW-PE and bare FRP surfaces, so the BOM asks for UV-stabilised UHMW-PE and a surfacing veil on the FRP",
        "chemically inert; UV handled by grade choice", WITHIN, "BOM 13, 14, 15, 18; PR-007")
c.cited("S21", "No metal coating, paint, grease or FRP touches the salt", "Chemistry", "Environmental and atmospheric chemistry",
        "The salt touches only the UHMW-PE blade and skids (food-contact grades exist), 316 stainless and the polyester rope; no zinc, "
        "paint, grease or FRP is in the pan below the blade top; the rope may shed fibres where it drags on the bed (to watch in trials)",
        "material list by inspection of the model", WITHIN, "cad/src/model.py option A; BOM 14 to 16")

# ------------------------------------------------------------------ Mathematics
c.order_of_magnitude("S23", f"At the design drag, one set gathers about {R['D8']:.0f} kg of salt an hour with a crew of four",
                     "Mathematics", "Orders of magnitude", claimed=R["D8"], estimate=R["A2"] / (R["D5"] + R["D6"] + 8.0) * 60,
                     unit="kg/h", law="One full heap per strip over pull, return and move times", closed_by=f"{CAL} [D8], [D9]")
c.order_of_magnitude("S24", f"One set gathers about {R['D11']:.0f} t in a 61-day harvest, about a third of one family pan's yearly output (6 cooler hours a day; about 130 t at 4 h)",
                     "Mathematics", "Orders of magnitude", claimed=R["D11"], estimate=0.55 * 61 * 6,
                     unit="t", law="Rate x 61 days x 6 cooler hours; a family pan yields 500 to 600 t a year (Business Standard, 2009)",
                     closed_by=f"SDG-DEC-001 D20; {CAL} [D11], [D12]")
c.claim("S25", "Each drum stores the 45 m of rope a 30 m pan needs", "Mathematics", "Units and dimensional analysis",
        "Turns per layer x layer circumference, four layers of 12 mm rope on a 168.3 mm barrel", round(R["B8"], 1), 45.0, "m",
        rule="above", closed_by=f"{CAL} [B8]; PR-012")

# ------------------------------------------------------------------ Concept options B and C (first-order, SDG-OPT-001)
heap_b = R["A1"] / 2 * 1200.0                         # half-width rake: half the heap
drag_b = 0.70 * heap_b * G + 300.0 * 1.5 + 0.30 * 60.6 * G   # 60.6 kg: half rake (model) and two 17 kg bags
pull_b = drag_b / 0.98 / 0.95 + 200.0                # bund roller and turning sheave, back tension
haul_n = 130.0                                        # sustained pull per hauler, N (order of Snook and Ciriello, 1991)
crew_b = math.ceil(pull_b / haul_n)
c.cited("B1", f"A team of {crew_b} walking haulers draws a 1.5 m rake at {pull_b / 1000:.2f} kN (option B)", "Biology", "Ergonomics",
        "Sustained walking pull of about 130 N per person, the order of the maximum acceptable sustained pull forces for most adult "
        "women (Snook and Ciriello, 1991); rope pull from the drag model of S1 at half width",
        f"{crew_b} x {haul_n:.0f} N >= {pull_b:.0f} N; possible, but the crew is large", PLAUSIBLE, "Option not carried forward")
c.cited("B2", "A post on four 25 mm stakes holds the 90 degree rope turn (option B)", "Physics", "Mechanics and statics",
        "Resultant of the turned rope, 1.41 times the pull, at 0.76 m height; lateral capacity of short stakes in clay",
        f"{1.41 * pull_b / 1000:.2f} kN at 0.76 m; stake capacity depends on the soil", PLAUSIBLE, "Option not carried forward")
arm, handle, eta_c = 81.0, 1052.0, 0.85
f_lever = R["A8"] * arm / handle / eta_c
c.claim("C1", "Two people at about 140 N on a 10 to 1 hand lever pull the 3 m rake (option C)", "Physics", "Mechanics and statics",
        f"Lever ratio {handle:.0f} / {arm:.0f} mm, 85 % efficiency at pins and jaws, the rope pull of {CAL} [A8]",
        round(f_lever / 2, 1), 150.0, "N per person", closed_by="Option not carried forward")
c.cited("C2", "Cam jaws grip polyester rope without wearing it out within a season (option C)", "Engineering and technology", "Standards practice",
        "Toothed cam grips cut and glaze fibre rope under repeated slip; commercial fibre-rope pullers use smooth or grooved jaws "
        "and limit the load", "rope wear under 600 strokes a pass is unknown", PLAUSIBLE, "Option not carried forward")

for row in c.rows:          # a row that needs field data stays open: its closure plan goes in the check text
    if row["closed_by"].startswith("Open"):
        row["check"] += f" ({row['closed_by'][6:]})"
        row["closed_by"] = ""
state = c.write()

# first-order numbers for SDG-OPT-001 Table 1
strip_b = 30.0 / 0.5 / 60 + 1.5 + 10.0
rate_b = heap_b / strip_b * 60
stroke = arm * math.radians(40.0) - 5.0               # rope advance per lever stroke, mm
t_c = 30000.0 / stroke / 20.0                         # min per pass at 20 strokes a minute
strip_c = t_c + t_c / 2 + 8.0
rate_c = R["A2"] / strip_c * 60
print(f"option B: heap {heap_b:.0f} kg, drag {drag_b:.0f} N, rope pull {pull_b:.0f} N, haulers {crew_b}, strip {strip_b:.1f} min, "
      f"{rate_b:.0f} kg/h, {rate_b / (crew_b + 2):.0f} kg per worker-hour (crew {crew_b + 2})")
print(f"option C: lever force {f_lever:.0f} N ({f_lever / 2:.0f} N each of two), stroke {stroke:.0f} mm, pass {t_c:.1f} min, strip {strip_c:.1f} min, "
      f"{rate_c:.0f} kg/h, {rate_c / 4:.0f} kg per worker-hour (crew 4), "
      f"{R['A8'] * 30 / eta_c / (t_c * 60) / 2:.0f} W each")
print(f"option A: {R['D8']:.0f} kg/h, {R['D9']:.0f} kg per worker-hour (crew 4), {R['B7']:.0f} W each")


def _table(rows):
    head = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    cell = lambda t: str(t).replace("|", "/")  # noqa: E731
    return "\n".join(head + [f"| {r['id']} | {cell(r['claim'])} | {r['field']} | {r['branch']} | {cell(r['law'])} | "
                             f"{cell(r['check'])} | {r['verdict']} | {cell(r['closed_by']) or 'Open'} |" for r in rows])


def fill_document(path=ROOT / "docs/01b-stem-check.md"):
    """Write the claims tables into the STM document between its marker comments."""
    text = path.read_text(encoding="utf-8")
    order = lambda r: (int(r["id"][1:]) if r["id"][1:].isdigit() else 0)  # noqa: E731
    a_rows = sorted([r for r in c.rows if r["id"].startswith("S")], key=order)
    o_rows = [r for r in c.rows if r["id"][0] in "BC"]
    for tag, rows in (("STM_TABLE", a_rows), ("OPT_TABLE", o_rows)):
        i0, i1 = text.index(f"<!-- {tag} -->"), text.index(f"<!-- /{tag} -->")
        text = text[:i0] + f"<!-- {tag} -->\n" + _table(rows) + "\n" + text[i1:]
    path.write_text(text, encoding="utf-8")


if (ROOT / "docs/01b-stem-check.md").exists():
    fill_document()
