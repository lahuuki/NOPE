import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

print("reading data...")
AA_data = pd.read_excel("AA_properties.xlsx")
charge = dict(zip(AA_data.AA, AA_data.charge))
all_grids = pickle.load(open("allgrids_AA_9.p","rb"))
print("making feature array...")
for d in tqdm(all_grids):
    d.append(np.array([charge[a] for a in d[2]]))

print("writing data")
pickle.dump(all_grids,open('allgrids_AA_charge9.p','wb'))
