#pragma once

#include <vector>
#include "assignment.hpp"

void print_out(const std::vector<Point> centers, const std::vector<double> &weights, const std::vector<Point> &clients,
               const Assignment &assignment);
