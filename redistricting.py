import numpy as np
import math
from copy import copy

import matplotlib.pyplot as plt
import scipy.spatial as sp
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = [x for x in color_dict if x not in {"w",'aliceblue','antiquewhite','azure','beige','bisque','blanchedalmond'}]


def find_bounding_box(S):
    return [[f(p[i] for p in S) for i in [0,1]] for f in [min, max]]

def find_extent(bbox):
    minpt, maxpt = bbox
    return [maxpt[i] - minpt[i] for i in range(2)]

### WARNING : this is for 2d for now!
def EuclidVoronoi(C,bbox):
    def unbounded(input_region): return any(x==-1 for x in input_region)
    ## insert points to remove
    ## infinite regions
    minpt, maxpt = bbox
    extent = find_extent([minpt,maxpt])
    smallpt, bigpt = [minpt[i]-extent[i] for i in range(2)], [maxpt[i]+extent[i] for i in range(2)]
    boundary = np.array([smallpt, [bigpt[0],smallpt[1]],[smallpt[0],bigpt[1]],bigpt])
    diagram = sp.Voronoi(np.concatenate((C,boundary)))
    bounded_regions = [[diagram.vertices[j] for j in region] for region in diagram.regions if region != [] and not unbounded(region)]
    return OrderRegions(C,bounded_regions)

def OrderRegions(C, bounded_regions):
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    return [[r for r in bounded_regions if Point(p[0],p[1]).distance(Polygon(r))==0][0] for p in C]

### WARNING : this is for 2d for now!
def EuclidCost(A, bounded_regions):
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    cost = {}
    for a in range(len(A)):
        pa = Point(A[a][0],A[a][1])
        cost[a] = {}
        for i in range(len(bounded_regions)):
            R = Polygon(bounded_regions[i])
            cost[a][i] = pa.distance(R)
    return cost


def FindAssignment(nb_cells, cost):
    import munkres as mk
    cluster_size = int(len(cost)/nb_cells)
    matrix = [sum([cluster_size*[c] for p,c in cost[v].items()],[]) for v in cost]
    # print(cost[0], assign_mat)
    m = mk.Munkres()
    assignment = m.compute(matrix)
    real_assignment = []
    for (i,j) in assignment:
        real_j = math.floor(j/cluster_size)
        real_assignment.append((i,real_j))
    finalcost = {}
    for (i,j) in real_assignment:
        finalcost[i] = cost[i][j]
    return real_assignment, finalcost

def Eval(val):
    cost = 0
    for i in val:
        cost+= val[i]
    return cost

## Warning : only for 2d for now
def FindMove(assignment, center, A, C, cost,
             bounded_regions, diameter, highconstant = 2000.0):
    c_x = C[center][0]
    c_y = C[center][1]
    cluster = [j for (j,i) in assignment if i == center]

    vector = [0,0]
    for j in cluster:
        w_j = MoveWeights(A[j], center, bounded_regions,len(cluster))
        #if cost[j][center] == 0 : continue
        j_x = A[j][0]
        j_y = A[j][1]
        vect_x = j_x - c_x
        vect_y = j_y - c_y
        norm_vect = math.sqrt(vect_x * vect_x  + vect_y * vect_y)
        if norm_vect > 0:
            vector[0] += w_j * float(vect_x)/float(norm_vect)
            vector[1] += w_j * float(vect_y)/float(norm_vect)
    vector[0] /= highconstant
    vector[1] /= highconstant
    return vector 

## Warning : only for 2d for now
def Algorithm(A,C, NBiterations=100):
    bbox = find_bounding_box(A)
    extent = find_extent(bbox)
    vor_regions = EuclidVoronoi(C,bbox)
    cost = EuclidCost(A, vor_regions)
    assignment, val = FindAssignment(len(C), cost)
    rr = 0
    init_val = Eval(val)
    for i in range(NBiterations):
        vector = FindMove(assignment, rr, A, C, cost, vor_regions, max(extent))
        C[rr][0] += vector[0]
        C[rr][1] += vector[1]
        vor_regions = EuclidVoronoi(C,bbox)
        old_val = Eval(val)
        cost = EuclidCost(A, vor_regions)
        assignment, val = FindAssignment(len(C), cost)
        if i%130 == 0:
            print("Iteration", i, "| moved center ", rr, "at",
                  C[rr][0] -vector [0], C[rr][1] -vector[1],
                  "to", C[rr][0], C[rr][1])
            print("Old val", old_val, "New val", Eval(val))
            PlotAll(C, A, assignment)
        rr = (rr + 1) % len(C)
        if Eval(val) == 0 : break

    print("Init Val", init_val, "Final Val", Eval(val))
    return C, assignment
    
def PlotAll(C, A, assign_pairs):
    assignment=dict(assign_pairs)
    diagram = sp.Voronoi(C)
    sp.voronoi_plot_2d(diagram)
    for i in range(len(C)):
        plt.plot(C[i][0],C[i][1], 'd', color = colors[i])
    for j in range(len(A)):
        plt.plot(A[j][0],A[j][1], 'x', color = colors[assignment[j]])
    axes = plt.gca()
    axes.set_xlim([-3,7])
    axes.set_ylim([-3,7])
    plt.show(block=False)

### Warning for 2d only    
def MoveWeights(a, c, bounded_regions, k):
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    pa = Point(a[0],a[1])
    R_c = Polygon(bounded_regions[c])
    if pa.distance(R_c) > 0:
        return 1 #pa.distance(R_c)
    else:
        return 1/k
        min_dist = min(pa.distance(Polygon(bounded_regions[i])) for i in range(len(bounded_regions)) if i != c)
    return -min_dist
    
