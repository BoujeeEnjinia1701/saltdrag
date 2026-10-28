---
doc_id: SDG-PRS-001
title: SaltDrag product requirements and specifications
project: SaltDrag
doc_type: Product requirements and specifications
version: "0.4"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold (as SDG-REQ-001)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2; every target made measurable; R10 to R12 added for rope, holding and rope capacity (SDG-DDR-001)
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status from SDG-CAL-001 against the constructable design (SDG-DDR-002); R5 not verified
- version: "0.4"
  date: '2026-10-24'
  author: Amish Chadha
  change: Kit 1.8 upgrade; SDG-REQ-001 becomes SDG-PRS-001; R1 to R12 migrated to PR-001 to PR-012 with tolerance, units and the user requirement each traces to; PR-013 to PR-018 added; status from SDG-CAL-001 v0.3 after the STEM check fixes (SDG-DEC-001 D17 to D24); the assumption that several families share one set is withdrawn
---

# SaltDrag product requirements and specifications

What the design must do, each requirement traced to a user need in SDG-URS-001 (`03a-user-requirements.md`); the links and the evidence are in the traceability matrix SDG-RTM-001 (`03b-traceability.md`). Seventeen of the eighteen requirements are met on paper or by design; PR-005, the gathering rate against the dantala, cannot be shown until the dantala baseline is measured on a partner's pan. Status is from the calculation note SDG-CAL-001 v0.3 (estimates). Physical verification is TRL 4 and TRL 5 work, and the targets remain proposals for review with a co-design partner. Method: STANDARDS section 22. This document replaces SDG-REQ-001; the old R numbers are in the "Was" column.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Usability | Work from the bund | A full harvest pass, including set-up and moving to the next strip, shall need no worker to enter the pan | 0 | max | workers in the pan | Analysis (layout), TRL 3; observed field trial on a partner pan, TRL 5 | Met by design | R1 |
| PR-002 | UR-002 | Usability | Crank effort | The force at each of two crank handles at the design rake load shall not exceed the target | 120 | max | N | Analysis (CAL-001 [B3]), TRL 3; spring scale on the handle, TRL 4 | Met on paper | R2 |
| PR-003 | UR-003, UR-009 | Performance | Pull capacity and margin | Two people at 120 N shall give at least the target rope pull, and every load-bearing part shall keep a margin of 2 on yield or rated strength at twice the target | 3.0 | min | kN | Analysis (CAL-001 [B4], [B5], Section C), TRL 3; proof load with CalRig, TRL 4 | Met on paper | R3 |
| PR-004 | UR-004 | Physical architecture | Protect the pan floor | The blade edge shall ride 5 to 25 mm above the floor, no steel shall touch the pan, and skid pressure shall not exceed 15 kPa | 15 | max | kPa | Analysis (CAL-001 [D1], [D2]), TRL 3; inspection after 20 passes, TRL 5 | Met by design | R4 |
| PR-005 | UR-003 | Performance | Gathering rate | The set shall gather at least as many kilograms per worker-hour as the dantala method on the same pan | dantala rate | min | kg per worker-hour | Side-by-side timed harvest trial, TRL 5 | Not met (not verified; no baseline) | R5 |
| PR-006 | UR-005 | Packaging and transport | Part mass | No single part shall exceed the target, and every part of the set shall be carried by up to four people | 25 | max | kg | Analysis (model masses, CAL-001 [E1]), TRL 3; weigh parts, TRL 4 | Met on paper | R6 |
| PR-007 | UR-006 | Materials | Corrosion resistance | The set shall keep working after one season in brine and salt with a daily freshwater rinse | 1 | min | season | Analysis (materials, SDG-STM-001 S18 to S20), TRL 3; season trial with inspection log, TRL 5 | Met by design (316 stainless in brine to confirm, S19) | R7 |
| PR-008 | UR-007 | Usability | Quick set-up | Capstans anchored and rake rigged by two crews working at once within the target | 20 | max | min | Analysis (CAL-001 [D10]), TRL 3; timed trials, TRL 4 | Met on paper, small margin | R8 |
| PR-009 | UR-008 | Physical architecture | Value engineering | The parts cost of the full set shall be reported against the value-engineering target | 4,000 | max | USD | Analysis (costed BOM, CAL-001 [E2]), TRL 3 | Met on paper (USD 2,897) | R9 |
| PR-010 | UR-009 | Safety | Rope safety | The rope's minimum breaking strength after splices shall be at least the target multiple of the rated 3 kN pull | 5 | min | times the rated pull | Analysis (CAL-001 [C8]), TRL 3; rope certificate and proof load, TRL 4 | Met on paper | R10 |
| PR-011 | UR-009 | Safety | Holding | The pawl shall hold 6 kN; the brake shall hold 3 kN with a hand force of 150 N or less; each ground anchor shall hold at least 1.5 times its share of the rated pull | 150 | max | N on the brake lever | Analysis (CAL-001 [C5b], [C7], [C10b]), TRL 3; proof load and anchor pull test on site, TRL 4 | Met on paper; soil to confirm | R11 |
| PR-012 | UR-012 | Performance | Pan coverage | Each drum shall store at least the target length of rope, for pans up to 30 m between bund crests | 45 | min | m | Analysis (CAL-001 [B8]), TRL 3; wind on and measure, TRL 4 | Met on paper | R12 |
| PR-013 | UR-010 | Physical architecture | Hand power only | The set shall have no engine, motor or stored-energy drive | 0 | max | W of non-human drive power | Inspection of the design (CAL-001 Section G), TRL 3 | Met by design | |
| PR-014 | UR-013 | Physical architecture | Nothing left in the sanctuary | Every part on site shall be removed with hand tools when the set moves, leaving no structure | 0 | max | fixed structures left | Inspection of the design (CAL-001 Section G; SDG-BLD-001), TRL 3; demonstration at the trial pan, TRL 5 | Met by design | |
| PR-015 | UR-011 | Materials | Local stock | Every made part shall be cut, drilled and welded from plate, hollow section, bar and sheet sold in Gujarat; every bought part shall be a catalogue item from an Indian stockist | 100 | min | % of BOM lines | Inspection of the BOM (CAL-001 Section G), TRL 3; build, TRL 4 | Met by design | |
| PR-016 | UR-014 | Usability | Crew size | The set shall be worked by a crew of no more than the target | 4 | max | people | Analysis (CAL-001 [D9], Section G), TRL 3; trials, TRL 5 | Met by design | |
| PR-017 | UR-015 | Usability | Daily care | A daily freshwater rinse and weekly grease shall keep the set working, with spares for the pawl, spring, lining and shackles in the kit | 15 | max | min of care a day | Inspection of the BOM and build plan (CAL-001 Section G), TRL 3; season trial, TRL 5 | Met by design | |
| PR-018 | UR-002, UR-009 | Safety | Cranking power | Each of two crankers shall work at no more than the target rate on the loaded pull | 75 | max | W | Analysis (CAL-001 [B7b]; SDG-STM-001 S15), TRL 3; heart-rate and timing trial with the partner, TRL 5 | Met on paper (71 W) | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- The drag of a rake on a crystallised bed is about 0.9 kN per metre of blade with a full heap (SDG-CAL-001, Section A); this is the main uncertainty and is measured with the partner before the first build is loaded (SDG-STM-001 S1).
- Hand capstans are not treated as machines under the Agariya access conditions, which bar heavy machinery; written clarification is sought through the partner before any trial (SDG-REG-001).
- One set serves one family pan. Version 0.3 assumed several families could share a set; at about 195 t a harvest one set gathers about a third of what one pan yields in a year (SDG-CAL-001 [D11], [D12]; SDG-DEC-001 D20), so that assumption is withdrawn.
- Salt gathered into the windrow, about 3.5 m from the bund toe, is loaded with existing methods (out of scope).
- The pans have dry, firm ground behind the bunds on the two sides where the capstans stand.

> **Safety:** PR-003, PR-010, PR-011 and PR-018 are safety requirements. A load-bearing part that misses its margin, a rope without a certificate, or an anchor that fails its proof load on site stops the work until it is replaced (SDG-BLD-001, Safety stops). Heat is the largest everyday hazard in the March and April harvest; cranking is planned for the cooler hours (SDG-STM-001 S16).
