import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = [x for x in color_dict if x not in {"w",'aliceblue','antiquewhite','azure','beige','bisque','blanchedalmond'}]

if len(sys.argv) < 2:
    print("Use: ", sys.argv[0], "[file name]")
    exit(-1)

def Parse(filename):
    f = open(filename, "r")
    lines = f.readlines()
    s = lines[0].split()
    nb_centers = int(s[0])
    nb_clients = int(s[1])

    C = []
    for i in range(1, nb_centers+1):
        s = lines[i].split()
        print(s)
        x = float(s[0])
        y = float(s[1])
        C.append([x,y])

    assign_pairs = {}
    A = []
    j = 0
    for i in range(nb_centers+1, nb_clients+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        A.append([x,y])
        assign_pairs[j] = int(s[2])
        j+=1

    return C,A,assign_pairs

def PlotAll(C, A, assignment):
    diagram = sp.Voronoi(C)
    sp.voronoi_plot_2d(diagram)
    for i in range(len(C)):
        plt.plot(C[i][0],C[i][1], 'd', color = colors[i])
    for j in range(len(A)):
        plt.plot(A[j][0],A[j][1], 'x', color = colors[assignment[j]])
    axes = plt.gca()
    axes.set_xlim([-3,7])
    axes.set_ylim([-3,7])
    plt.show(block=True)


C, A, assign_pairs = Parse(sys.argv[1])
PlotAll(C,A,assign_pairs)
