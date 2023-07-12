from sqdg import Config, col, thumb_col, export_color, thumb

chocmin_x, chocmin_y, chocmin_nnx = 18, 12.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
c = Config(gap=0.5, cr=65, ang=35)
ch = c + Config(crh=80)

F = col(c + Config(chocmin_x, chocmin_y))
R = col(ch + Config(chocmin_nx, chocmin_y, off=-chocmin_off))
RI = col(ch + Config(chocmin_nnx, chocmin_y, off=chocmin_nnx, soff=0))
L = col(ch + Config(chocmin_nx, chocmin_y, off=chocmin_off))
LI = col(ch + Config(chocmin_nnx, chocmin_y, off=-chocmin_nnx, soff=0))
N = col(ch + Config(chocmin_nnx, chocmin_y))
# T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1.5, ang=15))
T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1, ang=15, voff=2.5), rotated=False, offset=True)

right_disp = R | F.move(0, 7) | L | N.move(0, -21)

if "show_object" in locals():
    show_object(right_disp.thing, "right")
    # show_object(T.thing, "thumb")
    # show_object(whole.thing, "whole")

export_color(right_disp.thing, "musk-chocmini-min-whole")
