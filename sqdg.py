import cadquery as cq, math
from typing import Optional
from dataclasses import dataclass

rot_axis_z = ((0, 0, 0), (0, 0, 1))

@dataclass
class Config:
    x: float = 18               # Width of key (not keycap) outline; length for thumbs
    y: float = 17               # Length of key (not keycap) outline; width for thumbs
    r: float = 60               # Convex surface radius
    eh: float = 2               # Top/Bottom edge max height
    gap: float = 1              # Gap between cap outlines
    cr: float = 60              # Radius of concave/cut shape; only for alphas
    crh: Optional[float] = None # Horizontal radius of cut shape
    ch: float = 1.5             # Minimum height in the center; only for alphas
    sh: Optional[float] = None  # Height at which to be sliced, measured from top of stem; only for alphas
    ang: float = 30             # Angle of tangent of convex surface hits the top/bottom edge
    off: float = 0              # X-offset of cut sphere from the center of cap
    soff: Optional[float] = None# X-offset of center of stem from the center of cap
    sl: float = 3.5             # Stem length

    def __add__(self, c: 'Config'):
        default = vars(Config())
        ret = Config()
        for k, v in default.items():
            if getattr(self, k) != default[k]:
                setattr(ret, k, getattr(self, k))
            if getattr(c, k) != default[k]:
                setattr(ret, k, getattr(c, k))
        return ret

class Boxed:
    def __init__(self, thing, x, y):
        self.thing = thing
        self.x = x
        self.y = y

    def hcat(self, other):
        total_x, total_y = self.x + other.x, max(self.y, other.y)
        return Boxed(self.thing.translate(((self.x - total_x) / 2, 0, 0))
                     .union(other.thing.translate(((total_x - other.x) / 2, 0, 0))), total_x, total_y)

    def vcat(self, other):
        total_x, total_y = max(self.x, other.x), self.y + other.y
        return Boxed(self.thing.translate((0, -self.y / 2, 0))
                     .union(other.thing.translate((0, other.y / 2, 0))), total_x, total_y)

    def unwrap(self):
        return self.thing

    def __or__(self, other): return self.hcat(other)
    def __add__(self, other): return self.vcat(other)

def add_stem(obj, c: Config, thumb=False):
    stem_dist = 5.7
    stem = (
        cq.Workplane().box(1.2, 3, c.sl, (True, True, False)).faces("<X or |Z").shell(-0.8)
        .translate((stem_dist / 2, 0, -c.sl))
    )
    stems = stem.union(stem.rotate(*rot_axis_z, 180))
    if thumb:
        stems = stems.rotate(*rot_axis_z, 90)
    return (
        obj.union(obj.wires("<Z").toPending().extrude(-1, combine=False).faces("|Z").shell(-1))
        .union(stems.translate((c.soff if c.soff != None else c.off, 0, 0)))
    )

def base(c: Config, pos: str):
    base = cq.Workplane().box(c.x - c.gap, c.y - c.gap, 10, (True, True, False)).edges("|Z").chamfer(1)
    if pos == "mid":
        return add_stem(
            base
            .intersect(cq.Workplane().transformed(offset=(c.off, 0, 10 - c.r)).sphere(c.r)),
            c,
        )
    y_mul = -1 if pos == "top" else 1
    return add_stem(
        base
        .intersect(cq.Workplane().transformed(offset=(c.off,
                                                      y_mul * (c.r * math.sin(math.radians(c.ang)) - c.y / 2),
                                                      c.eh - c.r * math.cos(math.radians(c.ang)))).sphere(c.r)),
        c,
    )

def ellipsoid(x, y):
    return (cq.Workplane().sketch().ellipse(x, y).push([(0, y)]).rect(2 * x, 2 * y, mode="s").finalize()
            .revolve(360, axisEnd=(1, 0)))

def col(c: Config):
    b = lambda p: base(c, p)
    cut_shape = cq.Workplane().transformed(offset=(c.off, 0, c.cr + c.ch))
    if c.crh != None:
        cut_shape = cut_shape.sketch().ellipse(c.crh, c.cr).push([(0, c.cr)]).rect(2 * c.crh, 2 * c.cr, mode="s").finalize().revolve(360, axisEnd=(1, 0))
    else:
        cut_shape = cut_shape.sphere(c.cr)
    col = (
        b("mid").union(b("top").translate((0, c.y))).union(b("bot").translate((0, -c.y)))
        .cut(cut_shape)
    )
    if c.sh != None:
        col = col.transformed(offset=(0, 0, c.sh)).split(keepBottom=True)
    return Boxed(col, c.x, c.y * 3)

def thumb(c: Config):
    return add_stem(
        cq.Workplane().box(c.y - c.gap, c.x - c.gap, 10, (True, True, False))
        .edges("|Z").chamfer(1)
        .intersect(cq.Workplane().transformed(offset=(0,
                                                      c.r * math.sin(math.radians(c.ang)) - c.x / 2,
                                                      c.eh - c.r * math.cos(math.radians(c.ang)))).sphere(c.r)),
         c, thumb=True
    )

def thumb_col(c: Config):
    T = thumb(c)
    return Boxed(T.union(T.translate((-c.y, 0, 0))).union(T.translate((c.y, 0, 0))).rotate(*rot_axis_z, -90),
                 c.x, c.y * 3)

def export_color(obj, name):
    cq.Assembly(obj, color=cq.Color("gray")).save(name + ".step")
