def getFilename(file_dir):
	return file_dir.split("/")[-1].split(".")[0]
	
	
if __name__ == "__main__":
	file_dir = ".Datasets/dataset_10000/dataset.pkl"
	print(getFilename(file_dir))
