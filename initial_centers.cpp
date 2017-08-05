#include <cstdlib>
#include <algorithm>
#include <limits>
#include "initial_centers.hpp"
#include "rand_float.hpp"

using namespace std;

vector<Point> choose_initial_centers(const vector<Point> &clients, int num_centers){
  vector<int> rand_values(clients.size());
  generate(rand_values.begin(), rand_values.end(), rand);
  vector<Point> centers;
  centers[0] = clients[max_element(rand_values.begin(),rand_values.end()) - rand_values.begin()];
  vector<double> distances_sq(clients.size(), numeric_limits<double>::infinity());
  for (int j = 1; j < centers.size(); ++j){
    double sum_of_distances_sq = 0;
    for (int i = 1; i < clients.size(); ++i) {
      distances_sq[i] = min(distances_sq[i], centers[j-1].dist_sq(clients[i]));
      sum_of_distances_sq += distances_sq[i];
    }
    double choice = rand_float(0, sum_of_distances_sq);
    for (int i = 1; i < clients.size(); ++i) {
      choice -= distances_sq[i];
      if (choice <= 0){
	centers[j] = clients[j];
	break;
      }
    }
  }
  return centers;
}
