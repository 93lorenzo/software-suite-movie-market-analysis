from __future__ import division
import numpy as np
import json
import math
import scipy
import csv
from scipy.optimize import fmin
from scipy.optimize import minimize
import scipy.sparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import hinge_loss
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


'''files = open("movies.txt",'r')
liness = files.readline()
jmove = json.loads(liness)
files.close()
csvf  =csv.writer(open("dataset3.csv",'w'))
#csvf = open("dataset3.csv",'w')'''


#######################################################################################
'''MILIONI30 = 30000000
MILIONI100 = 100000000
MILIONI10 = 10000000
MILIONI250 = 250000000
MILIONI50 = 50000000
MILIONI500  = 500000000
MILIONI750  = 750000000
MILIARDO = 1000000000
MILIONI25 = 25000000
MILIONI150 = 150000000

LAB_MILIONI100 = 3
LAB_MILIONI50 =2
LAB_MILIARDO = 1
LAB_MILIONI750 = 2
LAB_MILIONI500 = 1
LAB_MILIONI250 = 1
LAB_MILIONI25 = 3
LAB_MILIONI10 = 4
LAB_MILIONI150 = 2
LAB_MILIONI = 5
LAB_MILIONI30 = 5'''






class LogisticRegression:
    '''index1 = 0
    index2 = 0
    index3 = 0
    index4 = 0
    index5 = 0'''

    def __init__(self,N,M,method,alpha):
        self.N,self.M = N,M     ## NUMERO CLASSI, ELEMENTI PER OSSERVAZIONE ##
        self.method = method    ## Methodo di Minimizzazione ##
        self.alpha = alpha      ## Learning Rate: Non utilizzato ##

    ## Calcola le medie dei ratings ##
    def calcolaMedie(self,actors,directors,writers):
        mediaAct = 0
        mediaDir = 0
        mediaWri = 0
        for elem in actors:
            mediaAct += float(jact.get(elem).get("rating"))
        for elem in directors:
            mediaDir += float(jdir.get(elem).get("rating"))
        for elem in writers:
            mediaWri += float(jwri.get(elem).get("rating"))
        mediaAct = float(mediaAct/len(actors))
        mediaDir = float(mediaDir/len(directors))
        mediaWri = float(mediaWri/len(writers))


        return mediaAct,mediaDir,mediaWri

        ## Estrae dati dai json per calcolare le medie dei ratings ##
    '''def readDatac(self):
        vector = []
        labels = []
        indice = 0
        for elem in jmove:
            print elem
            try:
                actors = jmove.get(elem).get("actors")
                directors = jmove.get(elem).get("director")
                print directors
                writers = jmove.get(elem).get("writer")
                imdbRating = float(jmove.get(elem).get("imdbRating"))

                mediaAct, mediaDir, mediaWri = self.calcolaMedie(actors, directors, writers)
                vect = [1, mediaAct, mediaDir, mediaWri]
                #vector.append(vect)
                #labels.append(int(imdbRating))  ## CAST PER CLASSI DISCRETE ##
                csvf.writerow((1, mediaAct, mediaDir, mediaWri, imdbRating))
            except:
                continue
        #data = np.array(vector)
        #labels = np.array(labels)
        #train_data, test_data, train_labels, test_labels = train_test_split(data, labels, train_size=0.05)
       # return train_data, train_labels, test_data, test_labels'''





    ## Estrae dati dai json per calcolare le medie dei ratings ##
    def readData(self):
        vector = []
        labels = []
        indice = 0
        for elem in gson:
            actors = gson.get(elem).get("actors")
            directors = gson.get(elem).get("director")
            writers = gson.get(elem).get("writer")
            imdbRating = int(float(gson.get(elem).get("imdbRating")))
            mediaAct, mediaDir, mediaWri = self.calcolaMedie(actors, directors, writers)
            vect = [1,mediaAct, mediaDir, mediaWri]
            vector.append(vect)
            labels.append(int(imdbRating))  ## CAST PER CLASSI DISCRETE ##
        data = np.array(vector)
        labels = np.array(labels)
        train_data,test_data,train_labels,test_labels = train_test_split(data,labels, train_size= 0.1)
        return train_data, train_labels,test_data,test_labels


    def readDataGross(self):
        vector = []
        labels = []
        indice = 0
        files = open("datasetGross2.csv",'w')
        writer = csv.writer(files)
        for elem in gson:
            gross = int(gson.get(elem).get("gross"))
            actors = gson.get(elem).get("actors")
            directors = gson.get(elem).get("director")
            writers = gson.get(elem).get("writer")
            imdbRating = float(gson.get(elem).get("imdbRating"))

            mediaAct, mediaDir, mediaWri = self.calcolaMedie(actors, directors, writers)
            vect = [1,mediaAct, mediaDir, mediaWri,imdbRating]
            vector.append(vect)
            if(gross >= MILIONI250):
                label = LAB_MILIONI250
                labels.append(LAB_MILIONI250)  ## CAST PER CLASSI DISCRETE ##
                self.index1+=1
            else:
                if(gross >= MILIONI50):
                    label = LAB_MILIONI50
                    labels.append(LAB_MILIONI50)
                    self.index2+=1
                else:
                    if(gross >= MILIONI25):
                        label = LAB_MILIONI25
                        labels.append(LAB_MILIONI25)
                        self.index3+=1
                    else:
                        if(gross >= MILIONI10):
                            label = LAB_MILIONI10
                            labels.append(LAB_MILIONI10)
                            self.index4 +=1
                        else:
                            label = LAB_MILIONI
                            labels.append(LAB_MILIONI)
                            self.index5 += 1
            writer.writerow((1,mediaAct, mediaDir, mediaWri,imdbRating,label))
        print labels
        data = np.array(vector)
        labels = np.array(labels)
        train_data,test_data,train_labels,test_labels = train_test_split(data,labels, train_size= 0.25)
        return train_data, train_labels,test_data,test_labels


    '''def readDataRating(self):
        vector = []
        labels = []
        indice = 0
        for elem in gson:
            actors = gson.get(elem).get("actors")
            directors = gson.get(elem).get("director")
            writers = gson.get(elem).get("writer")
            imdbRating = float(gson.get(elem).get("imdbRating"))
            gross = float(gson.get(elem).get("gross"))/10**8
            mediaAct, mediaDir, mediaWri = self.calcolaMedie(actors, directors, writers)
            vect = [1, mediaAct, mediaDir, mediaWri, gross]
            vector.append(vect)
            labels.append(imdbRating)  ## CAST PER CLASSI DISCRETE ##
        data = np.array(vector)
        labels = np.array(labels)
        train_data,test_data,train_labels,test_labels = train_test_split(data,labels, train_size= 0.7)
        return train_data, train_labels,test_data,test_labels'''


    ## x e' una osservazione, thetai e' l'i-esima lista di theta ( dim(x) = dim(thetai) ) ##
    def hypothesis(self,x,theta):
        l_theta = []
        for i in range(len(theta)):
            thetaX = x.dot(theta[i])    ## wx ##
            thetaX_exp = np.exp(thetaX)  ## exp(wx)##
            if np.isinf(thetaX_exp):
                print "overflow"
                ###prova a mettere una matrice con probabilita tutte uguali in caso di overflow
            l_theta.append(thetaX_exp)
        l_theta = np.array(l_theta)
        thetaX_exp_sum = np.sum(l_theta)  ## sum of exp(wx) ##
        p = l_theta.T / thetaX_exp_sum  ## 5xlen(x) predicted results ##
        #print np.sum(p)
        '''if np.isinf(p).any():  ## deal with overflow in results ##
            inf_idx = np.isinf(p)  ## idx where overflow occurs ##
            val = np.sum(p, 0) / np.sum(inf_idx, 0) * inf_idx ## values to be used to substitution ##
            p[inf_idx] = val[inf_idx]  ## substitute values ##'''
        return p.T

    ## Calcolo la Derivata della Funzione di Costo ##
    '''def costFunctionDerivative(self,data,labels,theta,j):
        m = len(data)
        derivative = 0
        for i in range(m):
            p = self.hypothesis(data[i],theta)
            if labels[i] == j+1:
                derivative += data[i] * (1 - p[j])
            else:
                derivative += data[i] * (0 - p[j])
        return -((self.alpha/m)*derivative)'''

    ## Calcolo la Funzione di Costo ##
    def costFunction(self,theta):
        theta = theta.reshape((self.N, self.M))
        cost = 0
        m = len(data)
        for i in range(m):
            p = self.hypothesis(data[i],theta)
            for j in range(0,len(theta)):
                if labels[i] == j+1:    ## NB: le labels vanno da 1-10, mentre il range da 0-9 ##
                    try:
                        cost += math.log(p[j])
                    except Exception:
                        cost+= 0
        return -(cost/m)

    ## Scrivo theta su file ##
    def printOnFile(self,theta):
        nome = "thetas.txt"
        f = open(nome,'w')
        t = list(theta)
        for i in range(len(t)):
            for j in range(len(t[i])):
                f.write(str(t[i][j])+" ")
            f.write("\n")
        f.close()

    ## Quante labels Corrette? ##
    def test(self,data,labels,theta):
        pred_lab = []
        correct = 0
        for i in range(len(data)):
            p = self.hypothesis(data[i], theta)
            max = 0
            ind = 0
            for k, x in enumerate(p):
                if x > max:
                    max = x
                    ind = k
            pred_lab.append(ind + 1)

        for j in range(len(labels)):
            c.write(str(labels[j])+" "+str(pred_lab[j])+"\n")
            if labels[j] == pred_lab[j]:
                correct += 1
        correctness = (correct * 100) / len(labels)
        return correctness,pred_lab







