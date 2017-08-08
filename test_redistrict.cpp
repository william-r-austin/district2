#include "redistrict.hpp"
#include "rand_point.hpp"

int main(){
  int num_clients = 100;
  int num_centers = 5;
  vector<Point> clients(num_clients);
  generate(clients.begin(), clients.end(), rand_point);
  long * populations = (long *) calloc(num_clients, sizeof(long));
  fill(populations, populations+num_clients, 1);
  vector<Point> centers = choose_centers(clients, populations, num_centers);
}
