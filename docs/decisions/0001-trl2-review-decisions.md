---
doc_id: SDG-DDR-001
title: SaltDrag TRL 2 review decisions
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
  change: TRL 2 review decisions, made under Amish's 2026-10-03 pre-approval of the batch
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted. Decided by Amish under his pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The scaffold (TRL 1, 2026-09-30) left the concept open on how the capstans stand and are anchored, the drive, the rope, the rake build and the people who would host a trial. Taking the repo to TRL 2 and on to TRL 3 in one run needed each of these settled. Amish pre-approved every recommendation for this batch, so each choice below is recorded as decided; safety choices take the conservative option and say what evidence would relax them.

## Options considered and decisions

*Table 1. Decisions at the TRL 2 review.*

| # | Question | Options | Decision | Reason |
| --- | --- | --- | --- | --- |
| D1 | Kind of capstan | Warping capstan with a person tailing the rope; geared drum winch that stores the rope | Geared drum winch, still called a hand capstan | Nobody holds a loaded rope by hand; simpler and safer for a small crew (conservative) |
| D2 | Where the capstan stands | On the bund crest; on dry ground behind the bund with a roller on the crest | Behind the bund, drum 1.5 m behind the crest centre, with a bund roller saddle on the crest | A 0.4 m crest cannot carry a capstan and two people cranking; the roller keeps the rope off the bund |
| D3 | Drive | Worm gear; two-stage spur; single-stage spur | Single spur stage, module 4, 84 and 14 teeth (6 to 1), two 330 mm cranks set 180 degrees apart | Efficient, repairable, gears can be bought cut in India; meets R2 with margin |
| D4 | Rope | Nylon; polypropylene; polyester; high-modulus polyethylene | 12 mm polyester double braid, 45 m per side | Low stretch limits snap-back energy; UV and brine tolerant; affordable (nylon stores too much energy; polypropylene degrades in sun) |
| D5 | Rake | Bolted sections; one piece; timber | One-piece 3.0 m FRP box beam with a 300 mm UHMW-PE blade | Light (12.8 kg beam), does not rust, carried by two people; width set by the 3 kN design drag |
| D6 | Blade height | Fixed; adjustable skids | Three UHMW-PE skids on slotted stainless hangers; blade 10 mm above the floor, adjustable 5 to 25 mm | Protects the hand-hardened floor (R4) |
| D7 | Anchoring | Stakes; deadweight; screw-in ground anchors | Two screw-in helical anchors per capstan, chained to ears on the side frames at rope height | Holds 3 kN without ballast; quick to move; chain at rope height stops tipping |
| D8 | Materials | Painted steel; galvanised steel; stainless throughout | Hot-dip galvanised steel on dry ground; FRP, UHMW-PE and 316 stainless in the pan; stainless-insert thermoplastic bearings; daily freshwater rinse | Nothing that rusts sits in brine (R7) at a moderate cost |
| D9 | Holding and paying out (safety) | Pawl only; brake only; pawl and brake | Pawl always engaged while winding; paying out only on the band brake with the crank handles removed | Conservative: a released crank cannot spin back. Relaxing it (cranks left on while paying out) would need a self-sustaining brake or a no-back crank tested with CalRig |
| D10 | Snap-back protection (safety) | Rope choice only; dampers and exclusion zone | Low-stretch rope plus a weighted damper bag on each loaded rope, and a 2 m exclusion zone along the rope line | Conservative; a test of rope behaviour at break with CalRig would show whether the zone can be narrowed |
| D11 | Anchor proof load (safety) | Trust the estimate; proof-load on site | Every anchor proof-loaded on site to 1.5 times its share of the rated pull before first use | Soil behind the bunds is unknown; a site pull test is the only evidence |
| D12 | Design pan | 20 m; 30 m; 45 m | 30 m between bund crests, rope for 45 m | Covers the pans described as tens of metres wide; survey to confirm |
| D13 | Crew | Three; four | Four: two cranking, one at the far capstan, one moving rollers and ropes | Keeps cranking shifts short in the heat |
| D14 | Co-design partner | Producer organisations and NGOs working with Agariyas | First candidate to approach: SEWA (Self Employed Women's Association), which works with salt-farming families in the Little Rann | Women-led and already working on livelihoods in the pans. Not agreed |
| D15 | First trial region | Little Rann of Kutch; coastal Kutch creeks | Little Rann of Kutch, first candidate | Where the problem was found and the users are |
| D16 | Machine-use condition | Assume hand tools are allowed; ask first | Ask the forest department in writing, through the partner, before any trial | The registration conditions forbid machine use; a written answer removes the doubt |
| D17 | Shared hand capstan block | Separate designs; share | SaltDrag's capstan offered as the first candidate for the common block with SiltHaul | One proven capstan for both; SiltHaul is not changed here |

## Consequences

- The concept gains a bund roller saddle (BOM 12) and loses the windrow board; ballast bags follow from the lift-off calculation (SDG-DDR-002).
- R10 to R12 are added to SDG-REQ-001 for rope safety, holding and rope capacity.
- The site facts the decisions rest on (crest width, ground behind the bunds, soil strength, drag per metre) are listed in SDG-DEC-001 to be confirmed.
- `budget_usd` in `project.yaml` is unchanged; the estimated cost is reported against it as a value-engineering target.
