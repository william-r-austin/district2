# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

sf = shapefile.Reader("tl_2016_51_sldu/tl_2016_51_sldu.shp")

print("Length = ", len(sf))
print("Type = ", sf.shapeType)
print(sf.fields)

for current in sf.iterShapeRecords():
	currentRecord = current.record
	proposedName = currentRecord['NAMELSAD']
	print("NAMELSAD = " + proposedName)
			
	currentShape = current.shape
	shapePartIndices = currentShape.parts
	numParts = len(shapePartIndices)
	shapePoints = currentShape.points
	numPoints = len(shapePoints)
	print("parts array = " + str(shapePartIndices))
	totalArea = 0
	combinedScore = 0
	totalConvexHullArea = 0
	
	for i in range(numParts):
		start = shapePartIndices[i]
		end = numPoints
		if i < numParts - 1:
			end = shapePartIndices[i + 1]
		
		print("i = " + str(i))
		print("Num points = " + str(end - start))
		currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points[start:end]])
		polyArea = currentPoly.area
		polyPerimeter = currentPoly.length
		print("Area = " + str(polyArea))
		print("Length = " + str(polyPerimeter))
		ppScore = (4 * math.pi * polyArea) / (polyPerimeter * polyPerimeter)
		
		convexHullPoly = currentPoly.convex_hull
		convexHullArea = convexHullPoly.area
		
		totalConvexHullArea += convexHullArea
		
		combinedScore += (ppScore * polyArea)
		totalArea += polyArea
	
	finalScore = combinedScore / totalArea
	print("Polsby-Popper Score for " + proposedName + " = " + str(finalScore))
	
	finalScore2 = totalArea / totalConvexHullArea
	print("Ration to convex hull area = " + str(finalScore2))
	#equalPerimeterArea = (polyPerimeter * polyPerimeter) / (4 * math.pi)
	#ipqScore = polyArea / equalPerimeterArea
	#print("Isoperimetric Quotient Score = " + str(ipqScore))

#print(allRecords[0])

#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

#outputFile = open("censusBlocks.txt", "w")


