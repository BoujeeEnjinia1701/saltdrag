# Review note: SaltDrag

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (SDG-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (SDG-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (SDG-REQ-001 v0.1): 9 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

### Next

- Run `/populate` to bring the repo to a strong TRL 2 with concept media.

## Session 2026-10-03: TRL 2 (/populate, kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md` from `.kit/CLAUDE.md`). Run under Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Every recommendation is therefore recorded as decided, not proposed.

### What was done

- `docs/01-problem.md` (SDG-PRB-001 v0.2): site assumptions stated (30 m design pan, 0.4 m crest, dry ground behind the bunds), co-design checklist, safety section, open questions answered where the work settles them.
- `docs/03-requirements.md` (SDG-REQ-001 v0.2): every target measurable; R10 (rope safety), R11 (holding) and R12 (rope capacity) added.
- `docs/02-concept.md` (SDG-PRC-001 v0.2): how it works, components, key design choices, first-order numbers, safety, concept media.
- `docs/decisions/0001-trl2-review-decisions.md` (SDG-DDR-001): TRL 2 review decisions D1 to D17.
- Concept media from `cad/src/concept_media.py`: `media/hero.png`, `media/concept-blueprint.png`, `.pdf` and `.svg` (SDG-DWG-010), `media/model.glb` (about 4 MB) and `media/viewer.html`, `media/exploded.png`, `media/cutaway.png`, `media/flow.png` (work per pass, estimates).
- `bom/bom.csv`: every line priced.

### Results

- A geared drum winch (6 to 1, two 330 mm cranks) on dry ground behind the bund, a roller on the crest, and a 3 m FRP and UHMW-PE rake set to 10 mm above the floor.
- The rake width follows from the drag estimate: a full 230 kg heap gives a design rope pull of 3.0 kN, the rated pull.

### Requirements not met

- R5 (gathering rate at least the dantala's) cannot be shown: there is no baseline yet.

### Decisions made under the pre-approval

SDG-DDR-001, D1 to D17: drum winch, capstan behind the bund with a crest roller, single spur stage, polyester rope, one-piece FRP rake, adjustable skids, helical anchors chained at rope height, materials for brine, conservative safety rules (pawl always on, pay out on the brake with cranks removed, dampers and a 2 m exclusion zone, anchors proof-loaded on site), 30 m design pan, crew of four, SEWA as the first co-design partner to approach and the Little Rann as the first trial region (candidates, not agreed), written clarification on the machine-use condition, and the capstan as the first candidate for the block shared with SiltHaul.

### Safety concerns

Rope snap-back, cranks and gears, anchor pull-out and heat. See SDG-PRC-001, Safety.

## Session 2026-10-03: TRL 3 (/advance-trl3 and /build-plan)

### What was done

- `docs/04-calcs/01-sizing.md` (SDG-CAL-001 v0.2) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: drag, capstan, strength at 6 kN, floor, lift-off near the bund, rate, set-up, mass and cost, with a results table against every requirement.
- `cad/src/model.py`: parametric build123d model of the capstan, rake, roller and layout, with 63 constructability checks (`--check`: 63 of 63 pass). STEP and STL in `cad/step/` and `cad/stl/` (capstan, rake, roller; assembly STEP of the layout).
- `cad/src/sheets.py`: general arrangement SDG-DWG-001 Rev P2 (Rev P1 superseded the same day by the design for construction).
- `cad/src/build_plan_media.py`: overview, 13 making sketches (SDG-DWG-101 to 113), 11 joint close-ups and 18 step pictures.
- `docs/05-build-plan.md` (SDG-BLD-001 v0.1), `docs/06-design-decisions.md` (SDG-DEC-001 v0.1), `docs/decisions/0002-design-for-construction.md` (SDG-DDR-002).
- `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded and detail) and render scenes exported to `/home/claude/renders/saltdrag` for the photoreal renders on Amish's Mac.
- `docs/02-concept.md` v0.3, `docs/03-requirements.md` v0.3, `README.md` (TRL 3, hero render, links, Building the prototype), `project.yaml` (trl 3, trl_target 3, design_state constructable, trl_evidence). `budget_usd` unchanged.

### Results (estimates, SDG-CAL-001)

- Crank force 89 N per handle at the design drag (R2: 120 N); two people at 120 N pull 4.0 kN (3.7 kN on a full drum) against 3 kN asked (R3).
- Lowest strength margin at 6 kN: crank shaft 2.1 on yield; rope working-load factor 7.7; anchors 2.4 on their chain force (soil assumed).
- A 30 m pass takes 9.5 min; one strip 23 min; about 600 kg/h, 150 kg per worker-hour for a crew of four.
- Capstan 102 kg assembled; heaviest single part 23.8 kg (a ballast bag filled on site), drum 21.3 kg.
- Value-engineering target: USD 4,000. Estimated cost of the constructable design: USD 2,803 (USD 1,197 under the target).

### Requirements not met

- R5 is not verified: no dantala baseline. The estimate of 150 kg per worker-hour may be below the dantala rate; if it is, the cycle (8 min moving per 3 m strip) is the first place to look.
- R8 is met with a small margin (19 min against 20).

### Decisions made under the pre-approval

- SDG-DDR-002, changes 1 to 17 (below), and the value-engineering wording of the cost.
- Open decisions in SDG-DEC-001: none. Eight facts to confirm when parts are bought or at the trial pan are listed there (rope certificate, gears, bearings, rigging ratings, FRP strength, anchor holding, measured drag, bund and ground survey).

### Design changes made for construction (SDG-DDR-002)

1. Capstan frame of two bolted side frames (cheek on runner) and three cross tubes.
2. Capstan on dry ground behind the bund; bund roller saddle on the crest (new BOM 12).
3. Welded drum with brake rim; rope over the top.
4. Flange bearings on the cheeks (new line 6b for the 25 mm size).
5. Bought webbed gear and pinion, keyed.
6. Pawl on a 40 mm welded boss (a plain pin would bend at 6 kN).
7. Differential band brake through the left cheek.
8. Removable crank handles with cross pins.
9. Gear guard.
10. Anchor ears at rope height, shackles, chains and turnbuckles (new line 11b).
11. One-piece 3 m FRP beam.
12. Blade bolts with crush sleeves.
13. Skids on slotted stainless hangers.
14. End caps with eye plates for the bridles.
15. Ballast bags (new line 22): without them the rope lifts the blade 5.9 m from the bund toe; with them, 3.3 m.
16. Windrow board removed: the windrow forms about 3.3 m from the toe.
17. Rope dampers (new line 20); fabrication labour and galvanising priced as line 23.

### Build plan findings

- The near-bund lift-off is the main finding the concept missed; it sets the windrow 3.3 m into the pan, so loading out still uses existing methods.
- Moving both capstans 3 m per strip (8 min) is a third of the cycle; a sliding anchor line along the bund is worth studying at TRL 4.
- The drum and gears must be bought or machined; everything else is town-workshop work.

### Appearance model and render scenes

- `cad/src/product_model.py` takes every part from `model.py`'s layout. Departures from `model.py`: the ground anchors are cut off at ground level (they are buried), the crank is drawn at 100 degrees (`crank_angle`) so the cranking figure's hands meet the upper handle, the rake is drawn 2.5 m from the bund toe with a heap of salt in front of it (context), and the far-side set is not shown. Decided under the pre-approval.
- Scenes exported with `.kit/export_views.py` to `/home/claude/renders/saltdrag` (hero, exploded, detail). `media/render-hero.png` is made on Amish's Mac; until then `render.py --check` warns that it is missing.

### Safety concerns

- Rope snap-back: certified rope, dampers, exclusion zone; safety stops S2, S3 and S5.
- Cranks and gears: guard, pawl always on, cranks off before paying out (S4).
- Anchor pull-out: on-site proof pull of every anchor (S6, S7); soil strength is an assumption.
- Heat in the harvest season: work in cooler hours with shade and water; each cranker works at about 84 W.
- The drag per metre is assumed; it is measured before the first loaded pass (SDG-DEC-001, item 7).

### Recommended next step

The design is ready for TRL 4 on paper. Recommendation: with the co-design partner, measure the drag of a short trial rake and time the dantala on the same pan, then build one capstan and proof-load it with CalRig before building the full set.

### Cross-repo note (not edited)

SiltHaul names the hand capstan as a shared block; SaltDrag's capstan (SDG-DWG-101 to 108) is offered as the first candidate.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.

2026-10-03: hero render reframed so the product fills the frame (saltdrag).

## Session 2026-10-24: kit 1.9.1 upgrade

Upgrade of a TRL 3 repository from kit 1.7 to kit 1.9.1 (`/upgrade-1.8` and `/upgrade-1.9`), with Amish's instructions of 2026-10-24 ("detailed TRL3 CAD", "Detail every option", "Kit 1.9.1 rollout") and his standing instruction of 2026-10-23 (fix rule). The coordinator installed kit 1.9.1 (`.kit/`, `CLAUDE.md`, `.claude/commands/`); nothing in them was edited.

### What was added

- STEM check: `docs/01b-stem-check.md` (SDG-STM-001) and `docs/04-calcs/stem_check.py` (writes `docs/04-calcs/stem_results.csv` and the claims tables), with an independent review.
- Concept options: `docs/02a-concept-options.md` (SDG-OPT-001) and the concept selection record `docs/decisions/0003-concept-selection.md` (SDG-DDR-003).
- Requirements: `docs/03a-user-requirements.md` (SDG-URS-001, 15 URs); `docs/03-requirements.md` migrated from SDG-REQ-001 to SDG-PRS-001 (R1 to R12 become PR-001 to PR-012, PR-013 to PR-018 added); `docs/03b-traceability.md` (SDG-RTM-001) generated by `.kit/trace.py`, 0 gaps.
- Pipeline documents: `docs/07-regulatory.md` (REG), `docs/08-feasibility.md` (FEA), `docs/09-risk.md` (RSK, with hazard analysis and design FMEA), `docs/10-market.md` (MKT), `docs/11-plan.md` (PLN, with the reference list). Web sources checked 2026-10-25.
- PRB v0.3 (users-and-needs and stakeholder tables), PRC v0.4, CAL v0.3, BLD v0.2, DEC v0.2 updated for the fixes below.
- CAD: `cad/src/model.py` rebuilt to the kit 1.9 interface (`PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN = "A"`, `OPTION_VIEWS`, `ALLOWED_CONTACTS`, `components(option)`), every option at D3; repo helpers in `cad/src/sdg_parts.py` (bolt sets on any axis, countersunk bolts, weld beads, ring welds, chain links, shackles, rope runs). The earlier per-component functions are kept, at the same geometry, for `sizing.py`, `sheets.py`, `build_plan_media.py` and `concept_media.py`.
- `cad/fidelity.json` and STEP: 80 per-part files in `cad/step/A/`, `cad/step/A-assembly.step`, `B-assembly.step`, `C-assembly.step`; the legacy `saltdrag-*.step` and STL (0.15 mm tolerance) regenerated.
- `cad/src/product_model.py` rebuilt from `components(CHOSEN)` plus site context; RENDER_VIEWS `hero` (outdoor, sand ground, ground at z = 0, sun at 38 degrees and azimuth -70 for a camera at -40), `studio`, `detail` and `exploded`.
- Drawings SDG-DWG-001 (Rev P3) and SDG-DWG-101 to 113 (Rev P2), build plan pictures and concept media regenerated from the model.
- README in the house structure; the broken Zenodo DOI badge (it held an error message) replaced with the standard badge for the concept DOI in CITATION.cff.

### STEM verdicts and fixes

Option A: 31 rows, 25 within known science, 6 plausible and open for field data or a test (S1 drag per metre, S7 drum barrel rope-pressure factor, S12 anchors in the soil, S16 heat, S19 316 stainless in brine, S27 rope life). `stem_check: open`. Options B and C: within known science, with B1, B2 and C2 open.

Nine details failed and were fixed under the standing instruction (SDG-DEC-001; none changes the working principle, pitch or scope; Amish can reverse any):

| Decision | Row | Fix |
| --- | --- | --- |
| D17 | S15 | Design cranking rate 23 turns a minute (was 30): 71 W at the end of a pass, within 75 W |
| D18 | S7 | Drum barrel 168.3 x 6.3 mm YSt 310 (was 4.5 mm pipe, margin 1.05) |
| D19 | S26 | Cross-tube end plates 100 x 80 with bolts at 36 mm; guard spacers moved off the cheek edge; roller axle 272 mm with split pins; bearing bolts heads inside |
| D20 | S24 | "Several families share one set" withdrawn: one set gathers about 195 t, a third of one pan's yearly output |
| D21 | S9 | Brake lever 600 mm (wet lining needed 179 N on 450 mm) |
| D22 | S11 | 10 mm chain, rated forged turnbuckles, anchor proof pull 3.42 kN (unequal chain tension) |
| D23 | S29 | Bridle eyes at the foot of the end caps, apex 70 mm (the rake would have pitched onto its blade) |
| D24 | S4, S5, S17, S22, S28 | C45+QT shafts; crank shaft stepped 30/25 mm in UCF206 bearings; 44 mm hubs on the gear and ratchet (keys were at or above yield); induction-hardened pinion |

Independent review: run headless with `claude -p` on the STEM check, CAL, PRS and `sizing.py` only. It refuted S2 (and the rows inheriting the assumed drag), S5 and S9 outright and weakened most others; D17 (revised), D21 to D24 and the S7 downgrade came from it. Findings and changes are tabulated in SDG-STM-001.

### Option scores

A geared drum capstans 158, C lever rope puller 154, B bund-walk haul 148: within 10 %, so all three go to Amish without a pick (SDG-OPT-001, SDG-DDR-003). A gathers 133 kg per worker-hour with a crew of 4; B about 35 (crew 16); C about 67 (crew 4). Parts cost: A USD 2,897; B about 1,400; C about 1,800.

### CAD: part counts and mass per option (`cad/fidelity.json`, detail level D3)

| Option | Parts | Made or bought | Fasteners | Welds | Bare share | Mass (kg) | STEP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A Geared drum capstans | 372 | 80 | 249 | 43 | 0 % | 196.9 | 80 per-part files and the assembly |
| B Bund-walk haul | 159 | 49 | 94 | 16 | 0 % | 118.3 | assembly |
| C Lever rope puller | 204 | 56 | 138 | 10 | 0 % | 128.0 | assembly |

No interference above 5 mm3 in any option; passed at D3 in 113 s.

Masses are for the modelled station (one pulling station, one roller, the rake and the rope), from `cad_parts` densities; the ballast bags count as canvas (500 kg/m3), so their salt (47.5 kg in CAL) is understated. The pawl return spring is not modelled (no spring in `cad_parts`).

### Requirements not met

- PR-005 (R5) gathering rate against the dantala: not verified; no baseline. Estimate 133 kg per worker-hour (was 150 before D17).
- All other PRs met on paper or by design; PR-008 set-up (19 of 20 min) has little margin.

### Decisions awaiting Amish

1. Concept choice among A, B and C (scores within 10 %), and with it the graft of a lever puller as option A's far-side unit (saves about USD 1,000 a set, slower return).
2. Sets per family pan: one set gathers about a third of a pan's yearly output in a 61-day harvest; keep one set per pan, or plan two sets, a wider rake or longer hours.
3. Review of D17 to D24, decided under the standing instruction.
4. `budget_usd` unchanged at 4,000; parts cost USD 2,897 (USD 1,103 under).

### Open technical items

- Drum flange thrust from the layered rope is not calculated; the multi-layer pressure factor for polyester is unsourced (S7, to confirm 12).
- Cheek plates, frame welds and turnbuckles are covered by catalogue ratings and the TRL 4 proof load, not by calculation.
- Regulatory: whether the forest department treats a hand capstan as barred machinery is to assess (SDG-REG-001 G2); Indian machinery-safety rules for hand tools to assess (G5).

### Safety concerns

Rope snap-back (H1), heat stress (H6, cranking is high work at about 470 W metabolic; plan for the cooler hours), anchor pull-out and a slack chain letting the capstan tip (H3, F11), and crevice corrosion of the stainless rake bolts (F3). See SDG-RSK-001.

### Kit bugs and notes

- `.kit/stem_check.py` `Check.summary()` counts any Plausible row with a non-empty `closed_by` as closed, so a row annotated "Open: ..." made the check report `pass`. Worked around in `docs/04-calcs/stem_check.py` by moving the note into the check text and blanking `closed_by`.
- The STM verdict label "Plausible, to confirm at TRL 3" cannot express rows that need field data at TRL 4; kept as the kit's label with a note.
- `.kit/render.py --check` requires `media/options.png`, which only `.kit/options.py` (Blender, coordinator) can make; until it is rendered the check reports that FAIL. Scenes exported with `.kit/options.py --export` for the coordinator.
- `.kit/trace.py` crashes with a raw YAML traceback when any document's front matter has an unquoted colon, without naming the file.
- `ALLOWED_CONTACTS` matching in `.kit/cad_check.py` is case-sensitive.
- `cad_parts.split_pin` has its head at 0.8 d of the pin length; through a shaft it overlaps unless the pin is sized up; `cad_parts` has no spring.

### Recommended next step

Amish decides open decisions 1 and 2; the coordinator renders `media/options.png` and the product renders. Then, when the cap allows TRL 4, measure the drag per metre and the dantala rate on a partner's pan before building.

## Session 2026-10-25: decisions

Amish, 2026-10-25 10:19 CT, after a report listing each repo's proposed decisions and recommendations: "i concur with your recommendations". Every decision that carried a recommendation is recorded as decided with the option recommended; every decision without a pick stays open.

### Decided by Amish, 2026-10-25

- **Open decision 2, sets per family pan (now D25):** one set per pan stays the design case; the partner is asked how long the gathering season really is and what share of the harvest a family would gather with the tool, before any scope change. No design, number or cost changed. Recorded in SDG-DEC-001 v0.3, SDG-RSK-001 v0.2 (P5), SDG-PLN-001 v0.2, SDG-FEA-001 v0.2, SDG-PRB-001 v0.4 and SDG-STM-001 v0.2 (S24 note).

### Still open (no recommendation to concur with)

- **Open decision 1, concept:** A (158), C (154) and B (148) are within 10 % and went to Amish without a pick, with the lever puller graft; `concept_chosen` stays unset and the repo stays on option A.
- **Review of D17 to D24** (made under the standing instruction): listed for Amish's review with no option recommended; they stand as made and he can reverse any.
- `budget_usd` stays 4,000 (parts USD 2,897): a note, not a decision.

### Checks

Run in this order on 2026-10-25 (no edit to `cad/src/` or `bom/bom.csv` this session):

- `python3 docs/04-calcs/sizing.py`: runs (figures unchanged).
- `python3 docs/04-calcs/stem_check.py`: open, 26 within, 9 plausible, 0 fail.
- `python3 .kit/trace.py`: RTM regenerated, 0 gaps.
- `python3 .kit/cad_check.py --export`: PASS at D3.
- `python3 .kit/render.py` and `python3 .kit/render.py --check`: the only FAIL is the expected missing `media/options.png` (Blender render on the Mac); because of it `render.py` stops before writing PDFs, so `docs/pdf/` is not refreshed.
- `python3 -m reuse lint`: compliant.
- Em and en dash scan outside `.kit/` and `LICENSES/`: none.
