import pandas as pd
from Environment import MonsterHunter
from binarySearch import binarySearch
from BinarySearchInitializer import BinarySearchInitializer
from preprocess import preprocess


if __name__ == "__main__":
	# Create environment
	env = MonsterHunter()
	env.reset()
	# Get inputs and proprocess
	inputs = pd.DataFrame(env.parameters)
	inputs = preprocess(inputs)
	# Create model and load parameters
	initializer = BinarySearchInitializer()
	# Tolerant of 2%
	tolerant = env.max_hp + 0.02
	# Find max_search and min_search
	# Predict attack_num
	attack_num = initializer.predict(inputs)
	# Check result
	if env.action(attack_num):
		# All monsters die
		max_search = attack_num
		min_search = max_search - tolerant
	else:
		# Monsters survive
		min_search = attack_num
		max_search = min_search + tolerant
	# Do binary search
	attack_num = binarySearch(max_search, min_search, env.action)
	if attack_num is None:
		print("Time out!")
		return
	else:
		# Check if answer correct
		if env.action(attack_num - 1) == 0:
			# Answer correct
			print("Answer is: {}".format(attack_num))
		else:
			# Answer incorrect
			max_search = attack_num
			min_search = 1
			attack_num = binarySearch(max_search, min_search, env.action)
			if attack_num is None:
				print("Time out!")
				return
			else:
				print("Answer is: {}".format(attack_num))
