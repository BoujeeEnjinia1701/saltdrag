---
doc_id: SDG-DEC-001
title: SaltDrag design decisions register
project: SaltDrag
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval
---

# SaltDrag design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The rope certificate shows a minimum breaking strength of at least 25 kN for the 12 mm polyester double braid, with eye splices | The 7.7 working-load factor (R10) rests on it | SDG-CAL-001 [C8] |
| 2 | The bought gear and pinion are module 4, 20 degree pressure angle, C45 or better, and the gear blank is webbed (about 10 kg) | Tooth strength, mesh at 196 mm centres and the part mass | SDG-CAL-001 [C3]; SDG-DDR-002 |
| 3 | The flange bearings fit 40 mm and 25 mm shafts on bolt squares of 102 mm and 70 mm, with stainless inserts | The cheek holes are drilled to these squares | SDG-DWG-101 |
| 4 | The chain, turnbuckles and shackles carry working load limits of at least 7.8 kN, 6 kN and 10 kN | The 2.4 margin on the chain line | SDG-CAL-001 [C9b] |
| 5 | The FRP tube's maker gives a flexural strength of 200 MPa or more | The beam margin of 7.1 | SDG-CAL-001 [C13b] |
| 6 | Each helical anchor holds at least 2.25 kN (1.5 times its share of the rated pull) in the proof pull on site, at the trial pan | The soil strength is assumed at 50 kPa; the anchors are a safety stop | SDG-CAL-001 [C10]; SDG-DDR-001, D11 |
| 7 | The drag of the rake on the partner's crystal bed, measured with a spring scale or CalRig on a short trial rake | The design drag and rope pull rest on an assumed 300 N per metre; if higher, raise the skids or shorten the rake | SDG-CAL-001, Section A |
| 8 | The bund crest is at least 0.35 m wide and the ground behind the bund is firm and dry on both capstan sides of the trial pan | The roller saddle footprint and capstan position assume it | SDG-PRB-001; SDG-DDR-001, D2 |

## Value engineering

Value-engineering target: USD 4,000 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,803 (USD 1,197 under the target). Main cost drivers and savings worth trying:

- The largest lines are fabrication labour and galvanising (USD 450), the four side frames (USD 220), the two drums (USD 220), the two bought gears (USD 190), the rake blade (USD 190) and the two pull ropes (USD 190).
- The four flange bearings with stainless inserts (USD 264 for eight) cost about twice plain cast-iron bearings; they stay because the capstans stand in salt dust and are rinsed daily.
- Savings worth trying: a single gear pair cut in a local workshop in place of bought gears; a laser-cut cheek nested with the ratchet wheel and pawl to cut plate waste; sharing one set between several families' pans, which spreads the cost per family.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Geared drum winch (still called a hand capstan) rather than a warping capstan | Amish, pre-approval: "I pre-approve the batch runs along with any recommendations you come up with." | SDG-DDR-001, D1 |
| 2026-10-03 | Capstan on dry ground 1.5 m behind the bund crest, with a bund roller saddle on the crest | Amish, same pre-approval | SDG-DDR-001, D2 |
| 2026-10-03 | Single spur stage 6 to 1, module 4; two 330 mm cranks 180 degrees apart | Amish, same pre-approval | SDG-DDR-001, D3 |
| 2026-10-03 | 12 mm polyester double braid rope, 45 m per side | Amish, same pre-approval | SDG-DDR-001, D4 |
| 2026-10-03 | One-piece 3.0 m FRP rake with a 300 mm UHMW-PE blade; three adjustable skids, blade 10 mm above the floor | Amish, same pre-approval | SDG-DDR-001, D5 and D6 |
| 2026-10-03 | Two helical ground anchors per capstan, chained at rope height | Amish, same pre-approval | SDG-DDR-001, D7 |
| 2026-10-03 | Galvanised steel on dry ground; FRP, UHMW-PE and 316 stainless in the pan; stainless-insert bearings; daily rinse | Amish, same pre-approval | SDG-DDR-001, D8 |
| 2026-10-03 | Safety: pawl always engaged while winding; pay out only on the brake with the cranks removed; rope dampers and a 2 m exclusion zone; anchors proof-loaded on site to 1.5 times their share | Amish, same pre-approval (conservative options) | SDG-DDR-001, D9 to D11 |
| 2026-10-03 | Design pan 30 m between crests; crew of four | Amish, same pre-approval | SDG-DDR-001, D12 and D13 |
| 2026-10-03 | First co-design partner to approach: SEWA; first trial region: Little Rann of Kutch (candidates, not agreed) | Amish, same pre-approval | SDG-DDR-001, D14 and D15 |
| 2026-10-03 | Seek written clarification from the forest department, through the partner, that a hand capstan is not a machine | Amish, same pre-approval | SDG-DDR-001, D16 |
| 2026-10-03 | SaltDrag capstan offered as the first candidate for the hand capstan block shared with SiltHaul | Amish, same pre-approval | SDG-DDR-001, D17 |
| 2026-10-03 | Design for construction: bolted side frames and cross tubes, welded drum with brake rim, flange bearings, bought gears, pawl on a welded boss, differential band brake, removable cranks, gear guard, anchor ears and chains, one-piece rake with crush-sleeved bolts, slotted skid hangers, end caps with eye plates | Amish, same pre-approval | SDG-DDR-002, changes 1 to 14 |
| 2026-10-03 | Ballast bags on the rake; windrow board removed (the windrow forms about 3.3 m from the bund toe); rope dampers added | Amish, same pre-approval | SDG-DDR-002, changes 15 to 17 |
| 2026-10-03 | Estimated cost reported against the unchanged value-engineering target of USD 4,000 | Amish: "I also accept any cost overruns or variations from the assumed scope cost." | This register |
