# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

sf = shapefile.Reader("FinalOutput/New_VA_Congress_3.shp")

print("Length = ", len(sf))
print("Type = ", sf.shapeType)
print(sf.fields)

for current in sf.iterShapeRecords():
	currentRecord = current.record
	stateCode = currentRecord['STATEFP']
	if stateCode == "51":
		currentShape = current.shape
		dnum = currentRecord['DNAME11']
		#print("Num points = " + str(len(currentShape.points)))
		currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points])
		polyArea = currentPoly.area
		polyPerimeter = currentPoly.length
		#print("Area = " + str(polyArea))
		#print("Length = " + str(polyPerimeter))
		ppScore = (4 * math.pi * polyArea) / (polyPerimeter * polyPerimeter)
		print("Polsby-Popper Score for District " + str(dnum) + " = " + str(ppScore))
		#equalPerimeterArea = (polyPerimeter * polyPerimeter) / (4 * math.pi)
		#ipqScore = polyArea / equalPerimeterArea
		#print("Isoperimetric Quotient Score = " + str(ipqScore))

#print(allRecords[0])

#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

#outputFile = open("censusBlocks.txt", "w")


