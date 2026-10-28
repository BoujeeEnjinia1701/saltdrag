---
doc_id: SDG-DEC-001
title: SaltDrag design decisions register
project: SaltDrag
doc_type: Design decisions register
version: '0.3'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval
- version: "0.2"
  date: '2026-10-24'
  author: Amish Chadha
  change: Kit 1.8 and 1.9.1 upgrade; decisions numbered D1 to D16; D17 to D24 decided under Amish's standing instruction of 2026-10-23 (STEM check fixes, four from the first check and five after the independent review); open decisions 1 (concept choice) and 2 (sets per pan) proposed, awaiting Amish
- version: '0.3'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Open decision 2 decided by Amish as recommended (D25, one set per pan as the design case), 2026-10-25; open decision 1 (concept, no pick) and the review of D17 to D24 (no recommendation stated) stay open'
---

# SaltDrag design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

Table 1. Decisions proposed, awaiting Amish. Open decision 2 (sets per family pan) was decided by Amish on 2026-10-25 as recommended and is D25 under Decisions made.

| # | Decision | Options | Recommendation | Record |
| --- | --- | --- | --- | --- |
| 1 | Concept to carry forward | A, geared drum capstans (current design), weighted score 158; B, bund-walk haul, 148; C, lever rope puller, 154 | **No pick**: the three lie within 10 % of each other, so under STANDARDS section 21 all go to Amish. A gathers two to four times as much per worker and suits a family crew; B and C cost about half to two-thirds as much. Graft worth deciding with it: a lever puller as the far-side unit of option A (saves about USD 1,000 a set, return about 14 min instead of 5.7). The repository stays on option A meanwhile (D16) | SDG-OPT-001; SDG-DDR-003 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The rope certificate shows a minimum breaking strength of at least 25 kN for the 12 mm polyester double braid, with eye splices | The 7.7 working-load factor (R10) rests on it | SDG-CAL-001 [C8] |
| 2 | The bought gear and pinion are module 4, 20 degree pressure angle, C45 or better, and the gear blank is webbed (about 10 kg) | Tooth strength, mesh at 196 mm centres and the part mass | SDG-CAL-001 [C3]; SDG-DDR-002 |
| 3 | The flange bearings fit 40 mm and 30 mm shafts on bolt squares of 102 mm and 83 mm (UCF208 and UCF206 sizes), with stainless inserts | The cheek holes are drilled to these squares (D24) | SDG-DWG-101 |
| 4 | The 10 mm grade 30 chain carries a working load limit of at least 11.8 kN, the forged turnbuckles at least 9.2 kN (1 t) and the shackles at least 9.8 kN | The 2.6 margin on the more loaded chain (D22) | SDG-CAL-001 [C9b] |
| 5 | The FRP tube's maker gives a flexural strength of 200 MPa or more | The beam margin of 7.1 | SDG-CAL-001 [C13b] |
| 6 | Each helical anchor holds at least 3.42 kN (1.5 times a 70 % share of the rated pull) in the proof pull on site, at the trial pan, pulled in line with its chain | The soil strength is assumed at 50 kPa; the anchors are a safety stop | SDG-CAL-001 [C10c]; SDG-DDR-001, D11 |
| 7 | The drag of the rake on the partner's crystal bed, measured with a spring scale or CalRig on a short trial rake | The design drag and rope pull rest on an assumed 300 N per metre; if higher, raise the skids or shorten the rake | SDG-CAL-001, Section A |
| 8 | The bund crest is at least 0.35 m wide and the ground behind the bund is firm and dry on both capstan sides of the trial pan | The roller saddle footprint and capstan position assume it | SDG-PRB-001; SDG-DDR-001, D2 |
| 9 | The drum barrel tube is 168.3 x 6.3 mm YSt 310 (IS 4923) or S355J2H (EN 10210), with a mill certificate | The barrel margin of 2.17 under rope crushing (D18) | SDG-CAL-001 [C15] |
| 10 | The rope maker's minimum sheave-to-rope diameter ratio for the chosen rope is 8 or less | The 100 mm bund roller bends the 12 mm rope at a ratio of 8.3 | SDG-STM-001 S27 |
| 11 | The shafts are C45+QT with a mill certificate (430 MPa yield, 650 MPa tensile strength for 16 to 40 mm), the gear is C45+QT and the pinion teeth are induction-hardened | The shaft, key and contact margins (D24) | SDG-CAL-001 [C1b], [C2b], [C16], [C17], [C3d] |
| 12 | The multi-layer pressure factor for polyester rope on the drum, from a rope maker or a winding standard; and the drum flanges' thrust | The barrel margin holds for a factor up to 1.95; flange thrust is not yet checked (SDG-STM-001 S7) | SDG-CAL-001 [C15] |

## Value engineering

Value-engineering target: USD 4,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,897 (USD 1,103 under the target), including an estimated USD 94 for the fixes of D18, D22 and D24. Main cost drivers and savings worth trying:

