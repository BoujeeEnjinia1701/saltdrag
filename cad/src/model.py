"""SaltDrag parametric model (build123d), TRL 3, constructable design (SDG-DDR-002).

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
    "xtube": (40.0, 3.0), "xplate": (80.0, 6.0),
    "xtubes": {"front": (-240.0, 110.0), "rear": (240.0, 110.0), "top": (0.0, 850.0)},
    # 3 drum: axis height; barrel pipe OD, wall, length; flange OD, thickness; brake rim width,
    #   thickness; shaft diameter, x from, x to; x of the outer face of the right flange
    "drum_z": 560.0, "barrel": (168.3, 4.5, 280.0), "flange": (330.0, 6.0), "rim": (50.0, 6.0),
    "dshaft": (40.0, -296.0, 296.0), "drum_right": 185.0,
    # 4, 5 spur gear pair, module 4: gear 84 teeth, face 30; pinion 14 teeth, face 35
    "module": 4.0, "z_gear": 84, "z_pinion": 14, "gear_face": 30.0, "pinion_face": 35.0,
    "gear_x0": 256.0, "pinion_x0": 253.5,
    # 5 crank shaft diameter and half-length; 9 crank: radius, arm (width, thickness), hub (OD, length),
    #   grip (OD, length); crank angle of the right handle from +Y toward +Z (deg)
    "pshaft": (25.0, 345.0), "crank_r": 330.0, "crank_arm": (40.0, 10.0), "crank_hub": (50.0, 40.0),
    "grip": (32.0, 120.0), "crank_angle": 60.0, "crank_x0": 305.0,
    # 6 flange bearings (housing square, flange thickness, overall length, bolt square, bolt dia)
    "brg_drum": (130.0, 16.0, 40.0, 102.0, 14.0), "brg_pin": (95.0, 13.0, 34.0, 70.0, 12.0),
    # 7 ratchet wheel (OD, teeth, thickness, x of inner face); pawl (pivot y, z; thickness; pin dia)
    "ratchet": (200.0, 20, 20.0, -256.0), "pawl": (130.0, 690.0, 16.0, 24.0, 40.0),
    # 8 brake band (width, thickness incl. lining, wrap deg), lever pivot (y, z), lever length
    "band": (40.0, 8.0, 270.0), "lever_pivot": (200.0, 330.0), "lever_len": 450.0,
    # 10 gear guard: radius around the gear, radius around the pinion, sheet thickness, x from, x to
    "guard": (200.0, 50.0, 2.0, 250.0, 300.0),
    # 11 anchors: anchor eye (y behind the drum axis, x), rod (dia, length, angle below horizontal),
    #   helix (dia, thickness); chain dia (drawn as a bar), turnbuckle body length
    "anchor_eye": (1700.0, 203.0), "anchor_rod": (20.0, 1000.0, 45.0), "helix": (150.0, 8.0),
    "chain_d": 10.0, "turnbuckle": 220.0,
    # ---------------------------------------------------------------- rake (BOM 13 to 17)
    # 13 beam: FRP square tube size, wall, length; z of its underside; y of its front face
    "beam": (100.0, 6.0, 3000.0), "beam_z0": 60.0,
    # 14 blade: UHMW-PE thickness, height, ground gap (set by the skids), length
    "blade": (15.0, 300.0, 10.0, 3000.0),
    # 15 skids: UHMW-PE (width, thickness, length, y start behind the blade); x positions;
    #   hanger plate (thickness, width, horizontal leg length)
    "skid": (60.0, 20.0, 450.0, 20.0), "skid_x": (-1200.0, 0.0, 1200.0), "hanger": (6.0, 60.0, 120.0),
    # 16 end caps: plate thickness, length along the beam; eye plate (thickness, reach, front eye y, rear eye y, hole)
    "cap": (6.0, 126.0), "eye": (12.0, 50.0, -25.0, 150.0, 18.0),
    # 19 blade bolts: diameter, x pitch, height
    "blade_bolts": (10.0, 300.0, 110.0),
    # 17 bridle: apex distance in front of the blade and behind the beam; apex height
    "bridle": (2000.0, 2175.0, 130.0),
    # 22 ballast bags of salt on the beam (length along X, depth behind the blade, height); x of each centre
    "ballast": (550.0, 300.0, 120.0), "ballast_x": 800.0,
    # ---------------------------------------------------------------- roller saddle (BOM 12)
    # side plate (thickness, length along Y, height); x of plate centre; axle height, axle dia;
    # roller (OD, length), flanges (OD, thickness); foot plate (width, thickness); tie bar dia, y
    "saddle": (6.0, 300.0, 140.0), "saddle_x": 118.0, "axle": (100.0, 25.0, 260.0),
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
            for dy in (-25.0, 25.0):
                cheek = cheek - xcyl(x0 - 1, x1 + 1, ty + dy, tz, 5.5)
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
            pl = bx(x0, x1, ty - ps / 2, ty + ps / 2, tz - ps / 2, tz + ps / 2)
            for dy in (-25.0, 25.0):
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
        flange_bearing(xo, 1, 0, pz, brg_p, p["pshaft"][0]), flange_bearing(-xo, -1, 0, pz, brg_p, p["pshaft"][0])]), 6, "brg")
    # 4 gear (webbed), 5 crank shaft with pinion
    m = p["module"]
    C["gear"] = Comp("Spur gear, 84 teeth", gear_profile(p["z_gear"], m, sd / 2, p["gear_face"], p["gear_x0"], 0, dz,
                                                         web=(12.0, 22.0, 80.0, 6, 60.0),
                                                         phase=math.pi / 2 - 0.875 * 2 * math.pi / p["z_gear"]), 4)
    pd_, ph = p["pshaft"]
    pin = gear_profile(p["z_pinion"], m, pd_ / 2, p["pinion_face"], p["pinion_x0"], 0, pz,
                       phase=1.5 * math.pi - 0.375 * 2 * math.pi / p["z_pinion"])
    C["pinion"] = Comp("Crank shaft and pinion", pin + xcyl(-ph, ph, 0, pz, pd_ / 2), 5)
    # 7 ratchet wheel on the left end of the drum shaft, and its pawl
    rod_, rn, rtk, rx0 = p["ratchet"]
    C["ratchet"] = Comp("Ratchet wheel", ratchet_profile(rod_, rn, rtk, rx0 - rtk, 0, dz, sd), 7)
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
    for (sy, sz) in ((gr - 10, dz), (-(gr - 10), dz), (0.0, dz - (gr - 10))):
        spacers.append(xcyl(xo, gx0, sy, sz, 7.0))
        guard = guard + xcyl(gx0, gx1 - gt, sy, sz, 7.0)
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
        eyep = bx(xp0, xp1, ey_f - 25, ey_r + 25, zc - et / 2, zc + et / 2)
        for yy in (ey_f, ey_r):
            eyep = eyep - zcyl((xp0 + xp1) / 2, yy, zc - et, zc + et, eh / 2)
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
        legs.append(rod((sg * xe, ey_f, zc), (0, -af, az), 6.0))
        legs.append(rod((sg * xe, ey_r, zc), (0, yr + ar - yc + yc, az), 6.0))
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
        export_stl(cpd, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
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
