from AC_grid_tools import get_alpha_carbon_cif, draw_grid, grid_info
import glob
from tqdm import tqdm
import time
"""
Test draw grid over all of the input files, get a maximum cube dimension (cd) for each file
some times couses crash...work in progress
"""
cifs = glob.glob("PDB/*.cif")
max_rt = 120

out = open("cd_data/all_cif_cd.csv", "w")
out.write("file,n_AC,n_AC_inGrid,n_cubes,max_cd\n")
for c in tqdm(cifs):
	result = ""
	timeout = time.time() + max_rt
	acs = get_alpha_carbon_cif(c)
	for i in range(37,0,-1):
		cd = i/10
		grid = draw_grid(acs,cd)
		n_cubes, max_aa, n_ac_inGrid = grid_info(grid)
		if max_aa == 1:
			result = f"{len(acs)},{n_ac_inGrid},{n_cubes},{cd}"
			break
		if time.time() > timeout:
			result = f"{len(acs)},{n_ac_inGrid},{n_cubes},RUNTIME {max_rt}s+"
			break

	out.write(f"{c},{result}\n")
out.close()
