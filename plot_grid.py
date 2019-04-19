import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from get_alpha_carbon import file_to_grid

def xy_heatmap(filename, dim):
	print("making grid...")
	xyz_grid = file_to_grid(filename, dim)
	xy_grid = []
	for x in xyz_grid:
		y_density = []
		for y in x:
			y_density.append([len(z) for z in y])
		xy_grid.append([sum(yz) for yz in y_density])

	#print(xy_grid)
	ax = sns.heatmap(xy_grid)
	plt.title(filename)
	plt.show()
	
xy_heatmap("PDB/1fnt.cif",2.4)