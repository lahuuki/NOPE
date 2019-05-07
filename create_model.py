from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pickle
import random


print("loading data...")
data = pickle.load(open("allgrids_AA_charge9.p", "rb"))
print(f"{len(data)} data points")

random.shuffle(data)
pos_data = [d for d in data if d[-2] == 1]
n_pos = len(pos_data)
neg_data = random.sample([d for d in data if d[-2] == 0],n_pos)
print(f"After balancing: {len(pos_data)} Positive  and {len(neg_data)} Negative")
print("normalizing data")
data_norm = pos_data + neg_data
random.shuffle(data_norm)
train_n = int(len(data_norm) *.8)
test_n = len(data_norm) - train_n

train_data = np.asarray([d[-1] for d in data_norm[:train_n]])
train_labels = np.asarray([d[-2] for d in data_norm[:train_n]])
test_data = np.asarray([d[-1] for d in data_norm[-test_n:]])
test_labels =np.asarray( [d[-2] for d in data_norm[-test_n:]])

model = keras.Sequential([
    # keras.layers.Flatten(input_shape=(3, 343)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
print("training model...")
model.fit(train_data, train_labels, epochs=5)
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
print(f"TEST DATA:{all_positive} ({100*all_positive/len(test_labels):.2f}%) Positive vs. {all_negative} ({100*all_negative/len(test_labels):.2f}%)  Negative")
print(f"TP: {tp} ({tp/all_positive:.2f})\tFP: {fp}\nTN: {tn} ({tn/all_negative:.2f})\tFN: {fn}")
