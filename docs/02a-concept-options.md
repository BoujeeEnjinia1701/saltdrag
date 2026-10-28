---
doc_id: SDG-OPT-001
title: SaltDrag concept options
project: SaltDrag
doc_type: Concept options
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First concept options (kit 1.8 upgrade); the current design is option A; options B and C added with different working principles; every option modelled at D3 (kit 1.9); scored against SDG-URS-001
---

# SaltDrag concept options

The three options score within 10 % of each other against the user requirements: option A, the current geared drum capstans, 158; option C, a lever rope puller, 154; option B, a bund-walk haul, 148. Under STANDARDS section 21 all three therefore go to Amish without a pick, and the choice is recorded as "Proposed, awaiting Amish" in SDG-DEC-001 and argued in SDG-DDR-003. The scores are close because the options share the rake, the bund roller and the hand-only, leave-nothing-behind layout, so most user requirements score the same; they separate on four things: gathering rate per worker and crew size, where A is far ahead; cost and simplicity, where B and C are ahead. The repository stays on option A, as it was designed before kit 1.8, until Amish decides. Method: STANDARDS section 21.

![Concept options side by side at one scale](../media/options.png)

*Figure 1. The three options, each modelled at detail level D3 in `cad/src/model.py` and rendered by `python .kit/options.py` (Blender Cycles) with a 1.75 m person for scale. The options picture is rendered by the coordinator on Amish's machine; until then this figure is missing from the repository.*

## The options

All three draw a rake across a 30 m pan with a rope over a roller on the bund crest, so nobody enters the pan, and all are hand powered. They differ in how human effort becomes rope pull.

### Option A: geared drum capstans (current design)

Two people wind a 6 to 1 geared drum winch on dry ground 1.5 m behind the bund; the drum stores the rope, a pawl holds it whenever the cranks are let go, and a band brake pays it out. The rope runs over a UHMW-PE roller on the crest to a 3 m FRP rake with a 300 mm UHMW-PE blade, which pushes a 230 kg heap of salt to a windrow 3.5 m from the bund toe. A second capstan on the far bund holds back tension and winds the rake back. Two people at 89 N each, 64 W on average and 71 W at the end of a pass, wind a full pass in 12.4 min; with a crew of four the set gathers about 532 kg/h, 133 kg per worker-hour (SDG-CAL-001). These figures rest on the assumed drag (SDG-STM-001 S1). Key risks: the drag per metre on a real crystal bed is assumed; the gears, bearings and pawl live in salt dust; the capstan is the heaviest kit to carry (107 kg in parts of up to 24 kg). From a partner: a pan to measure the drag and the dantala baseline, and the soil behind the bunds for the anchors. Modelled at D3 with 372 parts (80 made or bought, 249 fasteners, 43 welds).

### Option B: bund-walk haul

A team walks along the dry ground behind the bund hauling the rope by hardwood toggles spliced into it. A UHMW-PE turning sheave on a post, staked to the ground through a base plate, turns the rope through 90 degrees from the bund roller to the haul line, so the team walks parallel to the bund. Legs and body weight pull instead of arms, but a walker sustains only about 130 N, so the rake is halved to 1.5 m and still needs about 1.73 kN: about 14 haulers, plus two on the far side and the rollers (SDG-STM-001 B1). A pass takes about a minute at a walking pace, but each strip gathers half a heap and moving the staked post takes longer than sliding a capstan, so the set gathers about 556 kg/h with a crew of 16, 35 kg per worker-hour. Key risks: many people beside a loaded rope; the post's stakes in unknown soil (B2); a clear 30 m walkway behind the bund. From a partner: a crew of 16 and the walkway. Modelled at D3 with 159 parts (49 made or bought, 94 fasteners, 16 welds).

### Option C: lever rope puller

One or two people rock a hand lever on a small steel frame chained to two helical anchors behind the bund. A moving cam jaw on the lever and a holding cam jaw on the frame grip the rope in turn, so each stroke pulls about 52 mm of rope through and the holding jaw stops it slipping back; the free tail falls behind the puller and is coiled by hand. With a 13 to 1 lever the effort is about 136 N for each of two people, about 30 W each (C1), but a 30 m pass takes about 580 strokes, 29 min. With the same 3 m rake as option A and a crew of four the set gathers about 269 kg/h, 67 kg per worker-hour. Key risks: cam jaws wear and glaze fibre rope (C2); the loose rope tail must be tailed and coiled, the very task option A's drum was chosen to remove (SDG-DDR-001, D1); lever kick-back if a jaw slips. From a partner: the same pan trials as option A, plus a rope wear trial. Modelled at D3 with 204 parts (56 made or bought, 138 fasteners, 10 welds).

## First-order numbers

Table 1. Options compared (estimates; option A from SDG-CAL-001, options B and C from `docs/04-calcs/stem_check.py`; masses and part counts from `cad/fidelity.json` for the modelled set of one pulling station, one roller, the rake and the rope).

