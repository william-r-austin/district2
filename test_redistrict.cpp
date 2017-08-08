#include "redistrict.hpp"
#include "rand_point.hpp"

#include <algorithm>    // std::generate
using namespace std;

void print_out(int num_centers, int num_clients,
	      vector<Point> centers, vector<Point> clients,
	      vector<int> assignment){
    cout << num_centers << " " << num_clients << endl;
    for(int i = 0; i < num_centers; i++){
	cout << centers[i].x << " " << centers[i].y << endl;
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
  // vector<Point> centers 
  print_out(num_centers, num_clients, centers, clients, assignment);
}
