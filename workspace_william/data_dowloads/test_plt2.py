import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import shapely.geometry
import shapely.ops

points = np.random.random((10, 2))
vor = Voronoi(points)
voronoi_plot_2d(vor)