# mlp for regression
from numpy import sqrt
from pandas import read_csv
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import BatchNormalization
from matplotlib import pyplot

# load the dataset
path = '/home/wafiq/Prediction/data/dummy_data_reg.csv'
df = read_csv(path, header=None)
# split into input and output columns
X, y = df.values[:, :-1], df.values[:, -1]
# split into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# determine the number of input features
n_features = X_train.shape[1]
# define model
model = Sequential()
model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(4, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(2, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(1))

model.summary()

plot_model(model, 'model.png', show_shapes=True)

# compile the model
model.compile(optimizer='adam', loss='mse')
# fit the model
history = model.fit(X_train, y_train, epochs=250, batch_size=32, verbose=0)
# evaluate the model
pyplot.title('Learning Curves')
pyplot.xlabel('Epoch')
pyplot.ylabel('mse')
pyplot.plot(history.history['loss'], label='train')
# pyplot.plot(history.history['mse'], label='val')
pyplot.legend()
pyplot.show()

error = model.evaluate(X_test, y_test, verbose=0)
print('MSE: %.3f, RMSE: %.3f' % (error, sqrt(error)))
# make a prediction
row = [0.36605901362132276,0.5355695879662148,0.09837139841246248]
yhat = model.predict([row])
print('Predicted: %.3f' % yhat)
model.save('model.h5')