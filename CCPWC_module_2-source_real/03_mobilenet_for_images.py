# -*- coding: utf-8 -*-
"""03_MobileNet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10q-4omSh_nFLoAQdqsJhl1jXzuGqejgE

# 03. Extract features from dataset by using MobileNet(pre-trained model)

# Imports
"""

import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import random

"""# 03-A. Load datasets array(.npy) : trainning set & test set
* shape : `(# of Video file, # of frame img, img height, img width, RGB)`
"""

data_training_ar=np.load('D:/datasets/AllVideo_numpy_list_pickle/02_data_training_Numpy_210512.npy')
data_training_ar.shape #> (2878, 30, 160, 160, 3)

data_test_ar=np.load('D:/datasets/AllVideo_numpy_list_pickle/02_data_test_Numpy_210512.npy')
data_test_ar.shape #> (720, 30, 160, 160, 3)

"""# 03-B. Reshape data
* `(# of Video file, # of frame img, img height, img width, RGB)` to `((# of Video file)*(# of frame img), img height, img width, RGB)`
"""

data_training_ar=data_training_ar.reshape(data_training_ar.shape[0]*30, 160, 160, 3)
data_training_ar.shape #> (86340, 160, 160, 3)

data_test_ar=data_test_ar.reshape(data_test_ar.shape[0]*30, 160, 160, 3)
data_test_ar.shape #> (21600, 160, 160, 3)

"""# 03-C. Create Base Model : MobileNet"""

base_model=keras.applications.mobilenet.MobileNet(input_shape=(160, 160, 3),
                                                  include_top=False,
                                                  weights='imagenet', classes=2)

base_model.summary() #> (None, 5, 5, 1024)

"""# 03-D. Predict(Extract features) : Insert datasets to MobileNet base_model
* create **`X_train`**, **`X_test`**
* **output shape** : **`((# of Video file)*(# of frame img), 5, 5, 1024)`**
"""

np.random.seed(42)

X_train=base_model.predict(data_training_ar)
X_train.shape #> (86340, 5, 5, 1024)

X_test=base_model.predict(data_test_ar)
X_test.shape #> (21600, 5, 5, 1024)

"""# 03-E. Reshape predict result to insert LSTM
* **Output Shape** : **`(# of Video File, # of frame img, 5*5*1024)`**
"""

X_train_reshaped = X_train.reshape(int(X_train.shape[0]/30), 30, 5*5*1024) #> (2878, 30, 25600) ndarray

X_test_reshaped = X_test.reshape(int(X_test.shape[0]/30), 30, 5*5*1024) #> (720, 30, 25600) ndarray

X_train_reshaped.shape, X_test_reshaped.shape

"""# 03-F. Save reshaped result file(.npy)
* **`MobileNet_x_train_reshaped_210512.npy`**, **`MobileNet_x_test_reshaped_210512.npy`**
"""

np.save('D:/datasets/AllVideo_numpy_list_pickle/MobileNet_x_train_reshaped_210512.npy', X_train_reshaped)

np.save('D:/datasets/AllVideo_numpy_list_pickle/MobileNet_x_test_reshaped_210512.npy', X_test_reshaped)