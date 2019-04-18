from get_alpha_carbon import get_alpha_carbon_cif, draw_grid, grid_info
import glob
from tqdm import tqdm
import time
"""
Test draw grid over all of the input files, get a maximum cube dimension for each file
"""

cifs = glob.glob("PDB/*.cif")
dims = []
out = open("all_cif_dim.csv", "w")
out.write("file,n_AC,n_AC_inGrid,n_cubes,max_dim\n")
for c in tqdm(cifs):
	result = ""
	timeout = time.time() + 60
	try:
		acs = get_alpha_carbon_cif(c)
		for i in range(40,0,-1):
			dim = i/10	
			actin_grid = draw_grid(acs,dim)
			n_cubes, max_aa, n_ac_inGrid = grid_info(actin_grid)
			if max_aa == 1:
				dims.append(dim)
				result = f"{len(acs)},{n_ac_inGrid},{n_cubes},{dim}"
				break
			if time.time() > timeout:
				result = f"{len(acs)},{n_ac_inGrid},{n_cubes},RUNTIME 60s+"
				break
		
	except:
		result = f"{len(acs)},Error"

	out.write(f"{c},{result}\n")

print(f"max dim = {max(dims)} min dim = {min(dims)}")
out.close()