import time
import pandas as pd
from Environment.MonsterHunter import MonsterHunter, preprocess
from utilities import binarySearch
from BinarySearchInitializer import BinarySearchInitializer


if __name__ == "__main__":
	env = MonsterHunter()
	env.reset()

	attack_num = binarySearch(10000, 0, env.action)
	print("actual attack_num: {}".format(attack_num))

	inputs = pd.DataFrame(env.parameters)
	inputs = preprocess(inputs)

	initializer = BinarySearchInitializer(checkpoint_dir="./Save/SequenceDenseBalanced", scalers_dir="./Save")
	attack_num = int(initializer.predict(inputs))
	print("predicted attack_num: {}".format(attack_num))

	step = initializer.error
	print("Step: {}".format(step))
	max_search = None
	min_search = None
	start_time = time.time()
	while True:
		if env.action(attack_num):
			# All monsters die
			max_search = attack_num
			attack_num -= step
		else:
			# Monsters survive
			min_search = attack_num
			attack_num += step
		step *= 2
		if time.time() - start_time > 30:
			print("Time out!")
			break
		if max_search is not None and min_search is not None:
			print("Start binary search")
			print("Max search: {}".format(max_search))
			print("Min search: {}".format(min_search))
			attack_num = binarySearch(max_search, min_search, env.action)
			if attack_num is not None:
				# Check answer
				if env.action(attack_num - 1):
					# Answer is incorrect
					print("Answer is {} (incorrect)".format(attack_num))
				else:
					# Answer is incorrect
					print("Answer is {} (correct)".format(attack_num))
			else:
				print("Time out!")
			break
