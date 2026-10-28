---
doc_id: SDG-DDR-003
title: SaltDrag concept selection
project: SaltDrag
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: Concept selection argued for Amish (kit 1.8 upgrade); proposed, awaiting Amish
---

# 0003: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed, awaiting Amish. No option is picked: the three score within 10 % of each other (STANDARDS section 21).

## Context

SaltDrag was designed before kit 1.8 as a geared drum capstan on each bund drawing a rake across the pan (SDG-DDR-001 and SDG-DDR-002). The kit 1.8 upgrade requires at least two concept options with different working principles, scored against the user requirements, with the choice left to Amish. The current design became option A, and two options with different principles were developed and modelled at detail level D3: option B, a bund-walk haul, and option C, a lever rope puller (SDG-OPT-001). All three keep the rake, the bund roller, hand power and a layout that leaves nothing in the sanctuary; they differ in how human effort becomes rope pull.

## Options considered

| Option | Working principle | Weighted score | Gathering rate per worker | Crew | Parts cost of a set | Main risk |
| --- | --- | --- | --- | --- | --- | --- |
| A, geared drum capstans | A 6 to 1 geared drum winch, wound by two people, stores the rope; pawl and band brake | 158 | 133 kg per worker-hour | 4 | USD 2,897 | Gears, bearings and pawl in salt dust; the heaviest kit to carry |
| B, bund-walk haul | A team walks the dry ground pulling the rope by toggles; a staked turning sheave turns the pull 90 degrees; 1.5 m rake | 148 | about 35 kg per worker-hour | 16 | about USD 1,400 | Many people beside a loaded rope; a 16-person crew |
| C, lever rope puller | A hand lever with two cam jaws pulls the rope through in short strokes; the tail is coiled by hand | 154 | about 67 kg per worker-hour | 4 | about USD 1,800 | Jaws wear the rope; slow (29 min a pass); loose tail to tend |

Numbers are estimates from SDG-CAL-001 (option A) and `docs/04-calcs/stem_check.py` (options B and C). Every option's principle is within known science (SDG-STM-001).

## Decision

Proposed, awaiting Amish: choose among A, B and C. Because the weighted totals lie within 10 % (A 158, C 154, B 148), the standard sends all three to Amish without a pick. The facts most likely to decide it:

- If gathering speed per worker and a family-sized crew matter most, option A is the only one that delivers both: two to four times the rate of B or C with a crew of four.
- If first cost and simplicity matter most, option C costs about USD 1,100 less a set than A, works with the same crew of four, and is simple to make apart from its hardened jaws, but it gathers about half as much per worker.
- Option B is the cheapest and simplest to make, but its crew of about 16 does not fit a family pan.

A graft worth deciding with the choice: a lever puller (from option C) as the far-side unit of option A, saving about USD 1,000 a set for a slower return. The repository stays on option A until Amish decides (SDG-DEC-001 D16).

## Consequences

- If A is chosen, nothing in the repository changes, and the next step is the partner's drag and dantala measurements (SDG-PLN-001).
- If B or C is chosen, PRS, CAL, the drawings, the BOM and the build plan are redone for that option; its D3 model in `cad/src/model.py` is the starting point.
- `concept_chosen` in `project.yaml` stays unset until Amish decides.