N,M = 5,4       ## N = Numero di Classi, M = Dimensione Osservazione ##
alpha = 0.01    ## Learning Rate ##
method = 'BFGS' ## Minimization Algorithm ##
logReg = LogisticRegression(N=N,M=M,method=method,alpha=alpha)  ## Creo Oggetto Classe ##


#logReg.readDatac()
#print "fatto"

theta = np.random.normal(size = (N,M))  ## Scelgo casualmente theta da una Distribuzione Normale ##

data,labels,test_data,test_labels = logReg.readData()   ## Leggo dati da file e li splitto in train/test ##
'''print "index 1:" + str(logReg.index1)
print "index 2:" + str(logReg.index2)
print "index 3:" + str(logReg.index3)
print "index 4:" + str(logReg.index4)
print "index 5:" + str(logReg.index5)'''

res = minimize(logReg.costFunction, theta, method=method)    ## Minimizzo Funzione di Costo ##

success = res.success  ## Success dice se la minimizzazione e' stata completata con successo ##

message = res.message   ## Message dice perche' la minimizzazione e' terminata ##

print "RESULTS FOR "+str(method)+" METHOD"
print "OPTIMIZATION FOR " +str(theta.shape)
print " MINIMIZATION COMPLETED. EXITED SUCCESSFULLY: "+ str(success)
print " BECAUSE OF: "+str(message)

