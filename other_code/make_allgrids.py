from AC_grid_tools import file_to_tfin
import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

radius = 13
with open('dif_cd_refined.csv','r') as dim:
    readdim = dim.readlines()
    allgrids = []
    for line in tqdm(readdim[1:]):
        line = line.split(',')
        name = line[0]
        allgrids += file_to_tfin(name,float(line[5].strip('\n')),radius)

print(len(allgrids))

print("reading AA properties...")
AA_data = pd.read_excel("AA_properties.xlsx")
charge = dict(zip(AA_data.AA, AA_data.charge))

print("making feature array...")
for d in tqdm(allgrids):
    d.append(np.array([charge[a] for a in d[2]]))

print("writing data")
pickle.dump(all_grids,open(f'allgrids_AA_charge{radius}.p','wb'))
