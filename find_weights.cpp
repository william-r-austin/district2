#include <limits>
#include <cassert>
#include "find_weights.hpp"

using namespace std;

vector<double> find_weights(const vector<Point> & clients, const vector<Point> & centers, const vector<int> & assignment){
  /* Derive shortest-path inequalities, one for each client/center pair, 
     and use Bellman-Ford to find a solution.
     Let i be a client.  Let k be the center to which i is assigned, and let j be another center.
     There is an inequality x_k <= x_j + b.  These define arcs jk on which we can run Bellman-Ford.
     Namely, x_k + dist_sq(clients[i],centers[assignment[i]]) <= x_j + distance(clients[i],centers[k]).
  */
  //First find arc lengths
  //length of arc from j to k is lengths[j*num_centers+k]
  vector<double> lengths(centers.size()*centers.size(), numeric_limits<double>::infinity());
  for (int i = 0; i < clients.size(); ++i){
    double client_to_assigned_center_dist_sq = centers[assignment[i]].dist_sq(clients[i]);
    for (int j = 0; j < centers.size(); ++j){
      if (j != assignment[i]){
        double b = centers[j].dist_sq(clients[i]) - client_to_assigned_center_dist_sq;
        if (b < lengths[j*centers.size()+assignment[i]]){
          lengths[j*centers.size()+assignment[i]] = b;
        }
      }
    }
  }
  //Next compute distances from center 0 (arbitrarily chosen)
  vector<double> weights(centers.size(), numeric_limits<double>::infinity());
  weights[0] = 0.;
  int y = centers.size(); //upper bound on number of iterations
  bool different = true;
  do {
    different = false;
    for (int j = 0; j < centers.size(); ++j){
      for (int k = 0; k < centers.size(); ++k){
        if (j != k){
          //relax arc jk
          double new_dist = weights[j] + lengths[j*centers.size()+k];
          if (new_dist < weights[k]){
            weights[k] = new_dist;
            different = true;
          }
        }
      }
    }
    y -= 1;
    assert(y >= 0);
  } while (different);
  return weights;
}


         
