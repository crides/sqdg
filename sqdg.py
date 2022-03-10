import cadquery as cq
import math

rot_axis_z = ((0, 0, 0), (0, 0, 1))

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
    col = b("mid").union(b("top").translate((0, y))).union(b("bot").translate((0, -y)))
    col = col.cut(cq.Workplane().transformed(offset=(off, 0, cr + ch)).sphere(cr))
    if sh != None:
        col = col.workplane(sh).split(keepBottom=True)
    return col

def thumb(x, y, r=60, h=2, gap=1, ang=10):
    return add_stem(
        cq.Workplane().box(x - gap, y - gap, 10, (True, True, False))
        .edges("|Z").chamfer(1)
        .intersect(cq.Workplane().transformed(offset=(0,
                                                      r * math.sin(math.radians(ang)) - y / 2,
                                                      h - r * math.cos(math.radians(ang)))).sphere(r)),
         0, thumb=True
    )

def thumb_col(x, y, h=2, gap=1, ang=10):
    T = thumb(y, x, h=h, ang=ang, gap=gap)
    return T.union(T.translate((-y, 0, 0))).union(T.translate((y, 0, 0))).rotate(*rot_axis_z, -90)

def export_color(obj, name):
    cq.Assembly(obj, color=cq.Color("gray")).save(name + ".step")

chocmin_x, chocmin_y, chocmin_nnx = 18, 13.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
params = {"gap": 0.75, "cr": 75, "sh": 2.5, "ang": 35}

F = col(chocmin_x, chocmin_y, **params)
R = col(chocmin_nx, chocmin_y, off=-chocmin_off, **params)
L = col(chocmin_nx, chocmin_y, off=chocmin_off, **params)
N = col(chocmin_nnx, chocmin_y, **params)
T = thumb_col(chocmin_x, chocmin_y, h=1.5, ang=15, gap=0.75)

right = L.translate((-chocmin_nx * 3 / 2 - chocmin_x / 2, 0, 0)) \
    + R.translate((-chocmin_nx / 2 - chocmin_x / 2, 0, 0)) \
    + F \
    + L.translate((chocmin_nx / 2 + chocmin_x / 2, 0, 0)) \
    + N.translate((chocmin_nx + chocmin_nnx / 2 + chocmin_x / 2, 0, 0)) \
    + T.translate((-chocmin_nx * 2 - chocmin_x, 0, 0))

left = L.translate((-chocmin_nx * 3 / 2 - chocmin_x / 2, 0, 0)) \
    + R.translate((-chocmin_nx / 2 - chocmin_x / 2, 0, 0)) \
    + F \
    + R.translate((chocmin_nx / 2 + chocmin_x / 2, 0, 0)) \
    + N.translate((chocmin_nx + chocmin_nnx / 2 + chocmin_x / 2, 0, 0)) \
    + T.translate((-chocmin_nx * 2 - chocmin_x, 0, 0))

whole = left.translate((0, 3*chocmin_y, 0)) + right
if "show_object" in locals():
    show_object(whole, "whole")

export_color(whole, "whole")
