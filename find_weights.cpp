#include <limits>
#include <cassert>
#include <iomanip>      // std::setprecision for debugging

#include "find_weights.hpp"

using namespace std;

vector<double> find_weights(const vector<Point> & clients, const vector<Point> & centers, const Assignment & assignment){
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
    for (AssignmentElement ae : assignment[i]){
      double client_to_assigned_center_dist_sq = centers[ae.center].dist_sq(clients[i]);
      for (int j = 0; j < centers.size(); ++j){
        if (j != ae.center){
          double b = centers[j].dist_sq(clients[i]) - client_to_assigned_center_dist_sq;
          if (b < lengths[j*centers.size()+ae.center]){
            lengths[j*centers.size()+ae.center] = b;
          }
        }
      }
    }
  }
  //Next compute distances from center 0 (arbitrarily chosen)
  vector<double> weights(centers.size(), numeric_limits<double>::infinity());
  vector<int> pred(centers.size(), -1);
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
            pred[k] = j;
            different = true;
          }
        }
      }
    }
    y -= 1;
    if (y < 0){
      for (int k = 0; k < centers.size(); ++k){
      }
      weights.clear();
      return weights;
    }
  } while (different);
  //Finally, make all the weights nonnegative.
  //This involves just subtracting the minimum weight from all the weights
  double min_weight = *(min_element(weights.begin(), weights.end()));
  for (int j = 0; j < weights.size(); ++j) {weights[j] -= min_weight;}
  return weights;
}


         
