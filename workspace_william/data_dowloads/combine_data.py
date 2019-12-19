# Comment
import shapefile

sf = shapefile.Reader("CombinedData5/CombinedData5.shp")
print("Length = ", len(sf))
print("Type = ", sf.shapeType)

allShapeRecords = sf.shapeRecords()

#print(allRecords[0])
#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

outputFile = open("censusBlocks.txt", "w")


for currentShape in allShapeRecords:
	currentRecord = currentShape.record
	xCoord = currentRecord['XCOORD']
	yCoord = currentRecord['YCOORD']
	popCount = currentRecord['POPCOUNT']
	if popCount != None and popCount > 1:
		outputFile.write(str(xCoord) + " " + str(yCoord) + " " + str(int(popCount)) + "\n")

outputFile.close()	

print("Test!")
