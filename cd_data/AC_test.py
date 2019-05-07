from AC_grid_tools import get_base_fn,get_alpha_carbon_cif, file_to_grid
import glob
"""
test that get AC works for all of the protein files
"""

cif_files = glob.glob("PDB/*.cif")
out = open("get_alpha_works.csv","w")
out.write("file,n_ac\n")
for cf in cif_files:
    result = 0
    try:
        acs = get_alpha_carbon_cif(cf)
        result = len(acs)
    except:
        result = "ERROR"
    out.write(f"{get_base_fn(cf)},{result}\n")
out.close()
