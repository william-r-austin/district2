#include <iostream>
#include "mincostflow.hpp"

using namespace std;

int main(){
  int num_clients = 6;
  int num_centers = 2;
  long * costs = (long *) calloc(num_clients * num_centers, sizeof(long));
  for (int i = 0; i < num_clients; ++ i){
    costs[i*num_centers+0] = 1;
    costs[i*num_centers+1] = 3;
  }
  long * populations = (long *) calloc(num_clients, sizeof(long));
  for (int i = 0; i < num_clients; ++i){
    populations[i] = 1;
  }
  Assignment assignment(num_clients);
  vector<double> weights(num_centers);
  find_assignment(costs, populations, num_clients, num_centers, assignment, weights);
  for (int j = 0; j < num_centers; ++j){
    cout << "center " << j << " has weight " << weights[j] << "\n";
  }
  for (int i = 0; i < num_clients; ++i){
    cout << "client " << i;
    for (auto ae : assignment[i]){
      cout << " assigned to center " << ae.center << " with flow " << ae.flow;
    }
    cout << "\n";
    for (int j = 0; j < num_centers; ++j){
      cout << " weighted distance to center " << j << " is " << costs[i*num_centers+j] + weights[j] << "\n";
    }
    cout << "\n";
  }
}
