---
doc_id: SDG-BLD-001
title: SaltDrag prototype build plan
project: SaltDrag
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First build plan; design made constructable (SDG-DDR-002)
---

# SaltDrag prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. One capstan, one bund roller and one rope are shown; the set has two of each.*

The prototype is one SaltDrag set: two identical hand capstans, two bund rollers, two 45 m pull ropes and one 3 m rake. Each capstan is a pair of galvanised steel side frames bolted together by three cross tubes, carrying a welded drum, a gear pair, a ratchet and pawl, a band brake, a gear guard and two crank handles, and held to the ground by two chains and screw-in anchors. The rake is a green FRP box beam with a white plastic blade bolted to its front, three plastic skids, stainless end caps for the bridles and two salt-filled ballast bags. Figure 1 shows the 20 kinds of component in the order you make or fit them. Thirteen are made in a town workshop: the side frames, cross tubes, drum, crank shaft, crank handles, ratchet and pawl, brake, gear guard, roller saddle, and the drilled beam, blade, skids and end caps. The gears, bearings, anchors, chains, ropes, bridles, fasteners and bags are bought. The work is cutting, drilling and welding steel plate and tube, some lathe work on the drum, galvanising, and drilling plastic and FRP. The parts cost about USD 2,803 for the whole set, from the bill of materials.

> **Safety:** This is rope and lifting-class equipment. A loaded rope can whip back if it breaks or slips, cranks and gears can trap hands, and a ground anchor can pull out. Do not load any part until section 6 says so. Welding and galvanised steel give off fumes: weld only bare steel and galvanise afterwards, in a ventilated space. Drilling FRP makes glass dust: wear a dust mask and gloves. Parts weigh up to 24 kg: lift in pairs.

## 2. What changed to make it buildable

The concept showed what SaltDrag does; it did not say how any part is made or fixed. Each change below keeps what the set does, and all of them are recorded in decision record SDG-DDR-002.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Capstan frame | A portable geared drum | Two side frames bolted together by three cross tubes (Figures 2 and 4) | Each piece weighs under 21 kg; the drum fits between the cheeks |
| Capstan position | Staked on the bund | On dry ground behind the bund, with a roller saddle on the crest (Steps 16 and 17) | The crest is too narrow to crank on; the roller keeps the rope off the bund |
| Drum | A drum | Welded pipe barrel and flanges, brake rim, shaft welded through (Figure 5) | Holds 58 m of rope; carries the brake |
| Ratchet and pawl | A pawl | The pawl on a 40 mm boss welded to the cheek (Figure 12) | A plain pin would bend at twice the rated pull |
| Brake | A brake | A lined band round the brake rim, worked by a lever through the cheek (Figure 14) | Holds the rated pull with about 92 N on the lever |
| Anchoring | Screw or plate anchors | An ear on each cheek at rope height, shackle, chain and turnbuckle to a screw-in anchor (Figure 3) | The capstan cannot tip |
| Rake | Bolted sections | One 3 m FRP beam, blade bolted on with crush sleeves, skids on slotted hangers, end caps with eye plates (Figures 18 to 24) | Light, rust-free, and the bridles pull on parts made for the load |
| Ballast | None | Two salt-filled bags on the beam (Step 18) | Keeps the blade down as the rope steepens near the bund |
| Windrow board | A board at the bund edge | Removed | The rake lifts about 3.3 m from the bund toe, so the windrow forms there |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in the pan looking at the capstan (the ratchet and brake are on the left, the gears on the right). "Ahead" is toward the pan, "behind" is away from it. Heights are from the ground under the capstan. Workshop tolerance is 1 mm on steelwork and 0.5 mm on holes and shafts unless a step says otherwise; drawings carry no tolerances before TRL 4.

### 3.1 Side frames (make 4)

![Figure 2. Making sketch of a side frame](../cad/drawings/SDG-DWG-101.png)

*Figure 2. Side frame making sketch (SDG-DWG-101); a left frame, with the pawl boss, is shown.*

**What it is and what it is made from.** Each capstan has a left and a right side frame: a tall steel cheek plate welded on a box-section runner that sits on the ground like a sledge. S275 steel plate 6 mm, and square hollow section 40 x 40 x 3 mm, 900 mm long. The two left frames also carry a short round boss for the pawl.

