"""SaltDrag parametric model (build123d), TRL 3, constructable design (SDG-DDR-002), kit 1.9 interface.

Kit 1.9 (STANDARDS section 24): OPTIONS, PRINCIPLES, CHOSEN, OPTION_VIEWS, ALLOWED_CONTACTS and components(option)
are at the end of this file. Every concept option (SDG-OPT-001) is modelled at detail level D3 with
.kit/cad_parts.py and cad/src/sdg_parts.py; run `python .kit/cad_check.py --export` for the fidelity check and the
STEP files (cad/step/A/ and cad/step/<option>-assembly.step).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    saltdrag-capstan.step / .stl     one hand capstan with its anchor chains (two are built)
    saltdrag-rake.step / .stl        the rake: beam, blade, skids, end caps and bridles
    saltdrag-roller.step / .stl      one bund roller saddle (two are built)
    saltdrag-assembly.step           the working layout on a pan shortened to 7 m, with the bunds
and prints the constructability checks (python cad/src/model.py --check prints them only).

Three local frames, all in mm, Z up:
    capstan  X along the drum axis (parallel to the bund), the rope leaves the top of the drum
             toward -Y (the pan), ground at z = 0 under the drum axis.
    rake     X along the blade, the blade's front face at y = 0 facing -Y (the way the rake is
             pulled), the pan floor at z = 0.
    roller   X along the roller axis, the rope runs along Y, the bund crest at z = 0.
The layout (layout()) puts the near bund's inner toe at y = 0, the pan between y = 0 and
y = PAN_SHOWN, and turns the near capstan to face +Y. Main dimensions and interfaces only;
tolerances are TRL 4 work. The same PARAMS feed docs/04-calcs/sizing.py (SDG-CAL-001), the
general arrangement SDG-DWG-001 (cad/src/sheets.py), the concept media (cad/src/concept_media.py),
the build plan pictures (cad/src/build_plan_media.py) and the appearance model
(cad/src/product_model.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

PARAMS = {
    # ---------------------------------------------------------------- capstan (BOM 1 to 11)
    # 1 side frame: runner SHS (size, wall, y from, y to); cheek plate thickness, x of its centre,
    #   outline (base half-length at z_base, top half-length at z_top), anchor ear (y, z, radius, hole)
    "runner": (40.0, 3.0, -400.0, 500.0), "cheek_t": 6.0, "cheek_x": 203.0,
    "cheek": (330.0, 40.0, 110.0, 900.0), "ear": (230.0, 650.0, 35.0, 22.0),
    # 2 cross tubes: SHS size and wall, end plate (size, thickness), (y, z) of each tube
    #   end plate 100 along the bolt line by 80 high; bolt offset each side of the tube centre (SDG-DEC-001 D19:
    #   bolts at 36 mm so washers clear the tube's 5 mm fillet welds; was an 80 mm square plate with bolts at 25 mm)
    "xtube": (40.0, 3.0), "xplate": (100.0, 6.0), "xplate_h": 80.0, "xbolt": 36.0,
    "xtubes": {"front": (-240.0, 110.0), "rear": (240.0, 110.0), "top": (0.0, 850.0)},
    # 3 drum: axis height; barrel pipe OD, wall, length; flange OD, thickness; brake rim width,
    #   thickness; shaft diameter, x from, x to; x of the outer face of the right flange
    #   barrel 168.3 x 6.3 mm YSt 310 tube (SDG-DEC-001 D18; was 168.3 x 4.5 mm pipe, short of R3 under rope crushing)
    "drum_z": 560.0, "barrel": (168.3, 6.3, 280.0), "flange": (330.0, 6.0), "rim": (50.0, 6.0),
    #   drum shaft C45+QT, extended to -322 for the ratchet hub (SDG-DEC-001 D24; was -296)
    "dshaft": (40.0, -322.0, 296.0), "drum_right": 185.0,
    # gear hub (OD, x from, x to) and ratchet hub (OD, length outboard), keyed 12 x 8 (D24)
    "gear_hub": (80.0, 251.0, 295.0), "ratchet_hub": (70.0, 44.0),
    # 4, 5 spur gear pair, module 4: gear 84 teeth, face 30; pinion 14 teeth, face 35
    "module": 4.0, "z_gear": 84, "z_pinion": 14, "gear_face": 30.0, "pinion_face": 35.0,
    "gear_x0": 256.0, "pinion_x0": 253.5,
    # 5 crank shaft diameter and half-length; 9 crank: radius, arm (width, thickness), hub (OD, length),
    #   grip (OD, length); crank angle of the right handle from +Y toward +Z (deg)
    #   crank shaft stepped: 30 mm through the bearings, 25 mm outboard at the pinion and crank hubs (D24)
    "pshaft": (25.0, 345.0), "pshaft_brg": 30.0, "pshaft_step": 245.0, "crank_r": 330.0, "crank_arm": (40.0, 10.0), "crank_hub": (50.0, 40.0),
    "grip": (32.0, 120.0), "crank_angle": 60.0, "crank_x0": 305.0,
    # 6 flange bearings (housing square, flange thickness, overall length, bolt square, bolt dia)
    #   crank bearings UCF206 size for the 30 mm shaft (D24; was UCF205, 95 square, 70 bolt square); to confirm
    "brg_drum": (130.0, 16.0, 40.0, 102.0, 14.0), "brg_pin": (108.0, 14.0, 37.0, 83.0, 12.0),
    # 7 ratchet wheel (OD, teeth, thickness, x of inner face); pawl (pivot y, z; thickness; pin dia)
    "ratchet": (200.0, 20, 20.0, -256.0), "pawl": (130.0, 690.0, 16.0, 24.0, 40.0),
    # 8 brake band (width, thickness incl. lining, wrap deg), lever pivot (y, z), lever length
    #   brake lever 600 (D21; was 450) so 150 N holds the rated pull with a wet lining (friction 0.20)
    "band": (40.0, 8.0, 270.0), "lever_pivot": (200.0, 330.0), "lever_len": 600.0,
    # 10 gear guard: radius around the gear, radius around the pinion, sheet thickness, x from, x to
    "guard": (200.0, 50.0, 2.0, 250.0, 300.0),
    # guard spacers, (y, z) from the drum axis: 150 ahead and behind, 120 below; and 190 below (SDG-DEC-001 D19:
    #   the side holes were 190 ahead and behind at drum height, 2.5 mm from the cheek edge)
    "guard_sp": ((150.0, -120.0), (-150.0, -120.0), (0.0, -190.0)),
    # 11 anchors: anchor eye (y behind the drum axis, x), rod (dia, length, angle below horizontal),
    #   helix (dia, thickness); chain dia (drawn as a bar), turnbuckle body length
    "anchor_eye": (1700.0, 203.0), "anchor_rod": (20.0, 1000.0, 45.0), "helix": (150.0, 8.0),
    #   chain 10 mm grade 30 (D22; was 8 mm), drawn as links in components()
    "chain_d": 10.0, "chain_wire": 10.0, "turnbuckle": 220.0,
    # ---------------------------------------------------------------- rake (BOM 13 to 17)
    # 13 beam: FRP square tube size, wall, length; z of its underside; y of its front face
    "beam": (100.0, 6.0, 3000.0), "beam_z0": 60.0,
    # 14 blade: UHMW-PE thickness, height, ground gap (set by the skids), length
    "blade": (15.0, 300.0, 10.0, 3000.0),
    # 15 skids: UHMW-PE (width, thickness, length, y start behind the blade); x positions;
    #   hanger plate (thickness, width, horizontal leg length)
    "skid": (60.0, 20.0, 450.0, 20.0), "skid_x": (-1200.0, 0.0, 1200.0), "hanger": (6.0, 60.0, 120.0),
    # 16 end caps: plate thickness, length along the beam; eye plate (thickness, reach, front eye y, rear eye y, hole)
    #   eye plate centre height eye_z 66, at the foot of the end caps (D23; was at mid-height, 110)
    "cap": (6.0, 126.0), "eye": (12.0, 50.0, -25.0, 150.0, 18.0), "eye_z": 66.0,
    # 19 blade bolts: diameter, x pitch, height
    "blade_bolts": (10.0, 300.0, 110.0),
    # 17 bridle: apex distance in front of the blade and behind the beam; apex height
    "bridle": (2000.0, 2175.0, 70.0),     # apex height 70 (D23; was 130)
    # 22 ballast bags of salt on the beam (length along X, depth behind the blade, height); x of each centre
    "ballast": (550.0, 300.0, 120.0), "ballast_x": 800.0,
    # ---------------------------------------------------------------- roller saddle (BOM 12)
    # side plate (thickness, length along Y, height); x of plate centre; axle height, axle dia;
    # roller (OD, length), flanges (OD, thickness); foot plate (width, thickness); tie bar dia, y
    "saddle": (6.0, 300.0, 140.0), "saddle_x": 118.0, "axle": (100.0, 25.0, 272.0),   # axle 272 (was 260), D19
    "roller": (100.0, 200.0), "rflange": (160.0, 10.0), "foot": (80.0, 6.0), "tie": (20.0, 120.0),
    # ---------------------------------------------------------------- site (context, assumptions)
    # bund: height, crest width, base width; capstan drum axis behind the crest centre; rope dia
    "bund": (600.0, 400.0, 1800.0), "capstan_back": 1500.0, "rope_d": 12.0,
    "pan_design": 30000.0,      # design pan width, bund crest to bund crest (assumption)
    "pan_shown": 7000.0,        # pan width drawn in the layout and media (shortened)
    "rake_y": 3000.0,           # blade front face position in the layout
}

# BOM line numbers and names (bom/bom.csv)
BOM = {
    1: "Capstan side frame", 2: "Cross tubes", 3: "Drum", 4: "Spur gear, 84 teeth",
    5: "Crank shaft and pinion", 6: "Flange bearings", 7: "Ratchet wheel and pawl",
    8: "Brake band and lever", 9: "Crank handles", 10: "Gear guard",
    11: "Ground anchors, chains and turnbuckles", 12: "Bund roller saddle",
    13: "Rake beam", 14: "Rake blade", 15: "Skids and hangers", 16: "End caps with eye plates",
    17: "Bridles and swivels", 18: "Pull ropes", 19: "Fasteners", 20: "Rope dampers",
    21: "Maintenance kit", 22: "Ballast bags and straps",
}

DENSITY = {"steel": 7.85e-6, "stainless": 8.0e-6, "frp": 1.9e-6, "uhmw": 0.94e-6, "polyester": 1.0e-6,
           "brg": 3.0e-6, "salt": 1.2e-6}   # kg/mm3; "brg" is a housing average for stainless-insert polymer bearings


@dataclass
class Comp:
    name: str
    shape: object
    bom: int
    material: str = "steel"


def derived(p=PARAMS):
    m = p["module"]
    rg, rp = m * p["z_gear"] / 2, m * p["z_pinion"] / 2
    d = {"rg": rg, "rp": rp, "cd": rg + rp, "pin_z": p["drum_z"] + rg + rp, "ratio": p["z_gear"] / p["z_pinion"]}
    bo, bw, bl = p["barrel"]
    rope = p["rope_d"]
    turns = int(bl // rope) - 1
    layers, total = [], 0.0
    for n in range(1, 5):
        r = bo / 2 + rope / 2 + (n - 1) * rope * 0.866
        total += 2 * math.pi * r * turns / 1000
        layers.append((n, r, total))
    d.update(turns=turns, layers=layers, r_full=layers[-1][1], freeboard=p["flange"][0] / 2 - (layers[-1][1] + rope / 2))
    xr = p["drum_right"]
    ft = p["flange"][1]
    d.update(flange_r=(xr - ft, xr), barrel_x=(xr - ft - bl, xr - ft), flange_l=(xr - 2 * ft - bl, xr - ft - bl))
    d["rim_x"] = (d["flange_l"][0] - p["rim"][0], d["flange_l"][0])
    cx, ct = p["cheek_x"], p["cheek_t"]
    d.update(cheek_in=cx - ct / 2, cheek_out=cx + ct / 2)
    bund_h, crest, base = p["bund"]
    d.update(crest_y=-base / 2, roller_top=bund_h + p["axle"][0] + p["roller"][0] / 2)
    d["drum_y"] = d["crest_y"] - p["capstan_back"]
    return d


def _b():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def xcyl(x0, x1, y, z, r):
    """Cylinder along X from x0 to x1."""
    b = _b()
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def ycyl(x, y0, y1, z, r):
    b = _b()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def zcyl(x, y, z0, z1, r):
    b = _b()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, abs(z1 - z0))


def rod(a, c, r):
    """Round bar from point a to point c."""
    b = _b()
    a, c = b.Vector(*a), b.Vector(*c)
    v = c - a
    return b.Solid.make_cylinder(r, v.length, b.Plane(origin=a, z_dir=v))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def shs(x0, x1, y, z, size, wall, axis="x"):
    """Square hollow section of outside size, along X (or Y) from x0 to x1, centred on (y, z)."""
    if axis == "x":
        return bx(x0, x1, y - size / 2, y + size / 2, z - size / 2, z + size / 2) - \
            bx(x0 - 1, x1 + 1, y - size / 2 + wall, y + size / 2 - wall, z - size / 2 + wall, z + size / 2 - wall)
    return bx(y - size / 2, y + size / 2, x0, x1, z - size / 2, z + size / 2) - \
        bx(y - size / 2 + wall, y + size / 2 - wall, x0 - 1, x1 + 1, z - size / 2 + wall, z + size / 2 - wall)


def yz_plate(pts, x0, x1):
    """Plate in the YZ plane from a (y, z) outline, thickness from x0 to x1."""
    b = _b()
    face = b.Polyline(*[(y, z) for y, z in pts], close=True)
    f = b.make_face(face)
    sol = b.extrude(f, x1 - x0)
    return b.Location((x0, 0, 0)) * (b.Plane.YZ.location * sol)


def gear_profile(n, m, r_bore, face, x0, cy, cz, web=None, phase=0.0):
    """Spur gear (straight-flank teeth) along X from x0, centred on (cy, cz). web: (web thickness,
    rim depth, hub OD, number and diameter of lightening holes) for a webbed blank."""
    b = _b()
    rp = m * n / 2
    ra, rf = rp + m, rp - 1.25 * m
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n + phase
        da = 2 * math.pi / n
        for frac, r in ((0.0, rf), (0.18, rf), (0.30, ra), (0.45, ra), (0.57, rf)):
            a = a0 + frac * da
            pts.append((r * math.cos(a), r * math.sin(a)))
    prof = b.make_face(b.Polyline(*pts, close=True))
    g = b.extrude(prof, face)
    g = g - b.Pos(0, 0, face / 2) * b.Cylinder(r_bore, face + 2)
    if web:
        wt, rim, hub, nh, dh = web
        r_in = rf - rim
        recess = (face - wt) / 2
        for z0 in (0, face - recess):
            ring = b.Pos(0, 0, z0 + recess / 2) * (b.Cylinder(r_in, recess) - b.Cylinder(hub / 2, recess))
            g = g - ring
        rh = (r_in + hub / 2) / 2
        for k in range(nh):
            a = 2 * math.pi * k / nh
            g = g - b.Pos(rh * math.cos(a), rh * math.sin(a), face / 2) * b.Cylinder(dh / 2, face + 2)
    # local z -> world +X, local x -> world Y, local y -> world Z
    loc = b.Location(b.Plane(origin=(x0, cy, cz), x_dir=(0, 1, 0), z_dir=(1, 0, 0)))
    return loc * g


def ratchet_profile(od, n, t, x0, cy, cz, bore):
    b = _b()
    ro, rr = od / 2, od / 2 - 14
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        pts.append((rr * math.cos(a0), rr * math.sin(a0)))
        pts.append((ro * math.cos(a1 - 0.02), ro * math.sin(a1 - 0.02)))
    w = b.extrude(b.make_face(b.Polyline(*pts, close=True)), t)
    w = w - b.Pos(0, 0, t / 2) * b.Cylinder(bore / 2, t + 2)
    return b.Location(b.Plane(origin=(x0, cy, cz), x_dir=(0, 1, 0), z_dir=(1, 0, 0))) * w


def flange_bearing(x_face, outward, y, z, spec, bore):
    """4-bolt flange bearing on a cheek face at x_face, body toward 'outward' (+1 or -1)."""
    sq, ft, L, bs, bd = spec
    x1 = x_face + outward * ft
    hous = bx(min(x_face, x1), max(x_face, x1), y - sq / 2, y + sq / 2, z - sq / 2, z + sq / 2)
    boss_x1 = x_face + outward * L
    boss = xcyl(min(x_face, boss_x1), max(x_face, boss_x1), y, z, sq * 0.36)
    s = hous + boss - xcyl(min(x_face, boss_x1) - 1, max(x_face, boss_x1) + 1, y, z, bore / 2 + 0.01)
    for dy in (-bs / 2, bs / 2):
        for dz in (-bs / 2, bs / 2):
            s = s - xcyl(min(x_face, x1) - 1, max(x_face, x1) + 1, y + dy, z + dz, bd / 2)
    return s


# ====================================================================== capstan
def cheek_outline(p=PARAMS):
    hb, zb, ht, zt = p["cheek"]
    return [(-hb, zb), (hb, zb), (ht, zt), (-ht, zt)]


def capstan_components(p=PARAMS):
    """One hand capstan in its local frame. Returns {key: Comp}."""
    b = _b()
    D = derived(p)
    C = {}
    s_sz, s_w, ry0, ry1 = p["runner"]
    cx, ct = p["cheek_x"], p["cheek_t"]
    ey, ez, er, eh = p["ear"]
    dz, pz = p["drum_z"], D["pin_z"]
    brg_d, brg_p = p["brg_drum"], p["brg_pin"]
    for side, sg in (("r", 1), ("l", -1)):
        x0, x1 = sorted((sg * (cx - ct / 2), sg * (cx + ct / 2)))
        cheek = yz_plate(cheek_outline(p), x0, x1)
        cheek = cheek + bx(x0, x1, 120.0, ey, ez - er, ez + er) + xcyl(x0, x1, ey, ez, er)
        cheek = cheek - xcyl(x0 - 1, x1 + 1, ey, ez, eh / 2)
        cheek = cheek - xcyl(x0 - 1, x1 + 1, 0, dz, 30.0) - xcyl(x0 - 1, x1 + 1, 0, pz, 20.0)
        cheek = cheek - xcyl(x0 - 1, x1 + 1, p["pawl"][0], p["pawl"][1], p["pawl"][3] / 2 + 0.5)
        cheek = cheek - xcyl(x0 - 1, x1 + 1, p["lever_pivot"][0], p["lever_pivot"][1], 10.5)
        for spec, zc in ((brg_d, dz), (brg_p, pz)):
            for dy in (-spec[3] / 2, spec[3] / 2):
                for dz_ in (-spec[3] / 2, spec[3] / 2):
                    cheek = cheek - xcyl(x0 - 1, x1 + 1, dy, zc + dz_, spec[4] / 2)
        for (ty, tz) in p["xtubes"].values():
            for dy in (-p["xbolt"], p["xbolt"]):
                cheek = cheek - xcyl(x0 - 1, x1 + 1, ty + dy, tz, 5.5)
        if sg > 0:   # gear guard spacer bolt holes, 9 mm (right cheek)
            for (gy_, gz_) in p["guard_sp"]:
                cheek = cheek - xcyl(x0 - 1, x1 + 1, gy_, dz + gz_, 4.5)
        if sg < 0:   # pawl boss welded to the outside of the left cheek
            bx0, bx1 = p["ratchet"][3] + 2, -(cx + ct / 2)
            cheek = cheek + xcyl(bx0, bx1, p["pawl"][0], p["pawl"][1], p["pawl"][4] / 2) - \
                xcyl(bx0 - 1, bx1 + 1, p["pawl"][0], p["pawl"][1], p["pawl"][3] / 2 + 0.5)
        runner = shs(ry0, ry1, sg * cx, s_sz / 2, s_sz, s_w, axis="y")
        C[f"frame_{side}"] = Comp(f"Side frame ({'right' if sg > 0 else 'left'})", cheek + runner, 1)
    # 2 cross tubes with end plates, bolted to the cheek inner faces
    xs, xw = p["xtube"]
    ps, pt = p["xplate"]
    xi = D["cheek_in"]
    for key, (ty, tz) in p["xtubes"].items():
        t = shs(-xi + pt, xi - pt, ty, tz, xs, xw)
        for sg in (1, -1):
            x0, x1 = sorted((sg * xi, sg * (xi - pt)))
            pl = bx(x0, x1, ty - ps / 2, ty + ps / 2, tz - p["xplate_h"] / 2, tz + p["xplate_h"] / 2)
            for dy in (-p["xbolt"], p["xbolt"]):
                pl = pl - xcyl(x0 - 1, x1 + 1, ty + dy, tz, 5.5)
            t = t + pl
        C[f"xtube_{key}"] = Comp(f"Cross tube ({key})", t, 2)
    # 3 drum: barrel, two flanges, brake rim on the left flange, shaft right through
    bo, bw, bl = p["barrel"]
    fo, ft = p["flange"]
    sd, sx0, sx1 = p["dshaft"]
    bxr = D["barrel_x"]
    barrel = xcyl(bxr[0], bxr[1], 0, dz, bo / 2) - xcyl(bxr[0] - 1, bxr[1] + 1, 0, dz, bo / 2 - bw)
    fr = xcyl(*D["flange_r"], 0, dz, fo / 2) - xcyl(D["flange_r"][0] - 1, D["flange_r"][1] + 1, 0, dz, sd / 2)
    fl = xcyl(*D["flange_l"], 0, dz, fo / 2) - xcyl(D["flange_l"][0] - 1, D["flange_l"][1] + 1, 0, dz, sd / 2)
    rw, rt = p["rim"]
    rim = xcyl(*D["rim_x"], 0, dz, fo / 2) - xcyl(D["rim_x"][0] - 1, D["rim_x"][1] + 1, 0, dz, fo / 2 - rt)
    fr = fr - xcyl(D["flange_r"][0] - 1, D["flange_r"][1] + 1, 0, dz + bo / 2 + 10, 7.0)   # rope anchor hole
    shaft = xcyl(sx0, sx1, 0, dz, sd / 2)
    C["drum"] = Comp("Drum", barrel + fr + fl + rim + shaft, 3)
    # 6 bearings: drum shaft and crank shaft, on the outer cheek faces
    xo = D["cheek_out"]
    C["bearings"] = Comp("Flange bearings (4)", fuse([
        flange_bearing(xo, 1, 0, dz, brg_d, sd), flange_bearing(-xo, -1, 0, dz, brg_d, sd),
        flange_bearing(xo, 1, 0, pz, brg_p, p["pshaft_brg"]), flange_bearing(-xo, -1, 0, pz, brg_p, p["pshaft_brg"])]), 6, "brg")
    # 4 gear (webbed), 5 crank shaft with pinion
    m = p["module"]
    gh = p["gear_hub"]
    C["gear"] = Comp("Spur gear, 84 teeth", gear_profile(p["z_gear"], m, sd / 2, p["gear_face"], p["gear_x0"], 0, dz,
                                                         web=(12.0, 22.0, 80.0, 6, 60.0),
                                                         phase=math.pi / 2 - 0.875 * 2 * math.pi / p["z_gear"])
                     + (xcyl(gh[1], gh[2], 0, dz, gh[0] / 2) - xcyl(gh[1] - 1, gh[2] + 1, 0, dz, sd / 2)), 4)
    pd_, ph = p["pshaft"]
    pin = gear_profile(p["z_pinion"], m, pd_ / 2, p["pinion_face"], p["pinion_x0"], 0, pz,
                       phase=1.5 * math.pi - 0.375 * 2 * math.pi / p["z_pinion"])
    stp = p["pshaft_step"]
    C["pinion"] = Comp("Crank shaft and pinion", pin + xcyl(-ph, ph, 0, pz, pd_ / 2) + xcyl(-stp, stp, 0, pz, p["pshaft_brg"] / 2), 5)
    # 7 ratchet wheel on the left end of the drum shaft, and its pawl
    rod_, rn, rtk, rx0 = p["ratchet"]
    rh = p["ratchet_hub"]
    rhub = xcyl(rx0 - rtk - rh[1], rx0 - rtk, 0, dz, rh[0] / 2) - xcyl(rx0 - rtk - rh[1] - 1, rx0 - rtk + 1, 0, dz, sd / 2)
    C["ratchet"] = Comp("Ratchet wheel", ratchet_profile(rod_, rn, rtk, rx0 - rtk, 0, dz, sd) + rhub, 7)
    py, pzv, pth, pdia, pboss = p["pawl"]
    rr = rod_ / 2 - 14
    da = 2 * math.pi / rn
    k = int(math.atan2(pzv - dz, py) // da) - 0       # tooth face just below the pivot direction
    a_tip = k * da + 0.05
    tip = ((rr + 6) * math.cos(a_tip), dz + (rr + 6) * math.sin(a_tip))
    px0, px1 = rx0 - rtk + 2, rx0 - 2
    ux, uz = tip[0] - py, tip[1] - pzv
    L = math.hypot(ux, uz)
    nx, nz = -uz / L, ux / L
    pawl_pts = [(py - nx * 12, pzv - nz * 12), (py + nx * 12, pzv + nz * 12), (tip[0] + nx * 4, tip[1] + nz * 4), (tip[0] - nx * 4, tip[1] - nz * 4)]
    pawl = yz_plate(pawl_pts, px0, px1) + xcyl(px0, px1, py, pzv, pboss / 2)
    pin_ = xcyl(px0 - 6, -D["cheek_in"] + 14, py, pzv, pdia / 2) + xcyl(px0 - 18, px0 - 6, py, pzv, 18.0)
    C["pawl"] = Comp("Pawl and pivot bolt", pawl - xcyl(px0 - 1, px1 + 1, py, pzv, pdia / 2 + 0.5) + pin_, 7)
    # 8 brake band round the brake rim, open toward the lever pivot at the rear bottom
    bwid, bth, wrap = p["band"]
    xr0, xr1 = D["rim_x"]
    bxc = (xr0 + xr1) / 2
    r0 = fo / 2
    rb = r0 + bth / 2
    lyv, lzv = p["lever_pivot"]
    # differential band brake: both band ends run on tangent lines to the lever at its pivot
    vy, vz = lyv, lzv - dz
    dP = math.hypot(vy, vz)
    aP = math.atan2(vz, vy)
    t1, t2 = aP + math.acos(rb / dP), aP - math.acos(rb / dP)      # tangent points (upper, lower)
    band = xcyl(bxc - bwid / 2, bxc + bwid / 2, 0, dz, r0 + bth) - xcyl(bxc - bwid / 2 - 1, bxc + bwid / 2 + 1, 0, dz, r0)
    wedge = [(0.0, dz)] + [((r0 + 80) * math.cos(t2 + (t1 - t2) * i / 8), dz + (r0 + 80) * math.sin(t2 + (t1 - t2) * i / 8)) for i in range(9)]
    band = band - yz_plate(wedge, bxc - bwid, bxc + bwid)
    p1 = (bxc, (rb + 2) * math.cos(t1), dz + (rb + 2) * math.sin(t1))
    p2 = (bxc, (rb + 2) * math.cos(t2), dz + (rb + 2) * math.sin(t2))
    arm_tip = (bxc, p2[1] + (lyv - p2[1]) * 0.8, p2[2] + (lzv - p2[2]) * 0.8)
    fixed = rod(p1, (bxc, lyv, lzv), 5.0)
    live = rod(p2, arm_tip, 5.0)
    lever_in = rod((bxc, lyv, lzv), arm_tip, 6.0)
    piv = xcyl(bxc - 8, -D["cheek_out"] - 40, lyv, lzv, 10.0)
    lx = -D["cheek_out"] - 30
    la = math.radians(62.0)
    lend = (lx, lyv + p["lever_len"] * math.cos(la), lzv + p["lever_len"] * math.sin(la))
    lever_out = rod((lx, lyv, lzv), lend, 9.0) + xcyl(lx - 110, lx, lend[1], lend[2], 14.0)
    C["brake"] = Comp("Brake band and lever", band + fixed + live + lever_in + piv + lever_out, 8)
    # 9 crank handles, one each end, 180 deg apart
    cr = p["crank_r"]
    aw, at = p["crank_arm"]
    hod, hl = p["crank_hub"]
    god, gl = p["grip"]
    cranks = []
    for sg, a_deg in ((1, p["crank_angle"]), (-1, p["crank_angle"] + 180.0)):
        a = math.radians(a_deg)
        hx0, hx1 = sorted((sg * p["crank_x0"], sg * (p["crank_x0"] + hl)))
        hub = xcyl(hx0, hx1, 0, pz, hod / 2) - xcyl(hx0 - 1, hx1 + 1, 0, pz, pd_ / 2)
        ax0, ax1 = sorted((sg * (p["crank_x0"] + hl - at), sg * (p["crank_x0"] + hl)))
        gy, gz = cr * math.cos(a), pz + cr * math.sin(a)
        arm = yz_plate([(-aw / 2 * math.sin(a), pz + aw / 2 * math.cos(a)), (aw / 2 * math.sin(a), pz - aw / 2 * math.cos(a)),
                        (gy + aw / 2 * math.sin(a), gz - aw / 2 * math.cos(a)), (gy - aw / 2 * math.sin(a), gz + aw / 2 * math.cos(a))], ax0, ax1)
        arm = arm + xcyl(ax0, ax1, gy, gz, aw / 2)
        g0, g1 = sorted((sg * (p["crank_x0"] + hl), sg * (p["crank_x0"] + hl + gl)))
        grip = xcyl(g0, g1, gy, gz, god / 2)
        cranks.append(hub + arm + grip - xcyl(hx0 - 1, max(hx1, ax1) + 1, 0, pz, pd_ / 2))
    C["cranks"] = Comp("Crank handles (2)", fuse(cranks), 9)
    # 10 gear guard: a cup round both gears, open toward the cheek, on three spacers
    gr, gpr, gt, gx0, gx1 = p["guard"]
    pts = _hull_two_circles((0.0, dz, gr), (0.0, pz, gpr))
    outer = yz_plate(pts, gx0, gx1)
    inner = yz_plate(_hull_two_circles((0.0, dz, gr - gt), (0.0, pz, gpr - gt)), gx0 - 1, gx1 - gt)
    guard = outer - inner - xcyl(gx1 - gt - 1, gx1 + 1, 0, pz, 16.0)
    spacers = []
    for (sy, sz_) in p["guard_sp"]:
        sz = dz + sz_
        spacers.append(xcyl(xo, gx0, sy, sz, 7.0) - xcyl(xo - 1, gx0 + 1, sy, sz, 4.25))
        guard = guard + xcyl(gx0, gx1 - gt, sy, sz, 7.0)
    for (sy, sz_) in p["guard_sp"]:
        guard = guard - xcyl(gx0 - 1, gx1 + 1, sy, dz + sz_, 4.5)
    C["guard"] = Comp("Gear guard", guard + fuse(spacers), 10)
    # 11 anchor chains with turnbuckles, and the ground anchors behind (ground at z = 0)
    aey, aex = p["anchor_eye"]
    rd_, rl_, ra_ = p["anchor_rod"]
    hd_, ht_ = p["helix"]
    anchors = []
    for sg in (1, -1):
        ear = (sg * cx, ey, ez)
        eye = (sg * aex, aey, 25.0)
        start = (sg * cx, ey + er + 22, ez - 10)
        ch = rod(start, eye, p["chain_d"] / 2)
        mid = tuple((a_ + c_) / 2 for a_, c_ in zip(start, eye))
        v = [c_ - a_ for a_, c_ in zip(start, eye)]
        Lc = math.sqrt(sum(t * t for t in v))
        u = [t / Lc for t in v]
        tb0 = tuple(mid[i] - u[i] * p["turnbuckle"] / 2 for i in range(3))
        tb1 = tuple(mid[i] + u[i] * p["turnbuckle"] / 2 for i in range(3))
        tb = rod(tb0, tb1, 14.0)
        shackle = rod((sg * (cx - 18), ey, ez), (sg * (cx + 18), ey, ez), 8.0)
        for dx_ in (-18, 18):
            shackle = shackle + rod((sg * cx + dx_, ey, ez), (sg * cx + dx_ * 0.7, start[1], start[2]), 6.0)
        ra = math.radians(ra_)
        tip = (sg * aex, aey + rl_ * math.cos(ra), 25.0 - rl_ * math.sin(ra))
        anchor = rod((sg * aex, aey, 40.0), tip, rd_ / 2)
        hc = tuple(eye[i] + (tip[i] - eye[i]) * 0.85 for i in range(3))
        hdir = b.Vector(tip[0] - eye[0], tip[1] - eye[1], tip[2] - eye[2])
        helix = b.Solid.make_cylinder(hd_ / 2, ht_, b.Plane(origin=hc, z_dir=hdir))
        eye_ring = b.Pos(sg * aex, aey, 40.0) * b.Rot(90, 0, 0) * b.Torus(22.0, 5.0)
        anchors += [ch, tb, shackle, anchor, helix, eye_ring]
    C["anchors"] = Comp("Anchor chains, turnbuckles and ground anchors", b.Compound(anchors), 11)
    return C


def _hull_two_circles(c1, c2, n=48):
    """(y, z) outline of the convex hull of two circles given as (x, y, z, r) with x ignored."""
    (_, y1, z1, r1), (_, y2, z2, r2) = (0, c1[0], c1[1], c1[2]), (0, c2[0], c2[1], c2[2])
    pts = []
    for k in range(360):
        a = math.radians(k)
        for (yc, zc, r) in ((y1, z1, r1), (y2, z2, r2)):
            pts.append((yc + r * math.cos(a), zc + r * math.sin(a)))
    # Andrew's monotone chain
    pts = sorted(set((round(y, 3), round(z, 3)) for y, z in pts))

    def cross(o, a, c):
        return (a[0] - o[0]) * (c[1] - o[1]) - (a[1] - o[1]) * (c[0] - o[0])
    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    hull = lower[:-1] + upper[:-1]
    step = max(1, len(hull) // n)
    return hull[::step]


# ====================================================================== rake
def rake_components(p=PARAMS):
    b = _b()
    D = derived(p)
    C = {}
    bs, bw, bl = p["beam"]
    z0 = p["beam_z0"]
    bt, bh, bg, blen = p["blade"]
    y_bf = bt                                  # beam front face
    yc, zc = y_bf + bs / 2, z0 + bs / 2
    beam = bx(-bl / 2, bl / 2, y_bf, y_bf + bs, z0, z0 + bs) - bx(-bl / 2 - 1, bl / 2 + 1, y_bf + bw, y_bf + bs - bw, z0 + bw, z0 + bs - bw)
    bd, pitch, bz = p["blade_bolts"]
    xs = [-bl / 2 + 150 + i * pitch for i in range(int((bl - 300) // pitch) + 1)]
    sk_w, sk_t, sk_l, sk_y = p["skid"]
    hz = (85.0, 135.0)
    holes_x = xs
    for x in holes_x:
        beam = beam - ycyl(x, -1, y_bf + bs + 1, bz, bd / 2 + 0.5)
    for sx in p["skid_x"]:
        for z in hz:
            beam = beam - ycyl(sx, -1, y_bf + bs + 1, z, bd / 2 + 0.5)
    ct, cl = p["cap"]
    for sg in (1, -1):
        for xo_ in (cl - 46, cl - 86):
            beam = beam - zcyl(sg * (bl / 2 - xo_ + 6), yc, z0 - 1, z0 + bs + 1, 6.5)
    C["beam"] = Comp("Rake beam", beam, 13, "frp")
    blade = bx(-blen / 2, blen / 2, 0, bt, bg, bg + bh)
    for x in holes_x:
        blade = blade - ycyl(x, -1, bt + 1, bz, bd / 2 + 0.5)
    for sx in p["skid_x"]:
        for z in hz:
            blade = blade - ycyl(sx, -1, bt + 1, z, bd / 2 + 0.5)
    C["blade"] = Comp("Rake blade", blade, 14, "uhmw")
    # 15 skids with stainless hangers on the beam's rear face
    hth, hw, hll = p["hanger"]
    yr = y_bf + bs
    skids, hangers = [], []
    for sx in p["skid_x"]:
        sk = bx(sx - sk_w / 2, sx + sk_w / 2, sk_y, sk_y + sk_l, 0, sk_t)
        # upturned (chamfered) leading end
        sk = sk - (b.Pos(sx, sk_y, 0) * b.Rot(45, 0, 0) * b.Box(sk_w + 2, 20, 20))
        skids.append(sk)
        vert = bx(sx - hw / 2, sx + hw / 2, yr, yr + hth, sk_t, z0 + bs - 10)
        for z in hz:
            vert = vert - bx(sx - 5.5, sx + 5.5, yr - 1, yr + hth + 1, z - 12, z + 12)   # slots +-6.5 mm
        horiz = bx(sx - hw / 2, sx + hw / 2, yr, yr + hll, sk_t, sk_t + hth)
        hangers.append(vert + horiz)
    C["skids"] = Comp("Skids (3)", fuse(skids), 15, "uhmw")
    C["hangers"] = Comp("Skid hangers (3)", fuse(hangers), 15, "stainless")
    # 16 end caps: top, bottom and rear walls round the beam end, an end plate, and the eye plate
    caps = []
    et, ereach, ey_f, ey_r, eh = p["eye"]
    for sg in (1, -1):
        xa, xb_ = sorted((sg * (bl / 2 - cl + ct), sg * (bl / 2 + ct)))
        xe0, xe1 = sorted((sg * bl / 2, sg * (bl / 2 + ct)))
        top = bx(xa, xb_, y_bf, yr + ct, z0 + bs, z0 + bs + ct)
        bot = bx(xa, xb_, y_bf, yr + ct, z0 - ct, z0)
        rear = bx(xa, xb_, yr, yr + ct, z0 - ct, z0 + bs + ct)
        endp = bx(xe0, xe1, 0, yr + ct, z0 - ct, z0 + bs + ct)
        xp0, xp1 = sorted((sg * (bl / 2 + ct), sg * (bl / 2 + ct + ereach)))
        ez_ = p["eye_z"]
        eyep = bx(xp0, xp1, ey_f - 25, ey_r + 25, ez_ - et / 2, ez_ + et / 2)
        for yy in (ey_f, ey_r):
            eyep = eyep - zcyl((xp0 + xp1) / 2, yy, ez_ - et, ez_ + et, eh / 2)
        cap = top + bot + rear + endp + eyep
        for xo_ in (cl - 46, cl - 86):
            cap = cap - zcyl(sg * (bl / 2 - xo_ + 6), yc, z0 - ct - 1, z0 + bs + ct + 1, 6.5)
        caps.append(cap)
    C["caps"] = Comp("End caps with eye plates (2)", fuse(caps), 16, "stainless")
    # 19 fasteners: blade bolts with crush sleeves, skid hanger bolts, cap bolts (drawn plain)
    fx = []
    for x in holes_x:
        fx.append(ycyl(x, 0, yr + 9, bz, bd / 2))
        fx.append(ycyl(x, y_bf + bw, yr - bw, bz, 8.0) - ycyl(x, y_bf + bw - 1, yr - bw + 1, bz, bd / 2))
    for sx in p["skid_x"]:
        for z in hz:
            fx.append(ycyl(sx, 0, yr + hth + 9, z, bd / 2))
            fx.append(ycyl(sx, y_bf + bw, yr - bw, z, 8.0) - ycyl(sx, y_bf + bw - 1, yr - bw + 1, z, bd / 2))
    for sg in (1, -1):
        for xo_ in (cl - 46, cl - 86):
            xx = sg * (bl / 2 - xo_ + 6)
            fx.append(zcyl(xx, yc, z0 - ct - 10, z0 + bs + ct + 10, 6.0))
    C["rake_bolts"] = Comp("Rake bolts and crush sleeves", fuse(fx), 19, "stainless")
    # 17 bridles: front legs to the pull apex, rear legs to the return apex, swivels
    af, ar, az = p["bridle"]
    legs = []
    xe = bl / 2 + ct + ereach / 2
    for sg in (1, -1):
        legs.append(rod((sg * xe, ey_f, p["eye_z"]), (0, -af, az), 6.0))
        legs.append(rod((sg * xe, ey_r, p["eye_z"]), (0, yr + ar - yc + yc, az), 6.0))
    sw = ycyl(0, -af - 110, -af, az, 18.0) + ycyl(0, yr + ar, yr + ar + 110, az, 18.0)
    C["bridles"] = Comp("Bridles and swivels (2)", fuse(legs) + sw, 17, "polyester")
    # 22 ballast: two bags filled with salt on site, strapped on the beam behind the blade
    bl_, bd_, bh_ = p["ballast"]
    bags = [bx(sg * p["ballast_x"] - bl_ / 2, sg * p["ballast_x"] + bl_ / 2, y_bf, y_bf + bd_, z0 + bs, z0 + bs + bh_) for sg in (1, -1)]
    C["ballast"] = Comp("Ballast bags (2)", fuse(bags), 22, "salt")
    return C


# ====================================================================== roller saddle
def roller_components(p=PARAMS):
    C = {}
    st, sl, sh = p["saddle"]
    sx = p["saddle_x"]
    az, ad, al = p["axle"]
    ro, rl = p["roller"]
    fo, ft = p["rflange"]
    fw, fth = p["foot"]
    td, ty = p["tie"]
    frame = []
    for sg in (1, -1):
        x0, x1 = sorted((sg * (sx - st / 2), sg * (sx + st / 2)))
        pl = bx(x0, x1, -sl / 2, sl / 2, fth, sh) + xcyl(x0, x1, 0, az, 35.0)
        pl = pl - xcyl(x0 - 1, x1 + 1, 0, az, ad / 2 + 0.5)
        foot = bx(sg * sx - fw / 2, sg * sx + fw / 2, -sl / 2, sl / 2, 0, fth)
        frame += [pl, foot]
    for yy in (-ty, ty):
        frame.append(xcyl(-(sx - st / 2), sx - st / 2, yy, 40.0, td / 2))
    C["saddle"] = Comp("Bund roller saddle", fuse(frame), 12)
    roll = xcyl(-rl / 2, rl / 2, 0, az, ro / 2)
    for sg in (1, -1):
        a0, a1 = sorted((sg * rl / 2, sg * (rl / 2 + ft)))
        roll = roll + xcyl(a0, a1, 0, az, fo / 2)
    roll = roll - xcyl(-rl / 2 - ft - 1, rl / 2 + ft + 1, 0, az, ad / 2 + 0.5)
    C["roller"] = Comp("Roller with flanges", roll, 12, "uhmw")
    C["axle"] = Comp("Roller axle", xcyl(-al / 2, al / 2, 0, az, ad / 2), 12, "stainless")
    return C


# ====================================================================== site context and layout
def bund(p=PARAMS, length=6000.0, y_inner_toe=0.0, facing=1):
    """Earth bund along X: inner toe at y_inner_toe, the pan on the +Y side when facing = 1."""
    b = _b()
    h, crest, base = p["bund"]
    s = (base - crest) / 2
    if facing == 1:
        y0 = y_inner_toe - base
    else:
        y0 = y_inner_toe
    pts = [(y0, 0), (y0 + base, 0), (y0 + base - s, h), (y0 + s, h)]
    return b.Pos(-length / 2, 0, 0) * yz_plate(pts, 0, length)


def place(shape, dx, dy, dz=0.0, turn=False):
    b = _b()
    return b.Pos(dx, dy, dz) * (b.Rot(0, 0, 180) * shape if turn else shape)


def rope_points(p=PARAMS, rake_y=None, layer=2):
    """Pull-rope polyline in the layout: drum top, roller top, pull apex (and the far side)."""
    D = derived(p)
    rake_y = p["rake_y"] if rake_y is None else rake_y
    r = D["layers"][layer - 1][1]
    h = p["bund"][0]
    ztop = D["roller_top"] + p["rope_d"] / 2 + 0.5
    near_drum = (0.0, D["drum_y"], p["drum_z"] + r)
    near_roll = (0.0, D["crest_y"], ztop)
    apex = (0.0, rake_y - p["bridle"][0] - 110, p["bridle"][2])
    W = p["pan_shown"]
    far_crest = W + p["bund"][2] / 2
    yr = p["blade"][0] + p["beam"][0]
    far_apex = (0.0, rake_y + yr + p["bridle"][1] + 110, p["bridle"][2])
    far_roll = (0.0, far_crest, ztop)
    far_drum = (0.0, far_crest + p["capstan_back"], p["drum_z"] + D["layers"][0][1])
    return [near_drum, near_roll, apex], [far_apex, far_roll, far_drum]


def layout(p=PARAMS, rake_y=None):
    """Working layout: {key: (Comp, shape in layout coordinates)} plus context shapes."""
    D = derived(p)
    rake_y = p["rake_y"] if rake_y is None else rake_y
    h = p["bund"][0]
    W = p["pan_shown"]
    out = {}
    cap = capstan_components(p)
    for k, c in cap.items():
        out[f"near_{k}"] = (c, place(c.shape, 0, D["drum_y"], turn=True))
        out[f"far_{k}"] = (c, place(c.shape, 0, W + p["bund"][2] / 2 + p["capstan_back"]))
    rol = roller_components(p)
    for k, c in rol.items():
        out[f"near_{k}"] = (c, place(c.shape, 0, D["crest_y"], h))
        out[f"far_{k}"] = (c, place(c.shape, 0, W + p["bund"][2] / 2, h))
    for k, c in rake_components(p).items():
        out[k] = (c, place(c.shape, 0, rake_y))
    near, far = rope_points(p, rake_y)
    ropes = fuse([rod(a, c, p["rope_d"] / 2) for pts in (near, far) for a, c in zip(pts[:-1], pts[1:])])
    out["ropes"] = (Comp("Pull ropes (2)", ropes, 18, "polyester"), ropes)
    return out


def context(p=PARAMS, length=6000.0):
    """Bunds and a strip of pan floor and dry ground (grey context, no BOM line)."""
    b = _b()
    W = p["pan_shown"]
    base = p["bund"][2]
    near = bund(p, length, 0.0, 1)
    far = bund(p, length, W, -1)
    D = derived(p)
    y0 = D["drum_y"] - 2600.0
    y1 = W + base + p["capstan_back"] + 2600.0
    ground = bx(-length / 2, length / 2, y0, y1, -800.0, 0.0)
    return near, far, ground


def capstan_assembly(p=PARAMS):
    from build123d import Compound
    return Compound([c.shape for c in capstan_components(p).values()])


def mass(comp):
    return comp.shape.volume * DENSITY[comp.material]


# ====================================================================== constructability checks
def _vol(a, c):
    try:
        s = a & c
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    C = capstan_components(p)
    R = rake_components(p)
    S = roller_components(p)
    D = derived(p)
    rows = []

    def chk(desc, a, c, expect):
        v = _vol(a, c)
        g = a.distance_to(c)
        ok = v < 1e-2 and (g < 0.05 if expect == "touch" else g >= expect - 1e-6)
        rows.append((desc, v, g, expect, ok))

    c = lambda k: C[k].shape  # noqa: E731
    chk("Right side frame and left side frame apart", c("frame_r"), c("frame_l"), 300.0)
    for k in ("front", "rear", "top"):
        chk(f"Cross tube ({k}) on the right cheek", c(f"xtube_{k}"), c("frame_r"), "touch")
        chk(f"Cross tube ({k}) on the left cheek", c(f"xtube_{k}"), c("frame_l"), "touch")
        chk(f"Cross tube ({k}) clear of the drum", c(f"xtube_{k}"), c("drum"), 5.0)
    chk("Drum clear of the right cheek", c("drum") - xcyl(-400, 400, 0, p["drum_z"], p["dshaft"][0] / 2 + 0.1), c("frame_r"), 10.0)
    chk("Drum clear of the left cheek", c("drum") - xcyl(-400, 400, 0, p["drum_z"], p["dshaft"][0] / 2 + 0.1), c("frame_l"), 10.0)
    chk("Drum shaft through the cheek holes (radial clearance)", xcyl(-300, 300, 0, p["drum_z"], p["dshaft"][0] / 2), c("frame_r") + c("frame_l"), 5.0)
    chk("Bearings on the cheeks", c("bearings"), c("frame_r") + c("frame_l"), "touch")
    chk("Drum shaft in the bearings", c("drum"), c("bearings"), "touch")
    chk("Crank shaft in the bearings", c("pinion"), c("bearings"), "touch")
    chk("Crank shaft clear of the drum flanges", c("pinion"), c("drum"), 10.0)
    chk("Crank shaft clear of the top cross tube", c("pinion"), c("xtube_top"), 30.0)
    chk("Gear on the drum shaft", c("gear"), c("drum"), "touch")
    chk("Gear clear of the bearing", c("gear"), c("bearings"), 5.0)
    chk("Gear and pinion in mesh, not overlapping", c("gear"), c("pinion") - xcyl(-400, 400, 0, D["pin_z"], p["pshaft"][0] / 2 + 0.1), 0.0)
    chk("Ratchet wheel on the drum shaft", c("ratchet"), c("drum"), "touch")
    chk("Ratchet wheel clear of the bearing", c("ratchet"), c("bearings"), 5.0)
    chk("Pawl tip seated against a tooth face, not overlapping", c("pawl"), c("ratchet"), 0.0)
    chk("Pawl bolt through the boss and the left cheek", c("pawl"), c("frame_l"), 0.0)
    chk("Pawl boss clear of the ratchet wheel", c("frame_l"), c("ratchet"), 1.0)
    chk("Pawl clear of the bearings", c("pawl"), c("bearings"), 3.0)
    chk("Brake band on the brake rim", c("brake"), c("drum"), "touch")
    chk("Brake clear of the left cheek's drum bearing", c("brake"), c("bearings"), 3.0)
    chk("Brake clear of the rear cross tube", c("brake"), c("xtube_rear"), 10.0)
    chk("Gear guard clear of the gear", c("guard"), c("gear"), 3.0)
    chk("Gear guard clear of the crank shaft", c("guard"), c("pinion"), 2.0)
    chk("Gear guard spacers on the right cheek", c("guard"), c("frame_r"), "touch")
    chk("Gear guard clear of the cranks", c("guard"), c("cranks"), 3.0)
    chk("Cranks clear of the ratchet, pawl and brake", c("cranks"), c("ratchet") + c("pawl") + c("brake"), 10.0)
    chk("Cranks clear of the side frames", c("cranks"), c("frame_r") + c("frame_l"), 50.0)
    chk("Cranks on the crank shaft", c("cranks"), c("pinion"), "touch")
    chk("Anchor chains clear of the drum and brake", c("anchors"), c("drum") + c("brake"), 15.0)
    chk("Shackle pins through the ear holes", c("anchors"), c("frame_r") + c("frame_l"), 0.0)
    chk("Brake pivot through its hole in the left cheek", c("brake"), c("frame_l"), 0.0)
    # rope stays below the guard and clear of the top cross tube when the drum is full
    rf = D["r_full"] + p["rope_d"] / 2
    rows.append(("Rope at full drum clear of the crank shaft", 0.0, D["pin_z"] - p["pshaft"][0] / 2 - (p["drum_z"] + rf), 10.0,
                 D["pin_z"] - p["pshaft"][0] / 2 - (p["drum_z"] + rf) >= 10.0))
    rows.append(("Rope freeboard below the flange rim at four layers", 0.0, D["freeboard"], 2 * p["rope_d"], D["freeboard"] >= 2 * p["rope_d"]))
    # crank handle sweep: lowest point above ground
    low = D["pin_z"] - p["crank_r"] - p["grip"][0] / 2
    rows.append(("Crank grip clears the ground at the bottom of its circle", 0.0, low, 300.0, low >= 300.0))
    r = lambda k: R[k].shape  # noqa: E731
    chk("Blade on the beam front face", r("blade"), r("beam"), "touch")
    chk("Hangers on the beam rear face", r("hangers"), r("beam"), "touch")
    chk("Skids under the hangers", r("skids"), r("hangers"), "touch")
    chk("Skids clear of the blade", r("skids"), r("blade"), 2.0)
    chk("Skids clear of the beam", r("skids"), r("beam"), 10.0)
    chk("End caps on the beam", r("caps"), r("beam"), "touch")
    chk("End caps against the blade ends", r("caps"), r("blade"), "touch")
    chk("Ballast bags on the beam top, behind the blade", r("ballast"), r("beam"), "touch")
    chk("Ballast bags against the blade back", r("ballast"), r("blade"), "touch")
    chk("Ballast bags clear of the end caps", r("ballast"), r("caps"), 20.0)
    chk("Bolts clear of the cap walls (in their holes)", r("rake_bolts"), r("beam") + r("blade"), 0.0)
    gap = p["blade"][2]
    rows.append(("Blade edge above the floor when the skids rest on it (mm)", 0.0, gap, 5.0, 5.0 <= gap <= 25.0))
    s = lambda k: S[k].shape  # noqa: E731
    chk("Roller clear of the saddle side plates", s("roller"), s("saddle"), 3.0)
    chk("Axle in the side plates", s("axle"), s("saddle"), 0.0)
    chk("Roller on its axle", s("roller"), s("axle"), 0.0)
    chk("Roller clear of the tie bars", s("roller"), s("saddle"), 3.0)
    # layout: ropes clear of the bund crest and frames
    L = layout(p)
    near, far = rope_points(p)
    chk("Near rope clear of the near bund", L["ropes"][1], bund(p, 6000.0, 0.0, 1), 20.0)
    chk("Near rope on the near roller (not through it)", rod(near[0], near[1], p["rope_d"] / 2), L["near_roller"][1], 0.0)
    chk("Near rope clear of the capstan guard and top tube",
        rod(near[0], near[1], p["rope_d"] / 2), L["near_guard"][1] + L["near_xtube_top"][1], 5.0)
    chk("Near capstan clear of the bund", fuse([L[f"near_{k}"][1] for k in C]), bund(p, 6000.0, 0.0, 1), 100.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, g, expect, ok in rows:
        bad += 0 if ok else 1
        e = "touch" if expect == "touch" else f">= {expect:g} mm"
        print(f"{'ok  ' if ok else 'FAIL'} {desc}: overlap {v:.2f} mm3, gap {g:.2f} mm ({e})")
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def masses(p=PARAMS):
    out = {}
    for k, c in capstan_components(p).items():
        out[("capstan", k)] = (c.name, c.bom, mass(c))
    for k, c in rake_components(p).items():
        out[("rake", k)] = (c.name, c.bom, mass(c))
    for k, c in roller_components(p).items():
        out[("roller", k)] = (c.name, c.bom, mass(c))
    return out


# ---------------------------------------------------------------------------------------------- kit 1.9 imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cad_parts as cp  # noqa: E402
import sdg_parts as sp  # noqa: E402
from build123d import Axis, Box, Circle, Cone, Cylinder, Plane, Polygon, Pos, Rot, Sketch, Torus, extrude, revolve  # noqa: E402


# ====================================================================== kit 1.9 interface (STANDARDS section 24)
# Every concept option is modelled at detail level D3 from .kit/cad_parts.py and cad/src/sdg_parts.py, in the
# site frame: ground (dry ground behind the bund and the pan floor) at z = 0, the near bund's inner toe at
# y = 0, the pan toward +Y, X along the bund. The functions above (capstan_components() and the rest) keep the
# same geometry in each component's own frame for the calculations (docs/04-calcs/sizing.py), the drawings
# (cad/src/sheets.py, cad/src/build_plan_media.py) and the concept media; components() below splits it into
# made and bought parts, adds every bolt, nut, washer, pin and weld, and places it on the site.
OPTIONS = {"A": "Geared drum capstans", "B": "Bund-walk haul", "C": "Lever rope puller"}
PRINCIPLES = {
    "A": "Two people wind a 6 to 1 geared drum winch on dry ground behind the bund; the drum stores the rope, "
         "a pawl holds it, and the rope runs over a bund roller to a 3 m rake.",
    "B": "A team walks along the dry ground behind the bund hauling the rope by toggles; a turning block on a "
         "staked post turns the pull 90 degrees and a 1.5 m rake is drawn in.",
    "C": "One or two people work a 10 to 1 hand lever whose two cam jaws grip the rope in turn and pull it "
         "through in short strokes; the free rope tail is coiled by hand.",
}
CHOSEN = "A"
TITLE = "SaltDrag"
OPTION_VIEWS = {k: {"el": 24, "az": -40, "scale": "person", "keep_context": True, "ground_z": 0} for k in OPTIONS}
ALLOWED_CONTACTS = [
    ("split pin", "pin"),                    # split pins and R-clips sit in their cross holes
    ("Brake band", "Brake lever"),           # band end links pinned to the lever's pivot and inner arm
    ("chain", "shackle"), ("chain", "Turnbuckle"), ("chain", "anchor"),   # links through bows, eyes and the anchor eye
    ("Bridle", "shackle"), ("Bridle", "Swivel"), ("rope", "Swivel"),      # spliced eyes round bows and swivel eyes
    ("Rope damper", "rope"),                 # the damper's snap hook rides on the rope
    ("Toggle", "rope"),                      # haul toggles spliced into the rope (option B)
    ("Jaw", "rope"),                         # cam jaws bite the rope (option C)
]

GALV, STEEL, SS, UHMW, FRP, ROPE_M, CANVAS = "galvanised", "mild_steel", "stainless", "hdpe_natural", "hdpe_recycled", "rope", "canvas"
WELD_LEG = 5.0


def _site_cap(shape, p=PARAMS):
    """Capstan (or any behind-the-bund) local frame to the site: turned so the pan is toward +Y."""
    return place(shape, 0, derived(p)["drum_y"], turn=True)


def _site_roller(shape, p=PARAMS):
    D = derived(p)
    return place(shape, 0, D["crest_y"], p["bund"][0])


def _site_rake(shape, p=PARAMS):
    return place(shape, 0, p["rake_y"])


def _add(out, name, shape, mat, kind, bom=None, group="capstan", explode=(0, 0, 0)):
    out.append(cp.part(name, shape, mat, kind=kind, bom=bom, group=group, explode=explode))


def _bolts(out, d, grip, origin, n, mat=GALV, bom=19, group="capstan", label="", extra=None, explode=(0, 0, 0), xf=None):
    for nm, sh in sp.bolt_set(d, grip, origin, n, extra=extra):
        _add(out, nm + label, xf(sh) if xf else sh, mat, "fastener", bom, group, explode)


def _cheek_plate(p, sg):
    """Cheek plate alone (no runner, no boss), with every hole, in the capstan frame."""
    D = derived(p)
    cx, ct = p["cheek_x"], p["cheek_t"]
    ey, ez, er, eh = p["ear"]
    dz, pz = p["drum_z"], D["pin_z"]
    x0, x1 = sorted((sg * (cx - ct / 2), sg * (cx + ct / 2)))
    ch = yz_plate(cheek_outline(p), x0, x1)
    ch = ch + bx(x0, x1, 120.0, ey, ez - er, ez + er) + xcyl(x0, x1, ey, ez, er)
    cut = [xcyl(x0 - 1, x1 + 1, ey, ez, eh / 2), xcyl(x0 - 1, x1 + 1, 0, dz, 30.0), xcyl(x0 - 1, x1 + 1, 0, pz, 20.0),
           xcyl(x0 - 1, x1 + 1, p["pawl"][0], p["pawl"][1], p["pawl"][3] / 2 + 0.5),
           xcyl(x0 - 1, x1 + 1, p["lever_pivot"][0], p["lever_pivot"][1], 10.5)]
    for spec, zc in ((p["brg_drum"], dz), (p["brg_pin"], pz)):
        for dy in (-spec[3] / 2, spec[3] / 2):
            for dz_ in (-spec[3] / 2, spec[3] / 2):
                cut.append(xcyl(x0 - 1, x1 + 1, dy, zc + dz_, spec[4] / 2))
    for (ty, tz) in p["xtubes"].values():
        for dy in (-p["xbolt"], p["xbolt"]):
            cut.append(xcyl(x0 - 1, x1 + 1, ty + dy, tz, 5.5))
    if sg > 0:
        for (gy_, gz_) in p["guard_sp"]:
            cut.append(xcyl(x0 - 1, x1 + 1, gy_, dz + gz_, 4.5))
    for c in cut:
        ch = ch - c
    return ch


def _xplate(p, x_face, ty, tz):
    """Cross-tube end plate in the YZ plane from x_face along +X, 100 wide (Y) by 80 high (Z), two 11 mm holes."""
    ps, pt = p["xplate"]
    h = p["xplate_h"]
    pl = cp.sheet(ps, h, pt, holes=[(-p["xbolt"], 0, 11.0), (p["xbolt"], 0, 11.0)], r_corner=4.0, edge=0.8)
    return sp.frame((x_face, ty, tz), (1, 0, 0), u=(0, 1, 0)) * pl


def _disc(od, t, holes, x_face, z_axis):
    """Flat disc in the YZ plane from x_face along +X, centred on the drum axis, holes [(y, z, d)] from the centre."""
    sk = Sketch() + Circle(od / 2)
    for y, z, d in holes:
        sk -= Pos(y, z) * Circle(d / 2)
    return sp.frame((x_face, 0, z_axis), (1, 0, 0), u=(0, 1, 0)) * extrude(sk, t)


def _brake_parts(p):
    """Brake band with its lining and end links, and the brake lever with its pivot shaft and inner arm."""
    D = derived(p)
    dz = p["drum_z"]
    fo = p["flange"][0]
    bwid, bth, wrap = p["band"]
    xr0, xr1 = D["rim_x"]
    bxc = (xr0 + xr1) / 2
    r0 = fo / 2
    rb = r0 + bth / 2
    lyv, lzv = p["lever_pivot"]
    vy, vz = lyv, lzv - dz
    dP = math.hypot(vy, vz)
    aP = math.atan2(vz, vy)
    t1, t2 = aP + math.acos(rb / dP), aP - math.acos(rb / dP)
    band = xcyl(bxc - bwid / 2, bxc + bwid / 2, 0, dz, r0 + bth) - xcyl(bxc - bwid / 2 - 1, bxc + bwid / 2 + 1, 0, dz, r0)
    wedge = [(0.0, dz)] + [((r0 + 80) * math.cos(t2 + (t1 - t2) * i / 8), dz + (r0 + 80) * math.sin(t2 + (t1 - t2) * i / 8)) for i in range(9)]
    band = band - yz_plate(wedge, bxc - bwid, bxc + bwid)
    p1 = (bxc, (rb + 2) * math.cos(t1), dz + (rb + 2) * math.sin(t1))
    p2 = (bxc, (rb + 2) * math.cos(t2), dz + (rb + 2) * math.sin(t2))
    arm_tip = (bxc, p2[1] + (lyv - p2[1]) * 0.8, p2[2] + (lzv - p2[2]) * 0.8)
    links = rod(p1, (bxc, lyv, lzv), 5.0) + rod(p2, arm_tip, 5.0)
    lever_in = rod((bxc, lyv, lzv), arm_tip, 6.0)
    piv = xcyl(bxc - 8, -D["cheek_out"] - 40, lyv, lzv, 10.0)
    lx = -D["cheek_out"] - 30
    la = math.radians(62.0)
    lend = (lx, lyv + p["lever_len"] * math.cos(la), lzv + p["lever_len"] * math.sin(la))
    lever_out = rod((lx, lyv, lzv), lend, 9.0) + xcyl(lx - 112, lx, lend[1], lend[2], 9.0)
    grip = xcyl(lx - 110, lx - 12, lend[1], lend[2], 14.0) - xcyl(lx - 111, lx - 11, lend[1], lend[2], 9.5)
    return band + links, lever_in + piv + lever_out, grip


def _crank(p, sg, a_deg):
    """One crank: hub, arm and grip pin (a welded part), the turning grip sleeve, and the hub's cross hole."""
    D = derived(p)
    pz = D["pin_z"]
    cr = p["crank_r"]
    aw, at = p["crank_arm"]
    hod, hl = p["crank_hub"]
    god, gl = p["grip"]
    pd_ = p["pshaft"][0]
    a = math.radians(a_deg)
    hx0, hx1 = sorted((sg * p["crank_x0"], sg * (p["crank_x0"] + hl)))
    hub = xcyl(hx0, hx1, 0, pz, hod / 2)
    ax0, ax1 = sorted((sg * (p["crank_x0"] + hl - at), sg * (p["crank_x0"] + hl)))
    gy, gz = cr * math.cos(a), pz + cr * math.sin(a)
    arm = yz_plate([(-aw / 2 * math.sin(a), pz + aw / 2 * math.cos(a)), (aw / 2 * math.sin(a), pz - aw / 2 * math.cos(a)),
                    (gy + aw / 2 * math.sin(a), gz - aw / 2 * math.cos(a)), (gy - aw / 2 * math.sin(a), gz + aw / 2 * math.cos(a))], ax0, ax1)
    arm = arm + xcyl(ax0, ax1, gy, gz, aw / 2)
    g0, g1 = sorted((sg * (p["crank_x0"] + hl), sg * (p["crank_x0"] + hl + gl)))
    pin = xcyl(min(g0, g1) - (0 if sg > 0 else 6), max(g0, g1) + (6 if sg > 0 else 0), gy, gz, 8.0)
    xe = g1 + 6 if sg > 0 else g0 - 6
    head = xcyl(min(xe, xe + sg * 4), max(xe, xe + sg * 4), gy, gz, 12.0)
    xh = sg * (p["crank_x0"] + 20)
    body = hub + arm + pin + head - xcyl(hx0 - 1, max(hx1, ax1) + 1, 0, pz, pd_ / 2) - ycyl(xh, -40, 40, pz, 4.25)
    sleeve = xcyl(g0 + 0.5, g1 - 0.5, gy, gz, god / 2) - xcyl(g0 - 1, g1 + 1, gy, gz, 8.5)
    return body, sleeve, xh


