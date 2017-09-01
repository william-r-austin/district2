import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
import shapely.geometry as sg
from shapely.geometry.polygon import Polygon
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = {"moccasin":"red", "deeppink":"pink", "mediumseagreen":"green",
              "mediumblue":"blue", "darkgoldenrod":"gold"}


def PlotAll(C, A, assignment, bounded_regions, bbox, output):
    diagram = sp.Voronoi(C)
    f = open(output, "w")
    # sp.voronoi_plot_2d(diagram)
    f.write(str(len(C))+" "+str(len(A))+"\n")
    for i in range(len(C)):
        f.write(str(C[i][0])+" "+str(C[i][1])+" "+str(colors[i])+"\n")
    for j in range(len(A)):
        f.write(str(A[j][0])+" "+str(A[j][1])+" "+str(colors[assignment[j]])+"\n")


    for r in bounded_regions:
        if bounded_regions[r] == []: continue
        region = bounded_regions[r]
        convex_hull = sg.MultiPoint(region).convex_hull
        x,y = convex_hull.exterior.xy
        for i in range(len(x)):
            f.write(str(x[i])+","+str(y[i])+" ")
        f.write("\n") #x, y, color = 'black')
    f.close()

def Parse_boundary(filename):
    f = open(filename, "r")
    lines = f.readlines()
    boundaries = []
    i = 0
    points = []
    for l in lines:
        if l == "\n" :
            boundaries.append(Polygon(points))
            points = []
            continue
        s = l.split()
        x = float(s[0])
        y = float(s[1])
        points.append([x,y])
    boundaries.append(Polygon(points))
    f.close()
    return boundaries
    
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
        # print(polygons[-1].exterior.xy)
    f.close()
    return C,A,polygons,[[x_min,y_min],[x_max,y_max]]

def PlotAll(C, A, polygons, bbox):
    # diagram = sp.Voronoi(C)
    # sp.voronoi_plot_2d(diagram)
    for i in range(len(C)):
        # print(C[i])
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


def GNUplot_boundary(p,f):
    f.write("set object polygon from ")
    # print("________")
    # print(p.exterior.xy)
    # print("________")
    x,y = p.exterior.xy
    for i in range(len(x)):
        f.write(str(x[i])+","+str(y[i]))
        if i != len(x)-1:
            f.write(" to ")
    f.write(" fc rgb 'black' lc rgb 'black' lw 3\n")

    
def GNUplot_polygon(p,f):
    f.write("set object polygon from ")
    x,y = p.exterior.xy
    for i in range(len(x)):
        f.write(str(x[i])+","+str(y[i]))
        if i != len(x)-1:
            f.write(" to ")
    f.write(" fc rgb 'black' lw 2\n")

def GNUplot_point(p,f):
    col = p[2]
    if p[2] in colors:
            col = colors[p[2]]
    f.write('set object circle at '+str(p[0])+","+str(p[1])+' radius char 0.2 fillcolor rgb "'+col+'"\n')

def GNUplot(C,A,boundary,polygons, bbox,outputfilename):
    f = open(outputfilename, "w")
    for c in C+A:
        GNUplot_point(c,f)
    for i in range(len(polygons)):
        if type(polygons[i]) == sg.multipolygon.MultiPolygon:
            for p in polygons[i]:
                GNUplot_polygon(p, f)
            continue
        GNUplot_polygon(polygons[i], f)
    for i in range(len(boundary)):
        GNUplot_boundary(boundary[i],f)
    f.write("set xrange ["+str(bbox[0][0])+":"+str(bbox[1][0])+"]\n")
    f.write("set yrange ["+str(bbox[0][1])+":"+str(bbox[1][1])+"]\n")
    f.write("plot x lc rgb 'white'\n")
    f.write("pause -1\n")
    f.close()

def plot_helper(C_3D, A, boundary, polygons, bbox, outputfilename):
    # bbox = find_bounding_box(C_3D)
    # print(bbox)
    # minpt, maxpt = bbox
    # extent = find_extent([minpt,maxpt])
    # smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    # PlotAll(C_3D, A, polygons, bbox)
    GNUplot(C_3D, A, boundary, polygons, bbox, outputfilename)

def get_approx_boundary(A):
    Ap = [[p[0],p[1]] for p in A]
    return sg.MultiPoint(Ap).convex_hull

def clip(polygons, boundary):
    clipped = polygons
    new_clipped = []
    for b in boundary:
        for i in range(len(polygons)):
            p = polygons[i]
            if b.contains(p):
                new_clipped.append(p)
            elif p.intersects(b) :
                new_clipped.append(p.intersection(b))
    # for p in new_clipped:
    #     print(p)
    return new_clipped
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Use: ", sys.argv[0], "[file name] [boundary file] [output GNUplot file]")
        exit(-1)
    C_3D, A, polygons, bbox = Parse(sys.argv[1])

    ## For testing : HERE we need to replace with the actual
    ## state boundary
    # boundary = [get_approx_boundary(A)]
    boundary = Parse_boundary(sys.argv[2])

    clipped_polygons = clip(polygons, boundary)
    plot_helper(C_3D, A, boundary, clipped_polygons, bbox, sys.argv[3])
    
