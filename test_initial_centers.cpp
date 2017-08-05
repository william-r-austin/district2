#include <iostream>
#include <vector>
#include "initial_centers.hpp"

int main(){
  std::vector<Point> clients(10);
  std::generate(clients.begin(), clients.end(), rand_point);
  for (auto client: clients){
    std::cout << client << "\n";
  }
  std::vector<Point> centers(4);
  choose_initial_centers(centers, clients);
  for (int i = 0; i < centers.size(); ++i){
    std::cout << "center " << i << " is " << centers[i] << "\n";
  }
}
