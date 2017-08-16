#pragma once

#include <vector>
#include "point.hpp"
#include "assignment.hpp"

std::vector<double> find_weights(const std::vector<Point> & clients, const std::vector<Point> & centers, const Assignment & assignment);
