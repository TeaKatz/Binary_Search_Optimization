import time


def binarySearch(max_search, min_search, target, timeout=30):
	"""
	This function find optimal value to solve target problem.
	max_search: Maximum value to search for.
	min_search: Minimum value to search for.
	target: Target problem which return "True" if problem be solved or "False" otherwise.
	"""
	# Initial search value
	val_search = int((max_search + min_search) // 2)
	# Start searching
	start_time = time.time()
	while max_search != min_search:
		result = target(val_search)
		# Update min/max search
		if result == 1:
			# Decrease max search
			max_search = val_search
		else:
			# Increase min search
			if min_search == val_search:
				min_search += 1
			else:
				min_search = val_search
		# Update search value
		val_search = int((max_search + min_search) // 2)
		# Time out
		if time.time() - start_time > timeout:
			return None
	return val_search