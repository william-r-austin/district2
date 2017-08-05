#include <iostream>
#include <vector>
#include "initial_centers.hpp"

using namespace std;

int main(){
  vector<Point> clients(10);
  generate(clients.begin(), clients.end(), rand_point);
  for (auto client: clients){
    cout << client << "\n";
  }
  vector<Point> centers = choose_initial_centers(clients, 4);
  for (int i = 0; i < centers.size(); ++i){
    cout << "center " << i << " is " << centers[i] << "\n";
  }
}
