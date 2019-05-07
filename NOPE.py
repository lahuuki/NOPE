import sys
import pickle
from AC_grid_tools import file_to_tfin
import pandas as pd
import numpy as np

pdb_name = sys.argv[1]
cd_dict = pickle.load(open("cd_data/cd_dict.p","rb"))

cd = cd_dict[pdb_name]
my_data = file_to_tfin(pdb_name, cd, 13)
print(f"{pdb_name}, cd: {cd} AAs:{len(my_data)}")

print("reading AA properties...")
AA_data = pd.read_excel("AA_properties.xlsx")
charge = dict(zip(AA_data.AA, AA_data.charge))
my_data[2] = (np.array([charge[a] for a in my_data[2]]))
