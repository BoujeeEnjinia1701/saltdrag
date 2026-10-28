"""SaltDrag product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is (option A, geared drum capstans): one hand
capstan with its side frames, cross tubes, drum, bearings, gear, pinion, ratchet and pawl, band brake, cranks,
gear guard, every bolt and weld bead, and its chains, turnbuckles and helical anchors; the bund roller saddle on
the crest; the pull rope wound on the drum and run over the roller, with its damper bag; and the rake with its
blade, skids, hangers, end caps, bridles, swivels, shackles and ballast bags, 3 m into the pan. The far-side
capstan is not shown. Only the site is added, as context parts: the earth bund and the salt crust of the pan
(model.site_context(), both reaching below ground), a heap of gathered salt in front of the blade, and two
1.75 to 1.8 m mannequins standing on the dry ground, one at the right-hand crank.
The hero is rendered by .kit/photoreal.py as an outdoor scene, ground level at model z = 0, sandy saline ground
(RENDER_VIEWS "args"). APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Departures from model.py, recorded in docs/REVIEW.md: none in the product; the salt heap is a context shape, and
the cranking mannequin is 1.80 m tall so its hand meets the crank grip at the model's 60 degree crank angle.

Groups: "capstan", "roller", "rope", "rake" and "context".

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "SaltDrag: hand capstan and rake that gather salt from the bund"

_SITE = ["--scene=outdoor", "--ground=sand", "--ground-z=0", "--sun=38,-70", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["capstan", "roller", "rope", "rake", "context"], "explode": False, "el": 20, "az": -40,
     "args": _SITE,
     "note": "Site render from behind the capstan, front right and above (about 20 deg elevation): a person winds "
             "the hand capstan on the dry ground behind the bund; the rope runs over the bund roller to the rake, "
             "which pushes a heap of salt across the pan toward the bund; far-side capstan not shown; 1.75 m person "
             "standing back for scale"},
    {"name": "studio", "groups": ["capstan"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render of one hand capstan from behind, front right and above (about 24 deg elevation): side "
             "frames on their runners, cross tubes, drum with rope, gear guard, cranks, chains to the helical anchors"},
    {"name": "detail", "groups": ["capstan"], "explode": False, "el": 14, "az": -40,
     "note": "Detail of the ratchet side, slightly above (about 14 deg elevation): ratchet wheel and pawl on its "
             "welded boss, band brake and lever, bolted cross tubes and bearing housings"},
    {"name": "exploded", "groups": ["capstan"], "explode": True, "el": 26, "az": -55,
     "note": "Exploded view of one hand capstan from the front right and above (about 26 deg elevation): side "
             "frames and cross tubes with their bolts, drum, bearings, ratchet and pawl, gear, pinion and guard, "
             "brake, cranks"},
]


def site_extras():
    """Salt heap in front of the blade and two mannequins on the dry ground (context)."""
    P = M.PARAMS
    D = M.derived(P)
    out = []
    hb = P["blade"][1] * 0.95
    run = hb / math.tan(math.radians(35.0))
    ry = P["rake_y"]
    heap = M.yz_plate([(ry, -50.0), (ry, hb), (ry - run, 0.0), (ry - run - 60, -50.0)], -1450.0, 1450.0)
    out.append(part("Heap of gathered salt (site)", heap, "insulated_white", kind="context", group="context"))
    try:
        from context_parts import mannequin
        h = 1800.0
        a = math.radians(P["crank_angle"])
        gx = -(P["crank_x0"] + P["crank_hub"][1] + P["grip"][1] / 2)       # right grip, site x (capstan turned)
        gy = D["drum_y"] - P["crank_r"] * math.cos(a)
        k = h / 1750.0
        hx, hy = -520.0 * k, 171.0 * k                                      # push-pose hand, local (y, x)
        man = Pos(gx + hx, gy - hy, 0.0) * Rot(0, 0, 90) * mannequin(h, "push")
        out.append(part("Person cranking, 1.80 m (scale)", man, "skin", kind="context", group="context"))
        st = Pos(1700.0, D["drum_y"] + 300.0, 0.0) * Rot(0, 0, 200) * mannequin(1750.0, "stand")
        out.append(part("Person standing on the dry ground, 1.75 m (scale)", st, "skin", kind="context", group="context"))
    except Exception as e:     # the people are for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        q = dict(p)
        if q["group"] == "capstan":
            ex, ey, ez = q.get("explode", (0, 0, 0))
            q["explode"] = (-ex, -ey, ez)          # the capstan is turned 180 degrees on the site
        out.append(q)
    return out + site_extras()


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))
