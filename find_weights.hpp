#pragma once

#include <vector>
#include "point.hpp"

std::vector<double> find_weights(const std::vector<Point> & clients, const std::vector<Point> & centers, const std::vector<int> & assignment);
