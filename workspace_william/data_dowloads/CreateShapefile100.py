# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

f = open("voronoi_polygons_100.txt")
allLines = f.readlines()
i = 1

w = shapefile.Writer("MyGeneratedShapefiles/vor_100_v1")

w.field('TFIELD', 'C')

for currentLine in allLines:
	points = currentLine.split()
	mainPoly = []
	for point in points:
		vertexStrList = point.split(",")
		vertexList = [float(vertexStrList[i]) for i in range(2)]
		mainPoly.append(vertexList)
	
	w.poly([mainPoly])
	
	w.record(TFIELD=str(i))
	i += 1

f.close()
w.close()
