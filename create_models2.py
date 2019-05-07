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
        test_data = np.asarray([d[2] for d in test])
        test_labels =np.asarray( [d[-1] for d in test])

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
        print("testing model...")
        test_loss, test_acc = model.evaluate(test_data, test_labels)
        print('Test accuracy:', test_acc)

        prediction = model.predict(test_data)
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for i,p in enumerate(prediction):
            if np.argmax(p) == 1:
                if test_labels[i] == 1:
                    tp +=1
                else:
                    fp +=1
            else:
                if test_labels[i] == 0:
                    tn += 1
                else:
                    fn += 1
        all_positive = sum(test_labels)
        all_negative = len(test_labels) - all_positive
        result.write(f"{data_name}\t{all_positive}\t{all_negative}\t{tp}\t{tn}\t{fp}\t{fn}\n")
        model.save(f"models2\\NOPE_{data_name}_100n.h5")
