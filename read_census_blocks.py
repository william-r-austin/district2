import shapefile
from shapely.geometry import shape

'''Provides a procedure to read a shape file specifying census blocks,
   and write a file giving the clients.  For each census block, the client
   is located at the centroid of the block shape, and its weight is the
   population of the census block.
   Each line of the output consists of:
      the x coordinate,
      the y coordinate, and
      the population.
   Only census blocks with positive population are represented in the output.
'''


def write_client_file(input_filename, output_filename):
    sf = shapefile.Reader(input_filename)
    of = open(output_filename, 'w')
    for shape_rec in sf.iterShapeRecords():
        print("rec 0 = ", shape_rec.record[0])
        print("rec 1 = ", shape_rec.record[1])
        print("rec 2 = ", shape_rec.record[2])
        print("rec 3 = ", shape_rec.record[3])
        print("rec 4 = ", shape_rec.record[4])
        print("rec 5 = ", shape_rec.record[5])
        print("rec 6 = ", shape_rec.record[6])
        pop = shape_rec.record[7]
        if pop > 0:
            cent = shape(shape_rec.shape).centroid
            of.write(str(cent.x)+" "+str(cent.y)+" "+str(pop)+"\n")


import sys
write_client_file(sys.argv[1],sys.argv[2])
