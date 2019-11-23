from os.path import join, exists
from .getFilename import getFilename
from .getFileformat import getFileformat
from .getFilepath import getFilepath


def getUniquename(file_dir):
	if exists(file_dir):
		filename = getFilename(file_dir)
		fileformat = getFileformat(file_dir)
		filepath = getFilepath(file_dir)
		is_succeed = False
		for num in range(1, 10000):
			new_filename = filename + "_" + str(num)
			if not exists(join(filepath, new_filename + fileformat)):
				file_dir = join(filepath, new_filename + fileformat)
				is_succeed = True
				break
		if is_succeed == False:
			# Terminate
			print("[Error] Cannot find unique name")
			return None
	return file_dir
	
	
if __name__ == "__main__":
	file_dir = "getUniquename.py"
	print(getUniquename(file_dir))
