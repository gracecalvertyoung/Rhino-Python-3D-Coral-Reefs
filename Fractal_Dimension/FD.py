import Rhino 
import rhinoscriptsyntax as rs
import math

# -----  Initalize Variables -----
# ASSUMTION: corner ptA of quadrat is sitting at origin
# ASSUMTION: All of model is in positive z coordinate quadrant I 
# ASSUMTION: "Top" plane is selected

pt_origin = [0, 0, 10]
start = [pt_origin[0] + .05, pt_origin[1] + .05, pt_origin[2]]
array_N2 = [1.2, .6, .3, .15, .05, .01]
end_x = start[0] + array_N2[0] 
end_y = start[1] + array_N2[0] 

# ----- Function Definitions -----

def selPts(pts_input, ptA, ptB, ptC, ptD):
    # choose only the highest points 
    
    ptA_candidates = []
    ptB_candidates = []
    ptC_candidates = []
    ptD_candidates = []
    
    for pt in pts_input:
        if pt[0] == ptA[0] and pt[1] == ptA[1]: 
            ptA_candidates.append(pt)
        elif pt[0] == ptB[0] and pt[1] == ptB[1]:
            ptB_candidates.append(pt)
        elif pt[0] == ptC[0] and pt[1] == ptC[1]:
            ptC_candidates.append(pt)
        else:
            ptD_candidates.append(pt)

    ptA_max = ptA_candidates[0]
    for pt in ptA_candidates:
        if pt[2] > ptA_max[2]:
            ptA_max = pt

    ptB_max = ptB_candidates[0]
    for pt in ptB_candidates:
        if pt[2] > ptB_max[2]:
            ptB_max = pt

    ptC_max = ptC_candidates[0]
    for pt in ptC_candidates:
        if pt[2] > ptC_max[2]:
            ptC_max = pt

    ptD_max = ptD_candidates[0]
    for pt in ptD_candidates:
        if pt[2] > ptD_max[2]:
            ptD_max = pt

    pts_output = [ptA_max, ptB_max, ptC_max, ptD_max]       

    return pts_output

def flipBowtie(srf_id, pts_for_srf, N2):
    # corrects for Rhino bug by flipping "bow tie" surfaces 
    # I know there is a more consise way to code this,
    # but this is easy 

    rs.SelectObject(srf_id) # select surface 
    rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
    proj_id = rs.GetObject(preselect=True)

    if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
        [ptA1, ptB1, ptC1, ptD1] = pts_for_srf
        rs.DeleteObject(srf_id)
        srf_id = rs.AddSrfPt([ptB1, ptC1, ptD1, ptA1])
        rs.SelectObject(srf_id) # select surface 
        rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
        proj_id = rs.GetObject(preselect=True)
        if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
            rs.DeleteObject(srf_id)
            pts_for_srf = [ptC1, ptD1, ptA1, ptB1]
            srf_id = rs.AddSrfPt([ptC1, ptD1, ptA1, ptB1])
            rs.SelectObject(srf_id) # select surface 
            rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
            proj_id = rs.GetObject(preselect=True)
            if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                rs.DeleteObject(srf_id)
                pts_for_srf = [ptD1, ptA1, ptC1, ptC1]
                srf_id = rs.AddSrfPt([ptD1, ptA1, ptC1, ptC1])
                rs.SelectObject(srf_id) # select surface 
                rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
                proj_id = rs.GetObject(preselect=True)
                if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                    rs.DeleteObject(srf_id)
                    pts_for_srf = [ptA1, ptD1, ptC1, ptB1]
                    srf_id = rs.AddSrfPt([ptA1, ptD1, ptC1, ptB1])
                    rs.SelectObject(srf_id) # select surface 
                    rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
                    proj_id = rs.GetObject(preselect=True)
                    if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                        rs.DeleteObject(srf_id)
                        pts_for_srf = [ptD1, ptC1, ptB1, ptA1]
                        srf_id = rs.AddSrfPt([ptD1, ptC1, ptB1, ptA1])
                        rs.SelectObject(srf_id) # select surface 
                        rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
                        proj_id = rs.GetObject(preselect=True)
                        if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                            rs.DeleteObject(srf_id)
                            pts_for_srf = [ptC1, ptB1, ptA1, ptD1]
                            srf_id = rs.AddSrfPt([ptC1, ptB1, ptA1, ptD1])
                            rs.SelectObject(srf_id) # select surface 
                            rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
                            proj_id = rs.GetObject(preselect=True)
                            if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                                rs.DeleteObject(srf_id)
                                pts_for_srf = [ptB1, ptA1, ptD1, ptC1]
                                srf_id = rs.AddSrfPt([ptB1, ptA1, ptD1, ptC1])
                                rs.SelectObject(srf_id) # select surface 
                                rs.Command("-_projecttocplane " + "Yes " + "-_Enter ")
                                proj_id = rs.GetObject(preselect=True)
                                if rs.SurfaceArea(proj_id)[0] < .75*(N2**2):
                                    print("could not flip bowtie :( ")

    return pts_for_srf

