from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random
import glob

"""
Create a two layer nueral net prediction model for each data set in allgrids_data
"""

with open("model_results.tsv", "w") as result:
    result.write("data\ttest_pos\ttest_neg\tTP\tTN\tFP\tFN\n")
    data_sets = glob.glob("allgrids_data//*.p")
    # print(data_sets)
    for data_fn in data_sets:
        print(f"loading {data_fn}...")
        if '11' in data_fn:
            break
        data = pickle.load(open(data_fn, "rb"))
        data_name = data_fn.split('_')[-1].replace('.p','')
        print(f"{data_name} {len(data)} data points {data[0][2].shape}")
        n_pos = len([d for d in data if d[-1] == 1])
        d = len(data)
        class_weight = {0:1,1:(d-n_pos)/n_pos}
        # print(f"class weights {class_weight}")
        train_n = int(len(data) *.8)
        test_n = len(data) - train_n

        random.shuffle(data)
        train = data[:train_n]
        test = data[-test_n:]
        pickle.dump(test, open(data_fn.replace('.p','_test.p'),"wb"))
        train_data = np.asarray([d[2] for d in train])
        train_labels = np.asarray([d[-1] for d in train])

        model = keras.Sequential([
            keras.layers.Dense(100, activation=tf.nn.relu),
            keras.layers.Dense(2, activation=tf.nn.softmax)
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        print("training model...")
        n_epochs = 5
        model.fit(train_data, train_labels, epochs=n_epochs,class_weight=class_weight)
        model.save(f"models2/NOPE_{data_name}_100n.h5")
