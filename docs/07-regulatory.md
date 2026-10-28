---
doc_id: SDG-REG-001
title: SaltDrag regulatory and standards register
project: SaltDrag
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First register (kit 1.8 upgrade); web sources checked 2026-10-25
---

# SaltDrag regulatory and standards register

The question that decides whether SaltDrag can be used at all is not a product standard but the forest department's access conditions for the Little Rann, which bar heavy machinery; whether a hand capstan is acceptable is **to assess** in writing, through the partner, before any trial. SaltDrag hauls a rake horizontally and lifts nothing, so lifting-equipment rules do not apply, and no Indian machinery-safety rule for a hand tool used by self-employed workers has been found (to assess). The material and rope standards below are met by the design or by buying to them. Not legal advice; anything marked "to assess" needs a qualified reviewer before any claim is made about the product. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Wildlife (Protection) Act, 1972, and the Wild Ass Sanctuary in the Little Rann of Kutch (declared 1972) | India, Gujarat | Activities inside a protected area; the Indian wild ass is a Schedule I species | Every trial and use takes place inside the sanctuary | Co-design partner, with the project lead | Applies |
| G2 | Forest department access cards for Agariyas (yearly, 23 conditions as reported in 2023: heavy machinery barred, only the machines and technology of the 2004 to 2005 baseline, two brine wells, no inflammable substances) | India, Little Rann | Who may enter the Rann to make salt, and with what | A hand capstan has no engine or fuel, but it is a new device; whether it is "machinery" under the conditions is not stated | Co-design partner (written request to the forest department) | To assess |
| G3 | Survey and settlement of Agariya rights (provisional list, 2004 to 2005 baseline) | India, Little Rann | Which families may work pans | Trial families must be on the list; not a design matter | Co-design partner | Applies (to the users) |
| G4 | EU Machinery Directive 2006/42/EC, Article 2(a) | European Union (reference only) | Machinery with a drive "other than directly applied human or animal effort", and hand-powered assemblies "for lifting loads" | Reference for practice only: SaltDrag is hand powered and hauls; it lifts no load. Not in force in India | Design lead | Does not apply |
| G5 | Indian rules on machinery safety for hand tools used by self-employed workers | India | Guarding, rated loads, marking | None identified in this first pass | Design lead, with a safety consultant before any release | To assess |
| G6 | ISO 10547:2009, Polyester fibre ropes, double braid construction | International | Rope construction, marking and minimum breaking force | The 12 mm pull ropes and bridles (BOM 17, 18); the 7.7 working-load factor rests on the certificate (PR-010) | Design lead (purchase specification) | Applies; buy to it or with a test certificate |
| G7 | ISO 2307, Fibre ropes: determination of certain physical and mechanical properties | International | How a rope's breaking force is tested | The rope certificate asked for in SDG-DEC-001 (to confirm 1) | Design lead | Applies |
| G8 | ISO 1461, Hot dip galvanized coatings on fabricated iron and steel articles (IS 4759 is the Indian standard for hot-dip zinc coatings, to confirm the equivalence) | International, India | Coating thickness by steel thickness | Every galvanised steel part (BOM 1 to 3, 9, 10, 12) | Fabricator, checked by the design lead | Met by design (specified in the BOM) |
| G9 | IS 2062 (structural steel, grade E275) and EN 10025-2 (S275) | India, Europe | Plate and section strength | Cheeks, plates and the pawl boss are specified S275; IS 2062 E275 is the Indian grade with the same 275 MPa yield | Design lead | Met by design |
| G10 | IS 4923 (hollow sections, YSt 310) and EN 10210 (S355J2H) | India, Europe | Drum barrel tube | The 168.3 x 6.3 mm barrel (SDG-DEC-001 D18) | Design lead | Met by design |
| G11 | ISO 4017, ISO 4032, ISO 7089, ISO 10642, ISO 2341, ISO 1234 | International | Bolts, nuts, washers, countersunk bolts, clevis pins and split pins | Every fastener in the model and BOM 19 | Fabricator | Met by design |
| G12 | Chain and turnbuckle working load limits (grade 30 proof-coil class as specified) | US class designation; Indian equivalent to find | Rated load of the anchor chains, shackles and turnbuckles | The 2.4 margin on the chain line (PR-003) rests on a 7.8 kN WLL | Design lead (purchase specification) | To assess |
| G13 | ISO 7243 (heat stress, WBGT) and heat action guidance in India | International, India | Work and rest in the heat | Work organisation in the March and April harvest (SDG-STM-001 S16) | Co-design partner | To assess |
| G14 | FSSAI rules on common salt (non-iodised common salt may not be sold for direct human consumption) and food-contact plastics | India | Salt sold for food; materials touching food | Applies to the salt the families sell, not to the tool; the blade and skids touch raw salt, so a food-contact grade of UHMW-PE is preferred | Co-design partner (salt grade); design lead (material grade) | To assess |
| G15 | Patents: CA1243940A (salt harvester, expired) and CN102476810A (salt-pan rake) | Canada, China | Prior art and claims | No motorised harvester is used; the claims of CN102476810A to be reviewed before any release (SDG-PRC-001) | Project lead | To assess |
| G16 | CERN-OHL-S-2.0 (hardware) and MIT (software) | International | Open licensing | Whole repository (REUSE.toml) | Project lead | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- Mongabay India (2023), "Role of traditional salt workers in wild ass conservation recognised; get back access to Little Rann of Kutch," 19 October 2023, checked 2026-10-25. https://india.mongabay.com/2023/10/role-of-traditional-salt-workers-in-wild-ass-conservation-recognised-get-back-access-to-little-rann-of-kutch/
- Drishti IAS (2023), "Saltpan workers of Little Rann of Kutch," 24 July 2023 (sanctuary declared in 1972; wild ass in Schedule I), checked 2026-10-25. https://www.drishtiias.com/daily-updates/daily-news-analysis/saltpan-workers-of-little-rann-of-kutch
- ICSF, "Gujarat: In Kutch, booming salt business puts traditional salt Agariyas up against ginger prawn fishers" (registration on condition of two-foot bunds and no machine use). https://icsf.net/newss/gujarat-in-kutch-booming-salt-business-puts-traditional-salt-agariyas-up-against-ginger-prawn-fishers/
- Directive 2006/42/EC of the European Parliament and of the Council on machinery, Article 2, checked 2026-10-25. https://www.legislation.gov.uk/eudr/2006/42/body/data.html
- ISO 10547:2009, Polyester fibre ropes: double braid construction, checked 2026-10-25. https://www.iso.org/standard/45997.html
- FSSAI (2019), notification prohibiting the sale of non-iodised common salt, checked 2026-10-25. https://fssai.gov.in/upload/media/FSSAI_News_Salt_FNB_16_07_2019.pdf
- ISO 1461, ISO 2307, ISO 7243, ISO 4017, ISO 4032, ISO 7089, ISO 10642, ISO 2341, ISO 1234, IS 2062, IS 4923, IS 4759, EN 10025-2, EN 10210: titles as given in Table 1; editions to confirm when parts are specified for purchase (TRL 4).
