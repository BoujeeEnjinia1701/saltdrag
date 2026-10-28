---
doc_id: SDG-PRB-001
title: SaltDrag problem statement
project: SaltDrag
doc_type: Problem statement
version: '0.4'
status: Draft
date: '2026-10-25'
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
  change: TRL 2 update; site assumptions made explicit, co-design checklist, safety section, open questions answered where the TRL 3 work settles them (SDG-DDR-001)
- version: "0.3"
  date: '2026-10-24'
  author: Amish Chadha
  change: Kit 1.8 upgrade; users-and-needs and stakeholder tables (the sources of SDG-URS-001); forest department access conditions as reported in 2023; one set serves one family pan (SDG-DEC-001 D20)
- version: '0.4'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Sets per pan: one set per pan kept as the design case (SDG-DEC-001 D25, decided by Amish 2026-10-25)'
---

# SaltDrag problem statement

Brine pumping in the Little Rann has been modernised; gathering the salt has not.

## The problem

Agariyas dig wells for underground brine, build pans with two-foot embankments, harden the floors by hand and pump brine in to evaporate over the winter ([Press Institute of India](https://pressinstitute.in/grassroots/traditional-salt-workers-contribute-to-wild-ass-conservation-and-regain-access-to-little-rann-of-kutch/)). The salt is then scraped with a large hand tool called a dantala ([Mongabay India, 2021](https://india.mongabay.com/2021/10/when-salt-is-an-essential-commodity-and-salt-makers-are-not/)). A family can produce 500 to 600 tonnes a year from one pan ([Business Standard, 2009](https://www.business-standard.com/article/companies/growing-pan-of-worries-livelihood-of-over-45k-agariyas-in-jeopardy-109080500047_1.html)), which is a great deal of scraping by hand inside the pan.

The preliminary IP screen found expired and active patents for salt harvesters and salt-pan rakes, but these assume machines. Agariyas' registration cards require them to avoid machine use ([ICSF](https://icsf.net/newss/gujarat-in-kutch-booming-salt-business-puts-traditional-salt-agariyas-up-against-ginger-prawn-fishers/)), and their earnings are a small share of the retail price. The gap is a hand-powered tool, owned by the families, that gathers salt while the worker stays on the bund.

## Users and context

### Users and needs

Table 1. Users and needs (the source of the user requirements in SDG-URS-001).

| User type | Goals and needs | Typical use scenario | Pain points and challenges |
| --- | --- | --- | --- |
| Agariya salt-making families | Gather the crystallised salt with less time inside the pan and less direct handling; keep the floor and the crystals intact; carry the kit between pans; keep up the pace of the harvest | A family crew of about four works one pan in the March to April harvest, in the cooler hours, and moves to the next strip every 25 minutes or so | Months of work in brine, heat and glare; injuries from handling salt; labour is the family itself, so extra hands cost money |
| Women salt workers | A tool that does not need great upper-body strength and can be worked from the bund, at a pace that can be kept up through a session | Shared family labour in the pans; cranking or hauling in pairs | Heat stress; protective gear reaches them through NGOs, not employers |
| Producer groups and NGOs | A shareable, repairable kit they can fund, cost and train people on, with a clear safety case | Clusters of pans; existing solar pump and livelihood programmes; a pilot with a few families | Small budgets; need evidence that a tool saves time before scaling it |
| Local fabricators | Drawings they can build from steel plate, hollow section, round bar, plastic sheet and bought gears, bearings and rope | Workshops in towns around the Rann (Gandhidham, Dhrangadhra, Kharaghoda) | No CNC; galvanising and gear cutting are bought in; repairs in the season must be quick |

### Stakeholders

Table 2. Stakeholders.

| Stakeholder group | Role or interest | Engagement needed |
| --- | --- | --- |
| Gujarat Forest Department (Wild Ass Sanctuary) | Issues the yearly access cards whose conditions bar heavy machinery and limit what Agariyas may bring into the Rann; reported in 2023 to allow only the machines and technology in use in the 2004 to 2005 baseline year ([Mongabay India, 2023](https://india.mongabay.com/2023/10/role-of-traditional-salt-workers-in-wild-ass-conservation-recognised-get-back-access-to-little-rann-of-kutch/)) | Written confirmation, through the partner, that a hand capstan is allowed before any trial (SDG-DDR-001, D16; SDG-REG-001) |
| Co-design partner (first candidate: SEWA) | Hosts trials inside an existing trust relationship; shapes the tool with the people who will wind it | Agree trial pans, families, work hours and the measurements of the co-design checklist below |
| Salt traders and refiners | Buy the salt; may set crystal size and cleanliness | Check that gathered salt meets their grade (crystal damage, contamination) |
| Salt Commissioner's Organisation and Gujarat government | Salt land, licensing and welfare schemes for salt workers | Inform; possible route to funding sets |
| Funders of livelihood programmes | Pay for pilots and sets | A costed BOM, a safety case and trial results |

The design case is a family pan worked by a crew of four. One set gathers about 195 t in a harvest, about a third of what one pan yields in a year (SDG-CAL-001 [D11]), so one set serves one family pan; whether a family needs more than one set, or a longer season of work, is a question for the partner; Amish decided on 2026-10-25 to keep one set per pan as the design case until the partner answers (SDG-DEC-001 D25).

## Operating environment

- Flat pans with bunds of about 0.6 m (2 ft) height; pan widths of tens of metres. The design case is a pan 30 m across between bund crests, with bunds about 0.4 m wide at the crest and 1.8 m at the base, and dry, firm ground behind the bunds on the two sides where the capstans stand (assumptions, to be surveyed at the first trial pan).
- Crystallised salt bed under shallow brine; hand-hardened pan floor that must not be damaged.
- Extreme heat in the March to April harvest and cold winters; strong sun, wind and dust.
- Highly corrosive brine and salt; no mains power; long distances to repair shops.
- Protected wildlife sanctuary with rules on structures and machines.

## Constraints

- Prototype budget ceiling of $4,000 USD in parts for two capstans, rake, ropes and anchors.
- Hand power only; no engines or motors, to fit Agariya registration rules on machine use.
- Must not damage the hand-hardened pan floor.
- Corrosion-resistant materials or coatings throughout; repairable with local tools.
- Portable between pans by two to four people; no permanent structures in the sanctuary.
- Hardware under CERN-OHL-S-2.0; published as an open engineering reference, not certified equipment.

## Safety

> **Safety:** Gathering salt with ropes and hand capstans brings three hazards that hand scraping does not: a loaded rope that can break or slip and whip back, cranks and gears that can strike or trap a hand, and ground anchors that can pull out. The design answers each one (SDG-PRC-001, Safety), and the build plan has safety stops before the first load. Heat remains the largest everyday hazard in the March to April harvest, whatever tool is used.

## Out of scope

- Brine pumping (solar pumps already serve this).
- Salt washing, drying, grading or transport.
- Motorised or tracked harvesters.
- Large industrial salt works.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Dantala hand scraper | Large hand tool used by Agariyas to scrape salt in the pans | Worked from inside the pan with direct handling of salt | [link](https://india.mongabay.com/2021/10/when-salt-is-an-essential-commodity-and-salt-makers-are-not/) |
| Traditional Agariya pan method | Brine wells, two-foot bunds, hand-hardened pan floors, winter evaporation | No tool for gathering salt from the bund | [link](https://pressinstitute.in/grassroots/traditional-salt-workers-contribute-to-wild-ass-conservation-and-regain-access-to-little-rann-of-kutch/) |
| Solar brine pumps in the Little Rann | Solar pumps replacing diesel for brine lifting, now used by most Agariya families | Solves pumping only; harvest remains manual | [link](https://www.downtoearth.org.in/news/renewable-energy/great-change-in-little-rann-how-salt-workers-on-the-brink-in-gujarat-brought-about-a-solar-revolution-80652) |

## Co-design

A women-led producer organisation or NGO already working with Agariya families on solar pumps or livelihoods, so that harvest trials sit inside an existing trust relationship and the tool is shaped by the people who will wind it. The first candidate to approach is the Self Employed Women's Association (SEWA), which works with salt-farming families in the Little Rann; nothing has been agreed (SDG-DDR-001).

Co-design checklist, to complete with the partner before the first trial:

- [ ] Agree the trial pans and the families who host them.
- [ ] Measure the drag of a rake on a typical crystal bed (the main unknown in SDG-CAL-001).
- [ ] Time the dantala method on the same pans, to set the gathering-rate baseline for R5.
- [ ] Check with the forest department, through the partner, that a hand capstan is not a machine under the registration conditions.
- [ ] Survey bund sizes, pan widths and the ground behind the bunds.
- [ ] Agree work hours, shade and water for trials in the harvest season.

## Open questions

The TRL 3 work answers some of the scaffold's questions on paper; the rest can only be settled on a pan.

| Question | Where it stands |
| --- | --- |
| What is the drag force per metre of rake on a typical Agariya crystal bed? | Estimated at about 0.9 kN per metre with a full heap (SDG-CAL-001); to be measured with the partner before the first build is loaded. |
| Would the forest department regard a hand capstan as a machine under the registration conditions? | The design has no engine or motor. Written clarification is sought through the partner before any trial (SDG-DDR-001). |
| How wide are typical pans, and can one rake span them? | One rake 3.0 m wide works strip by strip across pans up to about 45 m between the capstans; the design case is 30 m. |
| Can the rake gather large Vadagra crystals without crushing them or damaging the floor? | The blade rides 10 mm above the floor on plastic skids and pushes rather than scrapes; crystal damage is to be checked in trials. |
| Which producer organisation would host the first trial pans? | SEWA is the first candidate to approach; nothing is agreed. |
