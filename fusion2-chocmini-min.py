from sqdg import Config, col, thumb_col, export_color, thumb

chocmin_x, chocmin_y, chocmin_nnx = 18, 13.5, 14.5
chocmin_nx = (chocmin_x + chocmin_nnx) / 2
chocmin_off = chocmin_nx / 2 - (chocmin_nx - chocmin_x / 2)
c = Config(gap=0.5, cr=75, sh=3.5, ang=35)
ch = c + Config(crh=100)

F = col(c + Config(chocmin_x, chocmin_y))
R = col(ch + Config(chocmin_nx, chocmin_y, off=-chocmin_off))
RI = col(ch + Config(chocmin_nnx, chocmin_y, off=chocmin_nnx, soff=0))
L = col(ch + Config(chocmin_nx, chocmin_y, off=chocmin_off))
LI = col(ch + Config(chocmin_nnx, chocmin_y, off=-chocmin_nnx, soff=0))
N = col(ch + Config(chocmin_nnx, chocmin_y))
NO = col(ch + Config(chocmin_nnx, chocmin_y, off=-chocmin_nnx, soff=0))
# T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1.5, ang=15))
T = thumb_col(c + Config(chocmin_x, chocmin_y, eh=1, ang=15, voff=2.5), rotated=False, offset=True)

right_disp = RI | R | F.move(0, 7) | L | N.move(0, -20) | NO.move(0, -20)

# right = T | RI | R | F | L | N
# left = T | N | R | F | L | LI
# whole = left + right

if "show_object" in locals():
    show_object(right_disp.thing, "right")
    # show_object(T.thing, "thumb")
    # show_object(whole.thing, "whole")

# export_color(whole.thing, "fusion2-chocmini-min-whole")
