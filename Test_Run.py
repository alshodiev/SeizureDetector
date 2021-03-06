# -*- coding: utf-8 -*-
from google.colab import drive
drive.mount("/content/drive", force_remount=True)

!pip install pyEDFlib

!pip install 'umap-learn==0.3.10'

DATASET_PATH = "/content/drive/My Drive/6.802 Project"
 LABEL_PATH = "/content/drive/MyDrive/6.802 Project/seizure_worksheet.xlsx"
 num_seconds = 1
 dimension = 42

from os import listdir
from os.path import isfile, join, isdir
import numpy as np
from PIL import Image
import random

data = listdir(DATASET_PATH)
full_dataset_list = []
for datum in data:
  if datum[-3:] == 'edf':
    new_data = join(DATASET_PATH, datum)
    full_dataset_list.append(new_data)
print(full_dataset_list)

from pyedflib import highlevel
import numpy as np

for_labeling = []
name_list = []
for i in range(len(full_dataset_list)):
  signal, signal_header, header = highlevel.read_edf(full_dataset_list[i])
  lister = full_dataset_list[i].split('/')
  name = lister[-1]
  sample_rate = signal_header[0]['sample_rate']
  num_data_points = len(signal[0])
  time_length = num_data_points/sample_rate
  data_info = [name, sample_rate, num_data_points, time_length]
  name_list.append(name)
  for_labeling.append(data_info)

np.save('/content/drive/My Drive/6.802 Project/for_labeling.npy', for_labeling)

for k in range(len(full_dataset_list)):
  signal, signal_header, header = highlevel.read_edf(full_dataset_list[k])
  lister = full_dataset_list[k].split('/')
  name = lister[-1]
  print(str(name) + ' ' + str(len(signal)))

import numpy as np
Dataset = {}
for k in range(len(full_dataset_list)):
  signal, signal_header, header = highlevel.read_edf(full_dataset_list[k])

  lister = full_dataset_list[k].split('/')
  name = lister[-1]

  sample_rate = signal_header[0]['sample_rate']
  num_data_points = len(signal[0])
  five_seconds = int(sample_rate * num_seconds)
  five_second_bins = int(num_data_points//five_seconds)
  final_array = np.zeros([five_second_bins,dimension])
  for i in range(five_second_bins):
    internal_array = np.zeros(dimension)
    val = int(dimension/2)
    for j in range(val):
      #power = 0
      #for k in range(five_seconds):
        #power += (signal[j][five_seconds*i + k])**2
      #power = power/five_seconds
      #activity = 0
      #for k in range(five_seconds):
        #activity += (signal[j][five_seconds * i + k]/power)**2
      #activity = activity/(five_seconds - 1)
      for k in range(five_seconds)
      average = np.average(signal[j][five_seconds * i:five_seconds * (i+1)])
      st_dev = np.std(signal[j][five_seconds * i:five_seconds * (i+1)])
      internal_array[j*2] = average
      internal_array[j*2 + 1] = st_dev
      #internal_array[j*4 + 2] = power
      #internal_array[j*2 + 1] = activity
    final_array[i] = internal_array
  Dataset[name] = final_array

#np.save('/content/drive/My Drive/6.802 Project/Dataset.npy', Dataset)

Dataset = np.load('/content/drive/My Drive/6.802 Project/Dataset.npy', allow_pickle=True).item()

print(Dataset['00000077_s003_t000.edf'].shape)
print(for_labeling)

import math
import pandas as pd

df = pd.read_excel(LABEL_PATH)

files_we_are_using = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,120,121,122,123,124,125,126,127,128,
                      219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,253,254,287,288,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,
                      445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,499,500,501,502,503,504,505,506,507,508,509,510,511,620,621,622,
                      623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,
                      699,700,701,702,703,704,705,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,749,750,751,776,778,783,784,785,786,833,834,967,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1082,1156,1157,1158,1159,1160,1161,1162,1163,
                      1164,1165,1166,1167,1168,1169,1170,1171,1172,1173,1177,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1277,1278,1279,1280,1281,1284,1293,1299,
                      1360,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1461,1462,1463,1464,1465,1555,1556,1557,1558,1559,1560,1580,1581,
                      1582,1583,1584,1585,1586,1669,1670,1671,1686,1687,1767,1884,1886,1889,1919,1920,1920,1921,1922,1923,1924,1925,1926,1942,1943,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2030,2031,2032,
                      2033]
