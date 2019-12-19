# Polsby Popper
import shapefile
#import shapely
from shapely import geometry

sf = shapefile.Reader("tl_2018_us_cd116/tl_2018_us_cd116.shp")
print("Length = ", len(sf))
print("Type = ", sf.shapeType)
print(sf.fields)

allShapeRecords = sf.shapeRecords()
print("allShapeRecords type = " + str(type(allShapeRecords)))

shapeRecord = allShapeRecords[0]
print("shapeRecord type = " + str(type(shapeRecord)))

features = shapeRecord.record
print("features type = " + str(type(features)))

for feature in features:
	print("feature type = " + str(type(feature)))
	print(feature)

print("bbox = ")
print(sf.bbox)

allShapes = sf.shapes()
print("allShapesLength = " + str(len(allShapes)))

firstShape = allShapes[0]
print("shape 0 bbox")
print(firstShape.bbox)

print("shape 0 parts")
print(firstShape.parts)

print("shape 0 points")
print(len(firstShape.points))

print(firstShape.points[0])

poly = geometry.Polygon([[pt[0], pt[1]] for pt in firstShape.points])

print("Area = " + str(poly.area))
print("Length = " + str(poly.length))







#print(allRecords[0])
#print(len(allRecords[0]))

#record = allRecords[0].record
#print(record['POPCOUNT'])

#outputFile = open("censusBlocks.txt", "w")


