# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

sf = shapefile.Reader("tl_2018_us_cd116/tl_2018_us_cd116.shp")

print("Length = ", len(sf))
print("Type = ", sf.shapeType)
print(sf.fields)

for current in sf.iterShapeRecords():
	currentRecord = current.record
	stateCode = currentRecord['STATEFP']
	if stateCode == "51":
		print("STATEFP = " + str(stateCode))
		print("CD116FP = " + str(currentRecord['CD116FP']))
		print("NAMELSAD = " + str(currentRecord['NAMELSAD']))
		print("LSAD = " + str(currentRecord['LSAD']))
		print("GEOID = " + str(currentRecord['GEOID']))
				
		currentShape = current.shape
		print("Num points = " + str(len(currentShape.points)))
		currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points])
		polyArea = currentPoly.area
		polyPerimeter = currentPoly.length
		print("Area = " + str(polyArea))
		print("Length = " + str(polyPerimeter))
		ppScore = (4 * math.pi * polyArea) / (polyPerimeter * polyPerimeter)
		print("Polsby-Popper Score = " + str(ppScore))
		equalPerimeterArea = (polyPerimeter * polyPerimeter) / (4 * math.pi)
		ipqScore = polyArea / equalPerimeterArea
		print("Isoperimetric Quotient Score = " + str(ipqScore))

#print(allRecords[0])

#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

#outputFile = open("censusBlocks.txt", "w")


