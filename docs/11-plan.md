---
doc_id: SDG-PLN-001
title: SaltDrag project plan
project: SaltDrag
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First project plan (kit 1.8 upgrade); stage P3 reached; references of every document collected
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Sets per pan decided (D25), 2026-10-25'
---

# SaltDrag project plan

SaltDrag is at stage P3 (design outputs, TRL 3), the portfolio's stage cap; the next gate is P4 (verification, TRL 4), which is on hold until Amish lifts the cap. Decisions requested now: the concept choice between options A, B and C, which score within 10 % (SDG-OPT-001), and whether one set per family pan is enough (SDG-DEC-001, open decisions 1 and 2). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and STEM check | Design lead | SDG-STM-001, SDG-OPT-001, SDG-DDR-003 | Done at P3; STEM check open on five field-data rows; concept choice awaiting Amish |
| Requirements and traceability | Design lead | SDG-URS-001, SDG-PRS-001, SDG-RTM-001 | Done at P3; PR-005 not verified |
| Calculations | Design lead | SDG-CAL-001 v0.3 | Done at P3 |
| Detailed CAD and drawings | Design lead | `cad/src/model.py` (three options at D3), STEP files, SDG-DWG-001 and SDG-DWG-101 to 113 | Done at P3 |
| Build plan and BOM | Design lead | SDG-BLD-001, bom/bom.csv | Done at P3 |
| Regulatory | Co-design partner, with the project lead | Written answer from the forest department (SDG-REG-001 G2) | To start, through the partner |
| Co-design partner | Project lead | An agreed partner and trial pans | Not started; SEWA is the first candidate to approach |
| Verification (P4) | Design lead with a fabricator | Build, proof load with CalRig, drag measurement, timed trials | On hold (stage cap P3) |
| Validation (P5) | Co-design partner | Season trial, dantala comparison, heat and work-rest study | On hold |

## Resources needed

Table 2. Resources (P4 resources are listed for planning only; nothing is committed while the cap is P3).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design partner liaison | Partner agreement, trial pans, forest department request | 5 to 10 days | to assess |
| Town fabrication workshop (P4, on hold) | One prototype set | About 4 weeks | 2,897 parts and labour (bom/bom.csv) |
| CalRig proof-load rig access (P4, on hold) | Proof load of rope, capstan and anchors to 4.5 kN | 1 day | to assess |
| Field measurement kit (P4, on hold) | Spring scale to 500 N, short trial rake, soil pull test | 2 days on site | to assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Reached (documents complete 2026-10-24) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT | Reached 2026-10-24 |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR | Reached 2026-10-24; STEM check open on field-data rows |
| P3 Design outputs | Model at D3, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Reached 2026-10-24 (kit 1.9.1) |
| P4 Verification | Prototype built; proof load; drag, crank force and set-up time measured; RSK updated | On hold (stage cap P3) |
| P5 Validation | Season trial with a partner; dantala comparison (PR-005); forest department agreement | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish: choose among options A, B and C, or ask for more evidence first (SDG-DEC-001, open decision 1; SDG-DDR-003). The repository stays on option A meanwhile.
2. Decided by Amish on 2026-10-25 (SDG-DEC-001 D25): one set per family pan is the design case. With the partner: ask how long the gathering season really is and what share of the harvest a family would gather with the tool, before any scope change.
3. Amish: review the eight fixes made under the standing instruction (SDG-DEC-001 D17 to D24), any of which he can reverse.
4. Approach SEWA and one other producer group with the costed set, the safety case and the co-design checklist (SDG-PRB-001).
5. Through the partner, ask the forest department in writing whether a hand capstan is allowed (SDG-REG-001 G2).
6. When the cap allows P4: measure the drag per metre and the dantala rate on a partner's pan before building, then build and proof-load one set.

## References

Every source cited in this repository's documents, Chicago style.

