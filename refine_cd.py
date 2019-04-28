from AC_grid_tools import get_alpha_carbon_cif, draw_grid, grid_info
from tqdm import tqdm
import time
import pandas as pd
"""
refine max cd to the hundreds place to minimize number of cubes and empty cubes
"""
data = pd.read_csv("done_cif_cd.csv")
max_rt = 120
refined_cds =[]
for index,row in data.iterrows():
	print(f"{index}	{row['file']} {row['max_cd']} {row['n_cubes']}")
	acs = get_alpha_carbon_cif(row['file'])
	cdr = int((row['max_cd']*100)+1)
	refined_cd = row['max_cd']
	for i in range(cdr,cdr+10,1):
		timeout = time.time() + max_rt
		cd = i/100
		grid = draw_grid(acs,cd)
		n_cubes, max_aa, n_ac_inGrid = grid_info(grid)
		if max_aa > 1:
			break
		elif time.time() > timeout:
			break
		else:
			refined_cd = cd
			# refine_n_cube = refined_n_cubes
	refined_cds.append(refined_cd)
	# refined_n_cubes.append(refined_n_cubes)
print("Compling data")

data['refined_cd'] = refined_cds
print(data)
# data['refined_n_cubes'] = refined_n_cubes
print("writing to file")
data.to_csv("dif_cd_refined.csv", index = False)
print("Done")
