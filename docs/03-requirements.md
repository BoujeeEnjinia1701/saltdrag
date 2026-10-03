---
doc_id: SDG-REQ-001
title: SaltDrag requirements
project: SaltDrag
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2; every target made measurable; R10 to R12 added for rope, holding and rope capacity (SDG-DDR-001)
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status from SDG-CAL-001 against the constructable design (SDG-DDR-002); R5 not verified
---

# SaltDrag requirements

Eleven of the twelve requirements are met on paper by the constructable design; R5, the gathering rate against the dantala, cannot be shown until the dantala baseline is measured on a partner's pan. Status is from the sizing note SDG-CAL-001 (estimates). Physical verification is TRL 4 and TRL 5 work.

*Table 1. Requirements and their status at TRL 3.*

| ID | Requirement | Target | Verification (TRL 4 or later) | TRL 3 status |
| --- | --- | --- | --- | --- |
| R1 | Work from the bund | A full harvest pass, including set-up and moving to the next strip, with no worker entering the pan | Observed field trial on a partner pan | Met by design: crews stand on dry ground behind the bunds; the return pull re-aligns the rake |
| R2 | Manageable crank effort | 120 N or less at each of two handles for the design rake load | Spring scale on the handle during trials | Met: 89 N estimated [B3] |
| R3 | Pull capacity | At least 3 kN rope pull from two people at 120 N; every load-bearing part at least 2 to 1 on yield or rated strength at 6 kN | Proof-load test with CalRig | Met: 4.0 kN at the end of a 30 m pass, 3.7 kN on a full drum [B4], [B5]; lowest margin 2.1 [C2b] |
| R4 | Protect the pan floor | Blade edge 5 to 25 mm above the floor; no steel in the pan; skid pressure 15 kPa or less; no visible cutting or cracking after 20 passes | Inspection of a test pan after trial passes | Met by design: 10 mm edge, 10.7 kPa [D1], [D2]; floor check at TRL 5 |
| R5 | Gathering rate | At least as many kilograms per worker-hour as the dantala method on the same pan | Side-by-side timed harvest trial | **Not verified**: no baseline yet; estimate 150 kg per worker-hour [D9] |
| R6 | Portable | Heaviest single part 25 kg or less; every part of the set carried by up to four people | Weigh parts; timed move between pans | Met: heaviest 23.8 kg (a ballast bag filled on site), drum 21.3 kg [E1] |
| R7 | Corrosion resistance | No loss of function after one season in brine and salt with a daily freshwater rinse | Season-long field trial with inspection log | Met by design: galvanised steel above the bund; FRP, UHMW-PE and 316 stainless in the pan |
| R8 | Quick set-up | Capstans anchored and rake rigged in 20 minutes or less (two crews at once) | Timed trials | Met: 19 min estimated [D10], small margin |
| R9 | Value engineering | Parts cost of the full set against the value-engineering target of USD 4,000 | Costed bill of materials | USD 2,803, USD 1,197 under the target [E2], [E3] |
| R10 | Rope safety | Rope minimum breaking strength, after splices, at least 5 times the rated 3 kN pull | Rope certificate; proof load | Met: 7.7 [C8] |
| R11 | Holding | Pawl holds 6 kN; brake holds 3 kN with a hand force of 150 N or less; each ground anchor holds at least 1.5 times its share of the rated pull (proof-loaded on site before use) | Proof-load test with CalRig; anchor pull test on site | Met on paper: pawl boss margin 4.7 [C5b], brake 92 N [C7], anchor 2.4 times its 6 kN chain force [C10b] (soil to confirm) |
| R12 | Pan coverage | Each drum stores at least 45 m of rope, for pans up to 30 m between bund crests | Wind on and measure | Met: 58 m in four layers, 38 mm flange freeboard [B8], [B9] |

## Assumptions

- The drag of a rake on a crystallised bed is about 0.9 kN per metre of blade with a full heap (SDG-CAL-001, Section A); this is the main uncertainty and is measured with the partner before the first build is loaded.
- Hand capstans are not treated as machines under Agariya registration conditions; written clarification is sought through the partner before any trial.
- Several families can share one set across a harvest season.
- Salt gathered into the windrow, about 3.3 m from the bund toe, is loaded with existing methods (out of scope).
- The pans have dry, firm ground behind the bunds on the two sides where the capstans stand.

> **Safety:** R3, R10 and R11 are safety requirements. A load-bearing part that misses its margin, a rope without a certificate, or an anchor that fails its proof load on site stops the work until it is replaced (SDG-BLD-001, Safety stops).
