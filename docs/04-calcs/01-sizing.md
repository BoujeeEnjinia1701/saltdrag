---
doc_id: SDG-CAL-001
title: SaltDrag sizing calculations
project: SaltDrag
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-10-03'
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
---

# SaltDrag sizing calculations

Two people at 89 N each on 330 mm cranks can pull a 3 m rake with a full 230 kg heap across a 30 m pan in under ten minutes, and every load-bearing part keeps at least a 2.1 margin on yield at twice the rated 3 kN pull. Eleven of twelve requirements are met on paper. R5, the gathering rate against the dantala, cannot be shown until the dantala baseline is measured; the estimate is 150 kg per worker-hour. The largest uncertainty is the drag of a rake on a real crystal bed, which is assumed here and must be measured before the first build is loaded.

## Scope and method

First-order hand calculations, scripted in `docs/04-calcs/sizing.py`, which reads its geometry and masses from the parametric model (`cad/src/model.py`) and the bill of materials, prints every result with a label in square brackets, and writes `docs/04-calcs/results.csv`. Strength checks use twice the rated rope pull (6 kN), as R3 asks. All results are estimates for TRL 3; none is a test result.

## Assumptions

*Table 1. Assumptions (every one is in the script's ASSUME list).*

| Assumption | Value | Basis |
| --- | --- | --- |
| Loose salt bulk density | 1,200 kg/m³ | Typical 1,100 to 1,300 for crystallised salt |
| Heap repose angle; heap sliding friction | 35 degrees; 0.70 | Granular salt; friction taken as tan 35 degrees |
| Allowance to loosen and lift the harvest layer | 300 N per metre of blade | Estimate; to be measured with the partner (PRB open questions) |
| Skids on wet salt | friction 0.30 | UHMW-PE on a wet crystalline surface |
| Back tension from the far capstan | 200 N | Enough to keep the rake square |
| Efficiencies | roller 0.98, one spur stage 0.96, bearings 0.98 | Greased gears with some dust |
| People | two crankers at up to 120 N; 30 turns a minute under load, 50 on the return | R2; sustained cranking |
| Moving to the next strip | 8 min | Unchain, slide both capstans 3 m, move the rollers, re-anchor |
| Crew | four | Two cranking near, one at the far capstan, one with rollers and ropes |
| Rope | 12 mm polyester double braid, 27 kN minimum breaking strength, splices 85 % | Catalogue class; certificate to confirm |
| Steels | C45 yield 340 MPa; S275 yield 275 MPa | Normalised bar; structural plate |
| FRP beam | flexural strength 200 MPa, modulus 23 GPa | Lower-bound pultruded values |
| Soil behind the bund | firm clay, undrained shear strength 50 kPa; helix bearing factor 9 | To confirm by a pull test on site |
| Brake lining | friction 0.30 | Woven lining on steel, dusty |
| Design pan | 30 m between bund crests | Assumption, to be surveyed |

## A. Drag on the rake (R2, R3)

The rake is sized so that its design drag with a full heap matches the rated 3 kN pull.

- Full heap: a 300 mm blade holds a heap of triangular section, 0.0643 m² over 3.0 m, or 0.19 m³ [A1], about 231 kg [A2].
- Sliding the full heap over the bed: 0.70 x 231 kg x 9.81 = 1,589 N [A3].
- Loosening and lifting the harvest layer: 300 N/m x 3.0 m = 900 N [A4].
- Skids: the rake weighs 40.4 kg [A5] and carries two ballast bags of 23.8 kg each [A5b]; 0.30 x 88 kg x 9.81 = 259 N [A6].
- Design drag 2,748 N [A7]; with the roller loss and 200 N of back tension the rope pull at the drum is 3,004 N [A8], equal to the rated 3 kN.

If the measured drag is higher, the skids are raised to take a thinner layer, the heap is smaller, or the rake is shortened; the capstan itself has margin (Section B).

## B. Capstan: crank force, pull and speed (R2, R3, R12)

- Gear ratio 84 to 14, 6 to 1 [B1]. At the end of a 30 m pass the rope is on its third layer, at 110.9 mm radius [B2].
- Crank force at the design drag: 3,004 N x 0.1109 m / (6 x 0.94) / (2 x 0.33 m) = 89 N per handle [B3]; R2 asks for 120 N or less.
- Pull from two people at 120 N: 4,030 N on the third layer [B4] and 3,685 N on a full fourth layer [B5]; R3 asks for 3 kN.
- Rope speed at 30 crank turns a minute: 0.053 m/s, about 3.1 m/min [B6]; each cranker works at 84 W [B7].
- Rope stored: 58 m in four layers of 22 turns [B8], with 38 mm of flange above the fourth layer [B9], which is more than two rope diameters. R12 asks for 45 m.

## C. Strength at twice the rated pull (R3, R10, R11)

*Table 2. Strength checks at 6 kN rope pull.*

| Part | Load case | Stress or force | Margin |
| --- | --- | --- | --- |
| Drum shaft, 40 mm C45 | Rope load mid-span between bearings 452 mm apart, plus torque on a full drum | 147 MPa combined [C1] | 2.3 on yield [C1b] |
| Crank shaft, 25 mm C45 | Tooth force on the pinion, 45 mm outside the bearing, plus torque | 161 MPa [C2] | 2.1 [C2b] |
| Pinion teeth, module 4, 35 mm face | Lewis bending, 14 teeth | 139 MPa [C3] | 2.5 [C3b] |
| Pawl and its boss | 7.8 kN at the tooth [C4]; 40 mm boss welded to the cheek, 52 mm long | 59 MPa [C5] | 4.7 [C5b] |
| Brake band | 247 degrees of wrap [C6] | 92 N on the lever holds the rated pull [C7] | R11 asks for 150 N or less |
| Rope | 3 kN rated pull, splices at 85 % | 27 kN breaking strength | 7.7 working-load factor [C8] |
| Chains, 8 mm grade 30 | Two chains at 23 degrees down to the anchors | 3.26 kN each [C9] | 2.4 on working load limit [C9b] |
| Ground anchors, 150 mm helix | Firm clay, 50 kPa | 7.95 kN holding each [C10] | 2.4 on the chain force [C10b] |
| Rake beam, FRP 100 x 100 x 6 | Heap and layer load along 3 m, pulled at both ends | 28 MPa [C13] | 7.1 [C13b]; bows 11 mm at the rated load [C14] |

The pawl was first drawn on a plain 16 mm pin cantilevered from the cheek; at 6 kN that pin would have bent (about 580 MPa), so the constructable design carries the pawl on a 40 mm boss welded to the cheek with an M24 bolt through it (SDG-DDR-002).

Tipping: the capstan weighs 102 kg without its anchors [C11]. With the rope leaving the top of the drum at 677 mm and the chains fixed at 650 mm, the resisting moment about the front tips of the runners is 1.55 times the tipping moment at the rated pull [C12].

> **Safety:** These margins hold only with certified rope, chain and shackles of the stated sizes, anchors that pass their on-site proof load, and parts made from the stated steels. Each is a safety stop in the build plan.

## D. Floor, lift-off near the bund, rate and set-up (R1, R4, R5, R8)

- Floor: with the ballast the skids press on the floor at 10.7 kPa [D1], less than a person standing; the blade edge stays 10 mm above the floor [D2] and no steel touches the pan.
- Lift-off near the bund: the rope comes down from the roller top, 156 mm above the crest, to the bridle swivel 130 mm above the floor. As the rake nears the bund the rope steepens, and once its upward pull exceeds the rake's weight the blade lifts and the heap is left behind. Without ballast this happens with the blade 5.9 m from the bund toe [D3]; with two 24 kg bags of salt it moves in to 3.3 m [D4]. The windrow therefore lies about 3.3 m from the toe, and loading it out uses existing methods.
- One strip: winding a 30 m pass 9.5 min [D5], winding the empty rake back 5.7 min [D6], moving 8 min; 23.2 min in all [D7].
- Gathering rate: one full heap per strip gives about 598 kg/h [D8], or 150 kg per worker-hour for a crew of four [D9]. R5 compares this with the dantala on the same pan; that baseline is not yet measured, so R5 is not verified.
- Set-up per crew, both crews working at once: carry the capstan into place 5 min, two anchors 6 min, chains 2 min, roller 1 min, rope round the pan to the rake 5 min: 19 min [D10], just inside R8.

## E. Mass and cost (R6, R9)

- Heaviest single part: a ballast bag at 23.8 kg, filled on site [E1]; the heaviest made parts are the drum (21.3 kg) and a side frame (20.9 kg). An assembled capstan weighs 102 kg; it is slid along the bund on its runners and is taken apart for moves between pans.
- Parts cost of the full set: USD 2,803 [E2]. Value-engineering target: USD 4,000. Estimated cost of the constructable design: USD 2,803 (USD 1,197 under the target) [E3].

## F. Results against every requirement

*Table 3. Results against SDG-REQ-001.*

| ID | Target | Result | Status |
| --- | --- | --- | --- |
| R1 | No worker enters the pan | Crews on dry ground; rake re-aligned by the return pull | Met by design |
| R2 | 120 N or less per handle | 89 N [B3] | Met |
| R3 | 3 kN from two people at 120 N; margin 2 at 6 kN | 4.0 and 3.7 kN [B4], [B5]; lowest margin 2.1 [C2b] | Met |
| R4 | Edge 5 to 25 mm up; no steel in the pan; 15 kPa or less | 10 mm; 10.7 kPa [D1], [D2] | Met by design |
| R5 | At least the dantala rate | 150 kg per worker-hour [D9]; no baseline | **Not verified** |
| R6 | Heaviest part 25 kg or less | 23.8 kg [E1] | Met |
| R7 | One season in brine | Material choice | Met by design |
| R8 | 20 min or less | 19 min [D10] | Met, small margin |
| R9 | Value-engineering target USD 4,000 | USD 2,803 [E2] | USD 1,197 under the target |
| R10 | Working-load factor 5 or more | 7.7 [C8] | Met |
| R11 | Pawl 6 kN; brake 150 N or less; anchors 1.5 times their share | 4.7, 92 N, 2.4 [C5b], [C7], [C10b] | Met on paper; soil to confirm |
| R12 | 45 m of rope per drum | 58 m [B8] | Met |

## Checks against the TRL 2 figures

The scaffold set a 3 kN pull (R3) before any drag estimate; the drag estimate here lands on it, which fixed the rake at 3.0 m and the blade at 300 mm. The scaffold had no figure for the windrow position; the lift-off calculation added the ballast bags and moved the windrow from the bund edge to about 3.3 m out (SDG-DDR-002).
