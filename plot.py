import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
import shapely.geometry as sg
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
    plt.plot(x, y, linewidth=3, color = 'black')
        
        
def Parse(filename):
    f = open(filename, "r")
    lines = f.readlines()
    s = lines[0].split()
    nb_centers = int(s[0])
    nb_clients = int(s[1])
    x_min, y_min, z_min = (float("inf"),float("inf"),float("inf"))
    x_max, y_max, z_max = (-float("inf"),-float("inf"),-float("inf"))
    
    C = []
    for i in range(1, nb_centers+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        z = float(s[2])
        C.append([x,y,z])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        z_max = max(z_max, z)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        z_min = min(z_min, z)
        

    assign_pairs = {}
    A = []
    j = 0
    for i in range(nb_centers+1, nb_centers+nb_clients+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        A.append([x,y])
        assign_pairs[j] = int(s[2])
        j+=1
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)

    return C,A,assign_pairs, [[x_min,y_min,z_min],[x_max,y_max,z_max]]

def PlotAll(C, A, assignment, bounded_regions,bbox):
    diagram = sp.Voronoi(C)
    # sp.voronoi_plot_2d(diagram)
    for i in range(len(C)):
        plt.plot(C[i][0],C[i][1], 'd', color = colors[i])
    for j in range(len(A)):
        plt.plot(A[j][0],A[j][1], 'x', color = colors[assignment[j]])
    axes = plt.gca()
    plot_regions(bounded_regions)
    # axes.set_xlim([-3,7])
    # axes.set_ylim([-3,7])
    plt.axis([bbox[0][0],bbox[1][0], bbox[0][1],bbox[1][1]])
    plt.show(block=True)



def find_bounding_box(S):
    return [[f(p[i] for p in S) for i in [0,1,2]] for f in [min, max]]

def find_extent(bbox):
    minpt, maxpt = bbox
    return [maxpt[i] - minpt[i] for i in range(3)]

def EuclidExample2(ncenters):
    vec_centers = np.random.randn(3, ncenters)

    C = np.array([[vec_centers[0][i],vec_centers[1][i],vec_centers[2][i]]
                  for i in range(len(vec_centers[0]))])

    bbox = find_bounding_box(C)

    def unbounded(input_region): return any(x==-1 for x in input_region)
    ## insert points to remove
    ## infinite regions
    minpt, maxpt = bbox
    extent = find_extent([minpt,maxpt])
    smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    # print(boundary)
    boundary = np.array([smallpt, [bigpt[0],smallpt[1],smallpt[2]],
                         [smallpt[0],bigpt[1],smallpt[2]],
                         [smallpt[0],smallpt[1],bigpt[2]],
                         [bigpt[0],bigpt[1],smallpt[2]],
                         [smallpt[0],bigpt[1],bigpt[2]],
                         [bigpt[0],smallpt[1],bigpt[2]],
                         bigpt])
    print(boundary)
    print(C)
    diagram = sp.Voronoi(np.concatenate((C,boundary)))
    bounded_regions = [[diagram.vertices[j] for j in region] for region in diagram.regions if region != [] and not unbounded(region)]
    return bounded_regions # OrderRegions(C,
                        
    # return sp.Voronoi(C)

def find_proj(bounded_regions):
    proj_regions = {}
    # print(bounded_regions)
    for i in range(len(bounded_regions)):
        region = bounded_regions[i]
        proj_regions[i] = []
        for p1 in region:
            if p1[2] < 0: continue
            for p2 in region:
                if p2[2] > 0: continue
                v = [p2[0]-p1[0],
                     p2[1]-p1[1],
                     p2[2]-p1[2]]
                t = -p1[2]/v[2]
                proj_point = [p1[0] + t*v[0],
                              p1[1] + t*v[1]]
                proj_regions[i].append(proj_point)
    return proj_regions

def plot_regions(proj_regions):

    for r in proj_regions:
        if proj_regions[r] == []: continue
        region = proj_regions[r]
        convex_hull = sg.MultiPoint(region).convex_hull
        x,y = convex_hull.exterior.xy
        plt.plot(x, y, color = 'black')
        
        

def unbounded(input_region): return any(x==-1 for x in input_region)
## insert points to remove
## infinite regions

def plot_helper(C_3D, A, assign_pairs,bbox):
    C = [[p[0],p[1]] for p in C_3D]
    # bbox = find_bounding_box(C_3D)
    minpt, maxpt = bbox
    extent = find_extent([minpt,maxpt])
    smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    boundary = np.array([smallpt, [bigpt[0],smallpt[1],smallpt[2]],
                     [smallpt[0],bigpt[1],smallpt[2]],
                     [smallpt[0],smallpt[1],bigpt[2]],
                     [bigpt[0],bigpt[1],smallpt[2]],
                     [smallpt[0],bigpt[1],bigpt[2]],
                     [bigpt[0],smallpt[1],bigpt[2]],
                     bigpt])
    diagram = sp.Voronoi(np.concatenate((C_3D,boundary)))
    bounded_regions = [[diagram.vertices[j] for j in region]
                       for region in diagram.regions
                       if region != [] and not unbounded(region)]
    proj_regions = find_proj(bounded_regions)
    PlotAll(C,A,assign_pairs, proj_regions,bbox)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Use: ", sys.argv[0], "[file name] [state boundary file]")
        exit(-1)
    C_3D, A, assign_pairs, box = Parse(sys.argv[1])
    Parse_and_plot_boundary(sys.argv[2])
    plot_helper(C_3D, A, assign_pairs, box)
    
