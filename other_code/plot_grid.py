import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

def xy_heatmap(grid):
	"""plot a heatmap of the xy dimesion"""
	xy_grid = []
	for x in grid:
		y_density = []
		for y in x:
			y_density.append([len(z) for z in y])
		xy_grid.append([sum(yz) for yz in y_density])

	#print(xy_grid)
	ax = sns.heatmap(xy_grid)
	plt.show()
	
def xy_heatmap2(grid):
	"""plot a heatmap of the xy dimesion"""
	xy_grid = []
	for x in grid:
		y_density = []
		for y in x:
			y_density.append([1 for z in y if z != '-'])
		xy_grid.append([sum(yz) for yz in y_density])

	#print(xy_grid)
	ax = sns.heatmap(xy_grid)
	plt.show()
	