theta = res.x   ## x e' il risultato della minimizzazione ##

theta = theta.reshape((N,M))    ## Il metodo minimize tende a effettuare reshape dei parametri, quindi li riporto ##
                                ## alla dimensione originale ##

c = open("ciao.txt", 'w')

correctness,pred_lab = logReg.test(data,labels,theta)    ## Quante predizioni corrette sul training set? ##

#print np.mean(regressor.predict(test_data)-test_labels)**2

#print np.mean(pred_lab - labels)


print "TIME TAKEN FOR TRAINING: "+str(time.time() - start_time)

print "ACCURACY ON TRAINING SET IS: " + str(correctness) + "% "

mseTrain = mean_squared_error(labels,pred_lab)

print "MEAN SQUARED ERROR ON TRAINING SET IS: " + str(mseTrain) + "% "


print "CONFUSION MATRIX ON TRAINING SET:"
print confusion_matrix(labels,pred_lab)

#print "THETA :"
#print list(theta)

start_time = time.time()

correctness,pred_lab = logReg.test(test_data,test_labels,theta)  ## Quante predizioni corrette sul test set? ##

c.close()
print "TIME TAKEN FOR TEST: "+str(time.time() - start_time)



print "ACCURACY ON TEST SET IS: " + str(correctness) + "% "

mseTest = mean_squared_error(test_labels,pred_lab)

print "MEAN SQUARED ERROR ON TEST SET IS: " + str(mseTest) + "% "

print "CONFUSION MATRIX ON TEST SET:"
print confusion_matrix(test_labels,pred_lab)



#logReg.printOnFile(theta)   ## Scrivo theta su file ##