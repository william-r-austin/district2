#include <numeric>
#include <limits>
#include "initial_centers.hpp"
#include "mincostflow.hpp"
/* 
 Assign initial center locations.
 Repeat: 
    Compute client-to-center distances
    Assign clients to centers
*/

using namespace std;

#include "redistrict.hpp"

vector<Point> choose_centers(vector<Point> clients, long * populations, int num_centers){
  long population = accumulate(populations, populations+clients.size(), 0);
  double population_per_center = population/num_centers;
  long * costs = (long *) calloc(clients.size() * num_centers, sizeof(long));
  vector<Point> centers = choose_initial_centers(clients, populations, num_centers);
  vector<double> distances_sq(clients.size()*num_centers, numeric_limits<double>::infinity());
  double max_dist_sq = 0;
  vector<int> assignment(clients.size());
  vector<Point> new_centers(num_centers);
  bool different = false;
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
    for (int i = 0; i < clients.size(); ++i){
      for (int j = 0; j < centers.size(); ++j){
	costs[i*num_centers+j] = (long) ((distances_sq[i*num_centers+j]/max_dist_sq) * 10000/*INT_MAX*/)/(num_centers*num_centers);
	//	std::cout << "at client " << i << " and center " << j << ", distance is " << distances_sq[i*num_centers+j] << ", fraction distance is " <<  distances_sq[i*num_centers+j]/max_dist_sq << ", cost is " << costs[i*num_centers+j] << "\n";
      }
    }
    //find assignment of clients to centers
    find_assignment(costs, populations, clients.size(), num_centers, assignment);
    //move centers to centroids
    //first initialize accumulators to the zero point
    fill(new_centers.begin(), new_centers.end(), Point(0.,0.));
    for (int i = 0; i < clients.size(); ++i){
      new_centers[assignment[i]] = new_centers[assignment[i]].add(clients[i].scale(populations[i]));
    }
    different = false;
    for (int j = 0; j < num_centers; ++j){
      Point new_center = new_centers[j].scale(1./population_per_center);
      if (new_center != centers[j]){
	different = true;
      }
      centers[j] = new_center;
    }
    double sum_of_dist_sq = 0.;
    double max_dist_sq_assigned = 0;
    for (int i = 0; i < clients.size(); ++i){
      double d = centers[assignment[i]].dist_sq(clients[i]);
      sum_of_dist_sq += d;
      if (d > max_dist_sq_assigned) max_dist_sq_assigned = d;
    }
    std::cout << "sum of dist sq: " << sum_of_dist_sq << " max: " << max_dist_sq_assigned << "\n";
  }
  while (different);
  return centers;
}
    
      
    
  
