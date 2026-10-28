"""SaltDrag repo-specific CAD helpers beside .kit/cad_parts.py (kit 1.9, STANDARDS section 24).

    frame(origin, n)        a Location whose +Z is the unit vector n, at origin
    bolt_set(d, grip, ...)  cad_parts.hex_bolt_set placed on any axis: the joint face the head bears on is at
                            origin, the head side is +n, the joint runs grip mm along -n
    csk_bolt(d, length)     countersunk bolt (ISO 10642 envelope), head flush in a 90 degree countersink
    weld_on(...)            cad_parts.weld_fillet bead along any axis with its legs on two faces
    ring_weld(r, leg, ...)  round fillet bead where a tube or shaft meets a plate
    chain(a, c, wire)       a run of round steel links from point a to point c
    shackle(...)            bow shackle: bow and pin, on any axis
    sleeve(od, id, length)  crush sleeve or spacer tube along +Z
    rope_run(points, d)     cad_parts.rope as one solid run
All sizes in millimetres; every function returns build123d solids.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Axis, Box, Compound, Cylinder, Location, Plane, Polygon, Pos, Rot, Sketch, Circle, Torus,  # noqa: E402
                       extrude, revolve, Cone, Solid, Vector)
import cad_parts as cp  # noqa: E402


def _unit(v):
    L = math.sqrt(sum(c * c for c in v))
    return tuple(c / L for c in v)


def _perp(n):
    n = _unit(n)
    a = (1.0, 0.0, 0.0) if abs(n[0]) < 0.9 else (0.0, 1.0, 0.0)
    u = (a[1] * n[2] - a[2] * n[1], a[2] * n[0] - a[0] * n[2], a[0] * n[1] - a[1] * n[0])
    return _unit(u)


def frame(origin, n, u=None):
    """Location at origin whose local +Z points along n (and local +X along u, if given)."""
    n = _unit(n)
    return Location(Plane(origin=tuple(origin), x_dir=u or _perp(n), z_dir=n))


def bolt_set(d, grip, origin, n, extra=None, label=""):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut through a joint grip mm thick. origin: the joint
    face under the head; n: unit vector from the joint toward the head. Returns [(name, shape), ...]."""
    L = frame(origin, n)
    return [(nm + label, L * s) for nm, s in cp.hex_bolt_set(d, grip, extra)]


def csk_bolt(d, length):
    """Countersunk head bolt along -Z: the head's top face at z = 0, 90 degree head of diameter 2d, shank down."""
    head = Pos(0, 0, -d / 2) * Cone(d / 2, d, d)          # bottom radius d/2 at z = -d, top radius d at z = 0
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        hex_key = Pos(0, 0, -d * 0.3) * Cylinder(d * 0.3, d * 0.6)   # socket drawn as a round recess
        return head + shank - hex_key
    except Exception:
        return head + shank


def csk_hole(d, depth, origin, n):
    """Cutting tool for a countersunk clearance hole: 90 degree countersink at origin, hole d + 1 along -n."""
    tool = Pos(0, 0, -d / 2) * Cone(d / 2 + 0.5, d + 0.2, d) + Pos(0, 0, -depth / 2) * Cylinder(d / 2 + 0.5, depth + 2)
    return frame(origin, n) * tool


def nut_washer(d, origin, n):
    """Washer and nut on a face at origin, nut side along +n."""
    s, k, m, d2, h, p = cp.ISO[d]
    L = frame(origin, n)
    return [(f"M{d} washer (ISO 7089)", L * cp.washer(d)), (f"M{d} hex nut (ISO 4032)", L * Pos(0, 0, h) * cp.hex_nut(d))]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def weld_on(start, axis, length, leg, d1, d2):
    """Fillet bead from start along unit vector axis for length; its two legs lie along unit vectors d1 and d2."""
    bead = cp.weld_fillet(length, leg)       # along +X, legs along local +Y and +Z
    for a, b in ((d1, d2), (d2, d1)):
        z = b
        y = _cross(z, axis)
        if all(abs(p - q) < 1e-6 for p, q in zip(y, a)):
            return Location(Plane(origin=tuple(start), x_dir=tuple(axis), z_dir=tuple(z))) * bead
    raise ValueError("weld_on: axis, d1 and d2 must be mutually perpendicular unit vectors")


