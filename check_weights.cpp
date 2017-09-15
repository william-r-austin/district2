#include "check_weights.hpp"

using namespace std;

bool check_weights(const vector<Point> & clients, const vector<Point> & centers, const Assignment & assignment, const vector<double> & weights){
  const double tolerance= 1e-9;
  for (int i = 0; i < clients.size(); ++i){
    for (AssignmentElement ae : assignment[i]){
      //cout << " distance to assigned: " << centers[ae.center].dist_sq(clients[i]) << "\n";
      //cout << " weight of assigned: " << weights[ae.center] << "\n";
      double client_to_assigned_center_weighted_dist_sq = centers[ae.center].dist_sq(clients[i]) + weights[ae.center];
      for (int j = 0; j < centers.size(); ++j){
        //cout << "distance to center " << j << " is " << centers[j].dist_sq(clients[i]) << "\n";
	//cout << "weight of center: " <<  weights[j] << "\n";
        if (client_to_assigned_center_weighted_dist_sq > centers[j].dist_sq(clients[i]) + weights[j]+tolerance){
          cerr << "ERROR: client " << i << " closer to center " << j << " than to assigned center " << ae.center << "\n";
          return false;
        }
      }
    }
  }
  return true;
}
        
