import matplotlib.pylab as plt
import pandas
from matplotlib.pylab import sqrt
import numpy as np
from processing import *
from datetime import datetime


fig_width_pt = 406.0  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'ps',
          'axes.labelsize': 10,
          'font.size': 10,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': False,
          'figure.figsize': fig_size}
plt.rcParams.update(params)
# Generate data


dataframe = pandas.read_csv('minidolar/wdo.csv', sep = '|',  engine='python', decimal='.',header=0)

# series = pandas.Series(dataframe['fechamento'].values, index=dataframe['ts'])
# y = np.array(dataframe['fechamento'].tolist())
# # Plot data
# plt.figure(1)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# series[0:100].plot(label='WDOU16')
# #plt.plot(y,'-b')
# plt.xlabel('t')
# plt.ylabel('MINI Dolar')
# plt.legend()
#
# plt.savefig('plots/minidolar.eps')
#

#EMAS
# y = dataframe['fechamento']
#
# ewm5 = y.ewm(span=5, min_periods=5).mean()
# ewm21 = y.ewm(span=21, min_periods=21).mean()
#
#
# plt.figure(2)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(y[0:160])
# plt.plot(ewm5[0:160])
# plt.plot(ewm21[0:160])
# plt.xlabel('t')
# plt.ylabel('MINI Dolar')
# plt.legend(['original', 'EMA5', 'EMA21'])
#
# plt.savefig('plots/emas.eps')
#

#SW exemplo


# y = dataframe['fechamento']
#
# hv, hv_scaler = minMaxNormalize(y[120:140].values.reshape(-1,1))
# lv, lv_scaler= minMaxNormalize(y[50:70].values.reshape(-1,1))
#
# plt.figure(3)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(range(0,20),lv)
# plt.plot(range(30,50),hv)
# plt.legend(['SW #1', 'SW #2'])
# plt.savefig('plots/sw_exemplo.eps')


#AN exemplo
#
#
# y = dataframe['fechamento']
# ewm5 = y.ewm(span=5, min_periods=5).mean()
# serie, scaler = minMaxNormalize((y[0:540]/np.mean(y[0:540])).values.reshape(-1,1)) # um dia (para simplificar usei media)
#
# hv = minMaxNormalizeOver((y[120:140]/ewm5[120]).values.reshape(-1,1), scaler)
# lv= minMaxNormalizeOver((y[50:70]/ewm5[50]).values.reshape(-1,1), scaler)
#
# plt.figure(4)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(range(0,20),lv)
# plt.plot(range(30,50),hv)
# plt.legend(['AN #1', 'AN #2'])
# plt.savefig('plots/an_exemplo.eps')


#MM exemplo


# y = dataframe['fechamento']
# y_1d = y[0:540]
#
# sample, scaler = minMaxNormalize(y_1d[0:90].values.reshape(-1,1))
# y_mm = minMaxNormalizeOver(y_1d.values.reshape(-1,1), scaler)
#
# plt.figure(5)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(y_mm)
# plt.xlabel('t(min)')
# plt.savefig('plots/mm_exemplo.eps')
#

#Dec

# y = dataframe['fechamento']
# y_1d = y[0:540]
#
# maximum = max(y_1d[0:90].values.reshape(-1))
#
# sample = decimalNormalize(y_1d[0:90].values.reshape(-1,1))
# y_dec = decimalNormalizeOver(y_1d.values.reshape(-1,1), maximum)
#
# plt.figure(6)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(y_dec)
# plt.plot(np.ones(540), 'r')
# plt.xlabel('t(min)')
# plt.savefig('plots/dec_exemplo.eps')
#
#
# y_1d_new = decimalDenormalize(y_dec, maximum)


#z-score

# y = dataframe['fechamento']
# y_1d = y[0:540]
#
# sample, scaler = zNormalize(y_1d[0:90].values.reshape(-1,1))
# y_z = zNormalizeOver(y_1d.values.reshape(-1,1), scaler)
#
# y_z_total, sca =  zNormalize(y_1d.values.reshape(-1,1))
# sca.mean_
# np.sqrt(sca.var_)
#
# plt.figure(7)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(y_z)
# plt.plot(y_z_total)
# plt.legend([(r'Z #1 ($\mu =%.2f, \sigma =%.2f$)'% (scaler.mean_,np.sqrt(scaler.var_))), (r'Z #2 ($\mu =%.2f, \sigma =%.2f$)' %(sca.mean_,np.sqrt(sca.var_)))])
# plt.xlabel('t(min)')
# plt.savefig('plots/z_exemplo.eps')
#
#
# y_1d_new = zDenormalize(y_z, scaler)