start_stop_dictionary = {}
for files in files_we_are_using:
  if len(str(df.loc[files, 'Patient'])) == 4:
      name = '000000' + str(df.loc[files, 'Patient'])[0:2] + '_' + str(df.loc[files, 'Session']) + '_' + str(df.loc[files, 'File']) + '.edf'
  elif len(str(df.loc[files, 'Patient'])) == 5:
      name = '00000' + str(df.loc[files, 'Patient'])[0:3] + '_' + str(df.loc[files, 'Session']) + '_' + str(df.loc[files, 'File']) + '.edf'
  elif len(str(df.loc[files, 'Patient'])) == 6:
      name = '0000' + str(df.loc[files, 'Patient'])[0:4] + '_' + str(df.loc[files, 'Session']) + '_' + str(df.loc[files, 'File']) + '.edf'
  if name not in start_stop_dictionary:
    start_stop_dictionary[name] = []
  if math.isnan(df.loc[files,'Start']):
    total = []
  else:
    start_value = df.loc[files,'Start']//num_seconds
    stop_value = (df.loc[files,'Stop']//num_seconds) + 1
    total = [start_value, stop_value]
  start_stop_dictionary[name].append(total)

print(start_stop_dictionary)

Labels = {}
for item in for_labeling:
  starts_and_stops = start_stop_dictionary[item[0]]
  val = int(item[3]//num_seconds)
  lister = np.array([[0,1] for i in range(val)])
  if starts_and_stops != [[]]:
    counter = 0
    for i in range(len(lister)):
      for j in range(len(starts_and_stops)):
        if i <= starts_and_stops[j][1] and i >= starts_and_stops[j][0]:
          lister[i] = [1,0]
  Labels[item[0]] = np.array(lister)

np.save('/content/drive/My Drive/6.802 Project/Labels.npy', Labels)

import math

X_list = []
Y_list = []
X_list_test = []
Y_list_test = []
random.shuffle(name_list)
print(len(name_list))
name_list_train = name_list[:177]
name_list_test = name_list[177:]
for name in name_list_train:
  flag = False
  for i in range(len(Labels[name])):
    for j in range(len(Labels[name][i])):
      if Labels[name][i][0] == 1:
        flag = True
  if flag:
    X_list += [Dataset[name]] 
    Y_list += [Labels[name]]
  else:
    X_list.append(Dataset[name])
    Y_list.append(Labels[name])
for name in name_list_test:
  X_list_test.append(Dataset[name])
  Y_list_test.append(Labels[name])
X_array = np.array(X_list)
Y_array = np.array(Y_list)
X_test = np.array(X_list_test)
Y_test = np.array(Y_list_test)

num_zeros = 0
num_ones = 0
for i in range(len(X_array)):
  for j in range(len(X_array[i])):
    if Y_array[i][j][0] == 0:
        num_zeros += 1
    else:
        num_ones += 1
print(num_zeros)
print(num_ones)
print('finished')

from keras import Sequential
from keras.utils import Sequence
from keras.layers import LSTM, Dense, Masking
import numpy as np


class MyBatchGenerator(Sequence):
    'Generates data for Keras'
    def __init__(self, X, y, batch_size=1, shuffle=True):
        'Initialization'
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.y)/self.batch_size))

    def __getitem__(self, index):
        return self.__data_generation(index)

    def on_epoch_end(self):
        'Shuffles indexes after each epoch'
        self.indexes = np.arange(len(self.y))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, index):
        Xb = np.empty((self.batch_size, *X_array[index].shape))
        yb = np.empty((self.batch_size, *Y_array[index].shape))
        for s in range(0, self.batch_size):
            Xb[s] = X_array[index]
            yb[s] = Y_array[index]
        return Xb, yb

import keras.backend as K

def custom_loss(y_pred, y_true):
  loss = tf.keras.losses.BinaryCrossentropy(y_true, y_pred)
  return(loss)

from keras import Sequential
from keras.utils import Sequence
from keras.layers import LSTM, Dense, Masking
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
import tensorflow as tf
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score


# Batch = 1

import math

