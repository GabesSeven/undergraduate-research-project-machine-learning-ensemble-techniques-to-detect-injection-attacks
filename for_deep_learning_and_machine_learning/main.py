# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ckg4SH0I4fnYz_LicKy430ihk4aSSz0D
"""

!pip install tf-nightly #!pip install sklearn numpy joblib pandas imblearn matplotlib

import glob
import time
import numpy as np
from numpy import genfromtxt
import pandas as pd

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_learning_curves

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix, recall_score, accuracy_score, ConfusionMatrixDisplay
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier, StackingClassifier
from sklearn.utils import shuffle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from joblib import dump, load
from imblearn.over_sampling import SMOTE

from google.colab import drive

diretorio  = '/content/drive/My Drive/IC_code_database/'
drive.mount('/content/drive', force_remount = True)

#--- Returns a possibly empty list of path names that correspond to '.joblib' files
joblibs = [f[2:] for f in glob.glob('./*.joblib')] 
print('[*] Joblibs found:')
print(joblibs)

# #--- Reading training set
# print('[*] Reading the contents of \'feautingTrainingAnomalousAndNormal.csv\', ie training set...')
# dataset_training=pd.read_csv(diretorio+'feautingTrainingAnomalousAndNormal.csv', sep=',', header=None)
# # dataset_training = genfromtxt(diretorio+'feautingTestAnomalousAndNormal.csv', delimiter=',')
# print('\t[*] dataset_training (rows, columns): {}.'.format(str(dataset_training.shape)))

# #--- Reading testing set
# print('[*] Reading the contents of \'feautingTestAnomalousAndNormal.csv\', ie testing set...')
# dataset_test=pd.read_csv(diretorio+'feautingTestAnomalousAndNormal.csv', sep=',', header=None)
# # dataset_test = genfromtxt(diretorio+'feautingTestAnomalousAndNormal.csv', delimiter=',')
# print('\t[*] dataset_test (rows, columns): {}.'.format(str(dataset_test.shape)))

# #--- Dividing the training set into features and labels
# print('[*] Dividing the training set into \'features\' and \'labels\'...')
# dataset_training_features = dataset_training.iloc[:,:5].values
# dataset_training_labels = dataset_training.iloc[:,5].values
# # dataset_training_features, dataset_training_labels = np.hsplit(dataset_training, [5])
# print(dataset_training_features)
# print('\t[*] dataset_training_features (rows, columns): {}.'.format(str(dataset_training_features.shape)))
# print('\t[*] dataset_training_labels (rows, columns): {}.'.format(str(dataset_training_labels.shape)))

# #--- Dividing the testing set into features and labels
# print('[*] Dividing the testing set into \'features\' and \'labels\'...')
# dataset_test_features = dataset_test.iloc[:,:5].values
# dataset_test_labels = dataset_test.iloc[:,5].values
# # dataset_test_features, dataset_test_labels = np.hsplit(dataset_test, [5])
# print('\t[*] dataset_test_features (rows, columns): {}.'.format(str(dataset_test_features.shape)))
# print('\t[*] dataset_test_labels (rows, columns): {}.'.format(str(dataset_test_labels.shape)))

#--- Reading set of data
print('[*] Reading the contents of \'feautingAnomalousAndNormal.csv\', ie testing set...')
dataset_training=pd.read_csv(diretorio+'feautingAnomalousAndNormal.csv', sep=',', header=None)
# dataset_training = genfromtxt(diretorio+'feautingTestAnomalousAndNormal.csv', delimiter=',')
print('\t[*] dataset_training (rows, columns): {}.'.format(str(dataset_training.shape)))

#--- Shuffling the data
print(dataset_training.head())
dataset_training = shuffle(dataset_training)
print(dataset_training.head()) 

#--- Dividing the set of data into features and labels
print('[*] Dividing the training set into \'features\' and \'labels\'...')
dataset_training_features = dataset_training.iloc[:,:5].values
dataset_training_labels = dataset_training.iloc[:,5].values
# dataset_training_features, dataset_training_labels = np.hsplit(dataset_training, [5])
print(dataset_training_features)
print(dataset_training_labels)
print('\t[*] dataset_training_features (rows, columns): {}.'.format(str(dataset_training_features.shape)))
print('\t[*] dataset_training_labels (rows, columns): {}.'.format(str(dataset_training_labels.shape)))

#--- Dividing the training set into training and validation
print('[*] Dividing the training set into training and validation...')
train_x, val_x, train_y, val_y = train_test_split(dataset_training_features, dataset_training_labels, test_size=.33, random_state=12)
print('\t[*] train_x (rows, columns): {}.'.format(str(train_x.shape)))
print('\t[*] train_y (rows, columns): {}.'.format(str(train_y.shape)))
print('\t[*] val_x (rows, columns): {}.'.format(str(val_x.shape)))
print('\t[*] val_y (rows, columns): {}.'.format(str(val_y.shape)))

#--- Applying the SMOTE
print('[*] Applying the Synthetic Minority Over-Sampling Technique (SMOTE) algorithm to the training set...')
sm = SMOTE(random_state=12, ratio=1.0)
train_x_resampled, train_y_resampled = sm.fit_sample(train_x, train_y)
print('\t[*] train_x_resampled (rows, columns): {}.'.format(str(train_x_resampled.shape)))
print('\t[*] train_y_resampled (rows, columns): {}.'.format(str(train_y_resampled.shape)))

# #--- Applying the Min Max Scaler
# print('[*] Applying the Min Max Scaler algorithm to the training/testing set...')
# scaler = MinMaxScaler()
# val_x_adjusted = scaler.fit_transform(val_x)
# train_x_resampled_adjusted = scaler.fit_transform(train_x_resampled)
# test_features_adjusted = scaler.fit_transform(dataset_test_features)

#------------------------>>>>>>>>>>>>>>>>>>> for DEEP LEARNING
# based on https://missinglink.ai/guides/keras/keras-conv1d-working-1d-convolutional-neural-networks-keras/
#          https://machinelearningmastery.com/cnn-models-for-human-activity-recognition-time-series-classification/
# #--- Running Multi-Layers Classifier
# #--- Creating evaluate model
train_x_resampled = np.reshape(train_x_resampled, (train_x_resampled.shape[0], train_x_resampled.shape[1], 1))
train_y_resampled = np.reshape(train_y_resampled, (train_y_resampled.shape[0], 1))
val_x = np.reshape(val_x, (val_x.shape[0],val_x.shape[1], 1))
val_y = np.reshape(val_y, (val_y.shape[0], 1))  
print(train_x_resampled.shape, train_y_resampled.shape)
print(val_x.shape, val_y.shape)

true = True
while true: # loop para garantir que train_x_resampled e val_x tenham o mesmo shape  
  train_x_resampled = to_categorical(train_x_resampled)
  try:
    # para train_x_resampled e val_x tenham possuirem o mesmo número de classes
    val_x = to_categorical(val_x, num_classes=train_x_resampled.shape[2]) 
    true = False
  except:
    true = True
    print('Não deu certo, valores diferentes')
train_y_resampled = to_categorical(train_y_resampled)
val_y = to_categorical(val_y)
print(train_x_resampled.shape, train_y_resampled.shape)
print(val_x.shape, val_y.shape)

n_timesteps, n_features, n_outputs = train_x_resampled.shape[1], train_x_resampled.shape[2], train_y_resampled.shape[1]
print(n_timesteps, n_features, n_outputs) # (5 1450 2)
model = Sequential()
model.add(Conv1D(filters=3, kernel_size=3, activation='relu', input_shape=(n_timesteps, n_features))) # (5 1450)
model.add(Conv1D(filters=3, kernel_size=3, activation='relu'))
model.add(Dropout(0.5))
model.add(MaxPooling1D(pool_size=1))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(n_outputs, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()
#--- Fitting network
epochs, batch_size = 20, 2
model.fit(train_x_resampled, train_y_resampled, epochs=epochs, batch_size=batch_size, verbose=1) #, validation_data=(val_x, val_y))
#--- Evaluate model
scores = model.evaluate(val_x, val_y, batch_size=batch_size, verbose=1)
print(scores)

#--- Confusion Matrix
preds = model.predict_classes(val_x)
print(preds)
print(preds.shape)

argmax_val_y = np.argmax(val_y, axis=1)
print(val_y)
print('Confusion Matrix')
print(confusion_matrix(argmax_val_y, preds))
print('Classification Report')
target_names = ['ataque', 'não-ataque']
print(classification_report(argmax_val_y, preds, target_names=target_names))

cm = confusion_matrix(argmax_val_y, preds, normalize='true')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
disp.plot()

#------------------------>>>>>>>>>>>>>>>>>>> for MACHINE LEARNING, isolated classifiers and ensemble.
# #--- Running classifiers individually
# #--- Listing of classifiers, task lists (joblists) and builders
# clf_names = ['Linear SVC', 'AdaBoost', 'Decision Tree', 'Random Forest', 'Bernoulli NB', 'Gaussian NB', 'Mutinominal NB', 'Stacking Classifier'] 
# clf_joblibs = ['clf_svc.joblib', 'clf_ab.joblib', 'clf_dt.joblib', 'clf_rf.joblib', 'clf_bnb.joblib', 'clf_gnb.joblib', 'clf_mnb.joblib', 'clf_sc.joblib']
# clf_constructors = [LinearSVC(C=100, dual=False), AdaBoostClassifier(), DecisionTreeClassifier(), RandomForestClassifier(), BernoulliNB(), GaussianNB(), MultinomialNB(), reg]
# results = []
  
# for i, clf in enumerate(clf_constructors):
#   start_time = time.time()
  
#   print('\n[*] Classifier: {}'.format(clf_names[i]))

#   #--- Training all classifier individually
#   if clf_joblibs[i] in joblibs:
#     print('[*] Loading {}...'.format(clf_joblibs[i]))
#     clf = load(clf_joblibs[i])
#     predictions = clf.predict(dataset_test_features)
#   else:
#     print('[*] No joblib was found. Running the classifier on the training set...')
#     predictions = clf.fit(train_x_resampled, train_y_resampled).predict(dataset_test_features)
#     dump(clf, clf_joblibs[i])

#   accuracy = accuracy_score(dataset_test_labels, predictions)
#   c_matrix = confusion_matrix(dataset_test_labels, predictions)
#   precision, recall, fscore, support = precision_recall_fscore_support(dataset_test_labels, predictions)
#   results.append([i, clf_names[i], accuracy, precision, recall, fscore, support, c_matrix, (time.time() - start_time)])
  
#   #--- Printing results
#   print('[*] Accuracy: {}'.format(accuracy))
#   print('[*] Result: {}'.format(results[i]))
  
#   #--- Printing plot of current classifier  
#   # if i == 7:
#   #   plot_learning_curves(X_train=train_x, y_train=train_y, X_test=val_x, y_test=val_y, clf=clf)
#   #   plt.show

#   #--- Printing feature_importances for some classifiers
#   if clf_names[i] in ['AdaBoost', 'Decision Tree', 'Random Forest']:
#     print(clf.feature_importances_)

# #--- Applying Grid Search to SVC
# print('\n[*] Applying Grid Search to SVC...')
# param_grid = {'C':[0.1,1,10,100]}
# grid = GridSearchCV(LinearSVC(dual=False), param_grid, n_jobs=2, verbose=3)
# grid.fit(train_x_resampled, train_y_resampled)
# print(grid.best_params_)

# #--- Running Ensemble classifier with SVC and Decision Tree
# #--- Configuring Stack Classifier
# estimators = [('linearSVC', LinearSVC(C=100, dual=False)),
#               ('decisionTreeClassifier', DecisionTreeClassifier())]
# #--- Using estimator forecasts as input with final_estimator
# reg = StackingClassifier(
#     estimators=estimators,
#     final_estimator=GradientBoostingClassifier(random_state=42)
#     # voting='hard'
# )
# #--- Training Stack Classifier
# reg.fit(train_x, train_y)

# # #--- Extra informations
# # print('\n[*] Validation Extra informations:')
# # val_unique, val_counts = np.unique(val_y, return_counts=True)
# # print(dict(zip(val_unique, val_counts)))	

# # print('[*] Testing Extra informations:')
# # test_unique, test_counts = np.unique(dataset_test_labels, return_counts=True)
# # print(dict(zip(test_unique, test_counts)))

# # results.append([i, clf_names[i], accuracy, precision, recall, fscore, support, c_matrix, (time.time() - start_time)])
