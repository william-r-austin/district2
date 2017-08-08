#include "find_weights.hpp"

using namespace std;

int main(){
  vector<Point> clients = {Point(-0.999984,-0.736924), Point(0.511211,-0.0826997), Point(0.0655345,-0.562082), Point(-0.905911,0.357729), Point(0.358593,0.869386), Point(-0.232996,0.0388327), Point(0.661931,-0.930856), Point(-0.893077,0.0594004), Point(0.342299,-0.984604), Point(-0.233169,-0.866316), Point(-0.165028,0.373545), Point(0.177953,0.860873), Point(0.692334,0.0538576), Point(-0.81607,0.307838), Point(-0.168001,0.402381), Point(0.820642,0.524396), Point(-0.475094,-0.905071), Point(0.472164,-0.343532), Point(0.265277,0.512821), Point(0.982075,-0.269323)};
  vector<Point> centers = {Point(0.614617,-0.632078), Point(0.572366,0.252094), Point(-0.410678,-0.767598), Point(-0.712013,0.19095), Point(0.0508792,0.626546)};
  vector<int> assignment = {2, 1, 2, 3, 4, 3, 0, 3, 0, 2, 4, 4, 1, 3, 4, 1, 2, 0, 1, 0};
  vector<double> weights = find_weights(clients, centers, assignment);
}
