import statistics
import numpy as np
import pandas as pd


def mixSampling(data, column, bins=100, target_samples="mean"):
	"""
	This function will down-up sampling data to mean samples of column's data.
	data: pandas DataFrame
	column: name of column in DataFrame
	"""
	is_warned = False
	# Get target column from DataFrame
	target = data[column].to_numpy()
	# Add Y_bin to DataFrame
	bin_range = np.linspace(target.min(), target.max() + 1, bins + 1, dtype=int)
	Y_bin = np.digitize(target, bin_range)
	data["Y_bin"] = Y_bin
	data_columns = data.columns
	
	queries = {}
	sample_nums = {}
	for bin_index in range(1, bins + 1):
		queries[bin_index] = data.query("Y_bin == {}".format(bin_index)).to_numpy()
		sample_nums[bin_index] = queries[bin_index].shape[0]
		
	# Get target samples
	if isinstance(target_samples, str):
		if target_samples == "mean":
			target_samples = statistics.mean(sample_nums.values())
		elif target_samples == "max":
			target_samples = max(sample_nums.values())
		elif target_samples == "min":
			target_samples = min(sample_nums.values())
		elif target_samples == "median":
			target_samples = statistics.median(sample_nums.values())
		else:
			target_samples = statistics.mean(sample_nums.values())
	target_samples = int(target_samples)
	
	# Get samplings size
	samplings_len = target_samples * bins
		
	samplings = np.zeros([samplings_len, len(data_columns)])
	start_index = 0
	for bin_index in range(1, bins + 1):
		end_index = start_index + target_samples
		try:
			if sample_nums[bin_index] > target_samples:
				# Down sampling
				indices = np.random.permutation(target_samples)
				samplings[start_index:end_index] = queries[bin_index][indices]
			elif sample_nums[bin_index] < target_samples:
				# Up sampling
				indices = np.random.randint(queries[bin_index].shape[0], size=(target_samples - queries[bin_index].shape[0]))
				samplings[start_index:end_index] = np.concatenate([queries[bin_index], queries[bin_index][indices]], axis=0)
			else:
				samplings[start_index:end_index] = queries[bin_index]
		except:
			if not is_warned:
				print("[Warning] bins = {} is too much, please decrease the number to get better result.".format(bins))
				is_warned = True
		start_index = end_index
		
	samplings = pd.DataFrame(samplings, columns=data_columns)
	samplings = samplings.query("Y_bin != 0").drop(columns="Y_bin")
	
	return samplings
	

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	
	data = pd.read_pickle("../../datasets/dataset_verysmall_hp100000.pkl")
	samplings = mixSampling(data, "attack_num", target_samples=900)
	samplings.to_pickle("../../datasets/dataset_verysmall_hp100000_balanced_4.pkl")
	plt.subplot(2, 1, 1)
	plt.hist(data["attack_num"], bins=100)
	plt.subplot(2, 1, 2)
	plt.hist(samplings["attack_num"], bins=100)
	plt.show()
