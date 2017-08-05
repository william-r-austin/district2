#include "point.hpp"

Point rand_point(){
  return Point(rand_float(-1,1), rand_float(-1,1));
}

std::ostream &operator<<(std::ostream & output, const Point &p){
  output << "(" << p.x << ", " << p.y << ")";
  return output;
}
