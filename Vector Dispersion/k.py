import rhinoscriptsyntax as rs
import math

# -----  Initalize Variables -----
# ASSUMTION: "Top" plane is selected
# ASSUMTIION: Model units are meters
# ASSUMPTION: x, y coordinates of grid pts are multiples of .01

unit = .01 # m

# ----- Function Definitions -----

def PtCldVecDisp(ptsList):
    # calculate vector disp

    # round x and y to eliminate sorting errors
    # create list ptsXYZ with rounded x, y values, full z value
    # create list ptsXY with only rounded x, y values
    [ptsXYZ, ptsXY] = RoundPts(ptsList) 

    # if there is more than one point with the same x, y value
    # choose point with the highest z value
    [ptsXY_clean, ptsXYZ_clean] = TakeTopZ(ptsXY, ptsXYZ)

    # add directional cosines; keep track of number of triangles created (i)
    i = 0
    noPts = len(ptsXY_clean)
    sumCosx = 0
    sumCosy = 0
    sumCosz = 0

    counter = 0 
    for iPt in range(0, noPts): 

        # define point1: x, y, z
        pt1 = ptsXYZ_clean[iPt]

        # only process if not an edge point
        if CheckIfEdge(pt1, ptsXY_clean):

            counter = counter + 1

            # find closest four points (points 2, 3, 4, 5)
            [pt2, pt3, pt4, pt5] = FindAdjPts(pt1, ptsXY_clean, ptsXYZ_clean)           

            # define vec1, pt1->pt2
            # define vec2, pt1->pt4
            # these two vectors define surface A
            vec1 = rs.VectorCreate(pt1, pt2)
            vec2 = rs.VectorCreate(pt1, pt4)

            # compute normal (via cross product) of surface A
            vecNormalA = rs.VectorCrossProduct(vec1, vec2)

            # note that we've defined one more surface
            i += 1

            # draw surface
            DrawVecSrf(pt1, pt2, pt4)

            # add to sum directional consines of surface A
            cosNormalA = CosNormal(vecNormalA[0], vecNormalA[1], vecNormalA[2])
            sumCosx += cosNormalA[0] 
            sumCosy += cosNormalA[1]
            sumCosz += cosNormalA[2] 

            # define vec3, pt1->pt3
            # define vec4, pt1->pt5
            # these two vectors define surface B
            vec3 = rs.VectorCreate(pt1, pt3)
            vec4 = rs.VectorCreate(pt1, pt5)
            
            # compute normal (via cross product) of surface B
            vecNormalB = rs.VectorCrossProduct(vec3, vec4)

            # note that we've defined one more surface
            i += 1

            # draw surface
            DrawVecSrf(pt1, pt3, pt5)

            # add to sum directional consines of surfaces B
            cosNormalB = CosNormal(vecNormalB[0], vecNormalB[1], vecNormalB[2])
            sumCosx += cosNormalB[1]
            sumCosy += cosNormalB[1]
            sumCosz += cosNormalB[2]

    # compute R1
    sumCosx2 = math.pow(sumCosx, 2)
    sumCosy2 = math.pow(sumCosy, 2)
    sumCosz2 = math.pow(sumCosz, 2)
    R1 = math.sqrt((sumCosx2 + sumCosy2 + sumCosz2))

    # compute vector dispersion vK
    vk = (i - R1) / (i - 1)

    return vk 

def RoundPts(unrounded_pts):

    # round x and y to eliminate sorting errors
    # create list ptsXYZ with rounded x, y values, full z value
    # create list ptsXY with only rounded x, y values
    ptsXYZ = []
    ptsXY = []
    for pt in unrounded_pts:
        ptXYZ = []
        ptXY = []
        i = 0
        for coord in pt:
            if i < 2:
                coordNew = round(coord, 2)
                ptXYZ.append(coordNew)
                ptXY.append(coordNew)
                i += 1
            else:
                ptXYZ.append(coord)               
        ptsXYZ.append(ptXYZ)
        ptsXY.append(ptXY)

    # sort list of points 
    ptsXYZ.sort()
    ptsXY.sort()

    # return rounded pts
    return [ptsXYZ, ptsXY]

def TakeTopZ(ptsXY, ptsXYZ):

    # get rid of lower point(s) if there are more than one point with same x, y value
    counter = 0
    ptsXYZ_clean = []
    ptsXY_clean = []
    for [x, y, z] in ptsXYZ:
        i = ptsXY.index([x, y])
        if i == counter:
            ptsXYZ_clean.append([x, y, z])
            ptsXY_clean.append([x, y])
        counter += 1
    
    return [ptsXY_clean, ptsXYZ_clean]

