import pandas as pd
import matplotlib.pyplot as plt
from os import listdir, remove, walk
from os.path import join, exists, isfile
from utilities import getFilepath, getFilename, getFileformat


def visualizeDataset(target_dir, plot_columns=None, save_dir=None):
	if not isfile(target_dir):
		# Input is folder path
		folder_dir = target_dir
		# Get all file names in the folder
		filenames = [file for (dirpath, dirnames, filenames) in walk(folder_dir) for file in filenames if file.split(".")[-1] == "pkl"]
	else:
		# Input is file path
		folder_dir = getFilepath(target_dir)
		filenames = [getFilename(target_dir) + getFileformat(target_dir)]
		
	# Load dataset
	temp_datasets = []
	for f in filenames:
		temp_datasets.append(pd.read_pickle(join(folder_dir, f)))
	dataset = pd.concat(temp_datasets, ignore_index=True)
	
	# Get plot columns
	if plot_columns is None:
		plot_columns = dataset.columns
	
	# Plot and save
	fig, axs = plt.subplots(len(plot_columns), figsize=(10, 5*len(plot_columns)))
	for i, column_name in enumerate(plot_columns):
		axs[i].set_title(column_name)
		axs[i].hist(dataset[column_name], bins=50)
		
	if save_dir is not None:
		if exists(save_dir):
			# Delete old file
			remove(save_dir)
		plt.savefig(save_dir)

	plt.close(fig)
	

if __name__ == "__main__":
	target_dir = "./dataset_verysmall_hp100000_balanced.pkl"
	save_dir = "./dataset_verysmall_hp100000_balanced.png"
	plot_columns = ["focus_damage", "aoe_damage", "attack_num"]
	visualizeDataset(target_dir, plot_columns, save_dir)
