from __future__ import absolute_import, division, print_function

# TensorFlow and tf.keras
from tensorflow import keras
import pickle
import glob

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