**How to make it.**

1. Cut the cheek from 6 mm plate: a trapezoid 660 wide at the base, 220 wide at the top and 860 tall, with the ear at the rear (a tab 70 tall ending in a 35 mm radius, centred 230 behind the drum centre line and 650 above the ground).
2. Mark the drum centre line square to the base. All hole positions are measured ahead or behind this line and up from the ground (the base edge of the cheek is 40 up).
3. Drill the 60 mm drum hole at 560 up and the 40 mm crank shaft hole at 756 up, both on the centre line.
4. Drill the bearing bolt holes: four 14 mm holes on a 102 mm square round the drum hole, four 12 mm holes on a 70 mm square round the crank shaft hole.
5. Drill the cross tube bolt holes: pairs of 11 mm holes 50 apart, at 240 ahead and 110 up, 240 behind and 110 up, and on the centre line at 850 up.
6. Drill the 22 mm hole in the ear, the 25 mm pawl bolt hole at 130 behind and 690 up, and the 21 mm brake pivot hole at 200 behind and 330 up. Drill these in all four frames, so any frame can be used either side.
7. Drill three 9 mm holes for the gear guard spacers, 190 from the drum hole centre: ahead, behind and below it (right frames only).
8. Cut the runner 900 long; it extends 400 ahead of and 500 behind the drum centre line. Weld the cheek on the runner's centre line, fillet welds both sides.
9. Left frames: weld a 40 mm OD, 24 mm bore tube 52 long on the outside face over the pawl hole, square to the plate.
10. Deburr, then hot-dip galvanise. Run a drill through the bolt holes afterwards.

**How it fits the parts next to it.** The cross tubes' end plates sit flat on the inner face of the cheek, two M10 bolts each (Figure 3a). The bearings bolt to the outer face. The ear takes a 10 mm bow shackle and the anchor chain, which runs back and down to the ground anchor (Figure 3).

![Figure 3a. Joint 1: cross tube end plate to the cheek](05-build-plan/joint-01.png)

*Figure 3a. Cross tube end plate on the inner face of the cheek.*

![Figure 3. Joint 7: anchor chain to the cheek ear](05-build-plan/joint-07.png)

*Figure 3. Shackle through the ear, chain running back to the anchor.*

**Check before moving on.** Stand a left and a right frame up 406 mm apart (centres) and pass a straight 40 mm rod through both drum holes and a 25 mm rod through both crank shaft holes: both rods must pass without forcing.

### 3.2 Cross tubes (make 6)

![Figure 4. Making sketch of a cross tube](../cad/drawings/SDG-DWG-102.png)

*Figure 4. Cross tube making sketch (SDG-DWG-102).*

**What it is and what it is made from.** Three per capstan, all the same: square hollow section 40 x 40 x 3 mm with an 80 x 80 x 6 mm end plate welded on each end.

**How to make it.**

1. Cut the tube 382 long, ends square.
2. Cut two 80 x 80 mm plates and drill two 11 mm holes in each, 25 each side of the centre.
3. Weld a plate on each end, centred, so the length over both plates is 394. Weld all round and grind flush on the outer faces.
4. Galvanise, then run a drill through the holes.

**How it fits the parts next to it.** The plates sit flat on the inner faces of the two cheeks (Figure 3a): front low (240 ahead, 110 up), rear low (240 behind, 110 up) and top (on the centre line, 850 up). Two M10 bolts each end.

**Check before moving on.** 394 over the plates, within 1 mm; the plates are parallel.

### 3.3 Drum (make 2)

![Figure 5. Making sketch of the drum](../cad/drawings/SDG-DWG-103.png)

*Figure 5. Drum making sketch (SDG-DWG-103).*

**What it is and what it is made from.** The drum stores the pull rope. A barrel of steel pipe 168.3 x 4.5 mm, 280 long; two flanges of 6 mm plate, 330 diameter; a brake rim of 50 x 6 mm flat bar on the left flange; and a 40 mm C45 (EN8) bright steel shaft, 592 long, welded right through.

**How to make it.**

