from __future__ import division
import numpy as np
from Tkinter import *
import json
import io
import unicodecsv as csv
#import csv


#file = open("moviesTest-1970.txt",'r')
act = open("invertedIndexActorsWeightedAll.txt",'r')
dir = open("invertedIndexDirectorsWeightedAll.txt", 'r')
wri = open("invertedIndexWritersWeightedAll.txt", 'r')
#line = file.readline()
lact = act.readline()
ldir = dir.readline()
lwri = wri.readline()
#gson = json.loads(line)
jact = json.loads(lact)
jdir = json.loads(ldir)
jwri = json.loads(lwri)
#file.close()
act.close()
dir.close()
wri.close()








class Test:
    def calcolaMedie(self,actors,directors,writers):
        mediaAct = 0
        mediaDir = 0
        mediaWri = 0
        for elem in actors:
            print elem
            mediaAct += float(jact.get(elem).get("rating"))
        for elem in directors:
            mediaDir += float(jdir.get(elem).get("rating"))
        for elem in writers:
            mediaWri += float(jwri.get(elem).get("rating"))
        mediaAct = float(mediaAct/len(actors))
        mediaDir = float(mediaDir/len(directors))
        mediaWri = float(mediaWri/len(writers))
        return mediaAct,mediaDir,mediaWri


    #### extract data from the json files ####
    def readData(self,filename):
        file = open(filename, 'r')
        line = file.readline()
        print line
        gson = json.loads(line)
        file.close()
        vector = []
        input = []
        labels = []
        titles = []
        #indice = 0
        for elem in gson:
            #titles.append(gson.get(elem).get("title"))
            actors = gson.get(elem).get("actors")
            directors = gson.get(elem).get("director")
            writers = gson.get(elem).get("writer")
            input.append([actors,directors,writers])
            #imdbRating = float(gson.get(elem).get("imdbRating"))
            mediaAct, mediaDir, mediaWri = self.calcolaMedie(actors, directors, writers)
            vect = [1,mediaAct, mediaDir, mediaWri]
            vector.append(vect)
            #labels.append(int(imdbRating))  ## CAST PER CLASSI DISCRETE ##
        data = np.array(vector)
        #labels = np.array(labels)
        #train_data,test_data,train_labels,test_labels = train_test_split(data,labels, train_size= 0.5)
        #return train_data, train_labels,test_data,test_labels
        print "lettura terminata"
        return data,input





    def hypothesis(self,x,theta):
        l_theta = []
        for i in range(len(theta)):
            #print theta[i]
            thetaX = x.dot(theta[i])#  wx
            thetaX_exp = np.exp(thetaX)  # exp(wx)
            l_theta.append(thetaX_exp)
        l_theta = np.array(l_theta)
        #print np.shape(l_theta)
        thetaX_exp_sum = np.sum(l_theta)  # sum of exp(wx)
        #print thetaX_exp_sum
        p = l_theta.T / thetaX_exp_sum  # 5xlen(x) predicted results
        if np.isinf(p).any():  # deal with overflow in results.
            inf_idx = np.isinf(p)  # idx where overflow occurs
            val = np.sum(p, 0) / np.sum(inf_idx, 0) * inf_idx  # values to be used to substitution
            p[inf_idx] = val[inf_idx]  # substitute values
        return p.T




#### predict the labels for a set of observations ####
    def test(self,data,theta):
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
            pred_lab.append(ind+1)
        '''for j in range(len(labels)):
            if labels[j] == pred_lab[j]:
                correct += 1
        correctness = (correct * 100) / len(labels)'''
        return pred_lab


#### predict the label for a single observation ####
    def singleTest(self,data,theta):
        max = 0
        ind = 0
        p = self.hypothesis(data,theta)
        for k, x in enumerate(p):
            if x > max:
                max = x
                ind = k
        pred_lab = ind+1
        return pred_lab

#### reads the theta from file ####
    def getTheta(self):
        filenameTheta = "thetas.txt"
        fileTheta = open(filenameTheta, 'r')
        lines = fileTheta.readlines()
        theta = []
        for line in lines:
            line = line.replace("\n", "")
            line = line.rstrip()
            l = line.split(' ')
            for i in range(len(l)):
                l[i] = float(l[i])
            theta.append(l)
        theta = np.array(theta)
        return theta

#### print the results on a file in the case of a batch prediction ####
    def results(self,fileResult,input,pred_lab):
        fileRes = open(fileResult,'w')
        writer = csv.writer(fileRes,delimiter = ',')
        writer.writerow(("ACTORS","DIRECTORS","WRITERS","PREDICTED"))
        for i in range(len(pred_lab)):
            writer.writerow((input[i][0],input[i][1],input[i][2],pred_lab[i]))
            #writer.writerow(unicode(titles[i]) + unicode("\t") + unicode(labels[i]) + unicode("\t") + unicode(
                #pred_lab[i]) + unicode("\n"))
        fileRes.close()


#### initialization for a set of predictions ####
    def init2(self,filename,fileResult):

        data,input =self.readData(filename)
        theta = self.getTheta()
        pred_lab = self.test(data,theta)
        self.results(fileResult,input,pred_lab)
        #print "ACCURACY ON TEST FILE IS: " + str(correctness) + "% "
        return 1



#### initialization for a single prediction ####
    def init(self,actors,directors,writers):
        act =  [x for x in actors if x != "None"]
        dir = [x for x in directors if x != "None"]
        wri = [x for x in writers if x != "None"]
        mediaAct,mediaDir,mediaWri = self.calcolaMedie(act,dir,wri)
        data = [1,mediaAct,mediaDir,mediaWri]
        data = np.array(data)
        #data,labels = self.readData()
        filenameTheta = "thetas.txt"
        fileTheta = open(filenameTheta,'r')
        lines = fileTheta.readlines()
        theta = []
        for line in lines:
            line = line.replace("\n","")
            line = line.rstrip()
            l = line.split(' ')
            for i in range(len(l)):
                l[i] = float(l[i])
            theta.append(l)
        theta = np.array(theta)
        label = self.singleTest(data,theta)
        return label
        #print " LABEL PREDICTED: "+ str(label)






