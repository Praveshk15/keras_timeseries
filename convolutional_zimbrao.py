from __future__ import print_function
import sys
import json
import numpy as np
import pandas
import math
import matplotlib.pylab as plt
#import talib

seed=7
np.random.seed(seed)  # for reproducibility

from processing import *


from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.optimizers import SGD
from keras.utils import np_utils
from custom_callbacks import CriteriaStopping
from keras.callbacks import CSVLogger, EarlyStopping, ModelCheckpoint, TensorBoard
from hyperbolic_nonlinearities import *
from keras import regularizers
#from hyperbolic_nonlinearities import AdaptativeAssymetricBiHyperbolic, AdaptativeBiHyperbolic, AdaptativeHyperbolicReLU, AdaptativeHyperbolic, PELU
#from keras.layers.advanced_activations import ParametricSoftplus, SReLU, PReLU, ELU, LeakyReLU, ThresholdedReLU


start_time = time.time()

#dataframe = pandas.read_csv('ibov_google_15jun2017_1min_15d.csv', sep = ',', usecols=[1],  engine='python', skiprows=8, decimal='.',header=None)
#dataset = dataframe[1].tolist()

train = pandas.read_csv('minidolar/train.csv', sep = ',',  engine='python', decimal='.',header=0)
test = pandas.read_csv('minidolar/test.csv', sep = ',',  engine='python', decimal='.',header=0)
#dataset = dataframe['fechamento'].tolist()

train_shift = train['shift']
train_target = train['f0']
train_close = train[['v3','v7','v11','v15','v19','v23','v27','v31','v35','v39','v43','v47','v51','v55','v59','v63','v67','v71','v75','v79','v83','v87','v91','v95','v99','v103','v107','v111','v115','v119']]

test_shift = test['shift']
test_target = test['f0']
test_close = test[['v3','v7','v11','v15','v19','v23','v27','v31','v35','v39','v43','v47','v51','v55','v59','v63','v67','v71','v75','v79','v83','v87','v91','v95','v99','v103','v107','v111','v115','v119']]


batch_size = 128
nb_epoch = 4200
patience = 500
look_back = 7

def evaluate_model(model, name, n_layers, ep):
    X_train, X_test, Y_train, Y_test =  np.array(train_close),  np.array(test_close),  np.array(train_target.values.reshape(train_target.size,1)),  np.array(test_target.values.reshape(test_target.size,1))
    X_trainp, X_testp, Y_trainp, Y_testp = X_train+train_shift.values.reshape(train_shift.size,1), X_test+test_shift.values.reshape(test_shift.size,1), Y_train+train_shift.values.reshape(train_shift.size,1), Y_test + test_shift.values.reshape(test_shift.size,1)

    csv_logger = CSVLogger('output/%d_layers/%s.csv' % (n_layers, name))
    es = EarlyStopping(monitor='loss', patience=patience)
    #mcp = ModelCheckpoint('output/mnist_adaptative_%dx800/%s.checkpoint' % (n_layers, name), save_weights_only=True)
    #tb = TensorBoard(log_dir='output/mnist_adaptative_%dx800' % n_layers, histogram_freq=1, write_graph=False, write_images=False)

    
    #sgd = SGD(lr=0.01, momentum=0.9, nesterov=True)

    #optimizer = sgd
    optimizer = "adam"
    #optimizer = "adadelta"

    model.compile(loss='mean_squared_error', optimizer=optimizer)

    # reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #X_train = np.expand_dims(X_train, axis=2)
    #X_test = np.expand_dims(X_test, axis=2)

    history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=ep, verbose=0, validation_split=0.1, callbacks=[csv_logger,es])

    #trainScore = model.evaluate(X_train, Y_train, verbose=0)
    #print('Train Score: %f MSE (%f RMSE)' % (trainScore, math.sqrt(trainScore)))
    #testScore = model.evaluate(X_test, Y_test, verbose=0)
    #print('Test Score: %f MSE (%f RMSE)' % (testScore, math.sqrt(testScore)))

    # make predictions (scaled)
    trainPredict = model.predict(X_train)
    testPredict = model.predict(X_test)
    
    
    # invert predictions (back to original)
    new_predicted = testPredict+test_shift.values.reshape(test_shift.size,1)
    new_train_predicted= trainPredict+train_shift.values.reshape(train_shift.size,1)
    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(new_train_predicted, Y_trainp))
    #trainScore = mean_squared_error(trainPredict, Y_train)
    #print('Train Score: %f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(new_predicted, Y_testp))
    #testScore = mean_squared_error(testPredict, Y_test)
    epochs = len(history.epoch)

    # fig = plt.figure()
    # plt.plot(Y_test[:150], color='black') # BLUE - trained RESULT
    # plt.plot(testPredict[:150], color='blue') # RED - trained PREDICTION
    #plt.plot(Y_testp[:150], color='green') # GREEN - actual RESULT
    #plt.plot(new_predicted[:150], color='red') # ORANGE - restored PREDICTION
    #plt.show()

    return trainScore, testScore, epochs, optimizer

def __main__(argv):
    n_layers = int(argv[0])
    print(n_layers,'layers')

    #nonlinearities = ['aabh', 'abh', 'ah', 'sigmoid', 'relu', 'tanh']
    nonlinearities = ['sigmoid', 'relu', 'tanh']
    #nonlinearities = ['relu']

    with open("output/%d_layers/compare.csv" % n_layers, "a") as fp:
        fp.write("-MINIDOLAR/Convolutional NN\n")

    hals = []

    TRAIN_SIZE = 30
    TARGET_TIME = 1
    LAG_SIZE = 1
    EMB_SIZE = 1
    
    testScore_aux = 999999
    f_aux = 0

    #for name in nonlinearities:
    #for f in np.arange(0.1,2,0.1):
    for f in range(1,2):
        #name=Hyperbolic(rho=0.9)
        name='relu'
        model = Sequential()

        #model.add(Dense(500, input_shape = (TRAIN_SIZE, )))
        #model.add(Activation(name))

        model.add(Conv1D(input_shape = (TRAIN_SIZE, EMB_SIZE),filters=5,kernel_size=2,activation=name,padding='causal',strides=1,
                kernel_regularizer=regularizers.l2(0.01)))
        #model.add(MaxPooling1D(pool_size=2))
        for l in range(n_layers):
            model.add(Conv1D(input_shape = (TRAIN_SIZE, EMB_SIZE),filters=5,kernel_size=2,activation=name,padding='causal',strides=1))
            #model.add(MaxPooling1D(pool_size=1))
        
        model.add(Dropout(0.25))
        model.add(Flatten())

        #model.add(Dense(5))
        #model.add(Dropout(0.25))
        #model.add(Activation(name))
        
        model.add(Dense(1))
        model.add(Activation('linear'))
        #model.summary()

        trainScore, testScore, epochs, optimizer = evaluate_model(model, name, n_layers,nb_epoch)
        # if(testScore_aux > testScore):
        #     testScore_aux=testScore
        #     f_aux = f

        elapsed_time = (time.time() - start_time)
        with open("output/%d_layers/compare.csv" % n_layers, "a") as fp:
            #fp.write("%i,%s,%f,%f,%d,%s --%s seconds\n" % (f, name, trainScore, testScore, epochs, optimizer, elapsed_time))
            fp.write("%s,%f,%f,%d,%s --%s seconds\n" % (name, trainScore, testScore, epochs, optimizer, elapsed_time))
            

        model = None

    #print("melhor parametro: %i" % f_aux)

if __name__ == "__main__":
   __main__(sys.argv[1:])