- The largest lines are fabrication labour and galvanising (USD 450), the two drums (USD 244), the four side frames (USD 220), the two bought gears (USD 190), the rake blade (USD 190) and the two pull ropes (USD 190).
- The four flange bearings with stainless inserts (USD 264 for eight) cost about twice plain cast-iron bearings; they stay because the capstans stand in salt dust and are rinsed daily.
- Savings worth trying: a single gear pair cut in a local workshop in place of bought gears; a laser-cut cheek nested with the ratchet wheel and pawl to cut plate waste; a lever puller in place of the far-side capstan (open decision 1). Sharing one set between several families' pans, suggested in version 0.1, is withdrawn: one set gathers about a third of one pan's yearly output in the harvest (D20).

## Decisions made

| ID | Date | Decision | Decided by | Record |
| --- | --- | --- | --- | --- |
| D1 | 2026-10-03 | Geared drum winch (still called a hand capstan) rather than a warping capstan | Amish, pre-approval: "I pre-approve the batch runs along with any recommendations you come up with." | SDG-DDR-001, D1 |
| D2 | 2026-10-03 | Capstan on dry ground 1.5 m behind the bund crest, with a bund roller saddle on the crest | Amish, same pre-approval | SDG-DDR-001, D2 |
| D3 | 2026-10-03 | Single spur stage 6 to 1, module 4; two 330 mm cranks 180 degrees apart | Amish, same pre-approval | SDG-DDR-001, D3 |
| D4 | 2026-10-03 | 12 mm polyester double braid rope, 45 m per side | Amish, same pre-approval | SDG-DDR-001, D4 |
| D5 | 2026-10-03 | One-piece 3.0 m FRP rake with a 300 mm UHMW-PE blade; three adjustable skids, blade 10 mm above the floor | Amish, same pre-approval | SDG-DDR-001, D5 and D6 |
| D6 | 2026-10-03 | Two helical ground anchors per capstan, chained at rope height | Amish, same pre-approval | SDG-DDR-001, D7 |
| D7 | 2026-10-03 | Galvanised steel on dry ground; FRP, UHMW-PE and 316 stainless in the pan; stainless-insert bearings; daily rinse | Amish, same pre-approval | SDG-DDR-001, D8 |
| D8 | 2026-10-03 | Safety: pawl always engaged while winding; pay out only on the brake with the cranks removed; rope dampers and a 2 m exclusion zone; anchors proof-loaded on site to 1.5 times their share | Amish, same pre-approval (conservative options) | SDG-DDR-001, D9 to D11 |
| D9 | 2026-10-03 | Design pan 30 m between crests; crew of four | Amish, same pre-approval | SDG-DDR-001, D12 and D13 |
| D10 | 2026-10-03 | First co-design partner to approach: SEWA; first trial region: Little Rann of Kutch (candidates, not agreed) | Amish, same pre-approval | SDG-DDR-001, D14 and D15 |
| D11 | 2026-10-03 | Seek written clarification from the forest department, through the partner, that a hand capstan is not a machine | Amish, same pre-approval | SDG-DDR-001, D16 |
| D12 | 2026-10-03 | SaltDrag capstan offered as the first candidate for the hand capstan block shared with SiltHaul | Amish, same pre-approval | SDG-DDR-001, D17 |
| D13 | 2026-10-03 | Design for construction: bolted side frames and cross tubes, welded drum with brake rim, flange bearings, bought gears, pawl on a welded boss, differential band brake, removable cranks, gear guard, anchor ears and chains, one-piece rake with crush-sleeved bolts, slotted skid hangers, end caps with eye plates | Amish, same pre-approval | SDG-DDR-002, changes 1 to 14 |
| D14 | 2026-10-03 | Ballast bags on the rake; windrow board removed (the windrow forms about 3.3 m from the bund toe); rope dampers added | Amish, same pre-approval | SDG-DDR-002, changes 15 to 17 |
| D15 | 2026-10-03 | Estimated cost reported against the unchanged value-engineering target of USD 4,000 | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | This register |
| D16 | 2026-10-24 | Option A, the design of 2026-10-03, stays the design of record while the concept choice is open | STANDARDS section 21 (existing designs are not redesigned without Amish's go) | SDG-OPT-001 |
| D17 | 2026-10-24 | Design cranking rate 23 turns a minute (was 30), so each cranker works at 71 W at the end of a pass and 64 W on average, within the 75 W an adult sustains (STEM check S15; 25 turns, the first fix, still gave 77 W on the third layer, found by the independent review). Options weighed: a 7 to 1 gear (new bought gear, slower rope, USD 0 to 40 more); a third cranker (crew of five, PR-016 not met); a slower rate (no cost; pass 12.4 min instead of 9.5, rate 532 instead of 598 kg/h). Chosen: the slower rate, which costs nothing and changes no part | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S15; SDG-CAL-001 [B7] |
| D18 | 2026-10-24 | Drum barrel 168.3 x 6.3 mm YSt 310 tube (was 168.3 x 4.5 mm pipe): margin 2.17 instead of about 1.05 under three layers of rope at 6 kN (STEM check S7). Options weighed: 168.3 x 11 mm pipe (margin 2.6 but the drum would weigh 28 kg, over PR-006); internal stiffening rings (more welding and distortion); 6.3 mm YSt 310 tube (same outside diameter, so rope geometry unchanged, +1.9 kg, drum 23.2 kg). Cost about USD 8 a drum (estimate) | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S7; SDG-CAL-001 [C15] |
| D19 | 2026-10-24 | Assembly fixes found by the D3 model (STEM check S26): cross-tube end plates 100 x 80 mm with bolts 36 mm from the tube centre (was 80 mm square, 25 mm), so washers clear the tube's welds; gear guard spacers at 150 mm ahead and behind and 120 mm below the drum axis (was 190 mm ahead and behind, 2.5 mm from the cheek edge); roller axle 272 mm with 6 mm split pins (was 260 mm with R-clips inside the plates); bearing bolts fitted heads inside the cheeks so no tail reaches a drum flange. Options weighed for the end plates: weld the tubes on two faces only (weaker), or larger plates (chosen, no cost change). Cost: none | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S26; `cad/fidelity.json` |
| D20 | 2026-10-24 | The assumption that several families share one set is withdrawn; one set serves one family pan (STEM check S24: one set gathers about 200 t in a 61-day harvest, 37 % of one pan's 550 t). The design does not change; how a family gathers the rest is open decision 2 | Decided under Amish's standing instruction of 2026-10-23 (fix rule: the claim is corrected; the scope question goes to Amish) | SDG-STM-001 S24; SDG-CAL-001 [D11], [D12] |
| D21 | 2026-10-24 | Brake lever 600 mm (was 450), so 134 N holds the rated pull with the lining wet with brine (friction 0.20); with the 450 mm lever it needed 179 N, over the 150 N of PR-011 (STEM check S9, independent review). Options weighed: a longer lever (chosen; clears the left crank and the cross tubes; about USD 1 more steel); more wrap (needs a new band layout round the rim); a covered rim (keeps the lining dry but does not change the design case). The lining is also to be kept dry and free of grease | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S9; SDG-CAL-001 [C7] |
| D22 | 2026-10-24 | Anchor chains 10 mm grade 30 (was 8 mm), forged jaw-and-eye turnbuckles rated 1 t (were M16 hook and eye) and 1 t shackles, with the anchor proof pull raised to 3.42 kN: two chains do not share the pull equally, and with 70 % on one the 8 mm chain kept only 1.71 on its working load limit (STEM check S11, independent review). Options weighed: a load-sharing bridle between the two chains (another part to rig each move); larger chain (chosen, margin 2.6). Cost about USD 32 a set (estimate) | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S11, S12; SDG-CAL-001 [C9b], [C10c] |
| D23 | 2026-10-24 | Bridle eye plates at the foot of the end caps (centre 66 mm above the floor, was 110) and the bridle apex at 70 mm (was 130): with the pull at mid-height the rake's pitching moment was about twice its restoring moment, so under a full heap the blade would tip onto the floor (STEM check S29, from the independent review's note on skid pressure). Options weighed: move the ballast forward (not enough on its own); skids ahead of the blade (they would plough the heap); lower the pull (chosen, no cost). The windrow moves from 3.3 to 3.5 m from the bund toe | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S29; SDG-CAL-001 [D13], [D4] |
| D24 | 2026-10-24 | Shafts, keys and gears (STEM check S4, S5, S17, S22, S28, independent review): drum shaft and crank shaft C45+QT (C45 normalised yields only 305 MPa above 16 mm, which left the 25 mm crank shaft at 1.89); crank shaft stepped, 30 mm through UCF206 bearings and 25 mm outboard, for fatigue in salt air; gear with a 44 mm hub in C45+QT and ratchet with a welded 44 mm hub, the drum shaft 26 mm longer (618 mm), because the keys in a 30 mm gear face and a 20 mm ratchet reached 303 and 455 MPa at 6 kN; pinion teeth induction-hardened for contact life. Options weighed for the crank shaft: a 30 mm shaft throughout (the pinion bore would leave a thin rim); a stepped shaft (chosen, pinion and crank hubs unchanged). Cost about USD 46 a set (estimate: quenched and tempered drum shafts 8, ratchet hubs 12, crank shafts and hardened pinions 10, larger bearings 16) | Decided under Amish's standing instruction of 2026-10-23 (fix rule); Amish can reverse it | SDG-STM-001 S4, S5, S17, S22, S28; SDG-CAL-001 [C1b], [C2b], [C16], [C17], [C18], [C3d] |
| D25 | 2026-10-25 | Sets per family pan: one set per pan stays the design case; the partner is asked how long the gathering season really is and what share of the harvest a family would gather with the tool, before any scope change (was open decision 2) | Amish: "i concur with your recommendations" | SDG-CAL-001 [D11], [D12]; D20; SDG-PLN-001 |
