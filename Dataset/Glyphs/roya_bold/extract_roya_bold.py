
import fontforge
F = fontforge.open("../../Fonts/roya_bold")
for name in F:
    filename = name + ".png"
    # print name
    # F[name].export(filename)
    F[name].export(filename, 600)     # set height to 600 pixels
    