from pandas import read_csv
import pandas as pd
import numpy as np
import statsmodels.tsa.arima_model as smt
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import os


path = os.getcwd()+'/forecast'
GENRE = "thriller"
FILE1 = path+'/'+'forecast_'
#FILE1 = path+'/forecast_gross_'
#FILE1 = 'forecast_'
FILE = FILE1+GENRE+".csv"


def tsplot(y, lags=None, figsize=(10, 8), style='bmh'):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    with plt.style.context(style):
        fig = plt.figure(figsize=figsize)
        # mpl.rcParams['font.family'] = 'Ubuntu Mono'
        layout = (3, 2)
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        qq_ax = plt.subplot2grid(layout, (2, 0))
        pp_ax = plt.subplot2grid(layout, (2, 1))

        y.plot(ax=ts_ax)
        ts_ax.set_title('Time Series Analysis Plots')
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax, alpha=0.5)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.5)
        sm.qqplot(y, line='s', ax=qq_ax)
        qq_ax.set_title('QQ Plot')
        scs.probplot(y, sparams=(y.mean(), y.std()), plot=pp_ax)

        plt.tight_layout()
    return





series = read_csv(FILE, header=0, parse_dates=[0], index_col=0, squeeze=True)
y = series.values
history = y[0:len(y)-12]
x = [float(q) for q in history]
test = y

#x = np.diff(x,n=3)
#lrets = np.log(series/series.shift(1)).dropna()
#print lrets

#seaborn.tsplot( np.diff(x,n=4))

#plt.show()

#_ = tsplot(np.diff(x,n=2))
#plt.show()




tmp_aic = 0
tmp_mdl = 0
best_aic = np.inf
best_order = None
best_mdl = None
bestmae = np.inf



pq_rng = range(15) # [0,1,2,3,4]
d_rng = range(15) # [0,1]
d = 0 # we set d = 0 because the behaviour with d = 1 or greater is bad
for i in pq_rng:
    for j in pq_rng:
        for k in range(2):
            try:
                tmp_mdl = smt.ARIMA( x, order=(i,k,j)).fit(disp = 0,method='css',trend='c',maxiter=10000,solver = 'bfgs')
                output = tmp_mdl.forecast(12)
                yhat = output[0]
                predictions = x[0:len(y)-12]
                for l in yhat:
                    predictions.append(l)
                mae = mean_absolute_error(test,predictions)
                print mae
                #tmp_aic = tmp_mdl.aic
                #if tmp_aic < best_aic:
                if mae < bestmae:
                    #best_aic = tmp_aic
                    bestmae = mae
                    best_order = (i, k, j)
                    best_mdl = tmp_mdl
            except:
                print "eccezione"
                continue


print('aic: {:6.5f} | order: {}'.format(bestmae, best_order))

out_file = open(str(FILE1)+str(GENRE)+"_parameters.txt","w")
out_file.write(str(best_order) )
out_file.close()
# aic: -11518.22902 | order: (4, 0, 4)

# ARIMA model resid plot
#_ = tsplot( best_mdl.resid , lags=30)






"""
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


#series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
series = read_csv(FILE, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
X = series.values


#size = int( len(X) )
#train, test = X[0:size], X[size:len(X)]

size = int( len(X) )
train, test = X[ 0 : size ], X[ 0 : size ]
history = [float(x) for x in train]
predictions = list()

for t in range(len(test)):
    model = ARIMA(history, order=(P_VAR,D_VAR,Q_VAR))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    # predictions has all the prediction extracted from the forecast method
    predictions.append(yhat)
    obs = test[t]
    # hystory has all the values
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))

error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)


# plot
COUNTER -= 1
new_predictions = 14
for i in range(new_predictions):

    if COUNTER % 12 == 0 :
        LAST_YEAR += 1
        date_list.append( str(LAST_YEAR) )
    else :
        date_list.append("")
    COUNTER+=1

    model = ARIMA(history, order=(P_VAR,D_VAR,Q_VAR))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)

    history.append(yhat)

pyplot.xticks( range(len(date_list)), date_list )
pyplot.plot(test)
pyplot.title(str(FILE)+"p="+str(P_VAR)+"d="+str(D_VAR)+"q="+str(Q_VAR))
pyplot.plot(predictions, color='red')
pyplot.legend(['Real Data', 'Predicted Data'] ,loc="upper center",
           columnspacing=1.0, labelspacing=0.0,handletextpad=0.0,handlelength=1.5,fancybox=True,shadow=True )

pyplot.show()
"""