1. Cut the barrel 280 long, ends square. Cut two 330 mm discs from 6 mm plate with a 40.5 mm centre hole.
2. Drill a 14 mm rope hole in the right flange, 94 above the centre (just outside the barrel).
3. Roll the 50 x 6 flat bar to a ring 330 outside diameter, butt weld it, and weld it to the outside face of the left flange, flush with its edge.
4. Slide both flanges and the barrel onto the shaft. The right flange's outer face is 185 right of the shaft's middle; the left flange's outer face is 107 left of it. Tack, check square, then weld the flanges to the barrel all round and to the shaft.
5. Cut a 12 mm keyway 40 long at each shaft end, for the gear (right) and the ratchet wheel (left).
6. Turn the brake rim true on the shaft in a lathe (within 0.5 mm).
7. Galvanise the barrel and flanges with the shaft ends masked; grease the shaft ends.

**How it fits the parts next to it.** The shaft runs in a 40 mm flange bearing on each cheek; the right flange stands 15 clear of the right cheek and the brake rim 43 clear of the left one. The gear is keyed on the right shaft end, 10 clear of the bearing (Figure 6).

![Figure 6. Joint 2: drum shaft, bearing, cheek and gear](05-build-plan/joint-02.png)

*Figure 6. Cut through the shaft centre: shaft, bearing, cheek and gear.*

**Check before moving on.** Spin the drum on its shaft between centres: the brake rim runs true within 0.5 mm and the flanges within 2 mm. It weighs about 21 kg.

### 3.4 Crank shaft and pinion (make 2)

![Figure 7. Making sketch of the crank shaft](../cad/drawings/SDG-DWG-104.png)

*Figure 7. Crank shaft with pinion making sketch (SDG-DWG-104).*

**What it is and what it is made from.** C45 bright steel bar 25 mm, 690 long, with a bought pinion: module 4, 14 teeth, 35 mm face, bored 25 mm.

**How to make it.**

1. Cut the bar 690 long and chamfer the ends.
2. Cut an 8 mm keyway 40 long, from 253 to 289 right of the bar's middle.
3. Drill 8 mm cross holes 20 in from each end, for the crank pins.
4. Key the pinion on and lock its set screw once it is in place (Step 6).

**How it fits the parts next to it.** The shaft runs in two 25 mm flange bearings, 756 up and 196 above the drum centre. The pinion sits outside the right bearing and meshes the gear inside the guard (Figure 8).

![Figure 8. Joint 3: gear and pinion in mesh](05-build-plan/joint-03.png)

*Figure 8. Gear and pinion in mesh, guard cut away at the front.*

**Check before moving on.** The shaft turns by hand in its bearings; with the pinion in mesh, a feeler gauge shows 0.2 to 0.5 mm of backlash.

### 3.5 Crank handles (make 4)

![Figure 9. Making sketch of a crank handle](../cad/drawings/SDG-DWG-105.png)

*Figure 9. Crank handle making sketch (SDG-DWG-105).*

**What it is and what it is made from.** A right and a left handle per capstan, mirror images: a hub of thick-wall tube 50 x 12.5 mm, an arm of 40 x 10 mm flat bar and a 32 mm grip turning on a 16 mm pin. Galvanised.

**How to make it.**

1. Cut the hub 40 long and bore it to 25 mm. Drill an 8 mm cross hole 20 from its inner end.
2. Cut the arm and round both ends to 20 radius; the shaft and grip centres are 330 apart.
3. Weld the arm to the outer end of the hub, square to it.
4. Weld the 16 mm pin to the arm's free end, slide on the 120 mm grip tube and a washer, and fit a split pin.
5. Galvanise; grease the grip pin.

**How it fits the parts next to it.** The hub slides onto the crank shaft end and is held by an 8 mm cross pin and R-clip through hub and shaft (Figure 10). The two handles on a capstan sit 180 degrees apart.

![Figure 10. Joint 6: crank hub on the shaft end](05-build-plan/joint-06.png)

*Figure 10. Crank hub on the shaft end, outside the guard.*

**Check before moving on.** The grip spins freely; with the pin in, the hub cannot slide off.

### 3.6 Ratchet wheel and pawl (make 2 sets)

