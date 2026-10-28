---
doc_id: SDG-FEA-001
title: SaltDrag feasibility assessment
project: SaltDrag
doc_type: Feasibility assessment
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First feasibility assessment (kit 1.8 upgrade), on the design after the STEM check fixes
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Sets per pan decided (D25), 2026-10-25'
---

# SaltDrag feasibility assessment

SaltDrag is feasible to build and, on paper, to work: the physics sits within known science (SDG-STM-001), every load-bearing part checked keeps a margin of 2 or more at twice the rated pull after nine detail fixes (SDG-CAL-001; SDG-DEC-001 D17 to D24), and a town workshop can make it from plate, tube and bought parts for about USD 2,897; what is not yet known is whether it gathers salt faster per worker than the dantala and whether the forest department will allow it, and neither can be settled on paper. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A geared drum winch, a rope over a roller and a skid-mounted rake: each is long-established practice. Crank effort 89 N, cranking power up to 71 W, rope pull 3.7 kN or more on a full drum, lowest strength margin 2.08 at 6 kN, tipping margin 1.56 (1.46 at 6 kN) | High | The drag per metre of rake (0.9 kN/m) is assumed; if a real bed drags more, the skids are raised or the rake shortened | SDG-STM-001 S1 to S17; SDG-CAL-001 Sections A to C; the drum barrel's rope pressure factor is open (S7) |
| Materials | Galvanised steel on the dry ground, UHMW-PE, FRP and 316 stainless in the pan, polyester rope; galvanising outlasts a season by a wide margin | Medium | 316 stainless in near-saturated warm brine can suffer crevice corrosion (S19); duplex bolts are the fallback | SDG-STM-001 S18 to S21; BOM |
| Manufacturing and assembly | Cut, drilled and welded plate and hollow section; lathe work on the drum shaft and keyways; bought gears, bearings, anchors and rope; every bolted joint checked for assembly at D3 | High | Gear cutting and galvanising are bought in; the cross-tube, guard and axle details were redrawn so they can be assembled (SDG-DEC-001 D19) | SDG-BLD-001; `cad/fidelity.json`; SDG-STM-001 S26 |
| Power and controls | Two people cranking; no power source, no controls beyond the pawl and the band brake | High | Heat limits safe cranking to the cooler hours (S16) | SDG-STM-001 S15, S16 |
| Supply of parts | Steel from stockists in Gandhidham or Ahmedabad; module 4 gears, flange bearings, helical anchors and polyester rope are catalogue items in India | Medium | Stainless-insert thermoplastic bearings and certified rope may need to come from a large city | BOM; SDG-MKT-001 |
| Site and permission | The capstans need firm, dry ground behind the bunds; use inside the sanctuary needs the forest department's agreement | Low | Access conditions bar heavy machinery; whether a hand capstan is acceptable is unknown (SDG-REG-001 G2); soil strength for the anchors is assumed (S12) | SDG-REG-001; SDG-STM-001 S12 |
| Usefulness | About 532 kg/h with a crew of four, 133 kg per worker-hour; one set gathers about a third of a family pan's yearly output in a 61-day harvest | Medium | The dantala baseline is unmeasured (PR-005); one set per pan may not be enough for a family; it stays the design case until the partner answers (SDG-DEC-001 D25, decided 2026-10-25) | SDG-CAL-001 [D8], [D9], [D11]; SDG-OPT-001 |

Ratings: High, Medium, Low.
