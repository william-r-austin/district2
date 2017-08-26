import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
import shapely.geometry as sg
from shapely.geometry.polygon import Polygon
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = [x for x in color_dict if x not in {"w",'aliceblue','antiquewhite','azure','beige','bisque','blanchedalmond'}]

def Parse_and_plot_boundary(filename):
    f = open(filename, "r")
    lines = f.readlines()
    points = []
    for l in lines:
        s = l.split()
        x = float(s[0])
        y = float(s[1])
        points.append([x,y])
        
    convex_hull = sg.MultiPoint(points).convex_hull
    x,y = convex_hull.exterior.xy
        
def Parse(filename):
    f = open(filename, "r")
    lines = f.readlines()
    s = lines[0].split()
    nb_centers = int(s[0])
    nb_clients = int(s[1])
    x_min, y_min = (float("inf"),float("inf"))
    x_max, y_max = (-float("inf"),-float("inf"))
    
    C = []
    for i in range(1, nb_centers+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        color = s[2]
        C.append([x,y,color])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        

    assign_pairs = {}
    A = []
    for i in range(nb_centers+1, nb_centers+nb_clients+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        color = s[2]
        A.append([x,y,color])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)

    polygons = []
    for i in range(nb_centers+nb_clients+1, len(lines)):
        points_unsplit = lines[i].split()
        points = [[float(points_unsplit[j].split(",")[0]),
                       float(points_unsplit[j].split(",")[1])]
                    for j in range(len(points_unsplit))]
        polygons.append(Polygon(points))
    f.close()
    print(C[0])
    return C,A,polygons,[[x_min,y_min],[x_max,y_max]]

def PlotAll(C, A, polygons, bbox):
    # diagram = sp.Voronoi(C)
    # sp.voronoi_plot_2d(diagram)
    for i in range(len(C)):
        print(C[i])
        plt.plot(C[i][0],C[i][1], 'd', color = C[i][2])
    for j in range(len(A)):
        if j % 1000 == 0 : print(j)
        plt.plot(A[j][0],A[j][1], 'x', color = A[j][2])
    # axes = plt.gca()
    for p in polygons:
        plt.plot(p.exterior.xy[0], p.exterior.xy[1],
                     color = 'black')
    plt.axis([bbox[0][0],bbox[1][0], bbox[0][1],bbox[1][1]])
    plt.show(block=True)


def GMLpolygon(p, f):
    f.write("<gml:Polygon>\n")
    f.write("<gml:exterior><gml:LinearRing>\n")
    x,y = p.exterior.xy
    for i in range(len(x)):
        f.write(str(x[i])+" "+str(y[i])+" ")
    f.write("\n")
    f.write("</gml:LinearRing></gml:exterior>\n")
    f.write("</gml:Polygon>\n")

def GMLpoint(p, f):
    f.write("<gml:Point>\n")
    f.write("<gml:pos>"+str(p[0])+" "+str(p[1])+"</gml:pos>\n")
    f.write("</gml:Point>\n")
    
def GMLplot(C,A,polygons,outputfilename):
    f = open(outputfilename, "w")
    for c in C+A:
        GMLpoint(c,f)
    for p in polygons:
        GMLpolygon(p,f)
    f.close()

def plot_helper(C_3D, A, polygons, bbox, outputfilename):
    # bbox = find_bounding_box(C_3D)
    print(bbox)
    # minpt, maxpt = bbox
    # extent = find_extent([minpt,maxpt])
    # smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    #PlotAll(C_3D, A, polygons, bbox)
    GMLplot(C_3D, A, polygons, outputfilename)

def get_approx_boundary(A):
    Ap = [[p[0],p[1]] for p in A]
    return sg.MultiPoint(Ap).convex_hull

def clip(polygons, boundary):
    clipped = []
    for i in range(len(polygons)):
        p = polygons[i]
        p_clipped = p.intersection(boundary)
        clipped.append(p_clipped)
    return clipped
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Use: ", sys.argv[0], "[file name] [output GML file]")
        exit(-1)
    C_3D, A, polygons, bbox = Parse(sys.argv[1])

    ## For testing : HERE we need to replace with the actual
    ## state boundary
    boundary = get_approx_boundary(A)
    
    clipped_polygons = clip(polygons, boundary)
    print(C_3D[0])
    plot_helper(C_3D, A, clipped_polygons, bbox, sys.argv[2])
    
