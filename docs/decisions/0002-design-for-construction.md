---
doc_id: SDG-DDR-002
title: SaltDrag design for construction
project: SaltDrag
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." The standing instruction for this step (Amish, 2026-09-30) is to "fix the design assumptions to match and be physically feasible".

## Context

The concept described portable geared drums "staked on the bunds", a rake "in bolted sections", ropes, bridles and a windrow board, without saying how any part is made or how it joins its neighbours. The constructability review went component by component through how each is made and fixed, and checked the parametric model for overlaps, floating parts and clearances with build123d (`python cad/src/model.py --check`: 63 of 63 checks pass).

## Changes

*Table 1. Changes from the concept to the constructable design.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| 1 | Capstan frame | A portable geared drum, no frame described | Two side frames (6 mm cheek welded on a 40 mm box runner) bolted together by three cross tubes with end plates | Each side frame is under 21 kg and the frame comes apart for carrying (R6); bolted tubes let the drum go in between the cheeks |
| 2 | Capstan position | Staked on the bund | On dry ground behind the bund, drum 1.5 m behind the crest centre, with a roller saddle on the crest | The crest is too narrow to stand on while cranking; the roller keeps the rope off the bund |
| 3 | Drum | A drum | Welded drum: 168 mm pipe barrel, 330 mm flanges, a brake rim on the left flange, a 40 mm shaft welded through; rope wound over the top | The flanges hold 58 m of rope in four layers; rope leaving the top is level with the roller, so it does not lift the capstan |
| 4 | Shaft supports | Not shown | Four-bolt flange bearings bolted to the cheeks, shafts through clearance holes | Bought bearings in stainless and thermoplastic for brine; holes leave 5 to 10 mm of clearance |
| 5 | Gearing | "Geared" | Bought module 4 gear (84 teeth, webbed) and pinion (14 teeth), keyed on; the pinion overhangs outside the right bearing | One stage gives 6 to 1; a webbed gear is 10 kg instead of 22 kg solid |
| 6 | Ratchet and pawl | A ratchet pawl | 20-tooth ratchet wheel on the drum shaft; the pawl on a 40 mm boss welded to the left cheek, with an M24 pivot bolt | A plain pin cantilevered from the cheek would bend at 6 kN (SDG-CAL-001, Section C) |
| 7 | Brake | A brake | Differential band brake: a lined steel band round the brake rim, both ends to a lever pivoted through the left cheek | Holds the rated pull with a 92 N hand force; no extra drum needed |
| 8 | Cranks | Crank handles | Two removable cranks on hubs with cross pins, set 180 degrees apart, on a 25 mm crank shaft in its own bearings | Removable so they are off whenever rope is paid out under load (SDG-DDR-001, D9) |
| 9 | Gear guard | None | A yellow 2 mm steel cup over the gear mesh on three spacers | Covers the nip between gear and pinion |
| 10 | Anchoring | "Screw or plate anchors" | An ear on each cheek at rope height, a shackle, chain and turnbuckle to a screw-in helical anchor 1.7 m behind | Chain at rope height keeps the capstan from tipping (1.55 times the tipping moment) |
| 11 | Rake beam | Bolted sections | One 3.0 m FRP box beam, 100 x 100 x 6 mm | At 12.8 kg one piece is carried by two people; no splice to wear in brine |
| 12 | Blade fixing | Not shown | Ten countersunk M10 stainless bolts through blade and beam, with stainless crush sleeves inside the tube | The sleeves stop the bolts crushing the FRP |
| 13 | Skids | Height-setting skids | Three UHMW-PE skids on L-shaped stainless hangers bolted to the beam's back face through slots | The slots set the blade 5 to 25 mm above the floor |
| 14 | Bridle fixing | "Bridle and swivels" | Stainless end caps on the beam ends with welded eye plates; bridles shackled to the eyes, front and rear | Pulls the beam at its ends through a part made for the load; the beam's bending stays at 28 MPa at 6 kN |
| 15 | Ballast | None | Two woven bags of about 24 kg of salt strapped on the beam behind the blade | Without them the rising rope lifts the blade 5.9 m from the bund toe; with them, 3.3 m (SDG-CAL-001, Section D) |
| 16 | Windrow board | A board at the bund edge collects the salt | Removed | The rake lifts before it reaches the bund edge, so a board there would collect nothing; the windrow forms about 3.3 m from the toe |
| 17 | Rope dampers | None | A weighted bag on each loaded rope | Snap-back protection (SDG-DDR-001, D10) |

## What did not change

What the product does, its pitch and its safety case are unchanged: two hand capstans on the bund side wind a rake across the pan and nobody enters the brine. The windrow position (change 16) and the ballast (change 15) follow from physics the concept had not checked, and both were made under the pre-approval.

## Consequences

- New BOM lines: 6b (25 mm bearings), 11b (chains and turnbuckles), 12 (bund roller saddle), 20 (rope dampers), 22 (ballast bags), 23 (fabrication labour and galvanising).
- General arrangement SDG-DWG-001 goes to Rev P2; making sketches SDG-DWG-101 to 113 are new.
- Concept media, STEP and STL files are regenerated from the constructable model.
- `design_state: constructable` in `project.yaml`.
