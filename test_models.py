from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
from tensorflow import keras
import pickle
import numpy as np

"""
Test the models produced by create_models.py
"""
results = open("test_models_results.csv", "w")
results.write("n,model,loss,accuracy,tp,tn,fp,fn\n")
nums = [7,9,11,13]
for n in nums:
    test_fn = f"allgrids_data/allgrids_AA_charge{n}_test.p"
    model_fn = f"models/NOPE_charge{n}_100n.h5"
    print(f"data: {test_fn}, model: {model_fn}")
    test = pickle.load(open(test_fn, "rb"))
    test_data = np.asarray([d[2] for d in test])
    test_labels =np.asarray( [d[-1] for d in test])

    model = keras.models.load_model(model_fn)
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
    results.write(f"{n},{model_fn},{test_loss},{test_acc},{tp},{tn},{fp},{fn}\n")