| Quantity | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Estimated parts cost of a set (USD) | 2,897 (bom/bom.csv) | about 1,400 (built up from the option A prices: two staked turning posts, a 1.5 m rake, 60 m ropes) | about 1,800 (two pullers, anchors and chains as option A, the option A rake) |
| Mass as modelled (kg) | 197 | 118 | 128 |
| Heaviest part (kg) | 23.8 (ballast bag); 23.5 (drum) | about 45 (welded post, base and block) | about 16 (puller side plate); ballast bag 23.8 |
| Rope pull at the station (kN) | 3.0 | 1.73 | 3.0 |
| Effort per person | 89 N, 64 to 71 W, 2 cranking | about 130 N walking, 14 hauling | 136 N, 30 W, 2 on the lever |
| Time for a 30 m pass (min) | 12.4 | about 1 | about 29 |
| Gathering rate (kg/h) | 532 | about 556 | about 269 |
| Crew | 4 | 16 | 4 |
| Rate per worker (kg per worker-hour) | 133 | about 35 | about 67 |
| Parts count (modelled, all kinds) | 372 | 159 | 204 |
| STEM check (SDG-STM-001) | Within known science after nine detail fixes; 6 rows open for field data or a test | Within known science; B1 and B2 open | Within known science; C2 open |

## Scoring

Table 2. Weighted scoring (weights: High UR 3, Medium 2, Low 1; scores 1 to 5). The four criteria the standard adds to the user requirements are covered by UR-008 (cost against the value-engineering target), UR-011 (buildable with local skills), UR-009 (safety) and UR-015 (maintenance), so they are not counted twice.

| Criterion | Source | Weight | A | B | C | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Stay out of the pan | UR-001 | 3 | 5 | 5 | 5 | All pull from the dry ground over a bund roller |
| Effort women can keep up | UR-002 | 3 | 4 | 4 | 3 | A 89 N and up to 71 W for 12 min; B 130 N with the legs for a minute; C 136 N for 29 min of strokes |
| Gather as fast as now | UR-003 | 3 | 4 | 1 | 2 | 133, 35 and 67 kg per worker-hour; the dantala baseline is unknown, so A is not given 5 |
| Keep the floor and crystals | UR-004 | 3 | 4 | 4 | 4 | Same blade on skids, 10 mm above the floor |
| Carry between pans | UR-005 | 3 | 3 | 3 | 4 | A: parts up to 24 kg but 107 kg per capstan; B: the welded post unit is about 45 kg; C: light puller, anchors as A |
| Last the season | UR-006 | 3 | 3 | 4 | 3 | A has gears, bearings and a pawl in salt dust; B has one sheave; C has jaws that clog and wear |
| Quick to set up | UR-007 | 2 | 3 | 3 | 4 | A 19 min; B four stakes driven; C a light frame and two anchors |
| Affordable to fund | UR-008 | 3 | 3 | 5 | 4 | USD 2,897, about 1,400 and about 1,800 against the USD 4,000 target |
| No new injuries | UR-009 | 3 | 4 | 2 | 3 | A: pawl, brake, guard, damper; B: 14 people beside a loaded rope; C: lever kick-back and jaw slip |
| Within the access conditions | UR-010 | 3 | 5 | 5 | 5 | All hand powered, no engine or motor |
| Build and repair in town | UR-011 | 2 | 3 | 5 | 3 | A needs bought gears and lathe work; B is plate, tube and one sheave; C needs hardened, machined cam jaws |
| Reach across the pans | UR-012 | 2 | 5 | 3 | 5 | A stores 58 m; C any length; B needs a clear 30 m walkway behind the bund |
| Leave nothing behind | UR-013 | 3 | 5 | 5 | 5 | Anchors unscrew, stakes pull out |
| A family crew | UR-014 | 2 | 5 | 1 | 5 | Crews of 4, 16 and 4 |
| Easy daily care | UR-015 | 2 | 3 | 5 | 3 | A: rinse, grease gears and bearings; B: rinse; C: rinse, clean and dress the jaws |
| **Weighted total** | | | **158** | **148** | **154** | |

## Recommendation

No pick: the three totals lie within 10 % of the highest (A 158; C 154, 2.5 % lower; B 148, 6.3 % lower), so under STANDARDS section 21 all three go to Amish as "Proposed, awaiting Amish" (SDG-DEC-001, open decision 1; SDG-DDR-003). The facts that should decide it are not in the totals' small spread but in two rows: option A gathers two to four times as much salt per worker as B or C and is the only one that a family crew can work at speed, while B and C cost about half to two-thirds as much and are simpler to build and keep. If the partner's dantala baseline turns out well above 67 kg per worker-hour, only option A can meet PR-005; if a producer group values a low first cost above speed, option C is the cheaper starting point.

Best ideas to graft, whichever option is chosen (each a design change for Amish to decide):

- From option C onto option A: a lever puller as the far-side unit. The far capstan only holds about 200 N of back tension and winds the empty rake back, so a light lever puller there could save about USD 1,000 a set, at the cost of a slower return (about 14 min instead of 5.7) and a gathering rate about 25 % lower.
- From option B onto option A: a staked turning sheave at the bund for pans where the ground behind the bund is too soft or too narrow for a capstan, so the capstan can stand along the bund instead.

The repository stays on option A until Amish decides (STANDARDS section 21, existing designs).
