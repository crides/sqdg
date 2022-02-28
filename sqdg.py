import cadquery as cq
import math

rot_axis_z = ((0, 0, 0), (0, 0, 1))

def add_stem(obj, off, thumb=False):
    stem_dist = 4.4
    stem_h = 3.5
    stem = (
        cq.Workplane().box(1.2, 3, stem_h, (False, True, False)).faces("<X or |Z").shell(-0.8)
        .translate((stem_dist / 2, 0, -stem_h + 1))
    )
    stems = stem.union(stem.rotate(*rot_axis_z, 180))
    if thumb:
        stems = stems.rotate(*rot_axis_z, 90)
    return (
        obj.edges("<Z").toPending()
        .offset2D(-1, forConstruction=True).toPending().cutBlind(1)
        .union(stems.translate((off, 0, 0)))
    )

def base(x, y, r, h, gap, pos, ang, off):
    if pos == "mid":
        return add_stem(
            cq.Workplane().box(x - gap, y - gap, h, (True, True, False))
            .edges("|Z").chamfer(1)
            .intersect(cq.Workplane().transformed(offset=(off, 0, h - r)).sphere(r)),
            off
        )
    sh = 2
    y_mul = -1 if pos == "top" else 1
    return add_stem(
        cq.Workplane().box(x - gap, y - gap, 10, (True, True, False))
        .edges("|Z").chamfer(1)
        .intersect(cq.Workplane().transformed(offset=(off,
                                                      y_mul * (r * math.sin(math.radians(ang)) - y / 2),
                                                      sh - r * math.cos(math.radians(ang)))).sphere(r)),
        off
    )

def col(x, y, r=60, h=3, gap=1, cr=90, ch=1.5, sh=2.7, ang=30, off=0):
    b = base(x, y, r, h, gap, "mid", ang, off)
    col = b.union(base(x, y, r, h, gap, "top", ang, off).translate((0, y))).union(base(x, y, r, h, gap, "bot", ang, off).translate((0, -y)))
    return (
        col.cut(cq.Workplane().transformed(offset=(off, 0, cr + ch)).sphere(cr))
        .workplane(sh).split(keepBottom=True)
    )

def thumb(x, y, r=60, h=2, gap=1, ang=10):
    return add_stem(
        cq.Workplane().box(x - gap, y - gap, 10, (True, True, False))
        .edges("|Z").chamfer(1)
        .intersect(cq.Workplane().transformed(offset=(0,
                                                      r * math.sin(math.radians(ang)) - y / 2,
                                                      h - r * math.cos(math.radians(ang)))).sphere(r)),
        0, thumb=True
    )

def export_color(obj, name):
    cq.Assembly(obj, color=cq.Color("gray")).save(name + ".step")

chocmin_x, chocmin_y, chocmin_nnx = 18, 13.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
params = {"gap": 0.5, "cr": 50, "sh": 2.5, "ang": 45}

middle = col(chocmin_x, chocmin_y, **params)
index = col(chocmin_nx, chocmin_y, off=-chocmin_off, **params).translate((-chocmin_nx / 2 - chocmin_x / 2, 0, 0))
outex = col(chocmin_nx, chocmin_y, off=chocmin_off, **params).translate((-chocmin_nx * 3 / 2 - chocmin_x / 2, 0, 0))
ring = col(chocmin_nx, chocmin_y, off=chocmin_off, **params).translate((chocmin_nx / 2 + chocmin_x / 2, 0, 0))
pinky = col(chocmin_nnx, chocmin_y, **params).translate((chocmin_nx + chocmin_nnx / 2 + chocmin_x / 2, 0, 0))
t = thumb(chocmin_y, chocmin_x, h=1.5, ang=15, gap=0.5)

export_color(t, "thumb")
export_color(middle, "middle")
export_color(index, "index")
export_color(outex, "outex")
export_color(pinky, "pinky")
export_color(ring, "ring")
