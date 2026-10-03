"""SaltDrag general arrangement sheet SDG-DWG-001, Rev P2 (TRL 3, constructable design SDG-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/SDG-DWG-001.svg, .pdf and .png from cad/src/model.py with .kit/drawing.py.
The three views show one hand capstan (two are built) without its anchors; the working layout
on a shortened pan is shown as an inset from media/hero.png, and the rake and bund roller
dimensions are in the notes. Dimensions come from PARAMS and derived(), so they follow any
parameter change. The concept blueprint in media/ is SDG-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, capstan_components, derived  # noqa: E402

DATE_P1 = "2026-10-03"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]
    tw, th = dims["top"]
    rw, rh = dims["right"]
    k = sheet.scale
    dl = 11
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    C = capstan_components(P)
    cap = Compound([c.shape for k, c in C.items() if k != "anchors"])
    work = ROOT / "cad" / "drawings" / "_views"
    views = project_views(cap, work)
    bb = cap.bounding_box()
    s = Sheet(project="SaltDrag", title="Hand capstan and rake set: general arrangement", dwg_no="SDG-DWG-001", rev="P2",
              author="Amish Chadha", date=DATE_P1, scale=None, theme="technical",
              material="Galvanised steel capstan; FRP and UHMW-PE rake; per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE_P1, "AC"),
                         ("P2", "SDG-DDR-002: design for construction", DATE_P1, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    # front view (looking along +Y, from the pan side): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k   # noqa: E731
    Z = lambda mz: y + h - (mz - bb.min.Z) * k   # noqa: E731
    L += leader(X(-60), Z(P["drum_z"] - 60), X(bb.min.X) - 16, Z(P["drum_z"] - 160), "DRUM (3)", "end")
    L += leader(X(P["gear_x0"] + 15), Z(P["drum_z"] - 150), X(bb.max.X) + 4, Z(P["drum_z"] - 300), "GEAR UNDER GUARD (4, 10)")
    L += leader(X(-P["cheek_x"]), Z(250), X(bb.min.X) - 16, Z(320), "SIDE FRAME (1)", "end")
    L += leader(X(0), Z(P["xtubes"]["top"][1]), X(bb.min.X) - 16, Z(P["xtubes"]["top"][1] + 120), "CROSS TUBES (2)", "end")
    L += leader(X(-(P["crank_x0"] + 60)), Z(D["pin_z"] - 120), X(bb.min.X) - 16, Z(D["pin_z"] - 40), "CRANKS (9), R330", "end")
    # right view (looking along -X): +Y to the left
    x, y, w, h = c["right"]
    Yr = lambda my: x + w - (my - bb.min.Y) * k   # noqa: E731
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k   # noqa: E731
    L += leader(Yr(P["ear"][0]), Zr(P["ear"][1]), Yr(P["ear"][0]) - 6, Zr(P["ear"][1]) - 22, "ANCHOR EAR, 22 HOLE", "end")
    L += leader(Yr(-150), Zr(P["drum_z"] + D["layers"][2][1]), Yr(bb.min.Y) + 4, Zr(P["drum_z"] + 330), "ROPE LEAVES DRUM TOP TOWARD PAN (-Y)")
    s._layers += L
    s.add_image(str(ROOT / "media" / "hero.png"), 276, 30, 140, 92, label="Working layout",
                sublabel="Seen from the front right and above; pan shortened to 7 m")
    m = P
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Gear pair module 4, 84 and 14 teeth, ratio {D['ratio']:.0f}:1, centres {D['cd']:.0f}",
        f"Drum barrel {m['barrel'][0]} OD x {m['barrel'][2]:.0f}; flanges {m['flange'][0]:.0f}; shaft {m['dshaft'][0]:.0f} C45",
        f"Rope 12 polyester; {D['layers'][3][2]:.0f} m in 4 layers; freeboard {D['freeboard']:.0f}",
        f"Bearings 4-bolt flange, 40 and 25 bore, stainless insert",
        f"Ratchet 200 OD, 20 teeth; pawl on 40 boss; band brake on 330 rim",
        f"Side frames 6 plate on 40 SHS runners {m['runner'][3] - m['runner'][2]:.0f} long, {2 * m['cheek_x']:.0f} apart",
        f"Anchors: 2 chains from ears to helical anchors {m['anchor_eye'][0]:.0f} behind",
        f"Rake: FRP 100 x 100 x 6 beam {m['beam'][2]:,.0f}; UHMW blade {m['blade'][1]:.0f} tall",
        f"Rake: blade edge {m['blade'][2]:.0f} above floor on 3 skids (5 to 25)",
        f"Bridles from end-cap eyes; apex {m['bridle'][0]:,.0f} ahead of blade",
        f"Bund roller 100 x 200 UHMW, top {D['roller_top'] - m['bund'][0]:.0f} above crest",
        f"Capstan drum {m['capstan_back']:,.0f} behind the crest centre",
        f"Drum axis {m['drum_z']:.0f} and crank axis {D['pin_z']:.0f} above the ground",
        "Third-angle; front view from the pan side; (n) = BOM line",
    ], x=276, y=140, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "SDG-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