![Figure 11. Making sketch of the ratchet wheel and pawl](../cad/drawings/SDG-DWG-106.png)

*Figure 11. Ratchet wheel and pawl making sketch (SDG-DWG-106).*

**What it is and what it is made from.** C45 plate, laser or flame cut: the wheel from 20 mm, the pawl from 16 mm. An M24 bolt is the pawl's pivot; a stainless spring keeps it in the teeth.

**How to make it.**

1. Cut the wheel 200 diameter with 20 teeth: each tooth rises 14 mm along the circle and drops straight back to the root.
2. Bore it 40 mm with a 12 mm keyway; drill and tap a set screw hole.
3. Cut the pawl: a 40 mm round end with a 25 mm hole, tapering to an 8 mm tip; harden the tip.
4. Drill a 6 mm hole near the pawl's tip end for the spring.

**How it fits the parts next to it.** The wheel is keyed on the left drum shaft end, 10 clear of the bearing. The pawl turns on the M24 bolt through its hole, the boss and the cheek, with a nyloc nut inside; its tip drops onto the face of a tooth (Figure 12). The spring runs from the pawl to a 6 mm hole in the ear.

![Figure 12. Joint 4: pawl seated on a ratchet tooth](05-build-plan/joint-04.png)

*Figure 12. Pawl on its boss, seated against a tooth face (spring not drawn).*

**Check before moving on.** Turn the drum to wind rope in: the pawl clicks into every tooth. Try to turn it back: the pawl holds.

### 3.7 Brake band and lever (make 2)

![Figure 13. Making sketch of the brake band and lever](../cad/drawings/SDG-DWG-107.png)

*Figure 13. Brake band and lever making sketch (SDG-DWG-107).*

**What it is and what it is made from.** A steel strip 40 x 3 mm lined with 5 mm woven brake lining; two end links of 10 mm bar; a 20 mm pivot shaft with a short inner arm and a 450 mm lever of 25 mm bar outside.

**How to make it.**

1. Cut the strip about 760 long and roll it to 340 inside diameter. Rivet the lining inside with countersunk rivets.
2. Form a loop at each end and fit a link.
3. Weld the inner arm to the pivot shaft so its end is 50 from the shaft centre; weld the lever to the shaft's outer end, rising at 62 degrees toward the rear when the brake is off. Weld a grip at the top.

**How it fits the parts next to it.** The band wraps about 245 degrees round the brake rim, open toward the lever. Its upper end links to the pivot shaft and its lower end to the inner arm (Figure 14). The pivot shaft passes through the 21 mm hole in the left cheek. With the lever down the lining stands 2 to 3 mm off the rim; lifting the lever squeezes it on.

![Figure 14. Joint 5: brake band, rim and lever pivot](05-build-plan/joint-05.png)

*Figure 14. Brake band on the rim, both ends running to the lever at its pivot.*

**Check before moving on.** Lever up: the drum cannot be turned by hand at the rim. Lever down: it spins freely.

### 3.8 Gear guard (make 2)

![Figure 15. Making sketch of the gear guard](../cad/drawings/SDG-DWG-108.png)

*Figure 15. Gear guard making sketch (SDG-DWG-108).*

**What it is and what it is made from.** A cup of 2 mm steel sheet over the gear and pinion, on three 14 mm tube spacers with M8 bolts. Painted bright yellow.

**How to make it.**

1. Cut the face to the outline: a 400 mm circle round the gear centre joined by straight sides to a 100 mm circle round the crank shaft centre, 196 above. Cut a 32 mm hole for the crank shaft.
2. Roll a 50 mm wide strip and weld it round the face edge, making a cup 50 deep.
3. Weld three bolt bushes inside the rim at the spacer positions (190 from the gear centre, ahead, behind and below).
4. Cut the spacers 44 long. Paint the guard yellow.

**How it fits the parts next to it.** The guard bolts to the right cheek through the spacers, its open side toward the cheek; it stands 11 clear of the gear teeth and 3.5 round the crank shaft.

**Check before moving on.** No finger can reach the gear mesh from outside the guard.

### 3.9 Bund roller saddle (make 2)

![Figure 16. Making sketch of the bund roller saddle](../cad/drawings/SDG-DWG-109.png)

