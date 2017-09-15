#pragma once

#include "assignment.hpp"
#include "point.hpp"

bool check_weights(const std::vector<Point> & clients, const std::vector<Point> & centers, const Assignment & assignment, const std::vector<double> & weights);
