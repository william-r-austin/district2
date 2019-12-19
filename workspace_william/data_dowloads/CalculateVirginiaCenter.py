# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

sf = shapefile.Reader("cb_2016_us_state_500k/cb_2016_us_state_500k.shp")

print("Length = ", len(sf))
print("Type = ", sf.shapeType)
print(sf.fields)

for current in sf.iterShapeRecords():
	currentRecord = current.record
	stateName = currentRecord['NAME']
	if stateName == "Virginia":
		currentShape = current.shape
		shapePartIndices = currentShape.parts
		numParts = len(shapePartIndices)
		shapePoints = currentShape.points
		numPoints = len(shapePoints)
		print("parts array = " + str(shapePartIndices))
		totalArea = 0
		combinedScore = 0
		totalConvexHullArea = 0
		total_x = 0
		total_y = 0
		
		for i in range(numParts):
			start = shapePartIndices[i]
			end = numPoints
			if i < numParts - 1:
				end = shapePartIndices[i + 1]
			
			print("i = " + str(i))
			print("Num points = " + str(end - start))
			currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points[start:end]])
			polyArea = currentPoly.area
			polyCenter = currentPoly.centroid
			print("Area = " + str(polyArea))
			print("X = " + str(polyCenter.x))
			print("Y = " + str(polyCenter.y))
			
			totalArea += polyArea
			total_x += (polyArea * polyCenter.x)
			total_y += (polyArea * polyCenter.y)

		final_x = total_x / totalArea
		final_y = total_y / totalArea
		
		print("Virginia Centroid = (" + str(final_x) + ", " + str(final_y) + ")")
#print(allRecords[0])

#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

#outputFile = open("censusBlocks.txt", "w")


