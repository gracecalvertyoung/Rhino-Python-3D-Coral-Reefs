import Rhino 
import rhinoscriptsyntax as rs
import math

# -----  Initalize Variables -----
link_length = .02 # m

# ----- Function Definitions -----

def Rugosity_horizontal_v1(crv_id):

    pts = rs.DivideCurveEquidistant(crv_id, link_length,
                                    create_points=False,
                                    return_points=True)

    # find the rugosity length (horizontal/vertical dependent)
    rugosity_start = pts[0] 
    rugosity_end = pts[len(pts)-1]
    rugosity_numerator = abs(rugosity_end.X - rugosity_start.X)

    # find the chain length (not horizontal/vertical dependent)
    rugosity_denominator = 0 
    for i in range(1, len(pts)):
        extra = rs.VectorLength(rs.VectorCreate(pts[i], pts[i-1]))
        rugosity_denominator = rugosity_denominator + extra

    rugosity = rugosity_numerator / rugosity_denominator

    return rugosity

# -----        Main          -----

# get input curve (polyline) from user
# this curve follows the mesh over at least the rugosity line length,
# it was created by a mesh-mesh intersection of plane with reef mesh
crv_ids = rs.GetObjects(message="Select curves",
                                filter = rs.filter.curve, 
                                preselect = True,
                                select = False)

list_R = []
for crv in crv_ids:
    R = Rugosity_horizontal_v1(crv)
    list_R.append(R)

# at end of script
# return results in format ready to paste into Excel
str_R = ""
for n in list_R:
    str_R = str_R + str(n)
    if list_R.index(n) != len(list_R) - 1:
        str_R = str_R + ", "

print("RUGOSITY data ready to paste into Excel (after an = sign): ")
print("AVERAGE(" + str_R + ")")
print("STDEV("+ str_R + ")")


