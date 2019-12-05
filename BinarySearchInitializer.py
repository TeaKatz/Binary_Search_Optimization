import os
import joblib
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LeakyReLU
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler


class SequenceDense(Model):
	def __init__(self):
		super().__init__()
		self.dense_1 = Dense(64, activation=LeakyReLU())
		self.dense_2 = Dense(1, activation="relu")

	def call(self, inputs):
		output = self.dense_1(inputs)
		output = self.dense_2(output)

		return output


class BinarySearchInitializer:
	def __init__(self, checkpoint_dir=None, scalers_dir=None):
		self.checkpoint_dir = checkpoint_dir
		self.scalers_dir = scalers_dir
		self.model = SequenceDense()
		self.scaler_x = MinMaxScaler()
		self.scaler_y = MinMaxScaler()
		self.error = 0.05 * 10000

		if self.checkpoint_dir is not None:
			self.load_weights()
		if self.scalers_dir is not None:
			self.load_scalers()
		
	def load_weights(self):
		assert self.model is not None, "Must build model before call this function."
		self.model.load_weights(self.checkpoint_dir)
		
	def load_scalers(self):
		self.scaler_x = joblib.load(os.path.join(self.scalers_dir, "X_scaler.pkl"))
		self.scaler_y = joblib.load(os.path.join(self.scalers_dir, "Y_scaler.pkl"))
		
	def train(self, X, Y, epochs=10, batch_size=32):
		X_scaled = self.scaler_x.fit_transform(X)
		Y_scaled = self.scaler_y.fit_transform(Y)
		self.model.fit(X_scaled, Y_scaled, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=1)
		
	def predict(self, X):
		X_scaled = self.scaler_x.transform(X)
		Y_scaled = self.model.predict(X_scaled)
		pred = self.scaler_y.inverse_transform(Y_scaled)
		
		return pred
		
		
if __name__ == "__main__":
	import pandas as pd
	
	dataset = pd.read_pickle("./Datasets/dataset_verysmall_balanced.pkl")
	X = dataset.drop(columns=["monster_num", "attack_num"]).to_numpy().reshape([-1, 1002])
	Y = dataset["attack_num"].to_numpy().reshape([-1, 1])
	
	initializer = BinarySearchInitializer(checkpoint_dir="./Save/SequenceDenseBalanced", scalers_dir="./Save")
	predict = initializer.predict(X[1].reshape([1, 1002]))
	print(predict)
	print(Y[1])
