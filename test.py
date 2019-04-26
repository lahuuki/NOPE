from AC_grid_tools import file_to_grid,get_alpha_carbon_cif,file_to_tfin, subgrid

test_AClist = get_alpha_carbon_cif("PDB\\121p.cif")

my_grid = file_to_grid("PDB\\121p.cif", 3)

subgrid(my_grid)