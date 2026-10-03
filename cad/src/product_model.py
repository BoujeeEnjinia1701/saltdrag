"""SaltDrag product appearance model (build123d), TRL 3, constructable design (SDG-DDR-002).

Finished-product look for photoreal renders: one hand capstan (galvanised side frames and drum,
dark steel gear and ratchet, yellow gear guard, thermoplastic bearing housings, galvanised crank
handles) standing on the dry ground behind the bund with its chains to the ground anchors; the
bund roller saddle astride the crest; the navy polyester pull rope over the roller to the bridle
swivel; the rake (green FRP beam, white UHMW-PE blade and skids, stainless end caps, two woven
ballast bags) on the white salt bed, pushing a heap of salt toward the bund. Context: the earth
bund, a patch of salt pan and dry ground, a person cranking and a second person standing back on
the dry ground (mannequin() from .kit/context_parts.py). The far-side capstan is not shown.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every part is a model.py solid in model.py's layout (layout(), PARAMS, derived()); nothing is
re-dimensioned here. Departures from model.py, recorded in docs/REVIEW.md: the ground anchors are
cut off at ground level (they are buried), the salt heap and the pan surface are context shapes,
and the crank is drawn at 100 deg so the cranking person's hands meet the upper handle.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import copy
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
from model import PARAMS, derived, layout, capstan_components, bund, bx, yz_plate, rope_points  # noqa: E402

TITLE = "SaltDrag: hand capstan and rake that gather salt from the bund"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["capstan", "roller", "rope", "rake", "context"], "explode": False, "el": 24, "az": -40,
     "note": "Product render from behind the capstan, front right and above (about 24 deg elevation): a person "
             "winds the hand capstan on dry ground behind the bund; the rope runs over the bund roller to the rake, "
             "which pushes a heap of salt across the pan toward the bund. Far-side capstan not shown"},
    {"name": "exploded", "groups": ["exploded"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view of one hand capstan from the front right and above (about 26 deg elevation): side frames "
             "and cross tubes, drum, bearings, ratchet and pawl (left), gear, pinion and guard (right), brake band, "
             "crank handles above"},
    {"name": "detail", "groups": ["capstan"], "explode": False, "el": 14, "az": -40,
     "note": "Detail from behind the capstan, front right and slightly above (about 14 deg elevation): ratchet "
             "wheel and pawl, brake band and lever on the left side frame, anchor chains to the ground anchors"},
]

C_GALV = "#A9AFB5"
C_GALV2 = "#9AA1A8"
C_STEEL = "#4A4F55"
C_YELLOW = "#E3B505"
C_BRG = "#2C3138"
C_ROPE = "#2B4C7E"
C_FRP = "#2F6F5E"
C_UHMW = "#EEEDE8"
C_SS = "#C3C7CC"
C_BAG = "#E6DFCB"
C_BUND = "#B8A586"
C_SALT = "#F1EFE9"
C_GROUND = "#C9B99A"
C_CLAY = "#B9B4AE"

LOOK = {  # model key -> (display name, colour, material)
    "frame_r": ("Side frame, galvanised steel", C_GALV, "metal"),
    "frame_l": ("Side frame with pawl boss, galvanised steel", C_GALV, "metal"),
    "xtube_front": ("Cross tube, galvanised", C_GALV2, "metal"),
    "xtube_rear": ("Cross tube, galvanised", C_GALV2, "metal"),
    "xtube_top": ("Cross tube, galvanised", C_GALV2, "metal"),
    "drum": ("Drum, galvanised steel", C_GALV, "metal"),
    "bearings": ("Flange bearings, thermoplastic housings", C_BRG, "plastic"),
    "gear": ("Spur gear, 84 teeth, oiled steel", C_STEEL, "metal"),
    "pinion": ("Crank shaft and pinion, steel", C_STEEL, "metal"),
    "ratchet": ("Ratchet wheel, steel", C_STEEL, "metal"),
    "pawl": ("Pawl and pivot bolt, steel", "#3B4046", "metal"),
    "brake": ("Brake band and lever, steel", "#5B6168", "metal"),
    "cranks": ("Crank handles, galvanised", C_GALV2, "metal"),
    "guard": ("Gear guard, painted yellow steel", C_YELLOW, "painted"),
    "anchors": ("Anchor chains, turnbuckles and anchor eyes, galvanised", "#8E959C", "metal"),
    "saddle": ("Bund roller saddle, galvanised", C_GALV, "metal"),
    "roller": ("Bund roller, UHMW-PE", C_UHMW, "plastic"),
    "axle": ("Roller axle, stainless", C_SS, "metal"),
    "beam": ("Rake beam, green FRP", C_FRP, "plastic"),
    "blade": ("Rake blade, UHMW-PE", C_UHMW, "plastic"),
    "skids": ("Skids, UHMW-PE", C_UHMW, "plastic"),
    "hangers": ("Skid hangers, stainless", C_SS, "metal"),
    "caps": ("End caps with eye plates, stainless", C_SS, "metal"),
    "rake_bolts": ("Rake bolts, stainless", C_SS, "metal"),
    "bridles": ("Bridles and swivels, polyester rope", C_ROPE, "fabric"),
    "ballast": ("Ballast bags, woven sack", C_BAG, "fabric"),
}
BOMS = {k: v for k, v in [("frame_r", 1), ("frame_l", 1), ("xtube_front", 2), ("xtube_rear", 2), ("xtube_top", 2),
                          ("drum", 3), ("bearings", 6), ("gear", 4), ("pinion", 5), ("ratchet", 7), ("pawl", 7),
                          ("brake", 8), ("cranks", 9), ("guard", 10), ("anchors", 11), ("saddle", 12), ("roller", 12),
                          ("axle", 12), ("beam", 13), ("blade", 14), ("skids", 15), ("hangers", 15), ("caps", 16),
                          ("rake_bolts", 19), ("bridles", 17), ("ballast", 22)]}
EXPLODE = {"frame_r": (300, 0, 0), "frame_l": (-300, 0, 0), "xtube_front": (0, -380, -150), "xtube_rear": (0, 380, -150),
           "xtube_top": (0, 0, 420), "drum": (0, -560, 0), "bearings": (0, 0, 0), "gear": (620, -260, 0),
           "pinion": (0, -260, 560), "ratchet": (-600, -260, 0), "pawl": (-720, 0, 280), "brake": (-460, 320, -280),
           "cranks": (0, 0, 820), "guard": (850, 0, 0)}

RAKE_Y = 2500.0          # blade front face in the hero layout (about 2.5 m from the bund toe)


def _p():
    p = copy.deepcopy(PARAMS)
    p["crank_angle"] = 100.0
    p["rake_y"] = RAKE_Y
    return p


def product_parts(P=None):
    P = P or _p()
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode=(0, 0, 0)):
        out.append({"name": name, "shape": shape, "color": color, "material": material, "bom": bom,
                    "group": group, "explode": tuple(float(v) for v in explode)})

    L = layout(P, rake_y=RAKE_Y)
    for key, (comp, shape) in L.items():
        if key.startswith("far_"):
            continue
        k = key[5:] if key.startswith("near_") else key
        if key == "ropes":
            near, _ = rope_points(P, RAKE_Y)
            from model import rod
            r = rod(near[0], near[1], P["rope_d"] / 2) + rod(near[1], near[2], P["rope_d"] / 2)
            add("Pull rope, 12 mm polyester", r, C_ROPE, "fabric", 18, "rope")
            continue
        if k == "anchors":
            shape = shape & bx(-3000, 3000, -9000, 9000, 0.0, 3000)      # buried part not drawn
        name, color, mat = LOOK[k]
        grp = "capstan" if comp.bom <= 11 else ("roller" if comp.bom == 12 else "rake")
        add(name, shape, color, mat, BOMS[k], grp)
    # exploded capstan, standalone at the origin
    for k, c in capstan_components(P).items():
        if k == "anchors":
            continue
        name, color, mat = LOOK[k]
        add(name, c.shape, color, mat, BOMS[k], "exploded", EXPLODE[k])
    # context: bund, pan floor of salt, dry ground behind, a heap of salt in front of the blade, people
    h, crest, base = P["bund"]
    add("Earth bund", bund(P, 7000.0, 0.0, 1), C_BUND, "clay", None, "context")
    add("Salt pan floor, crystal crust", bx(-3500, 3500, 0, 6500, -30, 0), C_SALT, "clay", None, "context")
    add("Dry ground behind the bund", bx(-3500, 3500, D["drum_y"] - 2400, -base, -30, 0), C_GROUND, "clay", None, "context")
    hb = P["blade"][1] * 0.95
    run = hb / math.tan(math.radians(35.0))
    heap = yz_plate([(RAKE_Y, 0.0), (RAKE_Y, hb), (RAKE_Y - run, 0.0)], -1450.0, 1450.0)
    add("Heap of gathered salt", heap, "#F7F6F2", "clay", None, "context")
    try:
        from context_parts import mannequin, mannequin_landmarks
        lm = mannequin_landmarks(1750, "push")
        hx = (lm["hands"][0][0] + lm["hands"][1][0]) / 2
        hy = (lm["hands"][0][1] + lm["hands"][1][1]) / 2
        hz = (lm["hands"][0][2] + lm["hands"][1][2]) / 2
        a = math.radians(P["crank_angle"])
        gx = -(P["crank_x0"] + P["crank_hub"][1] + P["grip"][1] / 2)     # right grip, layout x (capstan turned)
        gy = D["drum_y"] - P["crank_r"] * math.cos(a)
        gz = D["pin_z"] + P["crank_r"] * math.sin(a)
        man = Rot(0, 0, 90) * mannequin(1750, "push")
        # after the turn, local (x, y) -> (-y, x): the hands sit at (-hy, hx)
        add("Person cranking (scale)", Pos(gx + hy - 60, gy - hx, gz - hz) * man, C_CLAY, "clay", None, "context")
        st = Rot(0, 0, 200) * mannequin(1700, "stand")
        add("Person standing on the dry ground (scale)", Pos(1500, D["drum_y"] + 400, 0) * st, C_CLAY, "clay", None, "context")
    except Exception as e:   # the render still works without the people
        print("mannequin skipped:", e)
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:58s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.1f} cm3")