num_true_resets = 0
full_roc = 0
while num_true_resets < 10:
  X_list = []
  Y_list = []
  X_list_test = []
  Y_list_test = []
  num_vals = int(len(name_list) * .8)
  name_list_train = name_list[:num_vals]
  name_list_test = name_list[num_vals:]
  for name in name_list_train:
    flag = False
    for i in range(len(Labels[name])):
      for j in range(len(Labels[name][i])):
        if Labels[name][i][0] == 1:
          flag = True
    if flag:
      X_list += [Dataset[name]] * 7
      Y_list += [Labels[name]] * 7
    else:
      X_list.append(Dataset[name])
      Y_list.append(Labels[name])
  for name in name_list_test:
    X_list_test.append(Dataset[name])
    Y_list_test.append(Labels[name])
  X_array = np.array(X_list)
  Y_array = np.array(Y_list)
  X_test = np.array(X_list_test)
  Y_test = np.array(Y_list_test)

  final_roc_auc = 0
  num_resets = 0
  while num_resets < 1:
    
    model = Sequential()
    model.add(LSTM(100, activation = 'sigmoid', input_shape=(None, dimension), return_sequences=True))
    model.add(LSTM(100, activation = 'sigmoid', return_sequences=True))
    model.add(TimeDistributed(Dense(2,activation = 'softmax')))

    model.compile(loss= "binary_crossentropy", optimizer= keras.optimizers.Adam(learning_rate = .0001), metrics=['binary_accuracy'])
    model.fit_generator(MyBatchGenerator(X_array, Y_array, batch_size=1), epochs=4)

    model.summary()

    all_predictions = []
    for sample in X_test:
      input_array = np.array([sample])
      y_prediction = model(input_array) 
      all_predictions.append(y_prediction)

    listed_predictions = []
    for i in range(len(all_predictions)):
      for j in range(len(all_predictions[i])):
        for k in range(len(all_predictions[i][j])):
          val = all_predictions[i][j][k].numpy()
          listed_predictions.append(val[0])
    listed_true = []
    for i in range(len(Y_test)):
      for j in range(len(Y_test[i])):
          if np.array_equal(Y_test[i][j],np.array([0,1])):
            listed_true.append(0)
          else:
            listed_true.append(1)
    arrayed_y_pred = np.array(listed_predictions)
    arrayed_y_true = np.array(listed_true)
    roc_auc = roc_auc_score(arrayed_y_true, arrayed_y_pred)

    false_positive_rate, true_positive_rate, thresolds = roc_curve(arrayed_y_true, arrayed_y_pred)

    plt.figure(figsize=(10, 8), dpi=100)
    plt.axis('scaled')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.title("AUC & ROC Curve")
    plt.plot(false_positive_rate, true_positive_rate, 'g')
    plt.fill_between(false_positive_rate, true_positive_rate, facecolor='lightgreen', alpha=0.7)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()

    average_precision = average_precision_score(arrayed_y_true, arrayed_y_pred)
    print(average_precision)
    prec, recall, _ = precision_recall_curve(arrayed_y_true, arrayed_y_pred)

    plt.figure(figsize=(10, 8), dpi=100)
    plt.axis('scaled')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.title("PRC")
    plt.plot(recall, prec, 'g')
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.show()


    
    print(roc_auc)
    final_roc_auc += roc_auc
    num_resets += 1
  num_true_resets += 1
  full_roc += final_roc_auc
print("Final: " + str(full_roc/10))

import tensorflow as tf
from sklearn.metrics import roc_auc_score

all_predictions = []
for sample in X_test:
  input_array = np.array([sample])
  y_prediction = model(input_array) 
  all_predictions.append(y_prediction)
#all_predicitions_array = np.array(all_predictions)
#all_predictions_array.shape
#val = roc_auc_score(Y_test[0], y_prediction[0])

listed_predictions = []
for i in range(len(all_predictions)):
  for j in range(len(all_predictions[i])):
    for k in range(len(all_predictions[i][j])):
      val = all_predictions[i][j][k].numpy()
      listed_predictions.append(val)
listed_true = []
for i in range(len(Y_test)):
  for j in range(len(Y_test[i])):
    listed_true.append(Y_test[i][j])
arrayed_y_pred = np.array(listed_predictions)
arrayed_y_true = np.array(listed_true)
roc_auc = roc_auc_score(arrayed_y_true, arrayed_y_pred)
print(roc_auc)

"""### Numerical Labels"""

print(start_stop_dictionary)

print(name_list[2])
print(start_stop_dictionary['00006440_s002_t002.edf'])

