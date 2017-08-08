#pragma once
#include <vector>
#include "point.hpp"

using namespace std;

vector<Point> choose_centers(vector<Point> clients, long * populations, int num_centers);
