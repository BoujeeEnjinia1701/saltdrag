---
doc_id: SDG-RSK-001
title: SaltDrag risk register and hazard analysis
project: SaltDrag
doc_type: Risk register and hazard analysis
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 upgrade, stage P3)
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'P5 mitigation as decided by Amish (D25), 2026-10-25'
---

# SaltDrag risk register and hazard analysis

The top project risks are that the forest department treats a hand capstan as barred machinery, and that the rake drags harder on a real crystal bed than assumed; the top hazards are a loaded rope whipping back, heat stress in the harvest and hands caught in the cranks and gears. The highest design FMEA items are the rope (wear over the 100 mm roller and at the splices), the ground anchors in unknown soil and the stainless fittings in brine. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found before harm) to 5 (unlikely to be found).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The forest department does not allow the capstans in the sanctuary | Access conditions bar heavy machinery and new technology (SDG-REG-001 G2) | No trials in the Little Rann | 3 | 5 | Co-design partner | Written request before any build; fall back to coastal Kutch pans outside the sanctuary |
| P2 | The rake drags much harder than 0.9 kN/m on a real bed | Layer loosening term assumed (SDG-STM-001 S1) | Crank force above 120 N, or a narrower rake and a lower rate | 3 | 3 | Design lead | Measure with a short trial rake and a spring scale before the first build is loaded |
| P3 | SaltDrag gathers less per worker than the dantala | Baseline unknown; 133 kg per worker-hour estimated | PR-005 not met; the tool costs families time | 3 | 4 | Co-design partner | Time the dantala on the same pans first; compare in the first trial |
| P4 | No co-design partner takes it up | Nothing agreed with SEWA or others | No trials, no users' voice in the design | 3 | 4 | Project lead | Approach SEWA and one other group with the costed set and the safety case |
| P5 | One set per pan is not enough for a family | One set gathers about a third of a pan's yearly output in the harvest (SDG-CAL-001 [D12]) | Families need two sets or a longer working season; cost per family doubles | 3 | 3 | Project lead | One set per pan kept as the design case (SDG-DEC-001 D25, decided by Amish 2026-10-25); ask the partner how long the gathering season really is and what share a family would gather |
| P6 | Parts cost rises above the estimate | Indicative prices, first prototype | Less margin to the USD 4,000 target | 2 | 2 | Design lead | USD 1,103 of margin; prices confirmed on purchase (TRL 4) |
| P7 | Soil behind the bunds too soft for the anchors | Saline silty soil; strength assumed 50 kPa (S12) | Capstan cannot be anchored | 3 | 3 | Design lead | Site pull test; deadweight or longer anchors as fallback |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Loaded rope whips back | Rope breaks, slips off the drum or loses its anchor | Severe injury to anyone in line with the rope | 5 | 2 | Low-stretch polyester at a working-load factor of 7.7; certified rope; damper bag on every loaded rope; 2 m exclusion zone along the rope line (SDG-DDR-001, D10) | Medium |
| H2 | Hands caught in the gear mesh or struck by a crank | Unguarded mesh; crank spinning back | Crushed or broken fingers, struck forearm | 4 | 2 | Gear guard over the mesh; pawl always engaged while winding; cranks removed before paying out, which is done only on the brake (SDG-DDR-001, D9) | Low |
| H3 | Capstan lurches toward the pan | Anchor pulls out under load | Struck or trapped crank workers | 4 | 2 | Two anchors per capstan proof-pulled on site to 3.42 kN (1.5 times a 70 % share); rated 10 mm chains at rope height (tipping margin 1.56, 1.46 at 6 kN) | Low |
| H4 | Back strain or a dropped part when carrying | Parts up to 23.8 kg (ballast bag) and 23.5 kg (drum) | Back injury; crushed foot | 3 | 3 | Every part 25 kg or less; lift in pairs; capstan taken apart for moves | Medium |
| H5 | Fall from the bund crest into the pan or onto the roller | Working near the 0.4 m crest | Bruising, sprain; contact with brine | 2 | 2 | Nobody needs to stand on the crest during a pass; the roller saddle is placed before the rope is loaded | Low |
| H6 | Heat stress | Cranking at 64 to 71 W in March and April heat (SDG-STM-001 S16) | Heat exhaustion or heat stroke | 5 | 3 | Work in the early morning and evening; shade, water and rest at every strip change; crew rotation | Medium |
| H7 | Welding and galvanising fumes, FRP dust in the workshop | Welding galvanised steel; drilling FRP | Metal fume fever; skin and lung irritation | 3 | 2 | Weld bare steel and galvanise afterwards; ventilation; dust mask and gloves for FRP (SDG-BLD-001) | Low |
| H8 | Brine and salt on skin and eyes | Rigging the rake at the pan edge | Skin cracking, eye irritation | 2 | 3 | Rigging from the bund with the rope; gloves and eye protection; fresh water at hand | Low |
| H9 | Brake band gives way while paying out | Worn or oily lining | Rake runs back; crank-free capstan spins | 3 | 2 | Paying out only with cranks removed; lining inspected daily; spare lining in the kit | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Pull rope (BOM 18) | Carries up to 3 kN | Breaks at a splice or worn section | Snap-back (H1) | Wear over the 100 mm roller (D/d 8.3, at the low end; S27); UV; splice made badly | 5 | 2 | 3 | 30 | Certified rope with professional splices; daily inspection; replace at the first sign of glazing; check the maker's minimum D/d |
| F2 | Helical anchors (BOM 11) | Hold the capstan | Pulls out | Capstan lurches (H3) | Soil softer than assumed (S12) | 4 | 3 | 2 | 24 | Proof pull on site before first use; reject and re-site any anchor that moves more than 25 mm |
| F3 | Rake fittings, 316 stainless (BOM 15, 16, 19) | Hold blade, skids and bridles | Crevice corrosion under bolt heads | Loose blade or a bridle eye fails | Warm near-saturated brine, crevices (S19) | 3 | 3 | 3 | 27 | Daily rinse; inspect weekly; duplex 2205 bolts if pitting appears |
| F4 | Pawl and ratchet (BOM 7) | Holds the drum when the cranks are let go | Pawl skips or its spring breaks | Drum runs back, crank spins (H2) | Salt in the teeth; spring corrosion | 4 | 2 | 2 | 16 | Spare pawl and spring in the kit; daily rinse; check engagement at every set-up |
| F5 | Band brake (BOM 8) | Pays out under control | Slips | Rake runs back | Wet or salted lining | 3 | 2 | 2 | 12 | Cranks removed while paying out; lining kept dry and replaced when glazed |
| F6 | Flange bearings (BOM 6) | Carry the shafts | Seize | Hard cranking | Salt dust in the seals | 2 | 3 | 2 | 12 | Stainless inserts, sealed; rinse and grease weekly |
| F7 | Drum barrel (BOM 3) | Stores the rope | Crushes or ovalises | Rope binds, drum jams | Rope pressure under load (S7) | 4 | 1 | 3 | 12 | 168.3 x 6.3 mm YSt 310 barrel, margin 2.17 at 6 kN (SDG-DEC-001 D18); proof load with CalRig at TRL 4 |
| F8 | Skids (BOM 15) | Set the blade 10 mm above the floor | Wear through | Blade digs into the floor (UR-004) | Abrasion on the crystal bed | 3 | 3 | 2 | 18 | Slotted hangers re-set the height; skids replaced from plastic stock |
| F9 | Rake beam (BOM 13) | Carries the blade | Cracks at a bolt hole | Rake bends | FRP crushed by bolts; impact | 3 | 2 | 3 | 18 | Crush sleeves at every bolt; margin 7.1 at 6 kN |
| F10 | Gear pair (BOM 4, 5) | Multiply the crank torque 6 to 1 | Tooth wear or breakage | Hard cranking or loss of drive | Grit in the mesh | 3 | 2 | 2 | 12 | Guard over the mesh; grease weekly; Lewis margin 2.5 at 6 kN |
| F11 | Anchor chain and turnbuckle (BOM 11b) | Tie the capstan to the anchors | Turnbuckle unscrews | Capstan creeps | Vibration while cranking | 3 | 2 | 2 | 12 | Lock nuts on the turnbuckles; check at every strip change |
