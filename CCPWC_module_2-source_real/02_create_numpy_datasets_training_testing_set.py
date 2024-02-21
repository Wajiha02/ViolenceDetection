# -*- coding: utf-8 -*-
"""02_create-numpy-datasets_training-test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WJsB7HnXp_iLny-VhJiRyxdd_tMk_jND

# imports
"""

import numpy as np
import pickle
from random import shuffle

"""# 02-A. Load Fight / NonFight Video Pickle Files

"""

# Fight Video frames Numpy array list
with open("D:/datasets/AllVideo_numpy_list_pickle/01_data_Fight_210512.pickle","rb") as fr:
    data_Fight=pickle.load(fr)
print(len(data_Fight))

# NonFight Video frames Numpy array list
with open("D:/datasets/AllVideo_numpy_list_pickle/01_label_Fight_210512.pickle","rb") as fr:
    label_Fight=pickle.load(fr)
print(len(label_Fight))

# Fight label Numpy array list
with open("D:/datasets/AllVideo_numpy_list_pickle/01_data_NonFight_210507.pickle","rb") as fr:
    data_NonFight=pickle.load(fr)
print(len(data_NonFight))

# NonFight label Numpy array list
with open("D:/datasets/AllVideo_numpy_list_pickle/01_label_NonFight_210507.pickle","rb") as fr:
    label_NonFight=pickle.load(fr)
print(len(label_NonFight))

"""# 02-B. Merge data & Random Shuffle

## 1. Merge data : Fight + NonFight
"""

data_total=data_Fight+data_NonFight
print(len(data_total))

label_total=label_Fight+label_NonFight
print(len(label_total))

"""## 2. Shuffle merged dataset"""

np.random.seed(42)

c=list(zip(data_total, label_total)) # zip
shuffle(c) # Random Shuffle
data_total, label_total=zip(*c) # unpacking

"""## 3. save shuffled dataset as .pickle
* **`pickle.dump(protocol=pickle.HIGHEST_PROTOCOL)`** : To solve lack of memory issue for pickle save process
"""

# Save data
with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_total_210512.pickle","wb") as fw:
    pickle.dump(data_total, fw, protocol=pickle.HIGHEST_PROTOCOL)

# Save label
with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_total_210512.pickle","wb") as fw:
    pickle.dump(label_total, fw)

"""# 02-C. Split training set / test set

## 1. Load shuffled dataset(.pickle)
"""

# load data
with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_total_210512.pickle","rb") as fr:
    data_total=pickle.load(fr)

# load label
with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_total_210512.pickle","rb") as fr:
    label_total=pickle.load(fr)

"""## 2. Split dataset as training set / test set (8:2 ratio)

### 1) The number of training set, test set
"""

training_set=int(len(data_total)*0.8)
test_set=int(len(data_total)*0.2)

data_training=data_total[0:training_set] # Training set data
data_test=data_total[training_set:] # Test set data

label_training=label_total[0:training_set] # Training set label
label_test=label_total[training_set:] # Test set label

len(data_training), len(label_training), len(data_test), len(label_test)

"""### 2) Check the shape of elements"""

data_training[0].shape, label_training[0].shape

data_training[0][0, :, :, 0]

"""## 3. Save training set & test set as .pickle file

"""

# training set, data
with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_training_210512.pickle","wb") as fw:
    pickle.dump(data_training, fw, protocol=pickle.HIGHEST_PROTOCOL)

# training set, label
with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_training_210512.pickle","wb") as fw:
    pickle.dump(label_training, fw)

# test set, data
with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_test_210512.pickle","wb") as fw:
    pickle.dump(data_test, fw, protocol=pickle.HIGHEST_PROTOCOL)

# test set, label
with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_test_210512.pickle","wb") as fw:
    pickle.dump(label_test, fw)

"""# 02-D. Transform dataset as Numpy array

## 1. Load training set & test set (.pickle)

### 1) Training set : data, label
"""

with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_training_210512.pickle","rb") as fr:
    data_training=pickle.load(fr)

with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_training_210512.pickle","rb") as fr:
    label_training=pickle.load(fr)

"""### 2) Test set : data, label"""

with open("D:/datasets/AllVideo_numpy_list_pickle/02_data_test_210512.pickle","rb") as fr:
    data_test=pickle.load(fr)

with open("D:/datasets/AllVideo_numpy_list_pickle/02_label_test_210512.pickle","rb") as fr:
    label_test=pickle.load(fr)

"""## 2. Transform training set & test set as Numpy array, and save them (.npy)

### 1) Training set
"""

data_training_ar=np.array(data_training, dtype=np.float16) #> (2878, 30, 160, 160, 3)

np.save('D:/datasets/AllVideo_numpy_list_pickle/02_data_training_Numpy_210512.npy', data_training_ar)

label_training_ar=np.array(label_training) #> (2878, 2)

np.save('D:/datasets/AllVideo_numpy_list_pickle/02_label_training_Numpy_210512.npy', label_training_ar)

data_training_ar.shape, label_training_ar.shape

"""### 2) Test set"""

data_test_ar=np.array(data_test, dtype=np.float16) #> (720, 30, 160, 160, 3)

np.save('D:/datasets/AllVideo_numpy_list_pickle/02_data_test_Numpy_210512.npy', data_test_ar)

label_test_ar=np.array(label_test) #> (720, 2)

np.save('D:/datasets/AllVideo_numpy_list_pickle/02_label_test_Numpy_210512.npy', label_test_ar)

data_test_ar.shape, label_test_ar.shape