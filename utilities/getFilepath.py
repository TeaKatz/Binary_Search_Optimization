def getFilepath(file_dir):
	return "/".join(file_dir.split("/")[:-1])


if __name__ == "__main__":
	file_dir = ".Datasets/dataset_10000/dataset.pkl"
	print(getFilepath(file_dir))