from __future__ import division
import numpy as np
import json
import math
import itertools
import matplotlib.cm as cm
import scipy
import csv
from scipy.optimize import fmin
from scipy.optimize import minimize
import scipy.sparse
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import confusion_matrix
import statsmodels.api as sm
import time
#####   Apro i file, Leggo il json, e lo carico come Dizionario. Chiudo i files   #####

start_time = time.time()

file = open("moviesAll-Votes.txt",'r')
act = open("invertedIndexActorsWeightedAll.txt",'r')
dir = open("invertedIndexDirectorsWeightedAll.txt", 'r')
wri = open("invertedIndexWritersWeightedAll.txt", 'r')
line = file.readline()
lact = act.readline()
ldir = dir.readline()
lwri = wri.readline()
gson = json.loads(line)
jact = json.loads(lact)
jdir = json.loads(ldir)
jwri = json.loads(lwri)
file.close()
act.close()
dir.close()
wri.close()
c = open("ciao.txt", 'w')



def plot_confusion_matrix(cm, classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, str(((cm[i, j])/(np.sum(cm[i]))*100).round(2))+'%',
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


## Calcola le medie dei ratings ##
def calcolaMedie(actors, directors, writers):
    mediaAct = 0
    mediaDir = 0
    mediaWri = 0
    for elem in actors:
        mediaAct += float(jact.get(elem).get("rating"))
    for elem in directors:
        mediaDir += float(jdir.get(elem).get("rating"))
    for elem in writers:
        mediaWri += float(jwri.get(elem).get("rating"))
    mediaAct = float(mediaAct / len(actors))
    mediaDir = float(mediaDir / len(directors))
    mediaWri = float(mediaWri / len(writers))

    return mediaAct, mediaDir, mediaWri


## Estrae dati dai json per calcolare le medie dei ratings ##
def readData():
    vector = []
    labels = []
    indice = 0
    for elem in gson:
        try:
            actors = gson.get(elem).get("actors")
            directors = gson.get(elem).get("director")
            writers = gson.get(elem).get("writer")
            imdbRating = int(float(gson.get(elem).get("imdbRating")))
            mediaAct, mediaDir, mediaWri = calcolaMedie(actors, directors, writers)
            vect = [1,mediaAct, mediaDir, mediaWri]
            vector.append(vect)
            labels.append(int(imdbRating))  ## CAST PER CLASSI DISCRETE ##
        except Exception:
            continue
    data = np.array(vector)
    labels = np.array(labels)
    train_data, test_data, train_labels, test_labels = train_test_split(data, labels, train_size=0.4)
    return train_data, train_labels, test_data, test_labels






train_data, train_labels, test_data, test_labels = readData()

regressor = linear_model.LinearRegression()
regressor.fit(train_data,train_labels)

pred_lab = regressor.predict(test_data)

freq = [0,0,0,0,0,0]

for j in range(len(pred_lab)):
    if (pred_lab[j] <1.5 and pred_lab[j] >0 ):
        freq[0] += 1
    if(pred_lab[j] <2.5 and pred_lab[j] >1.5):
        freq[1] +=1
    if(pred_lab[j] <3.5 and pred_lab[j] >2.5):
        freq[2] +=1
    if (pred_lab[j] <4.5 and pred_lab[j] >3.5):
        freq[3] += 1

    if (pred_lab[j] <5.5 and pred_lab[j] >4.5):
        freq[4] += 1
    if (pred_lab[j] <6.5 and pred_lab[j] >5.5):
        freq[5] += 1


print freq

correct = 0


for i in range(len(pred_lab)):
    if(pred_lab[i] < 1):
        pred_lab[i] = 1
    else:
        if(pred_lab[i] > 5):
            pred_lab[i] = 5
        else:
            sub = pred_lab[i] - math.floor(pred_lab[i])
    #if(sub < 0):
        #sub = -sub
            if(sub >= 0.5):
                pred_lab[i] = math.ceil(pred_lab[i])
            else:
                pred_lab[i] = math.floor(pred_lab[i])
    c.write(str(pred_lab[i]) + "\n")
    if(pred_lab[i]==test_labels[i]):
        correct += 1
correctness = (correct * 100) / len(test_labels)



print "CORRECTNESS: "+str(correctness)

#print "ACCURACY SCORE"
#print confusion_matrix(test_labels,pred_lab)
plot_confusion_matrix( cm=confusion_matrix(test_labels, pred_lab) , classes=['1','2','3','4','5'])

c.close()

# The coefficients
print('Coefficients: \n', regressor.coef_)
# The mean squared error
#print np.mean(regressor.predict(test_data)-test_labels)**2
print mean_squared_error(test_labels,regressor.predict(test_data))
#print("Mean squared error: %.2f" % np.mean((regressor.predict(test_data) - test_labels) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regressor.score(test_data, test_labels))


#results  = sm.OLS(train_labels,train_data).fit()
#print results.summary()


# Plot outputs
'''print test_data.shape()
plt.scatter(test_data, test_labels,  color='black')
plt.plot(test_data, regressor.predict(test_data), color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()'''
