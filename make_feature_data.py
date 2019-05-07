import pickle
import pandas as pd
import numpy as np
from tqdm import tqdm

def make_feat_array(list):
    oi_array = [OI[a] for a in list]
    norm_PI_array = [PI[a] for a in list]
    charge_array = [charge[a] for a in list]
    return np.array([has_aa_array, norm_PI_array, aa_num_array])


print("reading data...")
AA_data = pd.read_excel("AA_properties.xlsx")
charge = dict(zip(AA_data.AA, AA_data.charge))
PI = dict(zip(AA_data.AA, AA_data.norm_PI))
OI = dict(zip(AA_data.AA, AA_data.OI_norm))
all_grids = pickle.load(open("allgrids_AA_9.p","rb"))
print("making feature array...")
for d in tqdm(all_grids):
    d.append(make_feat_array(d[2]))

print("writing data")
pickle.dump(all_grids,open('allgrids_AA_feat.p','wb'))
