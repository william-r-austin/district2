#include <numeric>
#include <limits>
#include <tuple>
#include "initial_centers.hpp"
#include "mincostflow.hpp"
#include "redistrict.hpp"
#include "find_weights.hpp"
/* 
 Assign initial center locations.
 Repeat: 
    Compute client-to-center distances
    Assign clients to centers
*/

using namespace std;

tuple<vector<Point>, vector<int>, vector<double> > choose_centers(const vector<Point> &clients, long * populations, int num_centers){
  long population = accumulate(populations, populations+clients.size(), 0);
  double population_per_center = population/num_centers;
  long * costs = (long *) calloc(clients.size() * num_centers, sizeof(long));
  vector<double> distances_sq(clients.size()*num_centers, numeric_limits<double>::infinity());
  double max_dist_sq = 0;
  vector<int> assignment(clients.size());
  vector<int> old_assignment(clients.size());
  vector<Point> centers;
  bool different;
  for (int tries = 0; tries < 100; ++tries){
    different = false;
  centers = choose_initial_centers(clients, populations, num_centers);
  vector<Point> new_centers(num_centers);
  int iter_count = 0;
  do {//iterate until stable
    for (int i = 0; i < clients.size(); ++i){
      //find distances to centers
      double dist_sq = numeric_limits<double>::infinity();
      for (int j = 0; j < centers.size(); ++j){
	dist_sq = centers[j].dist_sq(clients[i]);
	distances_sq[i*num_centers+j] = dist_sq;
	max_dist_sq = max(max_dist_sq, dist_sq);
      }
    }
    //convert doubles to ints
    double scale = (double) LONG_MAX / max_dist_sq/ (clients.size()*num_centers)/100;
    for (int i = 0; i < clients.size(); ++i){
      for (int j = 0; j < centers.size(); ++j){
	costs[i*num_centers+j] = (long) (scale * distances_sq[i*num_centers+j]);
      }
    }
    //find assignment of clients to centers
    find_assignment(costs, populations, clients.size(), num_centers, assignment);
    different = assignment != old_assignment;
    old_assignment = assignment;
    //move centers to centroids
    //first initialize accumulators to the zero point
    fill(new_centers.begin(), new_centers.end(), Point(0.,0.));
    for (int i = 0; i < clients.size(); ++i){
      new_centers[assignment[i]] = new_centers[assignment[i]].add(clients[i].scale(populations[i]));
    }
    for (int j = 0; j < num_centers; ++j){
      Point new_center = new_centers[j].scale(1./population_per_center);
      centers[j] = new_center;
    }
  }
  while (different and ++iter_count < 50);
  vector<double> weights = find_weights(clients, centers, assignment);
  if (weights.size() > 0){
    return make_tuple(centers, assignment, weights);
  }
  }
  centers.clear();
  vector<double> weights;
  return make_tuple(centers, assignment, weights);
}
  
