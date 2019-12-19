# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math


def getDistance(x1, y1, x2, y2):
	xDelta = x1 - x2
	yDelta = y1 - y2
	myDistSquared = (xDelta * xDelta) + (yDelta * yDelta) 
	return math.sqrt(myDistSquared)

sf0 = shapefile.Reader("FinalOutput/VA_Congress_2.shp")

centerMap = {}
totalDist = {}
totalPop = {}
areaWeightedDistance = {}
districtArea = {}

for x in sf0.iterShapeRecords():
	r = x.record
	dName = "District " + str(r['DNUM'])
	xcoord = r['XCOORD']
	ycoord = r['YCOORD']
	myList = [xcoord, ycoord]
	centerMap[dName] = myList
	totalDist[dName] = 0.0
	totalPop[dName] = 0
	areaWeightedDistance[dName] = 0.0
	districtArea[dName] = 0
	

sf0.close()

sf = shapefile.Reader("CombinedData7/CombinedData7.shp")

#print("Length = ", len(sf))
#print("Type = ", sf.shapeType)
#print(sf.fields)

for current in sf.iterShapeRecords():
	currentRecord = current.record
	districtName = "District " + str(currentRecord['OLDDNUM'])
	#print("NAMELSAD = " + districtName)
	currentShape = current.shape
	shapePartIndices = currentShape.parts
	numParts = len(shapePartIndices)
	shapePoints = currentShape.points
	numPoints = len(shapePoints)
	#print("parts array = " + str(shapePartIndices))
	totalArea = 0
	
	cbx = currentRecord['XCOORD']
	cby = currentRecord['YCOORD']
	cbpop = currentRecord['POPCOUNT']
	if cbpop is None:
		cbpop = 0
	
	other = centerMap[districtName]
	
	
	for i in range(numParts):
		start = shapePartIndices[i]
		end = numPoints
		if i < numParts - 1:
			end = shapePartIndices[i + 1]
		
		#print("i = " + str(i))
		#print("Num points = " + str(end - start))
		currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points[start:end]])
		polyArea = currentPoly.area
		totalArea += polyArea
	
	if other is not None:
		distance = getDistance(cbx, cby, other[0], other[1])
				
		# Weighted Computation		
		currentTotalDist = totalDist[districtName]
		currentTotalPop = totalPop[districtName]
		
		totalDist[districtName] = currentTotalDist + (distance * cbpop)
		totalPop[districtName] = currentTotalPop + cbpop
		
		# Area Weighted Computation
		currentAreaWeightedDist = areaWeightedDistance[districtName]
		areaWeightedDistance[districtName] = currentAreaWeightedDist + (totalArea * distance)
		
		currentDistrictArea = districtArea[districtName]
		districtArea[districtName] = currentDistrictArea + totalArea

final1 = 0.0
final2 = 0.0

for districtKey, aggregateDistance in totalDist.items():
	finalValue = aggregateDistance / totalPop[districtKey]
	final1 += finalValue
	print("Average population weighted distance for " + districtKey + " = " + str(finalValue))
	
	finalAreaWeighted = areaWeightedDistance[districtKey] / districtArea[districtKey]
	final2 += finalAreaWeighted
	print("Average area weighted distance for " + districtKey + " = " + str(finalAreaWeighted))

print()
print("Average across districts for population weighted = " + str(final1 / 11))
print("Average across districts for area weighted = " + str(final2 / 11))

sf.close()