*Figure 16. Bund roller saddle making sketch (SDG-DWG-109).*

**What it is and what it is made from.** Two galvanised side plates of 6 mm steel on foot plates, tied by two 20 mm bars, carrying a UHMW-PE roller 100 diameter and 200 long with two 160 mm flanges on a 25 mm stainless axle.

**How to make it.**

1. Cut two side plates 300 x 140 with a 70 mm round boss at 100 up; drill the 26 mm axle hole at its centre.
2. Weld each plate on an 80 x 6 mm foot plate 300 long.
3. Weld the two tie bars between the side plates, 120 ahead and behind the axle and 40 up, so the plates are 236 apart (centres). Galvanise.
4. Bore the roller 26 mm; fit the two flanges on its ends.
5. Cut the axle 260 long and drill 8 mm R-clip holes 8 from each end.

**How it fits the parts next to it.** The roller turns on the axle between the side plates with 5 mm each side (Figure 17). The saddle sits astride the bund crest; the rope runs over the roller top, 150 above the crest.

![Figure 17. Joint 11: roller on its axle in the saddle](05-build-plan/joint-11.png)

*Figure 17. Cut through the axle: roller, flanges, axle and side plates.*

**Check before moving on.** The roller spins freely; the feet sit flat on a board.

### 3.10 Rake beam

![Figure 18. Making sketch of the rake beam](../cad/drawings/SDG-DWG-110.png)

*Figure 18. Rake beam making sketch (SDG-DWG-110).*

**What it is and what it is made from.** One pultruded FRP square tube 100 x 100 x 6 mm, 3,000 long.

**How to make it.**

1. Cut to 3,000 with a fine-tooth blade. Mark a centre line on the front face; all positions are from the middle.
2. Drill the ten blade bolt holes, 11 mm through both walls front to back, 50 above the beam's underside: 150, 450, 750, 1,050 and 1,350 each side of the middle.
3. Drill the skid hanger holes, 11 mm through, at the middle and 1,200 each side, 25 and 75 above the underside.
4. Drill the end cap holes, 13 mm top to bottom, 74 and 114 in from each end.
5. Drill slowly with a sharp bit, backed with wood; wear a dust mask. Seal every cut end and hole with resin.

**How it fits the parts next to it.** The blade bolts to its front face, the skid hangers to its back face and the end caps over its ends.

**Check before moving on.** Lay the blade on the beam: every hole lines up.

### 3.11 Rake blade

![Figure 19. Making sketch of the rake blade](../cad/drawings/SDG-DWG-111.png)

*Figure 19. Rake blade making sketch (SDG-DWG-111).*

**What it is and what it is made from.** UHMW-PE sheet 15 mm, 3,000 x 300.

**How to make it.**

1. Cut to size. Round the top corners to 20 radius; keep the bottom edge straight and square, as it is the gathering edge.
2. Drill the ten blade bolt holes 11 mm, 100 above the bottom edge, at the beam's positions, and countersink them on the front face so M10 countersunk heads sit 1 mm below the surface.
3. Drill the six skid hanger bolt holes 75 and 125 above the bottom edge at the middle and 1,200 each side, countersunk the same way.

**How it fits the parts next to it.** The back face sits flat on the beam's front face, its bottom edge 50 below the beam. M10 countersunk bolts pass through blade and beam, with a stainless crush sleeve inside the tube and a nyloc nut at the back (Figure 20).

![Figure 20. Joint 8: blade to beam, cut through a bolt](05-build-plan/joint-08.png)

*Figure 20. Cut through a blade bolt: blade, beam walls and crush sleeve.*

**Check before moving on.** The bottom edge is straight within 3 mm over its length.

### 3.12 Skids and hangers (make 3)

![Figure 21. Making sketch of a skid and hanger](../cad/drawings/SDG-DWG-112.png)

*Figure 21. Skid and hanger making sketch (SDG-DWG-112).*

**What it is and what it is made from.** A UHMW-PE skid 60 x 20 x 450 and an L-shaped hanger of 6 mm stainless 316 plate.

**How to make it.**

