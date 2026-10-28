---
doc_id: SDG-CAL-001
title: SaltDrag sizing calculations
project: SaltDrag
doc_type: Calculation
version: "0.3"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First sizing note at TRL 3 (drag, capstan, strength, floor, rate, mass and cost)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Rerun on the constructable design (SDG-DDR-002); pawl boss, ballast and lift-off near the bund added
- version: "0.3"
  date: '2026-10-24'
  author: Amish Chadha
  change: Kit 1.8 and 1.9.1 upgrade; fixes from the STEM check and its independent review (SDG-DEC-001 D17 to D24); cranking rate 23 turns a minute, gear reaction on the drum shaft, C45 yield by section size, crank shaft fatigue, keys, wet brake, unequal chain tension, tipping at 6 kN, pinion contact, rake pitching, drum barrel crushing, roller axle, drag sensitivity and season throughput; results against PR-001 to PR-018
---

# SaltDrag sizing calculations

At the design drag, two people at 89 N each on 330 mm cranks pull a 3 m rake with a full 230 kg heap across a 30 m pan in about 12 minutes, each working at 64 W on average and 71 W at the end of a pass, and every load-bearing part checked keeps a margin of at least 2 on yield or rated strength at twice the rated 3 kN pull. Seventeen of the eighteen product requirements are met on paper or by design. PR-005 (R5), the gathering rate against the dantala, cannot be shown until the dantala baseline is measured; the estimate is 133 kg per worker-hour. One set gathers about 195 t in a 61-day harvest, about a third of what one family pan yields in a year, so one set serves one pan. Every number that depends on the drag rests on an assumed 300 N per metre to loosen the harvest layer; if the real drag is 1.5 times the estimate, the rope pull is 1.42 times the design pull, and the response is to raise the skids or shorten the rake. That drag must be measured before the first build is loaded.

Version 0.3 carries the fixes from the STEM check SDG-STM-001 and its independent review, all decided under Amish's standing instruction of 2026-10-23 (SDG-DEC-001 D17 to D24): the design cranking rate is 23 turns a minute, not 30 (S15); the drum barrel is 6.3 mm YSt 310 tube, not 4.5 mm pipe (S7); three bolted joints were redrawn so they can be assembled (S26); the season throughput is stated (S24); the brake lever is 600 mm so the brake holds with a wet lining (S9); the anchor chains are 10 mm, for unequal tension between the two (S11); the bridle eyes sit at the foot of the end caps so the rake does not pitch onto its blade (S29); and the shafts, keys and pinion are in quenched and tempered or hardened steel, with a stepped 30 mm crank shaft in UCF206 bearings and hubs on the gear and ratchet (S4, S5, S17, S22, S28).

## Scope and method

First-order hand calculations, scripted in `docs/04-calcs/sizing.py`, which reads its geometry and masses from the parametric model (`cad/src/model.py`) and the bill of materials, prints every result with a label in square brackets, and writes `docs/04-calcs/results.csv`. Strength checks use twice the rated rope pull (6 kN), as PR-003 asks; fatigue and gear contact use the rated pull. Parts not yet checked by calculation (the cheek plates and their welds, the cross tubes, the turnbuckles and shackles beyond their catalogue ratings) are covered by the proof load with CalRig at TRL 4 (SDG-BLD-001). All results are estimates for TRL 3; none is a test result.

## Assumptions

