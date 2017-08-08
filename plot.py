import matplotlib.pyplot as plt
import sys
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = [x for x in color_dict if x not in {"w",'aliceblue','antiquewhite','azure','beige','bisque','blanchedalmond'}]

if sys.argc < 2:
    print("Use: ", sys.argv[0], "[file name]")
    return(-1)

def Parse(filename):
    f = open(filename, "r")
    lines = f.readlines()
    s = lines[0].split()
    nb_centers = int(s[0])
    nb_clients = int(s[1])

    C = []
    for i in range(1, nb_centers):
        s = lines[i].split()
        x = int(s[0])
        y = int(s[1])
        C.append([x,y])

    assign_pairs = {}
    A = []
    j = 0
    for i in range(nb_centers, nb_clients):
        s = lines[i].split()
        x = int(s[0])
        y = int(s[1])
        A.append([x,y])
        assign_pairs[j] = int(s[2])
        j+=1

    return C,A,assign_pairs

def PlotAll(C, A, assign_pairs):
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


C, A, assign_pairs = Parse(sys.argv[1])
PlotAll(C,A,assign_pairs)