1. Cut the skid 450 long with a 45 degree nose, 14 mm deep, on its front bottom edge.
2. Drill two 11 mm holes 40 and 100 behind the nose, counterbored 20 mm and 12 deep from below so the bolt heads sit inside.
3. Bend the hanger plate, 60 wide, to an L: an upright leg 130 tall and a foot 120 long.
4. Cut two slots 11 wide and 24 long in the upright, centred 65 and 115 above the foot; drill two 11 mm holes in the foot to match the skid.

**How it fits the parts next to it.** The upright bolts flat to the beam's back face through its slots; the foot sits on the skid with two M10 bolts (Figure 22). The slots set the blade 5 to 25 mm above the floor.

![Figure 22. Joint 9: skid hanger on the beam](05-build-plan/joint-09.png)

*Figure 22. Skid hanger on the beam's back face, slots for height.*

**Check before moving on.** With all three skids on a flat floor and a 10 mm spacer under the blade, the edge is 10 mm up along its whole length.

### 3.13 End caps with eye plates (make 2)

![Figure 23. Making sketch of an end cap](../cad/drawings/SDG-DWG-113.png)

*Figure 23. End cap making sketch (SDG-DWG-113).*

**What it is and what it is made from.** A left and a right, mirror images, in stainless 316: a 6 mm sheet channel round the beam end with an end plate, and a 12 mm eye plate.

**How to make it.**

1. Fold the channel: top and bottom 126 long by 106 wide, rear 112 tall, inside width 100 so it slides on the beam; the front stays open for the blade.
2. Weld the end plate (121 x 112) across the end, reaching forward over the blade end.
3. Drill two 13 mm holes through top and bottom, 40 and 80 from the end plate.
4. Cut the eye plate 225 long front to back, standing 50 out from the end plate, with two 18 mm eyes 175 apart, the front eye 25 ahead of the blade face. Weld it to the end plate on both sides.

**How it fits the parts next to it.** The cap slides over the beam end, two M12 bolts with crush sleeves through cap and beam. The front eye takes the pull bridle and the rear eye the return bridle, each with a bow shackle (Figure 24).

![Figure 24. Joint 10: end cap, eye plate and bridles](05-build-plan/joint-10.png)

*Figure 24. End cap on the beam end, bridle legs shackled to the eyes.*

**Check before moving on.** A 10 mm bow shackle pin passes each eye.

### 3.14 Bought components

- **Spur gear (2):** module 4, 84 teeth, 30 mm face, C45, webbed; ordered bored 40 mm with a 12 mm keyway and set screw.
- **Flange bearings (8):** four-bolt, stainless insert in a thermoplastic housing; four 40 mm bore (102 mm bolt square), four 25 mm bore (70 mm bolt square).
- **Ground anchors (4):** helical, 20 mm rod 1.0 m long, one 150 mm helix, forged eye, galvanised.
- **Chains and turnbuckles (4 sets):** 8 mm grade 30 galvanised chain 1.4 m, M16 hook-and-eye turnbuckle, two 10 mm bow shackles each. Working load limits at least 7.8 kN (chain), 6 kN (turnbuckle).
- **Pull ropes (2):** 12 mm polyester double braid, 45 m, minimum breaking strength at least 25 kN, with a certificate; eye splice and thimble at the rake end, plain whipped end at the drum.
- **Bridles (2):** two 12 mm polyester legs about 2.5 m with spliced thimble eyes to a 1 t swivel; three 10 mm bow shackles each.
- **Fasteners:** stainless 316 M10 and M12 bolts, nyloc nuts, washers and 16 x 2 mm crush sleeves for the rake; galvanised M10, M12 and M8 bolts for the capstans.
- **Rope dampers (2), ballast bags and straps (2), maintenance kit:** as listed in the bill of materials. Fill the ballast bags on site with about 24 kg of salt each.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in. Build both capstans the same way.

### Step 1: cross tubes onto the left side frame

![Step 1](05-build-plan/step-01.png)

Two M10 bolts per plate, finger tight.

### Step 2: drum shaft into the left cheek

![Step 2](05-build-plan/step-02.png)

Feed the drum's long left shaft end through the 60 mm hole and rest the drum on blocks so the shaft sits central in the hole.

