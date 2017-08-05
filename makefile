# makefile for cs2
# compileler definitions
# COMP_DUALS to compute prices
# PRINT_ANS to print flow (and prices if COMP_DUAL defined)
# COST_RESTART to be able to restart after a cost function change
# NO_ZERO_CYCLES finds an opeimal flow with no zero-cost cycles
# CHECK_SOLUTION check feasibility/optimality. HIGH OVERHEAD!

# change these to suit your system
CCOMP = g++
#CCOMP = gcc-4
#CFLAGS = -O4 -DNDEBUG
#CFLAGS = -g -DCHECK_SOLUTION -Wall
CFLAGS = -g -Wall -Wc++11-extensions
#CFLAGS = -O4 -DNDEBUG -DNO_ZERO_CYCLES
BIN=cs2

cs2.exe: cs2.c types_cs2.h timer.c
#	$(CCOMP) $(CFLAGS) -o $(BIN) cs2.c -lm
	$(CCOMP) $(CFLAGS) -DPRINT_ANS -DCOMP_DUALS -DCOST_RESTART -o $(BIN) cs2.c -lm

clean:
	rm -f $(BIN) *~

rand_float.o: rand_float.cpp rand_float.hpp
	$(CCOMP) $(CFLAGS) -c rand_float.cpp

point.o: point.cpp point.hpp
	$(CCOMP) $(CFLAGS) -c point.cpp

initial_centers.o: initial_centers.cpp initial_centers.hpp point.hpp rand_float.hpp
	$(CCOMP) $(CFLAGS) -c initial_centers.cpp

test_initial_centers.o: test_initial_centers.cpp initial_centers.hpp point.hpp rand_float.hpp

test_initial_centers: test_initial_centers.o initial_centers.o point.o
	$(CCOMP) $(CFLAGS) test_initial_centers.o initial_centers.o point.o -o test_initial_centers