*Table 1. Assumptions (every one is in the script's ASSUME list).*

| Assumption | Value | Basis |
| --- | --- | --- |
| Loose salt bulk density | 1,200 kg/m³ | Typical 1,100 to 1,300 for crystallised salt |
| Heap repose angle; heap sliding friction | 35 degrees; 0.70 | Granular salt; friction taken as tan 35 degrees |
| Allowance to loosen and lift the harvest layer | 300 N per metre of blade | Estimate; to be measured with the partner (SDG-STM-001 S1) |
| Skids on wet salt | friction 0.30 | UHMW-PE on a wet crystalline surface |
| Back tension from the far capstan | 200 N | Enough to keep the rake square |
| Efficiencies | roller 0.98, one spur stage 0.96, bearings 0.98 | Greased gears with some dust |
| People | two crankers at up to 120 N; 23 turns a minute under load, 50 on the return | PR-002 (R2); 23 keeps each cranker within 75 W even on the third layer (SDG-DEC-001 D17; was 30) |
| Moving to the next strip | 8 min | Unchain, slide both capstans 3 m, move the rollers, re-anchor |
| Crew | four | Two cranking near, one at the far capstan, one with rollers and ropes |
| Rope | 12 mm polyester double braid, 27 kN minimum breaking strength, splices 85 % | Catalogue class (a UK maker gives about 2,957 kg); certificate to confirm |
| Steels | C45+N yield 305 MPa and C45+QT yield 430 MPa (UTS 650 MPa) for 16 to 40 mm; S275 yield 275 MPa; drum barrel YSt 310 yield 310 MPa | EN 10083-2 by section size (340 MPa applies only up to 16 mm); EN 10025-2; IS 4923 |
| Fatigue | endurance halved for bare steel in salt air; notch factor 1.6 at the crank shaft step; Goodman factor of 1.5 sought | Estimates for corrosion fatigue and a 1.5 mm fillet |
| Gear contact | allowable 1,000 MPa for induction-hardened C45 pinion teeth; application factor 1.25 | Estimates in the manner of ISO 6336 |
| Drum barrel pressure | multi-layer factor 1.8 for three layers wound under load | Wire-rope practice; not sourced for polyester (SDG-STM-001 S7, open) |
| Chains | 70 % of the pull on the more loaded chain; 10 mm grade 30 working load limit 11.8 kN | Unequal tension (independent review); catalogue class, to confirm |
| Harvest | 61 days (March and April), 6 cooler hours a day; one family pan yields 550 t a year | PRB; Business Standard (2009): 500 to 600 t a year from one pan |
| FRP beam | flexural strength 200 MPa, modulus 23 GPa | Lower-bound pultruded values |
| Soil behind the bund | firm clay, undrained shear strength 50 kPa; helix bearing factor 9 | To confirm by a pull test on site |
| Brake lining | friction 0.20 | Woven lining on steel, wet with brine (0.30 dry) |
| Design pan | 30 m between bund crests | Assumption, to be surveyed |

## A. Drag on the rake (PR-002, PR-003)

The rake is sized so that its design drag with a full heap matches the rated 3 kN pull.

- Full heap: a 300 mm blade holds a heap of triangular section, 0.0643 m² over 3.0 m, or 0.19 m³ [A1], about 231 kg [A2].
- Sliding the full heap over the bed: 0.70 x 231 kg x 9.81 = 1,589 N [A3].
- Loosening and lifting the harvest layer: 300 N/m x 3.0 m = 900 N [A4].
- Skids: the rake weighs 40.4 kg [A5] and carries two ballast bags of 23.8 kg each [A5b]; 0.30 x 88 kg x 9.81 = 259 N [A6].
- Design drag 2,748 N [A7]; with the roller loss and 200 N of back tension the rope pull at the drum is 3,004 N [A8], equal to the rated 3 kN.
- Sensitivity: if the heap and layer drag is 0.5, 1.5 or 2 times the estimate, the rope pull is 0.58, 1.42 or 1.85 times the design pull [A9] to [A11]. At 1.5 times, two people would need about 127 N each, over PR-002.

The design drag equals the rated pull by construction, so it is not evidence that 3 kN is enough. If the measured drag is higher, the skids are raised to take a thinner layer, the heap is smaller, or the rake is shortened; the capstan itself has margin (Section B).

## B. Capstan: crank force, pull and speed (PR-002, PR-003, PR-012, PR-018)

- Gear ratio 84 to 14, 6 to 1 [B1]. At the end of a 30 m pass the rope is on its third layer, at 110.9 mm radius [B2].
- Crank force at the design drag: 3,004 N x 0.1109 m / (6 x 0.94) / (2 x 0.33 m) = 89 N per handle [B3]; PR-002 asks for 120 N or less.
- Pull from two people at 120 N: 4,030 N on the third layer [B4] and 3,685 N on a full fourth layer [B5]; PR-003 asks for 3 kN.
- Rope speed at 23 crank turns a minute: 0.040 m/s, about 2.4 m/min [B6]. Each cranker works at 64 W on average over a pass [B7] and 71 W with the rope on its third layer at the end of it [B7b], within the 75 W an adult sustains when cranking (SDG-STM-001 S15). At the 30 turns a minute of version 0.2 it was 84 W; the independent review showed that 25 turns still gave 77 W on the third layer, so the design rate is 23 (SDG-DEC-001 D17). The pull is about 45 % of each strip's time.
- Rope stored: 58 m in four layers of 22 turns [B8], with 38 mm of flange above the fourth layer [B9], which is more than two rope diameters. PR-012 asks for 45 m.

## C. Strength at twice the rated pull (PR-003, PR-010, PR-011)

*Table 2. Strength checks at 6 kN rope pull (fatigue and contact at the rated 3 kN).*

| Part | Load case | Stress or force | Margin |
| --- | --- | --- | --- |
| Drum shaft, 40 mm C45+QT | Rope load at the barrel and the gear's tooth reaction on its 45 mm overhang, both planes, plus torque on a full drum | 159 MPa combined [C1] | 2.7 on yield [C1b] |
| Crank shaft, C45+QT, 30 mm at the bearings | Full tooth force on the pinion, 48 mm outside the bearing, plus torque | 96 MPa [C2] | 4.5 [C2b]; 3.9 at the 25 mm step [C2c] |
| Crank shaft fatigue | Rotating bending and steady torque at the rated pull; Goodman, endurance halved for salt air | | 1.59 at the 25 mm step [C16]; 2.6 at the cheek [C16b] |
| Pinion teeth, module 4, 35 mm face | Lewis bending, 14 teeth, C45+N | 139 MPa [C3] | 2.2 [C3b] |
| Pinion contact | Hertz at the rated pull, application factor 1.25, induction-hardened teeth | 670 MPa [C3c] | 1.49 [C3d] |
| Gear key and hub | 12 x 8 key along a 44 mm hub, C45+QT, bearing on half the key height | | 2.08 [C17] |
| Ratchet key and hub | 12 x 8 key along the 20 mm wheel and its welded 44 mm hub, C45+N | | 2.15 [C18] |
| Pawl and its boss | 7.8 kN at the tooth [C4]; 40 mm boss welded to the cheek, 52 mm long | 59 MPa [C5] | 4.7 [C5b] |
| Brake band | 247 degrees of wrap [C6]; wet lining, friction 0.20; 600 mm lever | 134 N on the lever holds the rated pull [C7] | PR-011 asks for 150 N or less |
| Rope | 3 kN rated pull, splices at 85 % | 27 kN breaking strength | 7.7 working-load factor [C8] |
| Chains, 10 mm grade 30 | The more loaded chain takes 70 % of the pull, at 23 degrees down to its anchor | 4.56 kN [C9] | 2.6 on working load limit [C9b] |
| Ground anchors, 150 mm helix | Firm clay, 50 kPa; 70 % share | 7.95 kN holding each [C10] | 1.74 on the 6 kN chain force [C10b]; proof pull on site 3.42 kN [C10c] |
| Rake beam, FRP 100 x 100 x 6 | Heap and layer load along 3 m, pulled at both ends | 28 MPa [C13] | 7.1 [C13b]; bows 11 mm at the rated load [C14] |
| Drum barrel, 168.3 x 6.3 YSt 310 | Three layers of rope wound on at 6 kN: hoop stress k T / (t s) with k = 1.8 | 143 MPa [C15] | 2.17 [C15b] (holds for k up to 1.95) |
| Roller axle, 25 mm 316 | Rope deflected over the roller up to the lift-off angle | | 3.9 [C19] |

The pawl was first drawn on a plain 16 mm pin cantilevered from the cheek; at 6 kN that pin would have bent (about 580 MPa), so the constructable design carries the pawl on a 40 mm boss welded to the cheek with an M24 bolt through it (SDG-DDR-002).

Drum barrel: rope wound on under load presses the barrel like a hoop; one layer gives a hoop stress of T / (t s), with s the rope pitch, and each further layer adds less as the barrel and the rope below it yield. The 4.5 mm pipe of version 0.2 reached about 200 MPa at 6 kN against a pipe yield of about 210 MPa, a margin of 1.05 where PR-003 asks for 2, so the barrel is now 168.3 x 6.3 mm YSt 310 tube with the same outside diameter (SDG-DEC-001 D18): 143 MPa, margin 2.17 [C15], [C15b]. The factor of 1.8 comes from wire-rope practice and has no source for polyester rope; the margin of 2 holds only for a factor up to 1.95, and the flange thrust has not been checked, so the STEM check keeps this row open until a sourced factor and a proof load with three layers wound on settle it.

Shafts, keys and gears (SDG-DEC-001 D24, after the independent review): C45 normalised has a yield of 305 MPa, not 340, above 16 mm, which left the 25 mm crank shaft at a margin of 1.89; the drum shaft also carries the gear's reaction. Both shafts are now C45+QT (430 MPa), and the crank shaft is 30 mm through its bearings (UCF206 size) and 25 mm outboard, where the pinion and the crank hubs sit, so that in fatigue it keeps a factor of 1.59 at the step even with its endurance halved for salt air [C16]. The keys of version 0.2 sat in a 30 mm gear face and a 20 mm ratchet wheel, where their bearing stress at 6 kN was 303 and 455 MPa; the gear now has a 44 mm hub and the ratchet a welded 44 mm hub, which takes the drum shaft 26 mm further to the left (618 mm long). The pinion teeth are induction-hardened, because the contact stress at the rated pull, 670 MPa with an application factor, is too high for normalised C45 over a season [C3c].

Tipping: the capstan weighs 107 kg without its anchors [C11]. With the rope leaving the top of the drum at 677 mm and the chains fixed at 650 mm, the resisting moment about the front tips of the runners is 1.56 times the tipping moment at the rated pull [C12] and 1.46 times at 6 kN [C12b], with both chains taut. A slack chain lets the capstan yaw and tip about one runner, so both turnbuckles are tensioned and checked at every set-up (SDG-RSK-001 F11).

> **Safety:** These margins hold only with certified rope, rated chain, turnbuckles and shackles of the stated sizes, anchors that pass their on-site proof pull of 3.42 kN, and parts made from the stated steels and heat treatments. Each is a safety stop in the build plan.

## D. Floor, pitching, lift-off near the bund, rate and set-up (PR-001, PR-004, PR-005, PR-008)

- Floor: with the ballast the skids press on the floor at 10.7 kPa [D1], less than a person standing; the blade edge stays 10 mm above the floor [D2] and no steel touches the pan.
- Pitching: the pull at the bridle height pitches the rake forward about the skid tips, and the heap and layer resist lower down. With the bridles at mid-height (130 mm), as drawn in version 0.2, the pitching moment was about twice the rake's restoring moment, so the blade would have tipped onto the floor under a full heap. With the eye plates at the foot of the end caps and the bridle apex at 70 mm (SDG-DEC-001 D23) the restoring moment is 9.8 times the pitching moment [D13], and the skid pressure stays near its static value.
- Lift-off near the bund: the rope comes down from the roller top, 156 mm above the crest, to the bridle swivel 70 mm above the floor. As the rake nears the bund the rope steepens, and once its upward pull exceeds the rake's weight the blade lifts and the heap is left behind. Without ballast this happens with the blade 6.4 m from the bund toe [D3]; with two 24 kg bags of salt it moves in to 3.5 m [D4]. The windrow therefore lies about 3.5 m from the toe, and loading it out uses existing methods.
- One strip: winding a 30 m pass 12.4 min [D5], winding the empty rake back 5.7 min [D6], moving 8 min; 26.1 min in all [D7].
- Gathering rate: one full heap per strip gives about 532 kg/h [D8], or 133 kg per worker-hour for a crew of four [D9]. PR-005 (R5) compares this with the dantala on the same pan; that baseline is not yet measured, so PR-005 is not verified.
- Season throughput: at 6 cooler hours a day over the 61 days of March and April one set gathers about 195 t [D11], 35 % of the 550 t one family pan yields in a year [D12]; at 4 hours a day, about 130 t. Version 0.2 assumed several families could share one set; the numbers do not support that, so the assumption is withdrawn and one set serves one pan (SDG-DEC-001 D20). How a family gathers the rest is a question for the partner and for Amish (SDG-DEC-001, open decision 2).
- Set-up per crew, both crews working at once: carry the capstan into place 5 min, two anchors 6 min, chains 2 min, roller 1 min, rope round the pan to the rake 5 min: 19 min [D10], just inside PR-008.

## E. Mass and cost (PR-006, PR-009)

- Heaviest single part: a ballast bag at 23.8 kg, filled on site [E1]; the heaviest made parts are the drum (23.5 kg with the 6.3 mm barrel and the longer shaft) and a side frame (21.2 kg with the pawl boss). An assembled capstan weighs 107 kg; it is slid along the bund on its runners and is taken apart for moves between pans.
- Parts cost of the full set: USD 2,897 [E2]. Value-engineering target: USD 4,000. Estimated cost of the constructable design: USD 2,897 (USD 1,103 under the target) [E3]. The fixes of SDG-DEC-001 D18, D22 and D24 add an estimated USD 94: the heavier drum barrel and quenched and tempered shafts, the ratchet hub, the stepped crank shaft and induction-hardened pinion, the larger crank bearings, and rated chains and turnbuckles.

## F. Results against every product requirement

*Table 3. Results against SDG-PRS-001 (the old R numbers of SDG-REQ-001 in brackets).*

| ID | Target | Result | Status |
| --- | --- | --- | --- |
| PR-001 (R1) | No worker enters the pan | Crews on dry ground; rake re-aligned by the return pull | Met by design |
| PR-002 (R2) | 120 N or less per handle | 89 N at the design drag [B3] | Met on paper |
| PR-003 (R3) | 3 kN from two people at 120 N; margin 2 at 6 kN | 4.0 and 3.7 kN [B4], [B5]; lowest margins 2.08 (gear key) [C17], 2.15 (ratchet key) [C18], 2.17 (drum barrel, factor to confirm) [C15b]; chain 2.6 [C9b] | Met on paper |
| PR-004 (R4) | Edge 5 to 25 mm up; no steel in the pan; 15 kPa or less | 10 mm; 10.7 kPa [D1], [D2] | Met by design |
| PR-005 (R5) | At least the dantala rate | 133 kg per worker-hour [D9]; no baseline | **Not verified** |
| PR-006 (R6) | Heaviest part 25 kg or less | 23.8 kg [E1] | Met on paper |
| PR-007 (R7) | One season in brine | Material choice; 316 stainless in brine to confirm (SDG-STM-001 S19) | Met by design |
| PR-008 (R8) | 20 min or less | 19 min [D10] | Met on paper, small margin |
| PR-009 (R9) | Value-engineering target USD 4,000 | USD 2,897 [E2] | USD 1,103 under the target |
| PR-010 (R10) | Working-load factor 5 or more | 7.7 [C8] | Met on paper |
| PR-011 (R11) | Pawl 6 kN; brake 150 N or less; anchors 1.5 times their share | 4.7, 134 N wet, proof pull 3.42 kN against 7.95 kN estimated [C5b], [C7], [C10c] | Met on paper; soil to confirm |
| PR-012 (R12) | 45 m of rope per drum | 58 m [B8] | Met on paper |
| PR-013 | No engine, motor or stored-energy drive | Two hand cranks drive the drum through one spur stage | Met by design |
| PR-014 | Nothing left on site after the harvest | Anchors unscrew, saddles lift off, capstans slide away (SDG-BLD-001) | Met by design |
| PR-015 | Made parts from stock steel and plastic sold in Gujarat; bought parts from Indian stockists | Every made part is cut, drilled and welded from plate, hollow section, bar and sheet (bom/bom.csv) | Met by design |
| PR-016 | Crew of four | Four: two cranking, one at the far capstan, one with rollers and ropes [D9] | Met by design |
| PR-017 | Daily rinse and weekly grease keep it working; spares cover the wearing parts | Maintenance kit, BOM 21 | Met by design |
| PR-018 | Each cranker 75 W or less at the design drag | 71 W on the third layer, 64 W mean [B7b], [B7] | Met on paper |

## G. Product requirements added in the kit 1.8 upgrade

PR-013 to PR-018 have no R number in SDG-REQ-001; their evidence is here. PR-013 (hand power only) and PR-014 (no structure left in the sanctuary) are met by the layout itself: the only drive is the two cranks, and the only ground fixings are the screw-in anchors, which are unscrewed when the set moves. PR-015 (local stock) is met by the bill of materials, where every made line is plate, hollow section, bar or sheet and every bought line is a catalogue item from an Indian stockist. PR-016 (crew of four) is the crew of item [D9]. PR-017 (maintenance) rests on the daily freshwater rinse and the spares in BOM 21. PR-018 (cranking power) is item [B7b], 71 W against 75 W with the rope on its third layer, the STEM check row S15 that fixed the design cranking rate at 23 turns a minute.

## Checks against the TRL 2 figures

The scaffold set a 3 kN pull (R3) before any drag estimate; the drag estimate here lands on it, which fixed the rake at 3.0 m and the blade at 300 mm. The scaffold had no figure for the windrow position; the lift-off calculation added the ballast bags and moved the windrow from the bund edge to about 3.3 m out (SDG-DDR-002), and 3.5 m with the lower bridles of D23.