- Business Standard. 2009. "Growing Pan of Worries: Livelihood of over 45k Agariyas in Jeopardy." https://www.business-standard.com/article/companies/growing-pan-of-worries-livelihood-of-over-45k-agariyas-in-jeopardy-109080500047_1.html.
- Down To Earth. "Great Change in Little Rann: How Salt Workers on the Brink in Gujarat Brought About a Solar Revolution." https://www.downtoearth.org.in/news/renewable-energy/great-change-in-little-rann-how-salt-workers-on-the-brink-in-gujarat-brought-about-a-solar-revolution-80652.
- Drishti IAS. 2023. "Saltpan Workers of Little Rann of Kutch." July 24, 2023. Accessed October 25, 2026. https://www.drishtiias.com/daily-updates/daily-news-analysis/saltpan-workers-of-little-rann-of-kutch.
- European Parliament and Council. 2006. Directive 2006/42/EC on Machinery. Accessed October 25, 2026. https://www.legislation.gov.uk/eudr/2006/42/body/data.html.
- FSSAI. 2019. "FSSAI, through Notification, Prohibits Sale of Non-Iodised Common Salt." Accessed October 25, 2026. https://fssai.gov.in/upload/media/FSSAI_News_Salt_FNB_16_07_2019.pdf.
- ICSF. "Gujarat: In Kutch, Booming Salt Business Puts Traditional Salt Agariyas up against Ginger Prawn Fishers." https://icsf.net/newss/gujarat-in-kutch-booming-salt-business-puts-traditional-salt-agariyas-up-against-ginger-prawn-fishers/.
- IndiaMART. "Manual Winches." Accessed October 25, 2026. https://m.indiamart.com/impcat/manual-winches.html.
- International Organization for Standardization. ISO 10547:2009, Polyester Fibre Ropes: Double Braid Construction. Accessed October 25, 2026. https://www.iso.org/standard/45997.html.
- International Organization for Standardization. ISO 1461, ISO 2307, ISO 7243, ISO 9223, ISO 4017, ISO 4032, ISO 7089, ISO 10642, ISO 2341, ISO 1234 (titles in SDG-REG-001 and SDG-STM-001).
- Bureau of Indian Standards. IS 2062, IS 4923, IS 4759. European Committee for Standardization. EN 10025-2, EN 10083-2, EN 10210, EN 1993-1-8.
- Knot and Rope Supply. "Maasdam Rope Puller (Rope Ratchet)." Accessed October 25, 2026. https://knotandrope.com/products/maasdam-rope-puller-rope-ratchet.
- Mongabay India. 2021. "When Salt Is an Essential Commodity and Salt Makers Are Not." October 2021. https://india.mongabay.com/2021/10/when-salt-is-an-essential-commodity-and-salt-makers-are-not/.
- Mongabay India. 2023. "Role of Traditional Salt Workers in Wild Ass Conservation Recognised; Get Back Access to Little Rann of Kutch." October 19, 2023. Accessed October 25, 2026. https://india.mongabay.com/2023/10/role-of-traditional-salt-workers-in-wild-ass-conservation-recognised-get-back-access-to-little-rann-of-kutch/.
- Nickel Institute. Guidance on stainless steels in seawater and chloride waters.
- Press Institute of India. "Traditional Salt Workers Contribute to Wild Ass Conservation and Regain Access to Little Rann of Kutch." https://pressinstitute.in/grassroots/traditional-salt-workers-contribute-to-wild-ass-conservation-and-regain-access-to-little-rann-of-kutch/.
- RopeServices UK. "12mm Black Double Braid Polyester Rope, 100 Metre Reel." Accessed October 25, 2026. https://www.ropeservicesuk.com/product/12mm-black-double-braid-polyester-rope-100-metre-reel/.
- Scroll.in. "Gujarat's Plan to Build Asia's Biggest Freshwater Lake Is a Threat to Agariya Salt Workers." https://scroll.in/article/1007602/gujarats-plan-to-build-asias-biggest-freshwater-lake-is-a-threat-to-agariya-salt-workers.
- Snook, Stover H., and Vincent M. Ciriello. 1991. "The Design of Manual Handling Tasks: Revised Tables of Maximum Acceptable Weights and Forces." Ergonomics 34 (9): 1197 to 1213.
- Wikipedia. "Little Rann of Kutch" (citing The Diplomat). https://en.wikipedia.org/wiki/Little_Rann_of_Kutch.
