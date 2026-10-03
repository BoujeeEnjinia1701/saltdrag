"""SaltDrag prototype build plan pictures (SDG-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SDG-DWG-101 to 113        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build123d as b  # noqa: E402
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, capstan_components, rake_components, roller_components, derived, bx, xcyl,  # noqa: E402
                   bund, rod, place, rope_points, layout)

OUT = ROOT / "docs" / "05-build-plan"
DATE = "2026-10-03"
D = derived(P)
CAP = capstan_components(P)
RK = rake_components(P)
RO = roller_components(P)
xo, xi = D["cheek_out"], D["cheek_in"]
dz, pz = P["drum_z"], D["pin_z"]

COL = {"frame_l": "#4B5563", "frame_r": "#4B5563", "xtube": "#6B7280", "drum": "#C2410C", "bearings": "#1D4ED8",
       "gear": "#B45309", "pinion": "#92400E", "ratchet": "#7C3AED", "pawl": "#9333EA", "brake": "#A21CAF",
       "guard": "#EAB308", "cranks": "#374151", "anchors": "#78716C", "rope": "#1E40AF", "beam": "#0F766E",
       "blade": "#CBD5E1", "skids": "#14B8A6", "hangers": "#64748B", "caps": "#94A3B8", "bolts": "#111827",
       "bridles": "#2563EB", "ballast": "#D6CFC0", "saddle": "#0E7490", "roller": "#F1F5F9", "axle": "#475569",
       "bund": "#C9BFA8"}


def part(name, shape, key, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, COL[key], None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The piece of a shape inside a box (for close-ups)."""
    try:
        s = shape & bx(x0, x1, y0, y1, z0, z1)
        return s if s is not None and s.volume > 1e-3 else None
    except Exception:
        return None


def split_lr(shape):
    """Right (+X) and left (-X) halves of a two-sided component, such as the bearings."""
    return win(shape, 0, 2000, -3000, 3000, -2000, 3000), win(shape, -2000, 0, -3000, 3000, -2000, 3000)


def xtubes():
    return CAP["xtube_front"].shape + CAP["xtube_rear"].shape + CAP["xtube_top"].shape


def rope_on_drum(layers=1):
    r = D["layers"][layers - 1][1] + P["rope_d"] / 2
    return xcyl(D["barrel_x"][0], D["barrel_x"][1], 0, dz, r) - xcyl(D["barrel_x"][0] - 1, D["barrel_x"][1] + 1, 0, dz, P["barrel"][0] / 2)


def rope_tail(length=900.0):
    r = D["layers"][0][1]
    return rod((40.0, 0.0, dz + r), (40.0, -length, dz + r), P["rope_d"] / 2)


BRG_R, BRG_L = split_lr(CAP["bearings"].shape)
BRG_DR = win(CAP["bearings"].shape, 0, 2000, -200, 200, dz - 100, dz + 100)
BRG_DL = win(CAP["bearings"].shape, -2000, 0, -200, 200, dz - 100, dz + 100)
BRG_PR = win(CAP["bearings"].shape, 0, 2000, -200, 200, pz - 70, pz + 70)
BRG_PL = win(CAP["bearings"].shape, -2000, 0, -200, 200, pz - 70, pz + 70)
CRANK_R, CRANK_L = split_lr(CAP["cranks"].shape)


