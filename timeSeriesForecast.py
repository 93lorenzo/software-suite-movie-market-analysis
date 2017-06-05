from pandas import read_csv
from pandas import datetime
import os
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import *
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np

date_list = []
COUNTER = 0
LAST_YEAR = 0

"""
    p: The number of lag observations included in the model, also called the lag order.
    d: The number of times that the raw observations are differenced, also called the degree of differencing.
    q: The size of the moving average window, also called the order of moving average.
"""
P_VAR = 14
D_VAR = 0
Q_VAR = 2

path = os.getcwd()+'/forecast'
FILE1 = path+'/forecast_gross_'
#FILE1 =path+'/'+'forecast_'
#FILE1 ='forecast_'
GENRE = "thriller"
FILE2 = '.csv'

FILE = FILE1+GENRE+FILE2
def parser(x):

    global COUNTER
    global date_list
    global LAST_YEAR

    if COUNTER % 12 == 0:
        if COUNTER == 0 :
            date_list.append(str(x)[2:6])
        else:
            date_list.append( str(x)[:4]+"\n"+str(x)[5:7] )
            if LAST_YEAR < int( str(x)[:4] ) :
                LAST_YEAR = int(str(x)[:4])

    else:
        date_list.append("")

    COUNTER+=1
    return datetime.strptime(x, '%Y-%m')

### get the time series ###
series = read_csv(FILE, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values

#X = np.diff(X,1)


'''# calc the trendline
z = np.polyfit(range(192),X, 1)
#print z
p = np.poly1d(z)
#pyplot.xticks(range(192),range(192))

line = []
for a in range(192):
    line.append(p(a))

pyplot.plot(np.array(line),'r')
pyplot.plot(X,'b')
#pyplot.plot(X,p(X),"k")

pyplot.show()'''





#### the train contains all the data except the last 12 months ####
size = int( len(X) )
train, test = X[ 0 : size-12], X[ 0 : size ]
history = [float(x) for x in train]

#plot_pacf(train)
#pyplot.show()

#### create the model ####
model = ARIMA(train, order=(P_VAR,D_VAR,Q_VAR))
#print model.geterrors(X)
#try:
#### fit the model ####
model_fit = model.fit(disp=0,method='css', trend='c',maxiter=10000,solver = 'bfgs')

#except Exception:
 #   pass
# model could be css-mle mle css


print "model fitting completed"


new_predictions = 12
history2 = history
predictions = history

for i in range(new_predictions):

    if COUNTER % 12 == 0 :
        LAST_YEAR += 1
        date_list.append( str(LAST_YEAR) )
    else :
        date_list.append("")
    COUNTER+=1

#### predict the forecast of the next 12 months ####
output = model_fit.forecast(new_predictions)
yhat = output[0]
for x in yhat:
    predictions.append(x)



print mean_squared_error(test,predictions)
print mean_absolute_error(test,predictions)

#### plot the predictions given by the model ( in red ), the real data ( in blue ) and the training data ( in black )   ####
pyplot.xticks( range(len(date_list)), date_list )
pyplot.title(str(FILE)+"p="+str(P_VAR)+"d="+str(D_VAR)+"q="+str(Q_VAR))
pyplot.plot(predictions, color='red')
pyplot.plot(test,'b')
pyplot.plot(train,'k')
pyplot.legend(['Real Data', 'Predicted Data'] ,loc="upper center",
           columnspacing=1.0, labelspacing=0.0,handletextpad=0.0,handlelength=1.5,fancybox=True,shadow=True )

#### fit the predictions to a line ####
z = np.polyfit(range(len(predictions)),predictions, 1)
z2 = np.polyfit(range(len(test)),test, 1)
#### get the equation of the line ####
p = np.poly1d(z)
p2 = np.poly1d(z2)

#### get len(predictions) points on the line ####
line = []
line2 = []
for a in range(len(predictions)):
    line.append(p(a))
    line2.append(p2(a))

#### plot the lines ( in yellow the line of the predictions, in magenta the line of the test data) ####
pyplot.plot(np.array(line),'y')
pyplot.plot(np.array(line2),'m')
#pyplot.plot(X,p(X),"k")


pyplot.show()