### Step 3: right side frame on

![Step 3](05-build-plan/step-03.png)

Over the right shaft end and onto the three tube plates; bolt all six plates and tighten.

### Step 4: drum bearings

![Step 4](05-build-plan/step-04.png)

Slide a 40 mm bearing onto each shaft end, four M12 bolts into the cheek each. Turn the drum, then tighten the set screws.

### Step 5: ratchet wheel and gear

![Step 5](05-build-plan/step-05.png)

Key the ratchet wheel onto the left shaft end and the gear onto the right, each 10 clear of its bearing; tighten the set screws.

### Step 6: crank shaft, its bearings and the pinion

![Step 6](05-build-plan/step-06.png)

Bolt the two 25 mm bearings to the cheeks, slide the crank shaft in from the right, key the pinion on in line with the gear and lock it. Grease the mesh.

### Step 7: pawl

![Step 7](05-build-plan/step-07.png)

M24 bolt through pawl, boss and cheek; nyloc nut inside, snug so the pawl swings freely. Hook on the spring.

### Step 8: brake band and lever

![Step 8](05-build-plan/step-08.png)

Slip the band over the brake rim from the side, pass the pivot shaft through the cheek, fit both end links. Set the lining 2 to 3 mm off the rim with the lever down.

### Step 9: gear guard

![Step 9](05-build-plan/step-09.png)

Three spacers and M8 bolts into the right cheek.

**Hold point.** Do not fit the crank handles until the guard is on.

### Step 10: crank handles

![Step 10](05-build-plan/step-10.png)

Handles 180 degrees apart; cross pin and R-clip each.

### Step 11: rope onto the drum

![Step 11](05-build-plan/step-11.png)

Pass the plain end through the hole in the right flange and knot it inside; leave five dead turns that are never unwound. Wind the rope on under light tension in even layers, leaving the drum over the top toward the pan.

### Step 12: blade onto the beam

![Step 12](05-build-plan/step-12.png)

Ten M10 countersunk stainless bolts from the front, crush sleeves inside the tube, nyloc nuts at the back. Tighten until the sleeves bear; do not crush the FRP.

### Step 13: skids

![Step 13](05-build-plan/step-13.png)

Hangers on the back face through their slots, skids on the hanger feet. Set the blade 10 mm up with a spacer and tighten.

### Step 14: end caps and bridles

![Step 14](05-build-plan/step-14.png)

Slide the caps on the beam ends, two M12 bolts each. Shackle the pull bridle legs to the front eyes and the return bridle legs to the rear eyes; mouse each shackle pin with wire.

### Step 15: roller into its saddle

![Step 15](05-build-plan/step-15.png)

Hold the roller between the side plates, push the axle through, fit both R-clips.

### Step 16: capstan behind the bund and anchored

![Step 16](05-build-plan/step-16.png)

Stand the capstan on firm, level ground with its drum 1.5 m behind the bund crest centre and square to the strip to be raked. Screw the two anchors in 1.7 m behind the drum, in line with the chains, until only the eye shows. Shackle the chains to the ears and take up the slack with the turnbuckles.

### Step 17: roller on the crest and rope to the rake

![Step 17](05-build-plan/step-17.png)

Set the saddle astride the crest in line with the drum. Walk the rope end round the pan on the bunds to the rake, lay it over the roller and shackle its eye to the pull bridle swivel. Rig the far capstan to the return bridle the same way.

### Step 18: ballast bags

![Step 18](05-build-plan/step-18.png)

