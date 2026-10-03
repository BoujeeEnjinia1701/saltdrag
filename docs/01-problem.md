---
doc_id: SDG-PRB-001
title: SaltDrag problem statement
project: SaltDrag
doc_type: Problem statement
version: "0.2"
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
  change: TRL 2 update; site assumptions made explicit, co-design checklist, safety section, open questions answered where the TRL 3 work settles them (SDG-DDR-001)
---

# SaltDrag problem statement

Brine pumping in the Little Rann has been modernised; gathering the salt has not.

## The problem

Agariyas dig wells for underground brine, build pans with two-foot embankments, harden the floors by hand and pump brine in to evaporate over the winter ([Press Institute of India](https://pressinstitute.in/grassroots/traditional-salt-workers-contribute-to-wild-ass-conservation-and-regain-access-to-little-rann-of-kutch/)). The salt is then scraped with a large hand tool called a dantala ([Mongabay India, 2021](https://india.mongabay.com/2021/10/when-salt-is-an-essential-commodity-and-salt-makers-are-not/)). A family can produce 500 to 600 tonnes a year from one pan ([Business Standard, 2009](https://www.business-standard.com/article/companies/growing-pan-of-worries-livelihood-of-over-45k-agariyas-in-jeopardy-109080500047_1.html)), which is a great deal of scraping by hand inside the pan.

The preliminary IP screen found expired and active patents for salt harvesters and salt-pan rakes, but these assume machines. Agariyas' registration cards require them to avoid machine use ([ICSF](https://icsf.net/newss/gujarat-in-kutch-booming-salt-business-puts-traditional-salt-agariyas-up-against-ginger-prawn-fishers/)), and their earnings are a small share of the retail price. The gap is a hand-powered tool, owned by the families, that gathers salt while the worker stays on the bund.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Agariya salt-making families | Gather salt with less time inside the pan and less direct handling | Family pans in the Little Rann during the March to April harvest |
| Women salt workers | A tool that does not need great upper-body strength and can be worked from the bund | Shared family labour in the pans |
| Producer groups and NGOs | A shareable, repairable kit they can fund and train people on | Clusters of pans; existing solar pump programmes |
| Local fabricators | Drawings they can build from steel pipe, rope and bearings | Workshops in towns around the Rann |

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
