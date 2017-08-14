#include "redistrict.hpp"
#include "rand_point.hpp"
#include <iomanip>      // std::setprecision
#include <cmath>

#include <algorithm>    // std::generate
using namespace std;

void print_out(int num_centers, int num_clients,
               const vector<Point> centers, const vector<double> &weights, const vector<Point> &clients,
	      const vector<int> &assignment){
    cout << num_centers << " " << num_clients << endl;
    cout << setprecision(12);
    for(int j = 0; j < num_centers; j++){
      cout << centers[j].x << " " << centers[j].y << " " << sqrt(weights[j]) << endl;
    }
    for(int i = 0; i < num_clients; i++){
	cout << clients[i].x << " " << clients[i].y
	     << " "<< assignment[i] << endl;
    }
}


int main(int argc, char *argv[]){
  int num_clients = 20;
  int num_centers = 5;
  if (argc > 1){
    num_centers = atoi(argv[1]);
    num_clients = atoi(argv[2]);
  }
  vector<Point> clients(num_clients);
  generate(clients.begin(), clients.end(), rand_point);
  long * populations = (long *) calloc(num_clients, sizeof(long));
  fill(populations, populations+num_clients, 1);
  auto [centers, assignment, weights ] = choose_centers(clients, populations, num_centers);
  if (centers.size() == 0){
    cout << "FAILURE TO CONVERGE\n";
    return -1;
  }
  print_out(num_centers, num_clients, centers, weights, clients, assignment);
}
