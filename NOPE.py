from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
from tensorflow import keras

import sys
import pickle
from AC_grid_tools import file_to_tfin, get_base_fn
import pandas as pd
import numpy as np

"""
Run charge 13 model on each amino acid in a protein. This is a protype of a
prediction tool that could be built with this model

input is file name of cif file in pdb format, can only be run with known
proteins for now.
"""


pdb_name = sys.argv[1]
cd_dict = pickle.load(open("cd_data/cd_dict.p","rb"))

cd = cd_dict[pdb_name]
my_data = file_to_tfin(pdb_name, cd, 13)
print(f"{pdb_name}, cd: {cd} AAs:{len(my_data)}")

print("reading AA properties...")
AA_data = pd.read_excel("AA_properties.xlsx")
charge = dict(zip(AA_data.AA, AA_data.charge))
for d in my_data:
    d[2] = (np.array([charge[a] for a in d[2]]))

nope = keras.models.load_model('models/NOPE_charge13_100n.h5')
my_data_charge = np.asarray([d[2] for d in my_data])
print(my_data_charge[0].shape)
pred = nope.predict(my_data_charge)
AA_n = [d[0] for d in my_data]
epitope = [d[-1] for d in my_data]
pred = [np.argmax(p) for p in pred]
output = pd.DataFrame()
output['Amino No.'] = AA_n
output['Epitope Anno.'] = epitope
output['NOPE pred.'] = pred

fn = "NOPE_results\\" + get_base_fn(pdb_name) + "_NOPE.csv"
output.to_csv(fn)
print(f"\nDONE, results writen to: {fn}")