def dataandlabels(name_list, Dataset, Labels, num_seconds):
  zero_label = np.array([0,1])
  one_label = np.array([1,0])
  seizure_length_labels = []
  seizure_length_data = []
  before_seizure = []
  seizure_length = 0
  mini_name_list = ['00000492_s003_t006.edf', '00000492_s003_t007.edf','00006440_s002_t002.edf']
  for name in name_list:
    if seizure_length != 0:
      seizure_length_labels.append(seizure_length)
    before_seizure = []
    seizure_length = 0
    for i in range(len(Labels[name])):
      if np.array_equal(zero_label, Labels[name][i]):
        if seizure_length != 0:
          seizure_length_labels.append(seizure_length * num_seconds)
          seizure_length = 0
        before_seizure.append(Dataset[name][i])
      else:
        if before_seizure != []:
          seizure_length_data.append(np.array(before_seizure))
          before_seizure = []
        seizure_length += 1
  if seizure_length != 0:
      seizure_length_labels.append(seizure_length)

  avg = np.average(seizure_length_labels)
  sd = np.std(seizure_length_labels)
  print(avg, sd)
  outlier = set()
  fixed_seizure_length_data = []
  fixed_seizure_length_labels = []
  for i in range(len(seizure_length_labels)):
    if seizure_length_labels[i] > avg + 2*sd:
      outlier.add(i)
    if seizure_length_data[i].shape[0] < 20:
      outlier.add(i)
  for i in range(len(seizure_length_labels)):
    if i not in outlier:
      fixed_seizure_length_labels.append(seizure_length_labels[i])
      fixed_seizure_length_data.append(seizure_length_data[i])

  seizure_length_data_a = np.array(fixed_seizure_length_data)
  seizure_length_labels_a = np.array(fixed_seizure_length_labels)
  return(seizure_length_data_a, seizure_length_labels_a)

from keras import Sequential
from keras.utils import Sequence
from keras.layers import LSTM, Dense, Masking
import numpy as np


class MyBatchGenerator(Sequence):
    'Generates data for Keras'
    def __init__(self, X, y, batch_size=1, shuffle=True):
        'Initialization'
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.y)/self.batch_size))

    def __getitem__(self, index):
        return self.__data_generation(index)

    def on_epoch_end(self):
        'Shuffles indexes after each epoch'
        self.indexes = np.arange(len(self.y))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, index):
        Xb = np.empty((self.batch_size, *X_array[index].shape))
        yb = np.empty((self.batch_size, *Y_array[index].shape))
        for s in range(0, self.batch_size):
            Xb[s] = X_array[index]
            yb[s] = Y_array[index]
        return Xb, yb

from keras import Sequential
from keras.utils import Sequence
from keras.layers import LSTM, Dense, Masking
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
import tensorflow as tf
from sklearn.metrics import roc_auc_score

# Batch = 1

import math

num_true_resets = 0
full_error = []
while num_true_resets < 5:
  random.shuffle(name_list)
  Seizure_length_dataset_final, Seizure_length_labels_final = dataandlabels(name_list, Dataset, Labels, num_seconds)
  print(Seizure_length_dataset_final.shape)
  maximum = np.amax(Seizure_length_labels_final)
  print(maximum)
  Seizure_length_labels_final = Seizure_length_labels_final/maximum
  X_array = Seizure_length_dataset_final[:213]
  Y_array = Seizure_length_labels_final[:213]
  X_test = Seizure_length_dataset_final[213:]
  Y_test = Seizure_length_labels_final[213:]
  num_resets = 0
  full_error_dataset = 0
  while num_resets < 1:
    
    model = Sequential()
    model.add(LSTM(500, activation = 'sigmoid', input_shape=(None, dimension)))
    model.add(Dense(100,activation='sigmoid'))
    model.add(Dense(100,activation='sigmoid'))
    model.add(Dense(1,activation = 'sigmoid'))

    model.compile(loss= "MSE", optimizer= keras.optimizers.Adam(learning_rate = .001), metrics=['MAE'])
    model.fit_generator(MyBatchGenerator(X_array, Y_array, batch_size=1), epochs=4)

    model.summary()
    num_resets += 1
    error = 0
    for i in range(len(X_test)):
      MAE = np.abs(Y_test[i] - model.predict(np.array([X_test[i]])))
      error += MAE * maximum
    print(error/len(X_test))
    full_error_dataset += error/len(X_test)
  full_error.append(full_error_dataset)
  num_true_resets += 1
print(np.average(full_error), np.std(full_error))

print(np.std([34.132095, 49.654457, 25.344894, 45.772568, 39.205837]))

"""UMAP"""

all_data_array = np.array([0])
for key in sample:
  if all_data_array.any() == np.array([0]):
    all_data_array = sample[key]
  else:
    new_array = sample[key]
    all_data_array = np.concatenate((all_data_array, new_array))
print(all_data_array)

import umap.umap_ as umap

#Keep this!
n_n = 960
reducer = umap.UMAP(random_state=42, n_neighbors = n_n, min_dist = .5) 
reducer.fit(all_data_array)
embedding = reducer.transform(all_data_array)

import matplotlib.pyplot as plt 
for i in range(len(embedding)):
  plt.scatter(embedding[i, 0], embedding[i, 1])
