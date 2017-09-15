import subprocess
import os

states_code = ["01","12","17","36","39","48","06"]
nb_centers_state = {
		 "01": 7,
		 "06": 53,
		 "12": 27,
		 "17": 18,
		 "36": 27,
		 "39": 16,
		 "48": 36,
}

for state in states_code:
    print("Working on "+state)
    cmd1 = "./do_redistrict "+str(nb_centers_state[state])+" data/pophu"+state
    cmd2 = "python3 Voronoi_boundaries.py c_output_"+state+" vor_output_"+state
    cmd3 = "python3 plotGNUPlot.py vor_output_"+state+" data/boundary_"+state+" gnuplot_"+state
    # print(cmd1.split())
    f = open("c_output_"+state, "w")
    process = subprocess.Popen(cmd1.split(), stdout=f)
    output, error = process.communicate()
    f.close()
    # exit(0)
    process = subprocess.Popen(cmd2.split()) 
    output, error = process.communicate()
    process = subprocess.Popen(cmd3.split()) 
    output, error = process.communicate()
    print("Done with "+state)
