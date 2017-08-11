#pragma once
#include <vector>
#include "point.hpp"
#include <utility>
#include <tuple> // C++11, for std::tie

using namespace std;


// pair<double, double> foo()
// {
//   return std::make_pair(42., 3.14);
// }


pair<vector<Point>, vector<int> > choose_centers(vector<Point> clients, long * populations, int num_centers);