from AC_grid_tools import file_to_grid,get_alpha_carbon_cif,file_to_tfin

test_AClist = get_alpha_carbon_cif("PDB\\121p.cif")

for a in test_AClist:
	print(a)
	
subgrids = file_to_tfin("PDB\\121p.cif", 3, 5)

for s in subgrids:
	print(s)