def ring_weld(r, leg, origin, n):
    """Round fillet weld where a tube or shaft of outside radius r stands on a plate: legs along the plate face
    (outward from r) and along n (up the tube). origin is on the plate face, on the tube axis."""
    ring = revolve(Plane.XZ * Polygon((r, 0), (r + leg, 0), (r, leg), align=None), Axis.Z, 360)
    return frame(origin, n) * ring


def sleeve(od, id_, length):
    """Crush sleeve or spacer tube along +Z from z = 0, edges lightly broken."""
    return cp.bush(od, id_, length)


def _half_torus(rm, r, keep):
    """Half of a torus lying in the local XZ plane (axis along Y), the half with z > 0 (keep = 1) or z < 0."""
    t = Rot(90, 0, 0) * Torus(rm, r)
    big = 2 * (rm + r) + 2
    return t - Pos(0, 0, -keep * big / 2) * Box(big, big, big)


def chain(a, c, wire=8.0, pitch=None):
    """Round-steel chain links from point a to point c: alternate links turned 90 degrees, inside length 3 wire
    diameters, inside width 1.4 wire diameters (proof-coil proportions). Returns one Compound."""
    pitch = pitch or 3.0 * wire
    v = tuple(q - p for p, q in zip(a, c))
    L = math.sqrt(sum(t * t for t in v))
    u = _unit(v)
    n = max(2, int(L // pitch))
    rm = 0.7 * wire + wire / 2               # centre-line radius of the link ends
    half = pitch / 2 + wire / 2 - rm          # straight half-length so links reach one pitch apart and interlock
    link = (Pos(0, 0, half) * _half_torus(rm, wire / 2, 1) + Pos(0, 0, -half) * _half_torus(rm, wire / 2, -1)
            + Pos(rm, 0, 0) * Cylinder(wire / 2, 2 * half) + Pos(-rm, 0, 0) * Cylinder(wire / 2, 2 * half))
    links = []
    for i in range(n):
        ctr = tuple(a[k] + u[k] * (pitch / 2 + i * pitch) for k in range(3))
        links.append(Location(Plane(origin=ctr, x_dir=_perp(u), z_dir=u)) * Rot(0, 0, 90.0 * (i % 2)) * link)
    return Compound(links)


def shackle(pin_d, gap, reach, origin, axis_pin, axis_bow):
    """Bow shackle: pin of diameter pin_d along unit vector axis_pin through origin, jaw gap 'gap', bow reaching
    'reach' from the pin axis along axis_bow. Returns (bow, pin) solids."""
    w = pin_d
    rb = gap / 2 + w / 2
    straight = max(1.0, reach - rb)
    legs = [Pos(sx * rb, straight / 2, 0) * Rot(90, 0, 0) * Cylinder(w / 2, straight) for sx in (-1, 1)]
    crown = Pos(0, straight, 0) * Rot(-90, 0, 0) * _half_torus(rb, w / 2, 1)
    eyes = [Pos(sx * rb, 0, 0) * Rot(0, 90, 0) * Cylinder(w * 0.95, w) for sx in (-1, 1)]
    bow = legs[0] + legs[1] + crown
    for e in eyes:
        bow = bow + e
    bow = bow - Rot(0, 90, 0) * Cylinder(pin_d / 2 + 0.3, 2 * rb + 2 * w)
    pin_len = 2 * rb + w + 6
    pin = Rot(0, 90, 0) * Cylinder(pin_d / 2, pin_len) + Pos(-(pin_len / 2 + w * 0.3), 0, 0) * Rot(0, 90, 0) * Cylinder(pin_d * 0.9, w * 0.6)
    z = _cross(_unit(axis_pin), _unit(axis_bow))
    loc = Location(Plane(origin=tuple(origin), x_dir=tuple(_unit(axis_pin)), z_dir=z))
    return loc * bow, loc * pin


def rope_run(points, d):
    """A rope through points as one fused solid (cad_parts.rope segments and joints)."""
    c = cp.rope(points, d)
    s = None
    for k in c.solids():
        s = k if s is None else s + k
    return s


def rod(a, c, r):
    """Round bar from point a to point c."""
    av, cv = Vector(*a), Vector(*c)
    v = cv - av
    return Solid.make_cylinder(r, v.length, Plane(origin=av, z_dir=v))
