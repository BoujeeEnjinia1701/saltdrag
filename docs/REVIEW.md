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