# ----------------------------------------------------------------- overview
def overview():
    rk = b.Pos(-700, -3300, 0)
    ro = b.Pos(1700, 300, 0)
    items = [
        ("Side frames, left and right (4)", CAP["frame_l"].shape + CAP["frame_r"].shape, "frame_l", (0, 0, 0)),
        ("Cross tubes (6)", xtubes(), "xtube", (0, 0, 520)),
        ("Drum (2)", CAP["drum"].shape, "drum", (0, -700, 0)),
        ("Flange bearings (8)", CAP["bearings"].shape, "bearings", (0, 450, 250)),
        ("Ratchet wheel (2)", CAP["ratchet"].shape, "ratchet", (-600, 0, -150)),
        ("Spur gear, bought and bored (2)", CAP["gear"].shape, "gear", (600, -150, -100)),
        ("Crank shaft and pinion (2)", CAP["pinion"].shape, "pinion", (0, 300, 650)),
        ("Pawl and pivot bolt (2)", CAP["pawl"].shape, "pawl", (-750, 250, 300)),
        ("Brake band and lever (2)", CAP["brake"].shape, "brake", (-500, 650, -350)),
        ("Gear guard (2)", CAP["guard"].shape, "guard", (950, 0, 150)),
        ("Crank handles (4)", CAP["cranks"].shape, "cranks", (0, 0, 1000)),
        ("Pull rope, 45 m (2)", rope_on_drum(2), "rope", (-1100, -700, 0)),
        ("Anchors, chains, turnbuckles (4)", CAP["anchors"].shape, "anchors", (0, 300, 0)),
        ("Bund roller saddle and roller (2)", ro * (RO["saddle"].shape + RO["roller"].shape + RO["axle"].shape), "saddle", (0, 0, 0)),
        ("Rake beam", rk * RK["beam"].shape, "beam", (0, 0, 0)),
        ("Rake blade and bolts", rk * (RK["blade"].shape + RK["rake_bolts"].shape), "blade", (0, -600, 0)),
        ("Skids and hangers (3)", rk * (RK["skids"].shape + RK["hangers"].shape), "skids", (700, 650, -450)),
        ("End caps with eye plates (2)", rk * RK["caps"].shape, "caps", (0, 0, 450)),
        ("Bridles and swivels (2)", rk * RK["bridles"].shape, "bridles", (0, 0, 0)),
        ("Ballast bags (2)", rk * RK["ballast"].shape, "ballast", (0, 300, 800)),
    ]
    cap_keys = 13      # the first 13 items are the capstan's; spread them wider than the rake
    parts = [part(n, s, k, tuple(v * (1.6 if i < cap_keys else 1.0) for v in e)) for i, (n, s, k, e) in enumerate(items)]
    return bv.overview(parts, OUT / "overview.png", "SaltDrag prototype: every component, pulled apart",
                       subtitle="Numbered in build order; one capstan, roller and rope shown of the two built. Seen from the front right and above",
                       elev=22, azim=-52, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    out = []
    base = dict(project="SaltDrag", date=DATE)
    fl = CAP["frame_l"].shape
    fr = CAP["frame_r"].shape
    # 101 side frame (left frame shown: it carries the pawl boss)
    out.append(bv.component_sheet(
        Part("Side frame", fl, COL["frame_l"]), [Part("x", fr, ""), Part("x", xtubes(), ""), Part("x", CAP["drum"].shape, "")],
        dwg_no="SDG-DWG-101", title="SaltDrag capstan side frame (make 4): making sketch",
        material="S275 steel plate 6 mm and SHS 40 x 40 x 3 mm; hot-dip galvanised",
        view_shape=b.Rot(0, 0, 90) * fl, inset_view=(20, -35),
        notes=["Make 4: two per capstan. Left frames also get the pawl boss.",
               "Cheek: 6 mm plate, 660 wide at the base, 220 at the top, 860 tall;",
               "  base edge 40 mm up (it sits on the runner).",
               "Ear at the rear: 70 mm tall, round end R35, 22 mm hole 230 behind",
               "  the drum centre line and 650 mm above the ground.",
               "Drum hole 60 mm at 560 mm up; crank shaft hole 40 mm at 756 mm up.",
               "Bearing bolts: 14 mm holes on a 102 square (drum), 12 mm on a 70",
               "  square (crank shaft), centred on each hole.",
               "Cross tube bolts: 11 mm pairs 50 apart at the three tube positions.",
               "Pawl bolt 25 mm at 130 back, 690 up; brake pivot 21 mm at 200 back,",
               "  330 up. Drill both in all four frames.",
               "Runner: SHS 40 x 40 x 3, 900 long, 400 ahead of and 500 behind the",
               "  drum centre. Weld the cheek on its centre line, both sides.",
               "Left frames: weld a 40 OD, 24 bore boss 52 long on the outside",
               "  over the pawl hole. Galvanise after welding and drilling.",
               "Check: the drum and crank shaft holes of a pair line up on a rod."], **base))
    # 102 cross tube
    t = CAP["xtube_front"].shape
    out.append(bv.component_sheet(
        Part("Cross tube", t, COL["xtube"]), [Part("x", fl, ""), Part("x", fr, "")],
        dwg_no="SDG-DWG-102", title="SaltDrag capstan cross tube (make 6): making sketch",
        material="SHS 40 x 40 x 3 mm and plate 6 mm, S275; hot-dip galvanised",
        view_shape=t, inset_view=(22, -40),
        notes=["Make 6: three per capstan, all the same.",
               "Tube: SHS 40 x 40 x 3 mm, 382 mm long, ends square.",
               "End plates: 80 x 80 x 6 mm, two per tube, welded on centre so",
               "  the length over both plates is 394 mm (the gap between cheeks).",
               "Two 11 mm holes in each plate, 25 mm each side of the tube centre,",
               "  on the horizontal centre line.",
               "Weld all round; grind the weld flush on the outer faces.",
               "Galvanise; run a drill through the holes after galvanising.",
               "Fit: plates sit flat on the inner faces of the cheeks, two",
               "  M10 bolts each end. Positions: front low (240 ahead, 110 up),",
               "  rear low (240 behind, 110 up) and top (over the drum, 850 up).",
               "Check: 394 mm over the plates, within 1 mm, plates parallel."], **base))
    # 103 drum
    dr = CAP["drum"].shape
    out.append(bv.component_sheet(
        Part("Drum", dr, COL["drum"]), [Part("x", fl, ""), Part("x", fr, ""), Part("x", CAP["bearings"].shape, "")],
        dwg_no="SDG-DWG-103", title="SaltDrag capstan drum (make 2): making sketch",
        material="Pipe 168.3 x 4.5 mm, plate 6 mm, flat bar 50 x 6 mm, C45 bar 40 mm",
        view_shape=dr, inset_view=(22, -40),
        notes=["Make 2. Barrel: pipe 168.3 OD x 4.5 wall, 280 long, ends square.",
               "Flanges: two discs 330 OD, 6 mm plate, 40.5 mm centre hole.",
               "Rope hole: 14 mm in the right flange, 94 mm above the centre.",
               "Brake rim: 50 x 6 flat bar rolled to 330 OD, butt welded, welded",
               "  to the outside face of the left flange, flush with its edge.",
               "Shaft: C45 (EN8) bright bar 40 mm, 592 long. The right flange's",
               "  outer face is 185 mm right of the shaft centre (its middle).",
               "Weld flanges to barrel all round; weld shaft to both flanges.",
               "Keyways 12 mm wide, 40 long at both ends for the gear and ratchet.",
               "Turn the brake rim true on the shaft after welding (0.5 mm).",
               "Galvanise barrel and flanges; mask and grease the shaft ends.",
               "Fit: the shaft runs in the 40 mm flange bearings; 15 mm gap to",
               "  the right cheek, 43 mm to the left. Mass about 21 kg.",
               "Check: spin it on the shaft; the rim runs true within 0.5 mm."], **base))
    # 104 crank shaft and pinion
    ps = CAP["pinion"].shape
    out.append(bv.component_sheet(
        Part("Crank shaft", ps, COL["pinion"]), [Part("x", fl, ""), Part("x", fr, ""), Part("x", CAP["gear"].shape, "")],
        dwg_no="SDG-DWG-104", title="SaltDrag crank shaft with pinion (make 2): making sketch",
        material="C45 (EN8) bright bar 25 mm; bought pinion, module 4, 14 teeth",
        view_shape=ps, inset_view=(22, -40),
        notes=["Make 2. Shaft: C45 bright bar 25 mm, 690 long, ends chamfered.",
               "Keyway 8 mm wide, 40 long, for the pinion, from 253 to 289 mm",
               "  right of the shaft middle.",
               "Cross-pin holes 8 mm through, 20 mm in from each end, for the",
               "  crank hub pins.",
               "Pinion: bought, module 4, 14 teeth, 35 face, bored 25, keyed and",
               "  held by a set screw. Its teeth line up with the gear's face.",
               "Fit: the shaft runs in two 25 mm flange bearings on the cheeks,",
               "  756 mm above the ground and 196 mm above the drum centre.",
               "The pinion sits outside the right bearing, inside the guard.",
               "Check: the shaft turns by hand in its bearings with the pinion",
               "  meshing the gear; a feeler shows backlash of 0.2 to 0.5 mm."], **base))
    # 105 crank handle
    cr = CRANK_R
    out.append(bv.component_sheet(
        Part("Crank handle", cr, COL["cranks"]), [Part("x", ps, ""), Part("x", fr, ""), Part("x", CAP["guard"].shape, "")],
        dwg_no="SDG-DWG-105", title="SaltDrag crank handle (make 4): making sketch",
        material="Steel tube 50 x 12.5, flat bar 40 x 10, tube 32 OD, pin 16; galvanised",
        view_shape=cr, inset_view=(22, -40),
        notes=["Make 4: a right and a left handle per capstan (mirror images).",
               "Hub: 50 OD, 40 long, bored 25 for the shaft; 8 mm cross-pin hole",
               "  20 mm from the inner end. The hub slides on the shaft end.",
               "Arm: flat bar 40 x 10, 330 mm between the shaft and grip centres,",
               "  ends rounded R20; welded to the outer end of the hub.",
               "Grip: 32 mm tube 120 long turning on a 16 mm pin welded to the arm;",
               "  washer and split pin on the outer end.",
               "On the capstan the two handles sit 180 deg apart, so one person",
               "  pushes while the other pulls.",
               "Galvanise; grease the grip pin.",
               "Fit: hub against the shaft shoulder; cross pin and R-clip hold it.",
               "  Handles come off before any paying out under load.",
               "Check: the grip spins freely; the hub cannot slide off with the pin in."], **base))
    # 106 ratchet wheel and pawl
    rw = CAP["ratchet"].shape + CAP["pawl"].shape
    out.append(bv.component_sheet(
        Part("Ratchet and pawl", rw, COL["ratchet"]), [Part("x", fl, ""), Part("x", CAP["drum"].shape, ""), Part("x", BRG_L, "")],
        dwg_no="SDG-DWG-106", title="SaltDrag ratchet wheel and pawl (make 2 sets): making sketch",
        material="C45 plate 20 mm (wheel) and 16 mm (pawl), laser or flame cut",
        view_shape=rw, inset_view=(18, -130),
        notes=["Wheel: 200 OD, 20 teeth, 20 mm C45 plate. Each tooth rises",
               "  14 mm along the circle and drops straight back to the root.",
               "Bore 40 with a 12 mm keyway; set screw M10 in the hub side.",
               "Pawl: 16 mm C45 plate, 25 wide at the pivot (40 OD round end),",
               "  8 wide at the tip; 25 mm pivot hole; harden the tip.",
               "Pivot: M24 bolt through the pawl, the 40 mm boss and the cheek,",
               "  nyloc nut inside. Pivot 130 behind and 130 above the drum centre.",
               "Spring: stainless return spring from the pawl to a 6 mm hole in",
               "  the cheek ear, so the pawl always drops into the teeth.",
               "The pawl lets the drum wind rope in and stops it running back.",
               "Fit: the wheel goes on the drum shaft outside the left bearing,",
               "  10 mm clear of it; the pawl lies in the same plane.",
               "Check: wind by hand; the pawl clicks into every tooth and holds."], **base))
    # 107 brake band and lever
    br = CAP["brake"].shape
    out.append(bv.component_sheet(
        Part("Brake band and lever", br, COL["brake"]), [Part("x", fl, ""), Part("x", CAP["drum"].shape, "")],
        dwg_no="SDG-DWG-107", title="SaltDrag brake band and lever (make 2): making sketch",
        material="Steel strip 40 x 3 with 5 mm woven lining; bar 25 and 20 mm",
        view_shape=br, inset_view=(18, -130),
        notes=["Band: steel strip 40 x 3 mm, about 760 long, rolled to 340 ID;",
               "  woven brake lining 5 mm riveted inside with countersunk rivets.",
               "The band wraps about 245 deg round the brake rim on the left flange,",
               "  open toward the rear bottom.",
               "Ends: a 10 mm link from each end. The upper end goes to the pivot",
               "  pin; the lower end goes to the inner arm, 50 mm from the pivot.",
               "Pivot: 20 mm shaft through a 21 mm hole in the left cheek, 200",
               "  behind and 330 above the ground. Inner arm inside, lever outside.",
               "Lever: 25 mm bar, 450 long, rising at 62 deg toward the rear; grip",
               "  at the top. Lifting the lever tightens the band.",
               "A 92 N pull on the grip holds the rated 3 kN rope pull (estimate).",
               "Fit: lining 2 to 3 mm off the rim when the lever is down.",
               "Check: lever up, the drum cannot be turned by hand at the rim."], **base))
    # 108 gear guard
    gd = CAP["guard"].shape
    out.append(bv.component_sheet(
        Part("Gear guard", gd, COL["guard"]), [Part("x", fr, ""), Part("x", CAP["gear"].shape, ""), Part("x", ps, "")],
        dwg_no="SDG-DWG-108", title="SaltDrag gear guard (make 2): making sketch",
        material="Steel sheet 2 mm, tube 14 OD spacers, M8 bolts; painted yellow",
        view_shape=gd, inset_view=(22, -40),
        notes=["Outline: a 400 mm circle round the gear centre joined by straight",
               "  sides to a 100 mm circle round the crank shaft centre (196 above).",
               "Face: 2 mm sheet cut to the outline; 32 mm hole for the crank shaft.",
               "Rim: 2 mm strip 50 wide, rolled and welded round the face edge,",
               "  so the guard is a cup 50 deep, open toward the cheek.",
               "Spacers: three 14 OD tubes 44 long between the cheek and the cup",
               "  edge, at the front, rear and bottom, 190 from the gear centre.",
               "  M8 bolts through cup, spacer and cheek (drill the cheek 9 mm).",
               "Paint bright yellow so the moving gears are marked.",
               "Fit: 11 mm clear of the gear teeth, 3.5 mm round the crank shaft.",
               "Check: no finger can reach the gear mesh from outside the guard."], **base))
    # 109 bund roller saddle
    sad = RO["saddle"].shape + RO["roller"].shape + RO["axle"].shape
    out.append(bv.component_sheet(
        Part("Bund roller saddle", sad, COL["saddle"]), [Part("x", bund(P, 900, 0, 1).moved(b.Location((0, 900, -600))), "")],
        dwg_no="SDG-DWG-109", title="SaltDrag bund roller saddle (make 2): making sketch",
        material="S275 plate 6 mm, bar 20 mm, galvanised; UHMW-PE roller; 316 axle",
        view_shape=sad, inset_view=(24, -50),
        notes=["Side plates: two, 6 mm, 300 long x 140 tall, with a 70 mm round boss",
               "  at 100 up; 26 mm axle hole at its centre. 236 apart (centres).",
               "Foot plates: 80 x 6 mm, 300 long, welded under each side plate.",
               "Tie bars: two 20 mm round bars between the side plates, 120 ahead",
               "  of and behind the axle, 40 up. Weld, then galvanise.",
               "Roller: UHMW-PE 100 OD x 200 long, 26 mm bore; two UHMW-PE flanges",
               "  160 OD x 10 bolted or pressed on the ends.",
               "Axle: stainless 316, 25 mm, 260 long, R-clip holes 8 from each end.",
               "The saddle sits astride the bund crest with the rope over the roller,",
               "  so the rope never cuts the bund. Roller top 150 above the crest.",
               "Fit: 5 mm clear between the flanges and the side plates.",
               "Check: the roller spins freely; the feet sit flat on a board."], **base))
    # 110 rake beam
    bm = RK["beam"].shape
    out.append(bv.component_sheet(
        Part("Rake beam", bm, COL["beam"]), [Part("x", RK["blade"].shape, ""), Part("x", RK["caps"].shape, "")],
        dwg_no="SDG-DWG-110", title="SaltDrag rake beam: making sketch",
        material="Pultruded FRP square tube 100 x 100 x 6 mm, 3,000 mm",
        view_shape=bm, inset_view=(24, -50),
        notes=["One beam: FRP 100 x 100 x 6 mm square tube, cut to 3,000 mm.",
               "Mark a centre line on the front face. Positions are from the middle.",
               "Blade bolt holes, 11 mm through both walls, front to back,",
               "  110 mm above the floor line (50 above the beam's underside):",
               "  ten holes, 150 to 1,350 mm each side of the middle, 300 apart.",
               "Skid hanger holes, 11 mm through, at the middle and 1,200 each side,",
               "  25 and 75 mm above the beam's underside.",
               "End cap holes: 13 mm top to bottom, 74 and 114 mm in from each end,",
               "  on the centre line.",
               "Use a sharp HSS or carbide drill, slow, backed with wood; wear a",
               "  dust mask (glass fibre). Seal every cut end and hole with resin.",
               "Fit: the blade bolts with stainless crush sleeves inside the tube.",
               "Check: lay the blade on the beam; all holes line up."], **base))
    # 111 rake blade
    bl = RK["blade"].shape
    out.append(bv.component_sheet(
        Part("Rake blade", bl, COL["blade"]), [Part("x", bm, ""), Part("x", RK["skids"].shape, "")],
        dwg_no="SDG-DWG-111", title="SaltDrag rake blade: making sketch",
        material="UHMW-PE sheet 15 mm, 3,000 x 300 mm",
        view_shape=bl, inset_view=(24, -50),
        notes=["One blade: UHMW-PE 15 mm sheet, 3,000 long x 300 tall.",
               "Round the two top corners R20. Keep the bottom edge straight",
               "  and square: it is the gathering edge.",
               "Holes match the beam: 11 mm, countersunk on the front face so the",
               "  M10 countersunk heads sit 1 mm below the surface.",
               "Ten blade bolt holes 100 mm above the bottom edge, 150 to 1,350",
               "  each side of the middle, 300 apart.",
               "Six skid hanger bolt holes 75 and 125 mm above the bottom edge at",
               "  the middle and 1,200 each side.",
               "Drill with a sharp wood bit; clear the swarf; no heat.",
               "Fit: the back face sits flat on the beam's front face; the bottom",
               "  edge 50 mm below the beam, 10 mm above the floor in use.",
               "Check: the bottom edge is straight within 3 mm along its length."], **base))
    # 112 skid and hanger
    sk = win(RK["skids"].shape + RK["hangers"].shape, -100, 100, -100, 600, -10, 400)
    out.append(bv.component_sheet(
        Part("Skid and hanger", sk, COL["skids"]), [Part("x", bm, ""), Part("x", bl, "")],
        dwg_no="SDG-DWG-112", title="SaltDrag skid and hanger (make 3): making sketch",
        material="UHMW-PE 60 x 20 mm bar; stainless 316 plate 6 mm",
        view_shape=b.Rot(0, 0, 90) * sk, inset_view=(24, -50),
        notes=["Make 3. Skid: UHMW-PE bar 60 x 20, 450 long; cut a 45 deg nose",
               "  14 mm deep on the front bottom edge so it rides over crystals.",
               "Two 11 mm holes 40 and 100 mm from the back of the nose, counter-",
               "  bored 20 mm, 12 deep from below so the bolt heads sit inside.",
               "Hanger: stainless 6 mm plate 60 wide, bent to an L: upright leg",
               "  130 tall, foot 120 long.",
               "Upright: two slots 11 wide x 24 long, centred 65 and 115 above the",
               "  foot. The slots set the blade 5 to 25 mm above the floor.",
               "Foot: two 11 mm holes to match the skid.",
               "Fit: the upright bolts flat to the beam's back face with the blade",
               "  bolts' neighbours; the foot sits on the skid, M10 bolts.",
               "Set all three skids to the same height with a 10 mm spacer under",
               "  the blade edge on a flat floor.",
               "Check: blade edge 10 mm above the floor along its whole length."], **base))
    # 113 end cap
    cp = win(RK["caps"].shape, 0, 2000, -200, 400, -100, 400)
    out.append(bv.component_sheet(
        Part("End cap", cp, COL["caps"]), [Part("x", win(bm, 1200, 1600, -50, 200, 0, 300), ""),
                                          Part("x", win(bl, 1200, 1600, -50, 200, 0, 400), "")],
        dwg_no="SDG-DWG-113", title="SaltDrag end cap with eye plate (make 2): making sketch",
        material="Stainless 316 sheet 6 mm and plate 12 mm",
        view_shape=cp, inset_view=(24, -50),
        notes=["Make 2 (a left and a right, mirror images).",
               "Cap: 6 mm stainless folded to a channel round the beam end: top and",
               "  bottom 126 long x 106 wide, rear 112 tall; end plate 121 x 112",
               "  welded across the end, reaching forward over the blade end.",
               "Inside width 100, so the cap slides on the beam; front open for",
               "  the blade.",
               "Two 13 mm holes top and bottom, 40 and 80 mm from the end plate.",
               "Eye plate: 12 mm, 50 out from the end plate, 225 long front to",
               "  back; two 18 mm eyes 175 apart, the front eye 25 ahead of the",
               "  blade face. Weld to the end plate both sides.",
               "The front eye takes the pull bridle, the rear eye the return bridle.",
               "Fit: M12 bolts with crush sleeves through cap and beam.",
               "Check: a 10 mm bow shackle pin passes each eye."], **base))
    return out


# ----------------------------------------------------------------- joint close-ups
def joints():
    out = []
    fl, fr = CAP["frame_l"].shape, CAP["frame_r"].shape
    J = lambda n, parts, title, sub, **kw: out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", title, subtitle=sub, **kw))  # noqa: E731
    ty, tz = P["xtubes"]["front"]
    J(1, [part("Cheek (right side frame)", win(fr, 180, 230, ty - 90, ty + 90, tz - 90, tz + 90), "frame_r"),
          part("Cross tube end plate", win(CAP["xtube_front"].shape, 100, 200, ty - 60, ty + 60, tz - 60, tz + 60), "xtube")],
      "Joint 1: cross tube end plate to the cheek", "Two M10 bolts per end; the plate sits flat on the cheek's inner face",
      elev=20, azim=-150)
    J(2, [part("Cheek", win(fr, 190, 220, -110, 110, dz - 110, dz + 110), "frame_r"),
          part("Flange bearing, 40 mm", BRG_DR, "bearings"),
          part("Drum shaft and right flange", win(CAP["drum"].shape, 120, 300, -170, 170, dz - 170, dz + 170), "drum"),
          part("Gear (keyed)", win(CAP["gear"].shape, 250, 300, -200, 200, dz - 200, dz + 200), "gear")],
      "Joint 2: drum shaft, bearing, cheek and gear", "Cut through the shaft centre; four M12 bolts hold the bearing; 15 mm gap from flange to cheek",
      cut="+Y", elev=18, azim=-60)
    J(3, [part("Gear, 84 teeth", win(CAP["gear"].shape, 240, 300, -120, 120, dz + 60, pz + 60), "gear"),
          part("Pinion, 14 teeth", win(CAP["pinion"].shape, 240, 300, -60, 60, pz - 60, pz + 60), "pinion"),
          part("Guard (cut)", win(CAP["guard"].shape, 240, 310, -10, 220, dz + 40, pz + 70), "guard")],
      "Joint 3: gear and pinion in mesh, inside the guard", "Module 4 teeth, 196 mm centres; grease the mesh; guard cut away at the front",
      elev=10, azim=-20)
    J(4, [part("Ratchet wheel", CAP["ratchet"].shape, "ratchet"), part("Pawl", CAP["pawl"].shape, "pawl"),
          part("Pawl boss on the cheek", win(fl, -280, -195, 60, 200, 620, 760), "frame_l")],
      "Joint 4: pawl on its boss, seated on a ratchet tooth", "Seen from the left; the spring (not drawn) keeps the pawl in the teeth",
      elev=8, azim=180)
    J(5, [part("Brake band on the rim", win(CAP["brake"].shape, -170, -100, -260, 260, 300, 800), "brake"),
          part("Brake rim (left flange)", win(CAP["drum"].shape, -170, -100, -200, 200, 350, 780), "drum"),
          part("Lever pivot in the cheek", win(fl, -210, -195, 150, 250, 280, 380), "frame_l")],
      "Joint 5: brake band, rim and lever pivot", "Both band ends run to the lever at its pivot; lifting the lever squeezes the band on the rim",
      elev=8, azim=180)
    J(6, [part("Crank hub and arm", win(CRANK_R, 300, 360, -60, 200, pz - 60, pz + 300), "cranks"),
          part("Crank shaft end", win(CAP["pinion"].shape, 290, 350, -20, 20, pz - 20, pz + 20), "pinion"),
          part("Guard face", win(CAP["guard"].shape, 290, 305, -80, 80, pz - 80, pz + 60), "guard")],
      "Joint 6: crank hub on the shaft end", "8 mm cross pin and R-clip through hub and shaft; remove before paying out under load",
      elev=20, azim=-40)
    ey, ez = P["ear"][0], P["ear"][1]
    J(7, [part("Ear on the cheek", win(fr, 190, 220, ey - 60, ey + 50, ez - 50, ez + 50), "frame_r"),
          part("Shackle and chain", win(CAP["anchors"].shape, 150, 260, ey - 40, ey + 260, ez - 160, ez + 40), "anchors")],
      "Joint 7: anchor chain to the cheek ear", "10 mm bow shackle through the 22 mm ear hole; chain runs back and down to the ground anchor",
      elev=15, azim=-30)
    bl_x = 1050.0
    J(8, [part("Blade (UHMW-PE)", win(RK["blade"].shape, bl_x - 60, bl_x + 60, -5, 30, 0, 320), "blade"),
          part("Beam (FRP)", win(RK["beam"].shape, bl_x - 60, bl_x + 60, 10, 130, 50, 170), "beam"),
          part("Bolt and crush sleeve", win(RK["rake_bolts"].shape, bl_x - 30, bl_x + 30, -5, 140, 90, 130), "bolts")],
      "Joint 8: blade to beam, cut through a bolt", "M10 countersunk from the front; stainless sleeve inside the tube stops the bolt crushing it",
      cut="-X", elev=12, azim=-10)
    J(9, [part("Hanger (slotted)", win(RK["hangers"].shape, -50, 50, 100, 260, 0, 170), "hangers"),
          part("Skid", win(RK["skids"].shape, -50, 50, 0, 480, -5, 30), "skids"),
          part("Beam back face", win(RK["beam"].shape, -120, 120, 60, 116, 50, 170), "beam")],
      "Joint 9: skid hanger on the beam", "Loosen two bolts, slide the hanger in its slots to set the blade 5 to 25 mm above the floor",
      elev=20, azim=-130)
    J(10, [part("End cap and eye plate", win(RK["caps"].shape, 1300, 1600, -80, 200, 30, 200), "caps"),
           part("Beam end", win(RK["beam"].shape, 1300, 1500, 10, 120, 50, 170), "beam"),
           part("Blade end", win(RK["blade"].shape, 1300, 1500, -2, 20, 0, 320), "blade"),
           part("Bridle legs (front and rear)", win(RK["bridles"].shape, 1300, 1700, -400, 500, 80, 160), "bridles")],
       "Joint 10: end cap, eye plate and bridles", "Two M12 bolts through cap and beam; bow shackles join the bridle eyes to the eye plate",
       elev=25, azim=-40)
    roll = RO["roller"].shape
    J(11, [part("Side plate (saddle)", RO["saddle"].shape, "saddle"), part("Roller with flanges", roll, "roller"),
           part("Axle, 25 mm stainless", RO["axle"].shape, "axle")],
       "Joint 11: roller on its axle in the saddle", "Cut through the axle; 5 mm between each flange and its side plate; R-clips outside",
       cut="+Y", elev=20, azim=-40)
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(name, shape, key, e):
        return part(name, shape, key, e)
    fl, fr = CAP["frame_l"].shape, CAP["frame_r"].shape
    g = lambda name, s: part(name, s, "frame_l")  # noqa: E731
    LF = g("Left side frame", fl)
    TUB = g("Cross tubes", xtubes())
    st(1, [LF], [mv("Cross tubes (3)", xtubes(), "xtube", (300, 0, 0))],
       "cross tubes onto the left side frame", "Two M10 bolts per plate, finger tight for now", elev=22, azim=-40)
    DRM = g("Drum", CAP["drum"].shape)
    st(2, [LF, TUB], [mv("Drum", CAP["drum"].shape, "drum", (450, 0, 0))],
       "drum shaft into the left cheek", "Feed the long left shaft end through the 60 mm hole; rest the drum on blocks", elev=22, azim=-40)
    st(3, [LF, TUB, DRM], [mv("Right side frame", fr, "frame_r", (450, 0, 0))],
       "right side frame on", "Over the right shaft end; bolt all six tube plates and tighten", elev=22, azim=-40)
    FR = g("Right side frame", fr)
    st(4, [LF, TUB, DRM, FR], [mv("Right drum bearing", BRG_DR, "bearings", (250, 0, 0)), mv("Left drum bearing", BRG_DL, "bearings", (-250, 0, 0))],
       "drum bearings onto the shaft ends", "Slide on, four M12 bolts each into the cheek; tighten the set screws last", elev=22, azim=-40)
    BRGD = g("Drum bearings", BRG_DR + BRG_DL)
    base4 = [LF, TUB, DRM, FR, BRGD]
    st(5, base4, [mv("Ratchet wheel", CAP["ratchet"].shape, "ratchet", (-300, 0, 0)), mv("Gear, 84 teeth", CAP["gear"].shape, "gear", (300, 0, 0))],
       "ratchet wheel and gear onto the drum shaft", "Key, push on 10 mm clear of the bearings, set screws", elev=22, azim=-40)
    base5 = base4 + [g("Ratchet wheel", CAP["ratchet"].shape), g("Gear", CAP["gear"].shape)]
    st(6, base5, [mv("Crank shaft bearings (2)", BRG_PR + BRG_PL, "bearings", (0, 0, 220)),
                  mv("Crank shaft and pinion", CAP["pinion"].shape, "pinion", (650, 0, 0))],
       "crank shaft bearings, crank shaft and pinion", "Bolt the 25 mm bearings on; slide the shaft in from the right; key the pinion in mesh", elev=22, azim=-40)
    base6 = base5 + [g("Crank shaft", CAP["pinion"].shape + BRG_PR + BRG_PL)]
    st(7, base6, [mv("Pawl and pivot bolt", CAP["pawl"].shape, "pawl", (-300, 0, 0))],
       "pawl onto its boss", "M24 bolt through pawl, boss and cheek; nyloc nut inside; hook on the spring", elev=18, azim=-130)
    base7 = base6 + [g("Pawl", CAP["pawl"].shape)]
    st(8, base7, [mv("Brake band and lever", CAP["brake"].shape, "brake", (-350, 0, 0))],
       "brake band and lever", "Band over the rim from the side, pivot shaft through the cheek, both end links on", elev=18, azim=-130)
    base8 = base7 + [g("Brake", CAP["brake"].shape)]
    st(9, base8, [mv("Gear guard", CAP["guard"].shape, "guard", (350, 0, 0))],
       "gear guard over the gears", "Three spacers and M8 bolts into the right cheek", elev=22, azim=-40)
    base9 = base8 + [g("Gear guard", CAP["guard"].shape)]
    st(10, base9, [mv("Crank handles (2)", CRANK_R, "cranks", (250, 0, 0)), mv("Left crank handle", CRANK_L, "cranks", (-250, 0, 0))],
       "crank handles on", "Handles 180 deg apart; cross pin and R-clip each", elev=22, azim=-40)
    base10 = base9 + [g("Crank handles", CAP["cranks"].shape)]
    st(11, base10, [mv("Pull rope, first layer", rope_on_drum(1) + rope_tail(), "rope", (0, -400, 0))],
       "rope onto the drum", "Plain end through the flange hole, knotted inside; wind on tight, even layers over the top", elev=22, azim=-40)
    # rake
    bm, bl = RK["beam"].shape, RK["blade"].shape
    st(12, [part("Rake beam", bm, "beam")], [mv("Rake blade", bl + RK["rake_bolts"].shape, "blade", (0, -400, 0))],
       "blade onto the beam", "Ten M10 countersunk bolts from the front, sleeves inside the tube, nyloc nuts at the back", elev=25, azim=-50)
    rb = [part("Beam and blade", bm + bl, "beam")]
    st(13, rb, [mv("Skids and hangers (3)", RK["skids"].shape + RK["hangers"].shape, "skids", (0, 300, -200))],
       "skids onto the beam", "Hangers on the back face; set the blade 10 mm up with a spacer; tighten", elev=25, azim=-50)
    rb2 = rb + [part("Skids", RK["skids"].shape + RK["hangers"].shape, "beam")]
    st(14, rb2, [mv("End caps (2)", RK["caps"].shape, "caps", (0, 0, 250)), mv("Bridles (2)", RK["bridles"].shape, "bridles", (0, 0, 0))],
       "end caps and bridles", "Caps slide on the beam ends, two M12 bolts each; shackle each bridle leg to its eye", elev=25, azim=-50, label_done=False)
    # roller
    st(15, [part("Saddle", RO["saddle"].shape, "saddle")],
       [mv("Roller and axle", RO["roller"].shape + RO["axle"].shape, "roller", (0, 0, 300))],
       "roller into its saddle", "Hold the roller between the side plates, push the axle through, R-clips both ends", elev=25, azim=-40)
    # site
    L = layout(P)
    near_cap = [s for k, (c, s) in L.items() if k.startswith("near_") and c.bom not in (11, 12)]
    capg = near_cap[0]
    for s in near_cap[1:]:
        capg = capg + s
    nb = bund(P, 4000.0, 0.0, 1)
    gr = bx(-2000, 2000, D["drum_y"] - 2600, 5600, -800, 0)
    ctx = [part("Bund", nb, "bund"), part("Ground", gr, "bund")]
    anc = L["near_anchors"][1]
    st(16, [part("Capstan", capg, "frame_l")], [mv("Ground anchors and chains", anc, "anchors", (0, -600, 400))],
       "capstan behind the bund and anchored", "Drum 1.5 m behind the crest centre; screw the anchors in line with the chains; tighten the turnbuckles",
       context=ctx, elev=26, azim=-55)
    roller = L["near_saddle"][1] + L["near_roller"][1] + L["near_axle"][1]
    near, far = rope_points(P, rake_y=2500.0)
    rope = rod(near[0], near[1], 6) + rod(near[1], near[2], 6)
    rake = place(RK["beam"].shape + RK["blade"].shape + RK["caps"].shape + RK["bridles"].shape + RK["skids"].shape, 0, 2500.0)
    st(17, [part("Capstan", capg + anc, "frame_l"), part("Rake", rake, "beam")],
       [mv("Bund roller", roller, "saddle", (0, 0, 400)), mv("Pull rope to the bridle swivel", rope, "rope", (0, 0, 0))],
       "roller on the crest and rope to the rake", "Saddle astride the crest in line with the drum; rope over the roller to the bridle swivel",
       context=ctx, elev=26, azim=-55)
    ball = place(RK["ballast"].shape, 0, 2500.0)
    st(18, [part("Rake", rake, "beam")], [mv("Ballast bags (2)", ball, "ballast", (0, 0, 350))],
       "ballast bags onto the rake", "Fill two bags with about 24 kg of salt each; strap them on the beam behind the blade",
       elev=26, azim=-55, label_done=False)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    for w in what:
        r = globals()[w]()
        print(w, "done", r if isinstance(r, Path) else len(r))
