# Polsby Popper
import shapefile
#import shapely
from shapely import geometry
import math

sf = shapefile.Reader("MyGeneratedShapefiles/VoronoiMap40v1.shp")

#print("Length = ", len(sf))
#print("Type = ", sf.shapeType)
#print(sf.fields)


districtMap = dict()
districtBounds = dict()


for current in sf.iterShapeRecords():
	currentRecord = current.record
	proposedName = "District " + str(currentRecord['N40DNUM'])
	#print("DNAME = " + proposedName)
			
	currentShape = current.shape
	shapePartIndices = currentShape.parts
	numParts = len(shapePartIndices)
	shapePoints = currentShape.points
	numPoints = len(shapePoints)
	#print("parts array = " + str(shapePartIndices))
	districtParts = []
	
	for i in range(numParts):
		start = shapePartIndices[i]
		end = numPoints
		if i < numParts - 1:
			end = shapePartIndices[i + 1]
		
		#print("i = " + str(i))
		#print("Num points = " + str(end - start))
		currentPoly = geometry.Polygon([[pt[0], pt[1]] for pt in currentShape.points[start:end]])
		districtParts.append(currentPoly)
		
		currentPolyBounds = list(currentPoly.bounds)
		if proposedName in districtBounds:
			existingBounds = districtBounds[proposedName]
			newBounds = [min(existingBounds[0], currentPolyBounds[0]), 
			             min(existingBounds[1], currentPolyBounds[1]),
						 max(existingBounds[2], currentPolyBounds[2]), 
						 max(existingBounds[3], currentPolyBounds[3])]
			districtBounds[proposedName] = newBounds
		else:
			districtBounds[proposedName] = currentPolyBounds
	
	districtMap[proposedName] = districtParts

for key in districtMap:
	print("District = " + key + ", polygon size = " + str(len(districtMap[key])))
	print("Bounds = " + str(districtBounds[key]))

sf.close()


def overlaps(b1, b2):
	return (b1[0] <= b2[2] and b2[0] <= b1[2] and b1[1] <= b2[3] and b2[1] <= b1[3])

# Part 2 - Iterate over all census blocks
sf2 = shapefile.Reader("CombinedData7/CombinedData7.shp")
outFile = open("district_assignments_40.csv", "w")
outFile.write("AFFGEOID,DNAME11\n")

censusBlockNumber = 0

for censusBlock in sf2.iterShapeRecords():
	censusBlockRecord = censusBlock.record
	censusBlockGeoid = censusBlockRecord['AFFGEOID']
	
	censusBlockShape = censusBlock.shape
	shapePartIndices = censusBlockShape.parts
	numParts = len(shapePartIndices)
	shapePoints = censusBlockShape.points
	numPoints = len(shapePoints)
	censusBlockPolyList = []
	censusBlockBounds = None
	districtsToCheck = []
	
	for i in range(numParts):
		start = shapePartIndices[i]
		end = numPoints
		if i < numParts - 1:
			end = shapePartIndices[i + 1]
		
		#print("i = " + str(i))
		#print("Num points = " + str(end - start))
		censusBlockPoly = geometry.Polygon([[pt[0], pt[1]] for pt in censusBlockShape.points[start:end]])
		censusBlockPolyList.append(censusBlockPoly)
		
		censusBlockPolyBounds = list(censusBlockPoly.bounds)
		if censusBlockBounds is None:
			censusBlockBounds = censusBlockPolyBounds
		else:
			censusBlockBounds[0] = min(censusBlockBounds[0], censusBlockPolyBounds[0])
			censusBlockBounds[1] = min(censusBlockBounds[1], censusBlockPolyBounds[1])
			censusBlockBounds[2] = max(censusBlockBounds[2], censusBlockPolyBounds[2])
			censusBlockBounds[3] = max(censusBlockBounds[3], censusBlockPolyBounds[3])
	
	for dName, dBounds in districtBounds.items():
		checkNeeded = overlaps(censusBlockBounds, dBounds)
		if checkNeeded:
			districtsToCheck.append(dName)
	
	numDistrictsToCheck = len(districtsToCheck)
	assignedDistrict = None
	if numDistrictsToCheck == 0:
		print("ERROR: Census Block " + str(censusBlockNumber) + " did not overlap any districts!!")
		print("Bounds for census block are: " + str(censusBlockBounds))
	elif numDistrictsToCheck == 1:
		assignedDistrict = districtsToCheck[0]
	else:
		assignedDistrict = None
		assignedDistrictArea = 0.0
				
		for checkDistrictName in districtsToCheck:
			totalDistrictArea = 0.0

			for dPoly in districtMap[checkDistrictName]:
				for cbPoly in censusBlockPolyList:
					totalDistrictArea += dPoly.intersection(cbPoly).area
			
			if assignedDistrict is None or totalDistrictArea > assignedDistrictArea:
				assignedDistrict = checkDistrictName
				assignedDistrictArea = totalDistrictArea
	
	if assignedDistrict is not None:
		finalAssigassignedDistrict = assignedDistrict.split()[1]
		outFile.write(censusBlockGeoid + ", " + finalAssigassignedDistrict + "\n")
	
	censusBlockNumber += 1
	
sf2.close()
outFile.close()