Fill two bags with about 24 kg of salt each and strap them on the beam behind the blade, 800 each side of the middle.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of SDG-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Gear mesh and free running | R2 | Turn each capstan by hand with no rope load | Smooth; backlash 0.2 to 0.5 mm; no rubbing on the guard |
| Pawl holds | R11 | Wind in, let go of the cranks under a 0.5 kN load from a spring scale | The pawl catches within one tooth; nothing moves |
| Brake holds and pays out | R11 | Cranks removed, pawl lifted, 3 kN load from CalRig | The brake holds with 150 N or less on the lever and pays out smoothly as it is eased |
| Proof load | R3, R10 | CalRig in line with the rope, anchored capstan, load to 4.5 kN (1.5 times rated) and hold 2 min | No permanent set in shafts, frames, ears or bolts; rope and splices undamaged |
| Anchors on site | R11 | Pull each anchor in line with its chain to 2.25 kN (1.5 times its share of the rated pull) | It moves less than 25 mm and holds for 2 min |
| Crank force | R2 | Spring scale on a handle while two people wind the rake with a full heap | 120 N or less at each handle |
| Blade height | R4 | Rake on a flat floor | 10 mm under the blade along its length |
| Rope stored | R12 | Wind on the full 45 m | Four even layers or fewer; at least 24 mm of flange left |
| Weights | R6 | Weigh each part | None over 25 kg |
| Set-up time | R8 | Time two crews setting up from a pan's edge | 20 min or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any part is welded or galvanised.** Steel is bare; welding is done in a ventilated space with screens; nobody welds galvanised steel.
- **S2. Before the first rope load.** The rope certificate shows at least 25 kN; the splice and thimble are whole; every shackle is moused; the pawl clicks into every tooth; the gear guard is on.
- **S3. Before any load above 0.5 kN.** The capstan is anchored with both chains tight; the frame's bolts are tightened; the rope damper bag hangs on the rope mid-span; nobody stands in line with the rope, behind the rake or on the bund within 2 m of the rope.
- **S4. Before paying out under load.** Both crank handles are off; one person holds the brake lever; the pawl is lifted only after the brake is on.
- **S5. Before the proof load.** CalRig is in line with the rope, its own anchor is checked, and the crew stands clear to the sides. Load in steps of 1 kN; stop and unload at any noise, slip or bending.
- **S6. Before the first pass on a pan.** Both anchors have passed their on-site pull; the bund roller sits square on the crest; the far capstan crew has the brake; the pan is clear of people and animals; shade and water are set up and work is planned for the cooler hours.
- **S7. At every move to the next strip.** The rope is slack and the pawl and brake are on before chains are unshackled; anchors are re-set and re-tensioned before the next load.

## 7. Tools, skills and workspace

**Tools.** Plasma, oxy-fuel or laser cutting for 6 to 20 mm plate (or a supplier who cuts to drawing); metal-cutting bandsaw or cut-off saw; pillar drill with drills to 25 mm and a 60 mm hole saw or boring; MIG or stick welder; lathe with 400 mm swing for the drum rim and keyways (or a machine shop); keyway broach or milling; plate rolls for the brake band and rim (or a supplier); angle grinder; taps and dies to M24; spanners and a torque wrench to 200 N·m; carbide or HSS drills and a dust extractor for FRP; wood bits for UHMW-PE; rivet tools for the brake lining; spring scale to 500 N; access to a CalRig proof-load rig to at least 5 kN; scales to 50 kg; tape and a long straightedge.

**Skills.** A fabricator who welds structural steel and reads drawings; a machinist for the drum, keyways and shafts; a rigger or someone trained in rope and shackle work for rigging and proof loading. No certified trade is needed beyond a competent welder, but proof loading and rigging must be supervised by someone who has done it before.

**Workspace.** A fabrication shop with a 3.5 m clear bench or trestles for the rake; a ventilated welding bay; galvanising done by a galvanising works; a firm yard at least 50 m long for the proof load, with an anchor point rated above 10 kN.

**Personal protective equipment.** Welding helmet, gloves and jacket; safety glasses and hearing protection for cutting and grinding; dust mask and gloves for FRP; safety boots and rigger's gloves for rope work and lifting; hats, light clothing, shade and water for work in the pans.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/SDG-DWG-101` to `SDG-DWG-113`.
- General arrangement: `cad/drawings/SDG-DWG-001.pdf`, Rev P2.
- Calculations: `docs/04-calcs/01-sizing.md` (SDG-CAL-001 v0.2) and `docs/04-calcs/sizing.py`; strength [C1] to [C14], lift-off [D3] and [D4], set-up [D10], masses [E1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0002-design-for-construction.md` (SDG-DDR-002) and `docs/decisions/0001-trl2-review-decisions.md` (SDG-DDR-001).
- Requirements: `docs/03-requirements.md` (SDG-REQ-001 v0.3).
