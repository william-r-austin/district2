#include "redistrict.hpp"
#include "rand_point.hpp"
#include "find_weights.hpp"

#include <algorithm>    // std::generate
using namespace std;

void print_out(int num_centers, int num_clients,
               const vector<Point> centers, const vector<double> &weights, const vector<Point> &clients,
	      const vector<int> &assignment){
    cout << num_centers << " " << num_clients << endl;
    for(int j = 0; j < num_centers; j++){
      cout << centers[j].x << " " << centers[j].y << " " << weights[j] << endl;
    }
    for(int i = 0; i < num_clients; i++){
	cout << clients[i].x << " " << clients[i].y
	     << " "<< assignment[i] << endl;
    }
}


int main(){
  int num_clients = 20;
  int num_centers = 5;
  vector<Point> clients(num_clients);
  generate(clients.begin(), clients.end(), rand_point);
  long * populations = (long *) calloc(num_clients, sizeof(long));
  fill(populations, populations+num_clients, 1);
  pair<vector<Point>, vector<int> > p = choose_centers(clients, populations, num_centers);
  vector<Point> centers = p.first;
  vector<int> assignment = p.second;
  vector<double> weights = find_weights(clients, centers, assignment);
  print_out(num_centers, num_clients, centers, weights, clients, assignment);
}