def _pawl_plate(p):
    D = derived(p)
    dz = p["drum_z"]
    rod_, rn, rtk, rx0 = p["ratchet"]
    py, pzv, pth, pdia, pboss = p["pawl"]
    rr = rod_ / 2 - 14
    da = 2 * math.pi / rn
    k = int(math.atan2(pzv - dz, py) // da)
    a_tip = k * da + 0.05
    tip = ((rr + 6) * math.cos(a_tip), dz + (rr + 6) * math.sin(a_tip))
    px0, px1 = rx0 - rtk + 2, rx0 - 2
    ux, uz = tip[0] - py, tip[1] - pzv
    L = math.hypot(ux, uz)
    nx, nz = -uz / L, ux / L
    pts = [(py - nx * 12, pzv - nz * 12), (py + nx * 12, pzv + nz * 12), (tip[0] + nx * 4, tip[1] + nz * 4), (tip[0] - nx * 4, tip[1] - nz * 4)]
    pawl = yz_plate(pts, px0, px1) + xcyl(px0, px1, py, pzv, pboss / 2)
    return pawl - xcyl(px0 - 1, px1 + 1, py, pzv, pdia / 2 + 0.5), px0, px1


def _guard_parts(p):
    D = derived(p)
    dz, pz = p["drum_z"], D["pin_z"]
    gr, gpr, gt, gx0, gx1 = p["guard"]
    outer = yz_plate(_hull_two_circles((0.0, dz, gr), (0.0, pz, gpr)), gx0, gx1)
    inner = yz_plate(_hull_two_circles((0.0, dz, gr - gt), (0.0, pz, gpr - gt)), gx0 - 1, gx1 - gt)
    guard = outer - inner - xcyl(gx1 - gt - 1, gx1 + 1, 0, pz, 16.0)
    spacers = []
    for (sy, sz_) in p["guard_sp"]:
        guard = guard + xcyl(gx0, gx1 - gt, sy, dz + sz_, 7.0)
    for (sy, sz_) in p["guard_sp"]:
        guard = guard - xcyl(gx0 - 1, gx1 + 1, sy, dz + sz_, 4.5)
        spacers.append(sp.frame((D["cheek_out"], sy, dz + sz_), (1, 0, 0)) * sp.sleeve(14.0, 9.0, gx0 - D["cheek_out"]))
    return guard, spacers


def _turnbuckle(a, c, body_len=220.0):
    """M16 hook-and-eye turnbuckle between points a and c (body centred), as one bought part."""
    u = sp._unit(tuple(q - p_ for p_, q in zip(a, c)))
    L = math.dist(a, c)
    loc = sp.frame(a, u)
    bl = body_len * 0.55
    z0 = (L - bl) / 2
    side = [Pos(sx * 13, 0, z0 + bl / 2) * Box(5, 12, bl) for sx in (-1, 1)]
    ends = [Pos(0, 0, z) * Cylinder(10, 14) for z in (z0 + 7, z0 + bl - 7)]
    screws = Pos(0, 0, L / 2) * Cylinder(7, L - 30)
    eyes = [Pos(0, 0, z) * (Rot(90, 0, 0) * Torus(11, 4)) for z in (11, L - 11)]
    tb = side[0] + side[1] + ends[0] + ends[1] + screws
    for e in eyes:
        tb = tb + e
    return loc * tb


def _anchor(eye, p, sg):
    """Helical ground anchor: forged eye at 'eye', 20 mm rod 1.0 m at 45 degrees into the ground, 150 mm helix."""
    rd_, rl_, ra_ = p["anchor_rod"]
    hd_, ht_ = p["helix"]
    ra = math.radians(ra_)
    ex, ey_, ez_ = eye
    tip = (ex, ey_ + rl_ * math.cos(ra), ez_ - 18 - rl_ * math.sin(ra))
    top = (ex, ey_, ez_ - 18)
    r = rod(top, tip, rd_ / 2)
    hc = tuple(top[i] + (tip[i] - top[i]) * 0.85 for i in range(3))
    hdir = tuple(tip[i] - top[i] for i in range(3))
    helix = sp.frame(hc, hdir) * (Pos(0, 0, ht_ / 2) * Cylinder(hd_ / 2, ht_) - Pos(0, hd_ / 2, ht_ / 2) * Box(4, hd_, ht_ + 2))
    ring = Pos(ex, ey_, ez_) * (Rot(90, 0, 0) * Torus(22.0, 5.0))
    point = sp.frame(tip, hdir) * Pos(0, 0, 0) * Cone(rd_ / 2, 1.0, 30)
    return r + helix + ring + point


def _chain_run(out, p, side_x, start, eye, group, bom=11, xf=None):
    """Shackle at the frame ear, chain, turnbuckle and chain to the anchor eye (bought parts)."""
    xf = xf or (lambda s: s)
    mid = tuple((a_ + c_) / 2 for a_, c_ in zip(start, eye))
    u = sp._unit(tuple(c_ - a_ for a_, c_ in zip(start, eye)))
    half = p["turnbuckle"] / 2
    t0 = tuple(mid[i] - u[i] * half for i in range(3))
    t1 = tuple(mid[i] + u[i] * half for i in range(3))
    w_ = p["chain_wire"]
    _add(out, f"Anchor chain, {w_:.0f} mm grade 30 galvanised, upper, {side_x}", xf(sp.chain(start, t0, w_)), GALV, "bought", bom, group)
    _add(out, f"Turnbuckle, forged jaw and eye, rated 1 t, galvanised, {side_x}", xf(_turnbuckle(t0, t1)), GALV, "bought", bom, group)
    end = (eye[0] - u[0] * 18, eye[1] - u[1] * 18, eye[2] + 6)
    _add(out, f"Anchor chain, {w_:.0f} mm grade 30 galvanised, lower, {side_x}", xf(sp.chain(t1, end, w_)), GALV, "bought", bom, group)


def site_context(p=PARAMS, length=7000.0, pan=6500.0):
    """Near bund and the pan floor's salt crust, as site parts reaching below ground (z = 0)."""
    h, crest, base = p["bund"]
    s = (base - crest) / 2
    y0 = -base
    pts = [(y0, -300), (0.0, -300), (0.0, 0.0), (-s, h), (y0 + s, h), (y0, 0.0)]
    bund_s = Pos(-length / 2, 0, 0) * yz_plate(pts, 0, length)
    crust = bx(-length / 2, length / 2, 0.0, pan, -300.0, 0.5)
    return [cp.part("Earth bund (site)", bund_s, "soil", kind="context", group="context"),
            cp.part("Salt pan floor, crystal crust (site)", crust, "insulated_white", kind="context", group="context")]


# ---------------------------------------------------------------------------------------------- option A
def capstan_a(p=PARAMS, xf=None, group="capstan"):
    """One hand capstan with its anchors, every part split out, in the site frame (xf: local to site)."""
    xf = xf or (lambda s: _site_cap(s, p))
    D = derived(p)
    out = []
    A = lambda nm, sh, mat, kind, bom=None, ex=(0, 0, 0): _add(out, nm, xf(sh), mat, kind, bom, group, ex)  # noqa: E731
    cx, ct = p["cheek_x"], p["cheek_t"]
    xi, xo = D["cheek_in"], D["cheek_out"]
    dz, pz = p["drum_z"], D["pin_z"]
    s_sz, s_w, ry0, ry1 = p["runner"]
    leg = WELD_LEG
    # 1 side frames: cheek plate, runner, welds; pawl boss on the left
    for side, sg in (("right", 1), ("left", -1)):
        ex = (sg * 300, 0, 0)
        A(f"Cheek plate, {side}, 6 mm S275", _cheek_plate(p, sg), GALV, "made", 1, ex)
        run = Pos(sg * cx, ry0, s_sz / 2) * cp.along(cp.shs(s_sz, s_w, ry1 - ry0), "y")
        A(f"Runner, {side}, SHS 40 x 40 x 3", run, GALV, "made", 1, ex)
        for f in (1, -1):
            xf_ = sg * cx + f * ct / 2
            A(f"Weld, cheek to runner, {side}, {'outer' if f * sg > 0 else 'inner'}",
              sp.weld_on((xf_, -300.0, s_sz), (0, 1, 0), 600.0, leg, (f, 0, 0), (0, 0, 1)), GALV, "weld", None, ex)
    py, pzv, pth, pdia, pboss = p["pawl"]
    bx0, bx1 = p["ratchet"][3] + 2, -xo
    boss = sp.frame((bx0, py, pzv), (1, 0, 0)) * cp.round_tube(pboss, (pboss - pdia - 1) / 2, bx1 - bx0)
    A("Pawl boss, left, 40 mm round tube", boss, GALV, "made", 1, (-300, 0, 0))
    A("Weld, pawl boss to left cheek", sp.ring_weld(pboss / 2, leg, (-xo, py, pzv), (-1, 0, 0)), GALV, "weld", None, (-300, 0, 0))
    # 2 cross tubes, end plates, welds and bolts
    xs, xw = p["xtube"]
    pt = p["xplate"][1]
    for key, (ty, tz) in p["xtubes"].items():
        ex = {"front": (0, -380, -150), "rear": (0, 380, -150), "top": (0, 0, 420)}[key]
        tube = Pos(-xi + pt, ty, tz) * cp.along(cp.shs(xs, xw, 2 * (xi - pt)), "x")
        A(f"Cross tube, {key}, SHS 40 x 40 x 3", tube, GALV, "made", 2, ex)
        for sg in (1, -1):
            side = "right" if sg > 0 else "left"
            A(f"Cross tube end plate, {key}, {side}", _xplate(p, sg * xi - (pt if sg > 0 else 0), ty, tz), GALV, "made", 2, ex)
            xw_ = sg * (xi - pt)
            for (st, ax, d1) in (((xw_, ty - 14, tz + xs / 2), (0, 1, 0), (0, 0, 1)), ((xw_, ty - 14, tz - xs / 2), (0, 1, 0), (0, 0, -1)),
                                 ((xw_, ty + xs / 2, tz - 14), (0, 0, 1), (0, 1, 0)), ((xw_, ty - xs / 2, tz - 14), (0, 0, 1), (0, -1, 0))):
                A(f"Weld, cross tube {key} to end plate, {side}", sp.weld_on(st, ax, 28.0, leg, d1, (-sg, 0, 0)), GALV, "weld", None, ex)
            for dy in (-p["xbolt"], p["xbolt"]):
                for nm, sh in sp.bolt_set(10, ct + pt, (sg * xo, ty + dy, tz), (sg, 0, 0)):
                    A(nm + ", galvanised", sh, GALV, "fastener", 19, ex)
    # 3 drum: barrel, flanges, brake rim, shaft, welds; rope anchor hole in the right flange
    bo, bw, bl = p["barrel"]
    fo, ft = p["flange"]
    sd, sx0, sx1 = p["dshaft"]
    bxr = D["barrel_x"]
    exd = (0, -560, 0)
    A("Drum barrel, 168.3 x 6.3 YSt 310 tube", sp.frame((bxr[0], 0, dz), (1, 0, 0)) * cp.round_tube(bo, bw, bxr[1] - bxr[0]), GALV, "made", 3, exd)
    A("Drum flange, right, 330 x 6", _disc(fo, ft, [(0, 0, sd), (0, bo / 2 + 10, 14.0)], D["flange_r"][0], dz), GALV, "made", 3, exd)
    A("Drum flange, left, 330 x 6", _disc(fo, ft, [(0, 0, sd)], D["flange_l"][0], dz), GALV, "made", 3, exd)
    rw, rt = p["rim"]
    A("Brake rim, 50 x 6 ring", sp.frame((D["rim_x"][0], 0, dz), (1, 0, 0)) * cp.round_tube(fo, rt, rw), GALV, "made", 3, exd)
    A("Drum shaft, 40 mm C45+QT", sp.frame((sx0, 0, dz), (1, 0, 0)) * cp.round_bar(sd, sx1 - sx0, 1.5), STEEL, "made", 3, exd)
    A("Weld, barrel to right flange", sp.ring_weld(bo / 2, leg, (D["flange_r"][0], 0, dz), (-1, 0, 0)), GALV, "weld", None, exd)
    A("Weld, barrel to left flange", sp.ring_weld(bo / 2, leg, (D["flange_l"][1], 0, dz), (1, 0, 0)), GALV, "weld", None, exd)
    A("Weld, shaft to right flange", sp.ring_weld(sd / 2, leg, (D["flange_r"][1], 0, dz), (1, 0, 0)), STEEL, "weld", None, exd)
    A("Weld, shaft to left flange", sp.ring_weld(sd / 2, leg, (D["flange_l"][0], 0, dz), (-1, 0, 0)), STEEL, "weld", None, exd)
    rim_in = fo / 2 - rt
    rim_w = revolve(Plane.XZ * Polygon((rim_in, 0), (rim_in - leg, 0), (rim_in, leg), align=None), Axis.Z, 360)
    A("Weld, brake rim to left flange", sp.frame((D["flange_l"][0], 0, dz), (-1, 0, 0)) * rim_w, GALV, "weld", None, exd)
    # 6 bearings and their bolts (heads inside the cheeks, so no bolt tail reaches the drum flanges)
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        for spec, zc, bore, d_b, nm in ((p["brg_drum"], dz, sd, 12, "40 mm"), (p["brg_pin"], pz, p["pshaft_brg"], 10, "30 mm")):
            A(f"Flange bearing {nm}, {side}, stainless insert, thermoplastic housing",
              flange_bearing(sg * xo, sg, 0, zc, spec, bore), "hdpe_black", "bought", 6, (sg * 120, 0, 0))
            for dy in (-spec[3] / 2, spec[3] / 2):
                for dz_ in (-spec[3] / 2, spec[3] / 2):
                    for n_, sh in sp.bolt_set(d_b, spec[1] + ct, (sg * xi, dy, zc + dz_), (-sg, 0, 0)):
                        A(n_ + ", galvanised", sh, GALV, "fastener", 19, (sg * 120, 0, 0))
    # 4, 5 gear, pinion, crank shaft; 9 cranks with cross pins and split pins
    C = capstan_components(p)
    A("Spur gear, module 4, 84 teeth, webbed, 44 mm hub, C45+QT", C["gear"].shape, STEEL, "bought", 4, (620, -260, 0))
    m = p["module"]
    pd_, ph = p["pshaft"]
    pin = gear_profile(p["z_pinion"], m, pd_ / 2, p["pinion_face"], p["pinion_x0"], 0, pz,
                       phase=1.5 * math.pi - 0.375 * 2 * math.pi / p["z_pinion"])
    A("Pinion, module 4, 14 teeth", pin, STEEL, "bought", 5, (0, -260, 560))
    stp, db = p["pshaft_step"], p["pshaft_brg"]
    shaft = (sp.frame((-ph, 0, pz), (1, 0, 0)) * cp.round_bar(pd_, 2 * ph, 1.0)) + \
        (sp.frame((-stp, 0, pz), (1, 0, 0)) * cp.round_bar(db, 2 * stp, 1.0))
    for sg in (1, -1):
        shaft = shaft - ycyl(sg * (p["crank_x0"] + 20), -20, 20, pz, 4.25)
    A("Crank shaft, C45+QT, 30 mm through the bearings, 25 mm outboard", shaft, STEEL, "made", 5, (0, -260, 560))
    for sg, a_deg in ((1, p["crank_angle"]), (-1, p["crank_angle"] + 180.0)):
        side = "right" if sg > 0 else "left"
        body, sleeve_, xh = _crank(p, sg, a_deg)
        A(f"Crank, {side}: hub, arm and grip pin", body, GALV, "made", 9, (0, 0, 820))
        A(f"Crank grip sleeve, {side}", sleeve_, "hdpe_black", "made", 9, (0, 0, 820))
        cpin = sp.frame((xh, p["crank_hub"][0] / 2, pz), (0, 1, 0)) * cp.clevis_pin(8, p["crank_hub"][0])
        A(f"Crank cross pin, 8 mm (ISO 2341), {side}", cpin, SS, "fastener", 19, (0, 0, 820))
        spl = sp.frame((xh, p["crank_hub"][0] / 2, pz), (0, 1, 0)) * Pos(0, 0, -p["crank_hub"][0] - 8) * cp.split_pin(8)
        A(f"Split pin for the crank cross pin (ISO 1234), {side}", spl, SS, "fastener", 19, (0, 0, 820))
    # 7 ratchet wheel, pawl, pivot bolt and spacer washer
    A("Ratchet wheel, 200 mm, 20 teeth, with welded 70 mm hub", C["ratchet"].shape, STEEL, "made", 7, (-600, -260, 0))
    rxo = p["ratchet"][3] - p["ratchet"][2]
    A("Weld, ratchet hub to ratchet wheel", sp.ring_weld(p["ratchet_hub"][0] / 2, leg, (rxo, 0, dz), (-1, 0, 0)), STEEL, "weld", None, (-600, -260, 0))
    pawl, px0, px1 = _pawl_plate(p)
    A("Pawl, 16 mm C45, hardened tip", pawl, STEEL, "made", 7, (-720, 0, 280))
    grip_pawl = (-xi) - px0
    for nm, sh in sp.bolt_set(24, grip_pawl, (px0, py, pzv), (-1, 0, 0)):
        A(nm + ", galvanised (pawl pivot, nyloc)", sh, GALV, "fastener", 7, (-720, 0, 280))
    A("M24 washer (ISO 7089), pawl spacer", sp.frame((px1, py, pzv), (1, 0, 0)) * cp.washer(24), GALV, "fastener", 7, (-720, 0, 280))
    # 8 brake
    band, lever, bgrip = _brake_parts(p)
    A("Brake band with woven lining and end links", band, STEEL, "made", 8, (-460, 320, -280))
    A("Brake lever with pivot shaft and inner arm", lever, GALV, "made", 8, (-460, 320, -280))
    A("Brake lever grip", bgrip, "epdm", "bought", 8, (-460, 320, -280))
    # 10 gear guard, spacers, M8 bolts
    guard, spacers = _guard_parts(p)
    A("Gear guard, 2 mm sheet, painted yellow", guard, "safety_yellow", "made", 10, (850, 0, 0))
    gx1 = p["guard"][4]
    for i, (s_, (sy, sz_)) in enumerate(zip(spacers, p["guard_sp"])):
        A(f"Gear guard spacer {i + 1}, 14 mm tube", s_, GALV, "made", 10, (850, 0, 0))
        for nm, sh in sp.bolt_set(8, gx1 - xi, (gx1, sy, dz + sz_), (1, 0, 0)):
            A(nm + ", galvanised", sh, GALV, "fastener", 19, (850, 0, 0))
    # 11 anchors: shackles in the ears, chains, turnbuckles, helical anchors
    ey, ez, er, eh = p["ear"]
    aey, aex = p["anchor_eye"]
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        bow, spin = sp.shackle(12.0, 22.0, 52.0, (sg * cx, ey, ez), (1, 0, 0), (0, 1, 0))
        A(f"Bow shackle, 10 mm, galvanised, at the {side} ear", bow, GALV, "bought", 11, (0, 0, 0))
        A(f"Shackle pin, {side} ear", spin, GALV, "fastener", 11, (0, 0, 0))
        eye = (sg * aex, aey, 40.0)
        start = (sg * cx, ey + 52.0 + 6.0 - 8.0, ez)
        _chain_run(out, p, side, start, eye, group, 11, xf)
        A(f"Helical ground anchor, 20 mm x 1.0 m, 150 mm helix, {side}", _anchor(eye, p, sg), GALV, "bought", 11, (0, 0, 0))
    return out


def roller_a(p=PARAMS, xf=None, group="roller"):
    """Bund roller saddle: side plates, feet, tie bars, welds, roller, axle and R-clips, on the near bund crest."""
    xf = xf or (lambda s: _site_roller(s, p))
    out = []
    A = lambda nm, sh, mat, kind, bom=None: _add(out, nm, xf(sh), mat, kind, bom, group)  # noqa: E731
    st, sl, sh_ = p["saddle"]
    sx = p["saddle_x"]
    az, ad, al = p["axle"]
    ro, rl = p["roller"]
    fo, ft = p["rflange"]
    fw, fth = p["foot"]
    td, ty = p["tie"]
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        x0, x1 = sorted((sg * (sx - st / 2), sg * (sx + st / 2)))
        pl = bx(x0, x1, -sl / 2, sl / 2, fth, sh_) + xcyl(x0, x1, 0, az, 35.0)
        pl = pl - xcyl(x0 - 1, x1 + 1, 0, az, ad / 2 + 0.5)
        A(f"Roller saddle side plate, {side}, 6 mm", pl, GALV, "made", 12)
        foot = Pos(sg * sx, 0, 0) * cp.sheet(fw, sl, fth, r_corner=6, edge=0.8)
        A(f"Roller saddle foot plate, {side}, 80 x 6", foot, GALV, "made", 12)
        for f in (1, -1):
            xx = sg * sx + f * st / 2
            A(f"Weld, saddle plate to foot, {side}", sp.weld_on((xx, -sl / 2 + 10, fth), (0, 1, 0), sl - 20, 4.0, (f, 0, 0), (0, 0, 1)), GALV, "weld")
    for yy in (-ty, ty):
        bar = sp.frame((-(sx - st / 2), yy, 40.0), (1, 0, 0)) * cp.round_bar(td, 2 * (sx - st / 2), 1.0)
        A(f"Roller saddle tie bar, 20 mm, {'ahead' if yy < 0 else 'behind'}", bar, GALV, "made", 12)
        for sg in (1, -1):
            A("Weld, tie bar to saddle plate", sp.ring_weld(td / 2, 4.0, (sg * (sx - st / 2), yy, 40.0), (-sg, 0, 0)), GALV, "weld")
    roll = xcyl(-rl / 2, rl / 2, 0, az, ro / 2)
    for sg in (1, -1):
        a0, a1 = sorted((sg * rl / 2, sg * (rl / 2 + ft)))
        roll = roll + xcyl(a0, a1, 0, az, fo / 2)
    roll = roll - xcyl(-rl / 2 - ft - 1, rl / 2 + ft + 1, 0, az, ad / 2 + 0.5)
    A("Bund roller, UHMW-PE 100 x 200 with 160 mm flanges", roll, UHMW, "made", 12)
    axle = sp.frame((-al / 2, 0, az), (1, 0, 0)) * cp.round_bar(ad, al, 1.0)
    for sg in (1, -1):
        axle = axle - zcyl(sg * (al / 2 - 6), 0, az - 20, az + 20, 3.3)
    A("Roller axle, 25 mm stainless 316", axle, SS, "made", 12)
    for sg in (1, -1):
        clip = Pos(sg * (al / 2 - 6), 0, az) * Rot(0, 90, 0) * cp.split_pin(20)
        A(f"Split pin in the roller axle pin hole, {'right' if sg > 0 else 'left'}", clip, SS, "fastener", 19)
    return out


def rake_a(p=PARAMS, xf=None, group="rake", bom=True):
    """The rake: beam, blade, skids, hangers, end caps, every bolt and crush sleeve, shackles, bridles, swivels and
    ballast bags, in the site frame."""
    xf = xf or (lambda s: _site_rake(s, p))
    out = []
    B = (lambda n: n) if bom else (lambda n: None)
    A = lambda nm, sh, mat, kind, b=None, ex=(0, 0, 0): _add(out, nm, xf(sh), mat, kind, B(b) if b else None, group, ex)  # noqa: E731
    R = rake_components(p)
    bs, bw, bl = p["beam"]
    z0 = p["beam_z0"]
    bt, bh, bg, blen = p["blade"]
    y_bf = bt
    yr = y_bf + bs
    yc, zc = y_bf + bs / 2, z0 + bs / 2
    bd, pitch, bz = p["blade_bolts"]
    xs = [-bl / 2 + 150 + i * pitch for i in range(int((bl - 300) // pitch) + 1)]
    hz = (85.0, 135.0)
    sk_w, sk_t, sk_l, sk_y = p["skid"]
    hth, hw, hll = p["hanger"]
    skid_bolt_y = (yr + 35.0, yr + 90.0)
    A("Rake beam, pultruded FRP 100 x 100 x 6", R["beam"].shape, FRP, "bought", 13, (0, 0, 0))
    blade = R["blade"].shape
    for x in xs:
        blade = blade - sp.csk_hole(10, bt + 2, (x, 0, bz), (0, -1, 0))
    for sx in p["skid_x"]:
        for z in hz:
            blade = blade - sp.csk_hole(10, bt + 2, (sx, 0, z), (0, -1, 0))
    A("Rake blade, UHMW-PE 15 mm", blade, UHMW, "bought", 14, (0, -550, 0))
    ct_, cl_ = p["cap"]
    et, ereach, ey_f, ey_r, eh = p["eye"]
    # blade and hanger bolts: countersunk heads flush in the blade face, crush sleeves inside the beam
    for x, z, grip, nm in [(x, bz, bt + bs, "blade") for x in xs] + [(sx, z, bt + bs + hth, "hanger") for sx in p["skid_x"] for z in hz]:
        L = math.ceil((grip + 2 + 8.4 + 3.75) / 5) * 5
        A(f"M10 x {L} countersunk bolt (ISO 10642), A4 stainless, {nm}", sp.frame((x, 0, z), (0, -1, 0)) * sp.csk_bolt(10, L), SS, "fastener", 19, (0, -550, 0))
        for n_, sh in sp.nut_washer(10, (x, grip, z), (0, 1, 0)):
            A(n_ + ", A4 stainless (nyloc)", sh, SS, "fastener", 19, (0, -550, 0))
        A("Crush sleeve, 16 x 2.7 stainless", sp.frame((x, y_bf + bw, z), (0, 1, 0)) * sp.sleeve(16.0, 10.6, bs - 2 * bw), SS, "fastener", 19, (0, -550, 0))
    # skids and hangers
    for i, sx in enumerate(p["skid_x"]):
        sk = bx(sx - sk_w / 2, sx + sk_w / 2, sk_y, sk_y + sk_l, 0, sk_t)
        sk = sk - (Pos(sx, sk_y, 0) * Rot(45, 0, 0) * Box(sk_w + 2, 20, 20))
        for yy in skid_bolt_y:
            sk = sk - zcyl(sx, yy, -1, 10.0, 12.5) - zcyl(sx, yy, -1, sk_t + 1, 5.5)
        A(f"Skid {i + 1}, UHMW-PE 60 x 20 x 450", sk, UHMW, "made", 15, (0, 350, -300))
        vert = bx(sx - hw / 2, sx + hw / 2, yr, yr + hth, sk_t, z0 + bs - 10)
        for z in hz:
            vert = vert - bx(sx - 5.5, sx + 5.5, yr - 1, yr + hth + 1, z - 12, z + 12)
        horiz = bx(sx - hw / 2, sx + hw / 2, yr, yr + hll, sk_t, sk_t + hth)
        for yy in skid_bolt_y:
            horiz = horiz - zcyl(sx, yy, sk_t - 1, sk_t + hth + 1, 5.5)
        A(f"Skid hanger {i + 1}, 6 mm stainless 316 angle", vert + horiz, SS, "made", 15, (0, 350, -140))
        for yy in skid_bolt_y:
            for n_, sh in sp.bolt_set(10, sk_t - 10.0 + hth, (sx, yy, 10.0), (0, 0, -1)):
                A(n_ + ", A4 stainless (skid)", sh, SS, "fastener", 19, (0, 350, -300))
    # end caps with eye plates, cap bolts with sleeves
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        xa, xb_ = sorted((sg * (bl / 2 - cl_ + ct_), sg * (bl / 2 + ct_)))
        xe0, xe1 = sorted((sg * bl / 2, sg * (bl / 2 + ct_)))
        top = bx(xa, xb_, y_bf, yr + ct_, z0 + bs, z0 + bs + ct_)
        bot = bx(xa, xb_, y_bf, yr + ct_, z0 - ct_, z0)
        rear = bx(xa, xb_, yr, yr + ct_, z0 - ct_, z0 + bs + ct_)
        endp = bx(xe0, xe1, 0, yr + ct_, z0 - ct_, z0 + bs + ct_)
        xp0, xp1 = sorted((sg * (bl / 2 + ct_), sg * (bl / 2 + ct_ + ereach)))
        ez_ = p["eye_z"]
        eyep = bx(xp0, xp1, ey_f - 25, ey_r + 25, ez_ - et / 2, ez_ + et / 2)
        for yy in (ey_f, ey_r):
            eyep = eyep - zcyl((xp0 + xp1) / 2, yy, ez_ - et, ez_ + et, eh / 2)
        cap = top + bot + rear + endp + eyep
        for xo_ in (cl_ - 46, cl_ - 86):
            cap = cap - zcyl(sg * (bl / 2 - xo_ + 6), yc, z0 - ct_ - 1, z0 + bs + ct_ + 1, 6.5)
        A(f"End cap with eye plate, {side}, stainless 316", cap, SS, "made", 16, (sg * 250, 0, 0))
        for xo_ in (cl_ - 46, cl_ - 86):
            xx = sg * (bl / 2 - xo_ + 6)
            for n_, sh in sp.bolt_set(12, bs + 2 * ct_, (xx, yc, z0 + bs + ct_), (0, 0, 1)):
                A(n_ + ", A4 stainless (end cap)", sh, SS, "fastener", 19, (sg * 250, 0, 0))
            A("Crush sleeve, 18 x 2.7 stainless", sp.frame((xx, yc, z0 + bw), (0, 0, 1)) * sp.sleeve(18.0, 12.6, bs - 2 * bw), SS, "fastener", 19, (sg * 250, 0, 0))
    # bridles: a shackle in each eye, two legs to each swivel
    af, ar, az = p["bridle"]
    xe = bl / 2 + ct_ + ereach / 2
    apex_f, apex_r = (0.0, -af, az), (0.0, yr + ar, az)
    for (yy, apex, nm) in ((ey_f, apex_f, "front"), (ey_r, apex_r, "rear")):
        crowns = []
        for sg in (1, -1):
            o = (sg * xe, yy, p["eye_z"])
            dirh = sp._unit((apex[0] - o[0], apex[1] - o[1], 0.0))
            bow, spin = sp.shackle(12.0, 22.0, 52.0, o, (0, 0, 1), dirh)
            A(f"Bow shackle, 10 mm, galvanised, {nm} eye, {'right' if sg > 0 else 'left'}", bow, GALV, "bought", 17)
            A(f"Shackle pin, {nm} eye, {'right' if sg > 0 else 'left'}", spin, GALV, "fastener", 17)
            crowns.append(tuple(o[i] + dirh[i] * 52.0 for i in range(3)))
        legs = sp.rope_run([crowns[0], apex], 12.0) + sp.rope_run([crowns[1], apex], 12.0)
        A(f"Bridle, {nm}, two 12 mm polyester legs with spliced eyes", legs, ROPE_M, "bought", 17)
        y0s = apex[1] - 110 if nm == "front" else apex[1]
        sw = sp.frame((0.0, y0s, az), (0, 1, 0)) * cp.break_edges(Pos(0, 0, 55) * Cylinder(18.0, 110.0), 3.0)
        sw = sw + sp.frame((0.0, y0s + 55, az), (0, 1, 0)) * (Cylinder(24.0, 16.0))
        A(f"Swivel, eye to eye, 1 t, galvanised, {nm}", sw, GALV, "bought", 17)
    # 22 ballast bags of salt (filled on site), strapped on the beam behind the blade
    bl_, bd_, bh_ = p["ballast"]
    for sg in (1, -1):
        bag = bx(sg * p["ballast_x"] - bl_ / 2, sg * p["ballast_x"] + bl_ / 2, y_bf + 1, y_bf + bd_, z0 + bs, z0 + bs + bh_)
        A(f"Ballast bag of salt, woven polypropylene, {'right' if sg > 0 else 'left'}", cp.break_edges(bag, 25.0), CANVAS, "bought", 22, (0, 0, 380))
    return out


def rope_a(p=PARAMS, rake_y=None, damper=True, group="rope"):
    """Near pull rope: three layers on the drum, run over the bund roller to the front swivel; the return rope's
    first 1.5 m toward the far capstan; a rope damper bag on the loaded rope."""
    D = derived(p)
    rake_y = p["rake_y"] if rake_y is None else rake_y
    out = []
    near, far = rope_points(p, rake_y)
    D_ = derived(p)
    centre = (D_["crest_y"], p["bund"][0] + p["axle"][0])
    run = sp.rope_run(over_roller(near[0], centre, p["roller"][0] / 2 + p["rope_d"] / 2 + 0.5, near[2]), p["rope_d"])
    bxr = D["barrel_x"]
    wound = xcyl(bxr[0] + 6, bxr[1] - 6, 0, p["drum_z"], D["layers"][2][1] + p["rope_d"] / 2) - \
        xcyl(bxr[0], bxr[1], 0, p["drum_z"], p["barrel"][0] / 2 + 0.2)
    _add(out, "Pull rope, 12 mm polyester double braid, 45 m (three layers on the drum)", run + _site_cap(wound, p), ROPE_M, "bought", 18, group)
    a = far[0]
    _add(out, "Return rope toward the far capstan, 12 mm polyester (first 1.5 m shown)",
         sp.rope_run([a, (a[0], a[1] + 750, a[2] + 20), (a[0], a[1] + 1500, a[2] + 60)], p["rope_d"]), ROPE_M, "bought", 18, group)
    if damper:
        damper_on(out, near[1], near[2], group=group)
        out[-1]["bom"] = 20
    return out


def over_roller(a, centre, R, c, step_deg=3.0):
    """Rope polyline from point a over a roller (axis along X at centre (y, z), rope centre-line radius R) to
    point c: straight to the tangent point, round the arc, straight on from the far tangent point."""
    yc, zc = centre

    def tangent(pt, side):
        dy, dz = pt[1] - yc, pt[2] - zc
        d = math.hypot(dy, dz)
        base = math.atan2(dz, dy)
        off = math.acos(R / d)
        return base + side * off
    ta = tangent(a, -1)          # incoming tangent point (from behind, -Y side)
    tc = tangent(c, +1)          # outgoing tangent point (pan side, +Y)
    if ta < tc:
        ta += 2 * math.pi
    n = max(2, int(math.degrees(ta - tc) // step_deg))
    arc = [(a[0], yc + R * math.cos(ta - (ta - tc) * i / n), zc + R * math.sin(ta - (ta - tc) * i / n)) for i in range(n + 1)]
    return [a] + arc + [c]


def option_a(p=PARAMS):
    return capstan_a(p) + roller_a(p) + rake_a(p) + rope_a(p)


def damper_on(out, r0, r1, t=0.6, group="rope"):
    """Rope damper bag hung by a snap hook on the rope between points r0 and r1."""
    c = tuple(r0[i] + (r1[i] - r0[i]) * t for i in range(3))
    u = sp._unit(tuple(r1[i] - r0[i] for i in range(3)))
    hook = sp.frame(c, u) * Torus(13.0, 3.5)
    strap = rod((c[0], c[1], c[2] - 16.5), (c[0], c[1], c[2] - 160), 4.0)
    bag = cp.break_edges(bx(c[0] - 110, c[0] + 110, c[1] - 80, c[1] + 80, c[2] - 360, c[2] - 160), 30.0)
    _add(out, "Rope damper bag, canvas, 5 kg of sand, snap hook on the rope", hook + strap + bag, CANVAS, "bought", None, group)


# ---------------------------------------------------------------------------------------------- option B
PARAMS_B = {"beam": (100.0, 6.0, 1500.0), "blade": (15.0, 300.0, 10.0, 1500.0), "skid_x": (-450.0, 450.0),
            "ballast": (400.0, 300.0, 120.0), "ballast_x": 380.0,
            "post": (100.0, 5.0), "base": (400.0, 12.0), "stake": (25.0, 900.0), "sheave": (250.0, 60.0),
            "block_plate": (340.0, 10.0), "haul_shown": 8000.0, "toggles": 6}


def _pB():
    p = dict(PARAMS)
    p.update(PARAMS_B)
    return p


def option_b(p=None):
    """Bund-walk haul: a team walks the dry ground behind the bund pulling the rope by toggles; a turning sheave on
    a staked post turns the rope 90 degrees; a 1.5 m rake (half of option A's) is drawn across the pan."""
    p = p or _pB()
    D = derived(p)
    out = []
    G = "turning block"
    A = lambda nm, sh, mat, kind, bom=None, grp=G: _add(out, nm, sh, mat, kind, None, grp)  # noqa: E731
    yp = D["drum_y"]
    sd, sw = p["sheave"]
    R = sd / 2 - 0.25 * sw + p["rope_d"] / 2 + 0.5           # rope centre-line radius in the groove
    xs0 = R                                                   # sheave centre x: the incoming rope runs on x = 0
    zr = D["roller_top"] + p["rope_d"] / 2 + 0.5               # rope height, level with the bund roller top
    zs = zr                                                    # sheave mid-plane
    pw, pt = p["post"]
    bw_, bt_ = p["base"]
    bpl, bpt = p["block_plate"]
    z_low = zs - sw / 2 - 2 - bpt                              # lower block plate underside
    # base plate with four stake holes, post, gussets, welds, stakes
    base = Pos(xs0, yp, 0) * cp.sheet(bw_, bw_, bt_, holes=[(sx * 150, sy * 150, 28.0) for sx in (-1, 1) for sy in (-1, 1)], r_corner=10, edge=1.0)
    A("Post base plate, 400 x 400 x 12", base, GALV, "made")
    post = Pos(xs0, yp, bt_) * cp.shs(pw, pt, z_low - bt_)
    A("Post, SHS 100 x 100 x 5", post, GALV, "made")
    seg = pw / 2 - 12 - 6
    for f, ax, d1, ln in (((xs0 - pw / 2 + 12, yp + pw / 2, bt_), (1, 0, 0), (0, 1, 0), seg), ((xs0 + 6, yp + pw / 2, bt_), (1, 0, 0), (0, 1, 0), seg),
                          ((xs0 - pw / 2 + 12, yp - pw / 2, bt_), (1, 0, 0), (0, -1, 0), seg), ((xs0 + 6, yp - pw / 2, bt_), (1, 0, 0), (0, -1, 0), seg),
                          ((xs0 + pw / 2, yp - pw / 2 + 12, bt_), (0, 1, 0), (1, 0, 0), pw - 24), ((xs0 - pw / 2, yp - pw / 2 + 12, bt_), (0, 1, 0), (-1, 0, 0), pw - 24)):
        A("Weld, post to base plate", sp.weld_on(f, ax, ln, 6.0, d1, (0, 0, 1)), GALV, "weld")
    for sy in (1, -1):
        g = yz_plate([(0, 0), (130, 0), (0, 260)], -5, 5)
        g = Pos(xs0, yp + sy * pw / 2, bt_) * (g if sy > 0 else Rot(0, 0, 180) * g)
        A(f"Gusset, 10 mm, {'pan side' if sy > 0 else 'back'}", cp.break_edges(g, 1.0), GALV, "made")
    for sx in (-1, 1):
        for sy in (-1, 1):
            st = Pos(xs0 + sx * 150, yp + sy * 150, bt_ + 15) * Rot(180, 0, 0) * (cp.round_bar(p["stake"][0], p["stake"][1], 2.0)) + \
                Pos(xs0 + sx * 150, yp + sy * 150, bt_) * cp.round_bar(40.0, 15.0, 1.5)
            A(f"Ground stake, 25 mm x 900 with collar", st, GALV, "made")
    # block: lower and upper plates, sheave, axle bolt, two spacer posts with bolts
    lowp = Pos(xs0, yp, z_low) * cp.sheet(bpl, bpl, bpt, holes=[(0, 0, 25.0), (110, 110, 13.0), (140, -60, 13.0), (-60, 140, 13.0)], r_corner=30, edge=1.0)
    A("Block lower plate, 340 x 340 x 10", lowp, GALV, "made")
    z_up = zs + sw / 2 + 2
    upp = Pos(xs0, yp, z_up) * cp.sheet(bpl, bpl, bpt, holes=[(0, 0, 25.0), (110, 110, 13.0), (140, -60, 13.0), (-60, 140, 13.0)], r_corner=30, edge=1.0)
    A("Block upper plate, 340 x 340 x 10", upp, GALV, "made")
    for f, ax, d1 in (((xs0 - pw / 2 + 12, yp + pw / 2, z_low), (1, 0, 0), (0, 1, 0)), ((xs0 - pw / 2 + 12, yp - pw / 2, z_low), (1, 0, 0), (0, -1, 0))):
        A("Weld, post to block lower plate", sp.weld_on(f, ax, pw - 24, 6.0, d1, (0, 0, -1)), GALV, "weld")
    shv = Pos(xs0, yp, zs) * (cp.pulley(sd, sw, 26.0))
    A("Turning sheave, UHMW-PE 250 mm", shv, UHMW, "made")
    for nm, sh in sp.bolt_set(24, z_up + bpt - z_low, (xs0, yp, z_up + bpt), (0, 0, 1)):
        A(nm + ", galvanised (sheave axle)", sh, GALV, "fastener")
    for dx, dy in ((110, 110), (140, -60), (-60, 140)):
        A("Block spacer, 25 mm tube", Pos(xs0 + dx, yp + dy, z_low + bpt) * sp.sleeve(25.0, 13.0, z_up - z_low - bpt), GALV, "made")
        for nm, sh in sp.bolt_set(12, z_up + bpt - z_low, (xs0 + dx, yp + dy, z_up + bpt), (0, 0, 1)):
            A(nm + ", galvanised", sh, GALV, "fastener")
    # rake (half width), roller on the crest, haul rope with toggles, damper bag
    out += roller_a(p)
    out += rake_a(p, bom=False)
    a_t = (0.0, yp, zr)
    near = over_roller(a_t, (D["crest_y"], p["bund"][0] + p["axle"][0]), p["roller"][0] / 2 + p["rope_d"] / 2 + 0.5,
                       (0.0, p["rake_y"] - p["bridle"][0] - 110, p["bridle"][2]))
    arc = [(xs0 + R * math.cos(math.radians(a)), yp + R * math.sin(math.radians(a)), zr) for a in range(180, 271, 6)]
    haul = [(-p["haul_shown"], yp - R, zr)]
    pts = list(reversed(near))[:-1] + arc + haul
    _add(out, "Haul rope, 12 mm polyester double braid, 45 m", sp.rope_run(pts, p["rope_d"]), ROPE_M, "bought", None, "rope")
    for i in range(p["toggles"]):
        x = -1500.0 - i * 1100.0
        tg = Pos(x, yp - R, zr) * Rot(90, 0, 0) * cp.break_edges(Cylinder(17.5, 320.0), 3.0)
        _add(out, f"Toggle {i + 1}, hardwood 35 x 320, spliced into the rope", tg, "hardwood", "made", None, "rope")
    damper_on(out, near[-2], near[-1])
    a = rope_points(p)[1][0]
    _add(out, "Return line toward the far bund, 12 mm polyester (first 1.5 m shown)",
         sp.rope_run([a, (a[0], a[1] + 750, a[2] + 20), (a[0], a[1] + 1500, a[2] + 60)], p["rope_d"]), ROPE_M, "bought", None, "rope")
    return out


# ---------------------------------------------------------------------------------------------- option C
PARAMS_C = {"puller_y": None, "plate": (700.0, 360.0, 8.0), "gap": 96.0, "rope_z": 200.0, "lever_len": 1000.0,
            "lever_angle": 65.0}


def option_c(p=None):
    """Lever rope puller: a hand lever with a moving cam jaw and a holding cam jaw pulls the rope through in short
    strokes; the frame is chained to two helical anchors; the same 3 m rake as option A."""
    p = p or dict(PARAMS, **PARAMS_C)
    D = derived(p)
    out = []
    G = "puller"
    A = lambda nm, sh, mat, kind, grp=G: _add(out, nm, sh, mat, kind, None, grp)  # noqa: E731
    y0 = D["drum_y"]
    pl_l, pl_h, pl_t = p["plate"]
    gi = p["gap"] / 2
    go = gi + pl_t
    zr = p["rope_z"]
    P_ = (y0 - 100.0, 300.0)             # lever pivot (y, z)
    J_ = (y0 - 40.0, 245.0)              # moving jaw pin
    H_ = (y0 + 180.0, 260.0)             # holding jaw pin
    holes = [(P_[0], P_[1], 21.0), (H_[0], H_[1], 17.0)]
    holes += [(y0 + s * 330, 179.0, 13.0) for s in (-1, 1)] + [(y0 + s * 300, 40.0, 13.0) for s in (-1, 1)] + [(y0 - 330, 100.0, 13.0)]
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        x_face = gi if sg > 0 else -go
        sh = cp.sheet(pl_l, pl_h, pl_t, holes=[(y - y0, z - pl_h / 2, d) for y, z, d in holes], r_corner=20, edge=1.0)
        A(f"Puller side plate, {side}, 8 mm S275", sp.frame((x_face, y0, pl_h / 2), (1, 0, 0), u=(0, 1, 0)) * sh, GALV, "made")
    # anvil plate welded between the side plates under the rope
    anv = bx(-gi, gi, y0 - 250, y0 + 250, zr - p["rope_d"] / 2 - 12, zr - p["rope_d"] / 2)
    anv = cp.break_edges(anv, 1.0)
    A("Anvil plate, 12 mm, serrated top", anv, STEEL, "made")
    for sg in (1, -1):
        A("Weld, anvil to side plate", sp.weld_on((sg * gi, y0 - 200, zr - p["rope_d"] / 2 - 12), (0, 1, 0), 400.0, 5.0, (-sg, 0, 0), (0, 0, -1)), STEEL, "weld")
    # guide rollers and spacers on M12 bolts
    for nm_, yy, zz, od in (("Front rope guide roller", y0 + 330, 179.0, 30.0), ("Rear rope guide roller", y0 - 330, 179.0, 30.0),
                            ("Frame spacer, front", y0 + 300, 40.0, 30.0), ("Frame spacer, rear", y0 - 300, 40.0, 30.0)):
        mat = UHMW if "roller" in nm_ else GALV
        L_ = p["gap"] - (2.0 if "roller" in nm_ else 0.0)
        A(nm_, sp.frame((-L_ / 2, yy, zz), (1, 0, 0)) * sp.sleeve(od, 13.0, L_), mat, "made")
        for nm, sh in sp.bolt_set(12, 2 * go, (go, yy, zz), (1, 0, 0)):
            A(nm + ", galvanised", sh, GALV, "fastener")
    # lever weldment: two fork plates, bridge, handle tube; grip
    def hull_plate(circles, x0, x1):
        pts = _hull_two_circles(circles[0], circles[1])
        return yz_plate(pts, x0, x1)
    top = (P_[0], P_[1] + 40.0, 16.0)
    lever = None
    for sg in (1, -1):
        x0, x1 = sorted((sg * 12.0, sg * 20.0))
        a = hull_plate([(P_[0], P_[1], 22.0), (J_[0], J_[1], 16.0)], x0, x1) + hull_plate([(P_[0], P_[1], 22.0), top], x0, x1)
        lever = a if lever is None else lever + a
    lever = lever + bx(-20, 20, P_[0] - 20, P_[0] + 20, P_[1] + 35, P_[1] + 52)
    la = math.radians(p["lever_angle"])
    u = (0.0, -math.cos(la), math.sin(la))
    hb = (0.0, P_[0], P_[1] + 52)
    handle = sp.frame(hb, u, u=(1, 0, 0)) * cp.shs(40.0, 3.0, p["lever_len"])
    lever = lever + handle
    for c_, r_ in ((P_, 10.5), (J_, 6.5)):
        lever = lever - xcyl(-25, 25, c_[0], c_[1], r_)
    A("Lever weldment: fork plates, bridge and 40 x 40 handle", lever, GALV, "made")
    ge = tuple(hb[i] + u[i] * (p["lever_len"] - 160) for i in range(3))
    grip = sp.frame(ge, u, u=(1, 0, 0)) * (cp.break_edges(Pos(0, 0, 75) * Box(50, 50, 150), 4.0) - Pos(0, 0, 75) * Box(40.2, 40.2, 152))
    A("Lever grip, EPDM sleeve", grip, "epdm", "bought")
    # jaws
    def jaw(c_, r_, f0, f1, hole):
        poly = [(c_[0] - r_, c_[1]), (c_[0], c_[1] + r_), (c_[0] + r_, c_[1]), (f1, zr + p["rope_d"] / 2 + 1), (f0, zr + p["rope_d"] / 2 + 1)]
        j = yz_plate(poly, -10.0, 10.0) + xcyl(-10.0, 10.0, c_[0], c_[1], r_)
        return j - xcyl(-11, 11, c_[0], c_[1], hole)
    A("Jaw, moving, 20 mm C45 cam, hardened serrated face", jaw(J_, 16.0, J_[0] - 30, J_[0] + 30, 6.5), STEEL, "made")
    A("Jaw, holding, 20 mm C45 cam, hardened serrated face", jaw(H_, 18.0, H_[0] - 35, H_[0] + 25, 8.5), STEEL, "made")
    # pins, spacers and split pins
    for nm_, c_, d_, grip_, x_head in (("lever pivot", P_, 20, 2 * go, go), ("holding jaw", H_, 16, 2 * go, go), ("moving jaw", J_, 12, 40.0, 20.0)):
        pin = sp.frame((x_head, c_[0], c_[1]), (1, 0, 0)) * cp.clevis_pin(d_, grip_)
        A(f"Clevis pin, {d_} mm (ISO 2341), {nm_}", pin, SS, "fastener")
        spl = sp.frame((x_head, c_[0], c_[1]), (1, 0, 0)) * Pos(0, 0, -grip_ - d_) * cp.split_pin(d_)
        A(f"Split pin (ISO 1234), {nm_}", spl, SS, "fastener")
    for sg in (1, -1):
        A("Pivot spacer, 30 mm tube", sp.frame((sg * 20.0 if sg > 0 else -gi, P_[0], P_[1]), (1, 0, 0)) * sp.sleeve(30.0, 21.0, gi - 20.0), GALV, "made")
        A("Holding jaw spacer, 24 mm tube", sp.frame((10.0 if sg > 0 else -gi, H_[0], H_[1]), (1, 0, 0)) * sp.sleeve(24.0, 17.0, gi - 10.0), GALV, "made")
    # anchor shackles in the side plates, chains, turnbuckles, helical anchors
    aey = y0 - 1700.0
    for sg in (1, -1):
        side = "right" if sg > 0 else "left"
        xc = sg * (gi + pl_t / 2)
        bow, spin = sp.shackle(12.0, 22.0, 52.0, (xc, y0 - 330, 100.0), (1, 0, 0), (0, -1, 0))
        A(f"Bow shackle, 10 mm, galvanised, {side} plate", bow, GALV, "bought")
        A(f"Shackle pin, {side} plate", spin, GALV, "fastener")
        eye = (sg * 203.0, aey, 40.0)
        _chain_run(out, p, side, (xc, y0 - 330 - 50, 100.0), eye, G, None, None)
        A(f"Helical ground anchor, 20 mm x 1.0 m, 150 mm helix, {side}", Rot(0, 0, 180) * Pos(0, 0, 0) * _anchor((-sg * 203.0, -aey, 40.0), p, sg), GALV, "bought")
    # bund roller, rake, rope through the puller into a hand-coiled tail, damper bag
    out += roller_a(p)
    out += rake_a(p, bom=False)
    apex = (0.0, p["rake_y"] - p["bridle"][0] - 110, p["bridle"][2])
    crest = (D["crest_y"], p["bund"][0] + p["axle"][0])
    Rr = p["roller"][0] / 2 + p["rope_d"] / 2 + 0.5
    gfront = (y0 + 330, 179.0)
    Rg = 15.0 + p["rope_d"] / 2 + 0.5
    over = over_roller((0.0, gfront[0], gfront[1] + Rg), crest, Rr, apex)
    guide = over_roller((0.0, y0 - 330, gfront[1] + Rg), gfront, Rg, over[1])
    tail = [(0.0, y0 - 380, gfront[1] + Rg - 4), (0.0, y0 - 520, 60.0), (0.0, y0 - 600, 8.0)]
    coil = [(260 * math.sin(math.radians(a)), y0 - 860 + 260 * math.cos(math.radians(a)) * (1 - a / 2400), 8.0 + 13 * (a // 360)) for a in range(0, 1081, 20)]
    pts = list(reversed(over[1:])) + list(reversed(guide[:-1])) + tail + coil
    _add(out, "Pull rope, 12 mm polyester double braid, 45 m (tail coiled by hand)", sp.rope_run(pts, p["rope_d"]), ROPE_M, "bought", None, "rope")
    damper_on(out, over[-2], over[-1])
    a = rope_points(p)[1][0]
    _add(out, "Return rope toward the far capstan, 12 mm polyester (first 1.5 m shown)",
         sp.rope_run([a, (a[0], a[1] + 750, a[2] + 20), (a[0], a[1] + 1500, a[2] + 60)], p["rope_d"]), ROPE_M, "bought", None, "rope")
    return out


def components(option=CHOSEN):
    parts = {"A": option_a, "B": option_b, "C": option_c}[option]()
    return parts + site_context()


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    groups = {
        "saltdrag-capstan": [c.shape for c in capstan_components().values()],
        "saltdrag-rake": [c.shape for c in rake_components().values()],
        "saltdrag-roller": [c.shape for c in roller_components().values()],
    }
    for name, shapes in groups.items():
        cpd = Compound(shapes)
        export_step(cpd, str(out / "step" / f"{name}.step"))
        export_stl(cpd, str(out / "stl" / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.3)
        bb = cpd.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    lay = layout()
    asm = Compound([s for _, s in lay.values()] + list(context()))
    export_step(asm, str(out / "step" / "saltdrag-assembly.step"))
    D = derived()
    print(f"gear ratio {D['ratio']:.1f}, centre distance {D['cd']:.0f} mm, crank shaft {D['pin_z']:.0f} mm above ground")
    for n, r, tot in D["layers"]:
        print(f"rope layer {n}: radius {r:.1f} mm, cumulative {tot:.1f} m")
    print(f"freeboard at four layers {D['freeboard']:.1f} mm")
    tot = {}
    for (grp, k), (name, bom, m) in masses().items():
        tot[grp] = tot.get(grp, 0) + m
        print(f"{grp:8s} {name:46s} BOM {bom:2d} {m:7.2f} kg")
    print({k: round(v, 1) for k, v in tot.items()})
    print_checks()
    for opt in OPTIONS:
        real = [q for q in components(opt) if q["kind"] != "context"]
        print(f"option {opt} ({OPTIONS[opt]}): {len(real)} parts, {sum(cp.mass_kg(q) for q in real):.1f} kg")
