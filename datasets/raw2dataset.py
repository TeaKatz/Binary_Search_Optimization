import pandas as pd
from environments.monster_hunter import preprocess
from os import listdir, walk
from os.path import join
from utilities import getFilepath


def raw2dataset(folder_dir, max_monsters_num=1000, save_dir=None, file_format="pkl"):
	"""
	- Load all pickle file in the folder
	- Concatenate them in row axis
	- Create monster_hp_xxx column with sorting and padding
	- Delete monster_hps column
	- Delete duplicate data
	- Save to given directory or same directory of raw folder
	"""
	assert file_format == "pkl" or file_format == "csv", "file_format must be 'pkl' or 'csv'."

	if save_dir is None:
		save_dir = getFilepath(folder_dir)
		save_dir = join(save_dir, "dataset" + "." + file_format)

	# Get pickle filename in folder
	file_dirs = [join(dirpath, file) for (dirpath, dirnames, filenames) in walk(folder_dir) for file in filenames if file.split(".")[-1] == file_format]

	# Load all files
	data = []
	for i, file_dir in enumerate(file_dirs):
		if (i + 1) % 10 == 0:
			print("Reading...({}/{})".format(i + 1, len(file_dirs)))
		if file_format == "pkl":
			data.append(pd.read_pickle(file_dir))
		else:
			data.append(pd.read_csv(file_dir))

	# Concatenate in row
	print("Concatenating...")
	dataset = pd.concat(data, ignore_index=True)

	# Pre-processing
	print("Preprocessing...")
	dataset = preprocess(dataset, max_monsters_num=max_monsters_num, truncate_mode="cut")

	# Save
	print("Saving to {}...".format(save_dir))
	if file_format == "pkl":
		dataset.to_pickle(save_dir)
	else:
		dataset.to_csv(save_dir)
	print("Done")

if __name__ == "__main__":
	raw2dataset("./verysmall_hp100000_num10000", save_dir="./dataset_verysmall_hp100000_num10000.pkl")
