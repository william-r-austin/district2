#include <iostream>
#include <vector>
#include "initial_centers.hpp"

using namespace std;

int main(){
  const int num_clients = 10;
  vector<Point> clients(10);
  generate(clients.begin(), clients.end(), rand_point);
  long * populations = (long *) calloc(num_clients, sizeof(long));
  for (auto client: clients){
    cout << client << "\n";
  }
  vector<Point> centers = choose_initial_centers(clients, populations, 4);
  for (int i = 0; i < centers.size(); ++i){
    cout << "center " << i << " is " << centers[i] << "\n";
  }
}