# Fs = 100
# f = 5
# sample = 100
# x = np.arange(sample)
# y = np.sin(2 * np.pi * f * x / Fs)
# ewm5 = pandas.DataFrame(y).ewm(span=5, min_periods=5).mean()
#
# plt.figure(8)
# plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
# plt.plot(y)
# plt.plot(ewm5)
# plt.plot(np.zeros(len(y)), ':k')
# plt.xlabel('t')
# plt.legend(['sen(t)', 'EMA5'])
# plt.savefig('plots/an_avg_zero_problem.eps')
#




#AN types compare exemplo


y = dataframe['fechamento']
ewm5 = y.ewm(span=5, min_periods=5).mean()

y = np.array(y.iloc[5 - 1:])
ewm5 = np.array(ewm5.iloc[5 - 1:])

X, Y, shift = split_into_chunks_adaptive_type(y[0:540], ewm5[0:540], 20, 1, 1, binary=False,
                                             scale=True, type='o')
X, Y, shift = np.array(X), np.array(Y), np.array(shift)


X2, Y2, shift2 = split_into_chunks_adaptive(y[0:540], ewm5[0:540], 20, 1, 1, binary=False,
                                             scale=True)

X2, Y2, shift2 = np.array(X2), np.array(Y2), np.array(shift2)


serie, scaler = minMaxNormalize((X[0:540]).reshape(-1,1))


serie2, scaler2 = minMaxNormalize((X2[0:540]).reshape(-1,1))


hv = minMaxNormalizeOver((X[116]).reshape(-1,1), scaler)
lv = minMaxNormalizeOver((X[46]).reshape(-1,1), scaler)

hv2 = minMaxNormalizeOver((X2[116]).reshape(-1,1), scaler2)
lv2 = minMaxNormalizeOver((X2[46]).reshape(-1,1), scaler2)


plt.figure(9)
plt.clf()
# plt.axes([0.125,0.2,0.95-0.125,0.95-0.2])
plt.plot(range(0,20),lv - lv2)
plt.plot(range(30,50),hv - hv2)
# plt.plot(range(0,20),X[46])
# plt.plot(range(0,20),X2[46])
# plt.plot(range(30,50),X[116])
# plt.plot(range(30,50),X2[116])
plt.legend(['AN - AND #1', 'AN - AND #2'])
plt.savefig('plots/an_compare.eps')




#USD-BRL
# dataframe = pandas.read_csv('compare_dolar.csv', sep = ',',  engine='python', decimal='.', header = None, names=['w', 'k', 'activation', 'normalization', 'train', 'test', 'optimizer', 'epochs'])
#
#
# dataframe = dataframe.sort_values(['w','normalization','k'])
#
# df_an = dataframe.loc[dataframe['normalization'] == 'AN']
# df_sw = dataframe.loc[dataframe['normalization'] == 'SW']
#
# for w in range(2,16):
#     plt.clf()
#     plt.plot(range(2,30), df_an.loc[dataframe['w'] == w]['test'], 'bo')
#     plt.plot(range(2,30), df_sw.loc[dataframe['w'] == w]['test'], 'ro')
#     plt.legend(['AN','SW'])
#     plt.title('Model RMSE with Window size '+str(w)+ ' for MINI Dolar')
#     plt.ylabel('loss')
#     plt.xlabel('k')
#     plt.savefig('plots/dolar_rmse_k_w_'+str(w)+'.eps')
#
#
# for w in range(2,16):
#     plt.clf()
#     plt.plot(range(2,30), df_an.loc[dataframe['w'] == w]['train'], 'bo')
#     plt.plot(range(2,30), df_sw.loc[dataframe['w'] == w]['train'], 'ro')
#     plt.legend(['AN','SW'])
#     plt.title('Model Train RMSE with Window size '+str(w)+ ' for MINI Dolar')
#     plt.ylabel('loss')
#     plt.xlabel('k')
#     plt.savefig('plots/dolar_train_rmse_k_w_' + str(w) + '.eps')




#BTC
# dataframe = pandas.read_csv('compare_btc.csv', sep = ',',  engine='python', decimal='.', header = None, names=['w', 'k', 'activation', 'normalization', 'train', 'test', 'optimizer', 'epochs'])
#
#
# dataframe = dataframe.sort_values(['w','normalization','k'])
#
# df_an = dataframe.loc[dataframe['normalization'] == 'AN']
# df_sw = dataframe.loc[dataframe['normalization'] == 'SW']
#
# for w in range(2,16):
#     plt.clf()
#     plt.plot(range(2,30), df_an.loc[dataframe['w'] == w]['test'], 'bo')
#     plt.plot(range(2,30), df_sw.loc[dataframe['w'] == w]['test'], 'ro')
#     plt.legend(['AN','SW'])
#     plt.title('Model RMSE with Window size '+str(w)+ ' for BTC')
#     plt.ylabel('loss')
#     plt.xlabel('k')
#     plt.savefig('plots/btc_rmse_k_w_' + str(w) + '.eps')