def CheckIfEdge(pt1, ptsXY):
    pt2 = [round(pt1[0] + unit, 2), round(pt1[1], 2)]
    pt3 = [round(pt1[0] - unit, 2), round(pt1[1], 2)]
    pt4 = [round(pt1[0], 2) , round(pt1[1] + unit, 2)]
    pt5 = [round(pt1[0], 2), round(pt1[1] - unit, 2)]
    boolpt2 = pt2 in ptsXY
    boolpt3 = pt3 in ptsXY
    boolpt4 = pt4 in ptsXY
    boolpt5 = pt5 in ptsXY
    if boolpt2 & boolpt3 & boolpt4 & boolpt5:
        return True
    else:            
        return False
    
def FindAdjPts(pt1, ptsXY, ptsXYZ):

    # define point2: x+1, y, z2
    pt2x = round(pt1[0] + unit, 2)
    pt2y = round(pt1[1], 2)
    iPt2 = ptsXY.index([pt2x, pt2y])
    pt2z = ptsXYZ[iPt2][2]

    # define point3: x-1, y, z3
    pt3x = round(pt1[0] - unit, 2)
    pt3y = round(pt1[1], 2)
    iPt3 = ptsXY.index([pt3x, pt3y])
    pt3z = ptsXYZ[iPt3][2]

    # define point4: x, y+1, z4
    pt4x = round(pt1[0], 2)
    pt4y = round(pt1[1] + unit, 2)
    iPt4 = ptsXY.index([pt4x, pt4y])
    pt4z = ptsXYZ[iPt4][2]

    # define point5: x, y-1, z4
    pt5x = round(pt1[0], 2)
    pt5y = round(pt1[1] - unit, 2)
    iPt5 = ptsXY.index([pt5x, pt5y])
    pt5z = ptsXYZ[iPt5][2]

    # define all points
    pt2 = [pt2x, pt2y, pt2z]
    pt3 = [pt3x, pt3y, pt3z]
    pt4 = [pt4x, pt4y, pt4z]
    pt5 = [pt5x, pt5y, pt5z]

    return [pt2, pt3, pt4, pt5]

def CosNormal(lenNormalx, lenNormaly, lenNormalz):

    # square normals
    lenNormalx2 = math.pow(lenNormalx, 2)
    lenNormaly2 = math.pow(lenNormaly, 2)
    lenNormalz2 = math.pow(lenNormalz, 2)

    # calculate directional cosines 
    denominator = math.sqrt((lenNormalx2 + lenNormaly2 + lenNormalz2))
    cosNormalx = lenNormalx / denominator
    cosNormaly = lenNormaly / denominator
    cosNormalz = lenNormalz / denominator
    
    return [cosNormalx, cosNormaly, cosNormalz]

def DrawVecSrf(pt1, pt2, pt4):
    strCrvA1 = rs.AddLine(pt1, pt2)
    strCrvA2 = rs.AddLine(pt1, pt4)
    rs.AddEdgeSrf([strCrvA1, strCrvA2])
    strCrvA3 = rs.AddLine(pt2, pt4)

    return 

# -----        Main          -----

# ask user to select reef mesh
mesh_id = rs.GetObject(message="Select the reef mesh",
                           filter = 32, # mesh
                           preselect = False, 
                           select = False)

# ask user to select point clouds
cloud_ids = rs.GetObjects(message="Select Point Clouds",
                       filter = 2, 
                       preselect = True, 
                       select = True)

# have the point clouds projected onto the mesh
# and each result made into another cloud
new_cloud_ids = []
for cloud in cloud_ids:

    ptsList = rs.PointCloudPoints(cloud)
    
    pts_proj = rs.ProjectPointToMesh(ptsList, mesh_id, [0, 0, -10])
    new_cloud_ids.append(rs.AddPointCloud(pts_proj))

list_vk = []
for cloud in new_cloud_ids:
    ptsList = rs.PointCloudPoints(cloud)
    
    # calculate the vector dispersion   
    list_vk.append(PtCldVecDisp(ptsList))

# return results in format ready to paste into Excel
str_vk = ""
for n in list_vk:
    str_vk = str_vk + str(n)
    if list_vk.index(n) != len(list_vk) - 1:
        str_vk = str_vk + ", "

print("VECTOR DISPERSION data ready to paste into Excel (after an = sign): ")
print("AVERAGE(" + str_vk + ")")
print("STDEV("+ str_vk + ")")