# -----        Main          -----

# ensure that there are six layers
rs.AddLayer()
rs.AddLayer()
rs.AddLayer()
rs.AddLayer()
rs.AddLayer()
rs.AddLayer()

# ensure that "top" is the CPlane
# planeXY = rs.WorldXYPlane()
# rs.ViewCPlane(view = None, plane = planeXY)

# get mesh ID from user 
mesh_id = rs.GetObject(message="Select the reef mesh. Remember to select from TOP viewport.",
                           filter = 32, # mesh
                           preselect = False, 
                           select = False)

# initialize values 
pt_start = start
srfArea = 0
list_srfArea = []

for N2 in array_N2:

    # lay out points
    # the rounding gets rid of some floating-pt errors
    while round(pt_start[1], 2) < round(end_y, 2):

        # define four corners points of surface
        # explained more clearly in seperate document
        ptA = pt_start
        ptB = [pt_start[0] + N2, pt_start[1], pt_start[2]]
        ptC = [pt_start[0] + N2, pt_start[1] + N2, pt_start[2]]
        ptD = [pt_start[0], pt_start[1] + N2, pt_start[2]]
        pts_for_srf = [ptA, ptB, ptC, ptD]

        # drop the points to the reef mesh
        # note that rs.PullPoints(mesh_id, pts_for_srf) isn't right
        pts_for_srf = rs.ProjectPointToMesh(pts_for_srf, mesh_id, [0, 0, -1])
        
        # select only the (four) highest points
        pts_for_srf = selPts(pts_for_srf, ptA, ptB, ptC, ptD)

        # set layer to draw stuff in
        l = "Layer 0" + str(array_N2.index(N2) + 1)
        rs.CurrentLayer(layer=l)

        # draw a surface between four points, counterclockwise
        srf_id = rs.AddSrfPt(pts_for_srf)

        # flip "bowtie" surfaces
        # ASSUMES "Top" CPlane!
        pts_for_srf = flipBowtie(srf_id, pts_for_srf, N2)  

        # redraw surface
        rs.AddSrfPt(pts_for_srf)
        srf_id = rs.AddSrfPt(pts_for_srf)
        
        # compute area of surface, add to total area
        srfArea = srfArea + rs.SurfaceArea(srf_id)[0]

        # delete surface
        rs.DeleteObject(srf_id)

        # reset layer
        rs.CurrentLayer(layer="Default")

        # move pt_start to ptB until ptB[0] = end_x,
        # at which point move pt_start to [start[0], start[1] + row * N2, start[2]],
        if round(ptB[0], 2) < round(end_x, 2):
            pt_start = ptB
        else:
            pt_start = [start[0], pt_start[1] + N2, start[2]]

    # save surface area
    list_srfArea.append(srfArea)

    # reset values
    pt_start = start
    srfArea = 0

# at end of script... 
# print ln(srfArea) for each scale
# print in one line, seperated by a comma
print("ln(S(delta)) for deltas " + str(array_N2) + " (m) resp.:")
str_areas = "" 
for i in range(0, len(list_srfArea)):
    ln_area = math.log(list_srfArea[i])
    str_areas = str_areas + str(ln_area)
    if not i == len(list_srfArea) - 1:
        str_areas = str_areas + ", "
print(str_areas + "\n")

# print D for each area group
# e.g., for 1.60--0.80, 0.80--0.40, 0.40--0.20, 0.20--0.10, 0.10--0.05
#   if array_N2 = [1.6, .8, .4, .2, .1, .05]
print("D for for deltas " + str(array_N2) + " (m) resp.: ") 			
str_D = "" 
for i in range(0, len(array_N2) - 1):
    num = math.log(list_srfArea[i]) - math.log(list_srfArea[i + 1])
    den = math.log(array_N2[i]) - math.log(array_N2[i + 1])
    D = 2 - num / den
    str_D = str_D + str(D)
    if not i == len(array_N2) - 2:
        str_D = str_D + ", "
print(str_D) 
    
          


