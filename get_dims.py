from AC_grid_tools import get_alpha_carbon_cif, draw_grid, grid_info
import glob
from tqdm import tqdm
import time
"""
Test draw grid over all of the input files, get a maximum cube dimension (cd) for each file
some times couses crash...work in progress
"""

cifs = glob.glob("PDB/*.cif")
out = open("all_cif_dim.csv", "w")
out.write("file,n_AC,n_AC_inGrid,n_cubes,max_dim\n")
for c in tqdm(cifs[264:]):
	result = ""
	timeout = time.time() + 60
	try:
		acs = get_alpha_carbon_cif(c)
		for i in range(40,0,-1):
			cd = i/10
			grid = draw_grid(acs,cd)
			n_cubes, max_aa, n_ac_inGrid = grid_info(grid)
			if max_aa == 1:
				result = f"{len(acs)},{n_ac_inGrid},{n_cubes},{cd}"
				break
			if time.time() > timeout:
				result = f"{len(acs)},{n_ac_inGrid},{n_cubes},RUNTIME 60s+"
				break

	except:
		result = f"{len(acs)},Error"

	out.write(f"{c},{result}\n")
out.close()
