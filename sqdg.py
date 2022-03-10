import cadquery as cq
import math

rot_axis_z = ((0, 0, 0), (0, 0, 1))

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

def add_stem(obj, off, thumb=False):
    stem_dist = 5.7
    stem_h = 3.5
    stem = (
        cq.Workplane().box(1.2, 3, stem_h, (True, True, False)).faces("<X or |Z").shell(-0.8)
        .translate((stem_dist / 2, 0, -stem_h))
    )
    stems = stem.union(stem.rotate(*rot_axis_z, 180))
    if thumb:
        stems = stems.rotate(*rot_axis_z, 90)
    return (
        # obj.faces("<Z").workplane().sketch().face(obj.wires("<Z").val()).wires().offset(-1, mode="s").finalize().extrude(1)
        obj.union(obj.wires("<Z").toPending().extrude(-1, combine=False).faces("|Z").shell(-1))
        .union(stems.translate((off, 0, 0)))
    )

def base(x, y, r, h, gap, pos, ang, off):
    base = cq.Workplane().box(x - gap, y - gap, 10, (True, True, False)).edges("|Z").chamfer(1)
    if pos == "mid":
        return add_stem(
            base
            .intersect(cq.Workplane().transformed(offset=(off, 0, h - r)).sphere(r)),
            off
        )
    sh = 2
    y_mul = -1 if pos == "top" else 1
    return add_stem(
        base
        .intersect(cq.Workplane().transformed(offset=(off,
                                                      y_mul * (r * math.sin(math.radians(ang)) - y / 2),
                                                      sh - r * math.cos(math.radians(ang)))).sphere(r)),
        off
    )

def col(x, y, r=60, h=3, gap=1, cr=90, ch=1.5, sh=None, ang=30, off=0):
    b = lambda p: base(x, y, r, h, gap, p, ang, off)
    col = (
        b("mid").union(b("top").translate((0, y))).union(b("bot").translate((0, -y)))
        .cut(cq.Workplane().transformed(offset=(off, 0, cr + ch)).sphere(cr))
    )
    if sh != None:
        col = col.workplane(sh).split(keepBottom=True)
    return Boxed(col, x, y * 3)

def thumb(x, y, r=60, h=2, gap=1, ang=10):
    return add_stem(
        cq.Workplane().box(x - gap, y - gap, 10, (True, True, False))
        .edges("|Z").chamfer(1)
        .intersect(cq.Workplane().transformed(offset=(0,
                                                      r * math.sin(math.radians(ang)) - y / 2,
                                                      h - r * math.cos(math.radians(ang)))).sphere(r)),
         0, thumb=True
    )

def thumb_col(x, y, h=2, r=60, gap=1, ang=10):
    T = thumb(y, x, h=h, r=r, ang=ang, gap=gap)
    return Boxed(T.union(T.translate((-y, 0, 0))).union(T.translate((y, 0, 0))).rotate(*rot_axis_z, -90),
                 x, y * 3)

def export_color(obj, name):
    cq.Assembly(obj, color=cq.Color("gray")).save(name + ".step")