def EuclidExample(ncenters, npoints, iters, ndim =2):
    vec_points = np.random.randn(ndim, npoints)
    vec_centers = np.random.randn(ndim, ncenters)

    ### random set of points/centers
    coord_points = np.array([[vec_points[0][i],vec_points[1][i]]
                             for i in range(len(vec_points[0]))])

    coord_centers = np.array([[vec_centers[0][i],vec_centers[1][i]]
                              for i in range(len(vec_centers[0]))])
    ### more complicated example
    # coord_centers = np.array([[0,0],[0.01,0], [0,0.01],[0.01,0.01],
    #                           [0.005,0.005]])    
    # vor_regions = EuclidVoronoi(coord_centers)
    # cost = EuclidCost(coord_points, vor_regions)
    # assignment, val = FindAssignment(len(coord_centers), cost)

    ### Easy example
    # coord_centers = np.array([[0,0],[1,0],[0,1],[1,1]])
    # coord_points = np.array([[0.1,0.1],[0.2,0.2],[0.3,0,3],[0.9,0.1],[0.9,0.2],[0.9,0.3],[0.9,0.9],[0.9,1],[1,0.9],
    #                         [0.1,0.9],[0.1,0.8],[0.1,1]])
    
    A= coord_points
    C, assign_pairs = Algorithm(coord_points,coord_centers,NBiterations=iters)
    assignment={}
    for i,x in assign_pairs:
        assignment[i] = x
    minCx = 10
    minCy = 10
    for i in range(len(C)):
        minCx=min(minCx, C[i][0])
        minCy=min(minCy, C[i][1])
    Cprime=[]
    for i in range(len(C)):
        Cprime.append([C[i][0]+abs(minCx), C[i][1]+abs(minCy)])
    Aprime = []
    for i in range(len(A)):
        Aprime.append([A[i][0]+abs(minCx), A[i][1]+abs(minCy)])

    PlotAll(Cprime,Aprime, assignment)
    
def createEuclidExample(ncenters, npoints, ndim=2):
    vec_points = np.random.randn(ndim, npoints)
    vec_centers = np.random.randn(ndim, ncenters)

    ### random set of points/centers
    coord_points = np.array([[vec_points[0][i],vec_points[1][i]]
                             for i in range(len(vec_points[0]))])

    coord_centers = np.array([[vec_centers[0][i],vec_centers[1][i]]
                              for i in range(len(vec_centers[0]))])
    ### more complicated example
    # coord_centers = np.array([[0,0],[0.01,0], [0,0.01],[0.01,0.01],
    #                           [0.005,0.005]])    
    # vor_regions = EuclidVoronoi(coord_centers)
    # cost = EuclidCost(coord_points, vor_regions)
    # assignment, val = FindAssignment(len(coord_centers), cost)

    ### Easy example
    # coord_centers = np.array([[0,0],[1,0],[0,1],[1,1]])
    # coord_points = np.array([[0.1,0.1],[0.2,0.2],[0.3,0,3],[0.9,0.1],[0.9,0.2],[0.9,0.3],[0.9,0.9],[0.9,1],[1,0.9],
    #                         [0.1,0.9],[0.1,0.8],[0.1,1]])
    
    return coord_points, coord_centers

def runExample(coord_points, coord_centers, iter):
    A = coord_points
    C, assign_pairs = Algorithm(coord_points,copy(coord_centers),iter)
    print("centers: ", repr(C))
    minCx = 10
    minCy = 10
    for i in range(len(C)):
        minCx=min(minCx, C[i][0])
        minCy=min(minCy, C[i][1])
    Cprime=[]
    for i in range(len(C)):
        Cprime.append([C[i][0]+abs(minCx), C[i][1]+abs(minCy)])
    Aprime = []
    for i in range(len(A)):
        Aprime.append([A[i][0]+abs(minCx), A[i][1]+abs(minCy)])

    PlotAll(Cprime,Aprime, assign_pairs)
    
#EuclidExample(5,40)



















##############################  GRAPH VERSION ##############################
############################################################################
############################################################################
############################################################################
## Compute a Voronoi diagram of a set of points P in a general metric space G
## (i.e.: weighted graph)
##
## Return : the partition of the vertices of G into Voronoi cells, a map from
## each vertex to its Voronoi cell, the boundary vertices 
######
def Voronoi(G, P):
    import heapq as hq
    # voronoi_parts = {p:[] for p in P}
    voronoi_cells = {v:-1 for v in G}
    vertices = [(0,p,p) for p in P] # dist, id vertex, voronoi cell
    seen = [p for p in P]
    
    while vertices:
        (dist, v, cell) = hq.heappop(vertices)
        if v in seen: continue
        seen.append(v)
        # voronoi_parts[cell].append(v)
        voronoi_cells[v] = cell
        for u in G[v]:
            if u not in seen:
                hq.heappush(vertices, (dist+G[v][u]['weight'], u, cell))

    voronoi_boundaries = {p:[] for p in P}
    for u in G:
        for v in G[u]:
            if voronoi_cells[v] != voronoi_cells[u]:
                voronoi_boundaries[voronoi_cells[u]].append(u)
                break
    return voronoi_boundaries,voronoi_cells


######
## Compute the cost of assigning vertex v to Voronoi cell V
#####
def GetAssignmentCost(G, voronoi_boundaries, voronoi_cells):
    cost = {}
    for v in G:
        cost[v] = {}
        for p in voronoi_boundaries:
            mincost_p = min([G[v][u]['weight'] for u in voronoi_boundaries[p]])
            cost[v][p] = mincost_p
    return cost





    
    

