import numpy as np
import pandas as pd


def preprocess(data, max_monsters_num=1000):
	# Create monster_hps_xxx column
	temp_hps = np.zeros((data["monster_hps"].shape[0], max_monsters_num), dtype=int)
	for row in range(len(data["monster_hps"])):
		# Sorted and padding
		if (row + 1) % 10000 == 0:
			print("Sorting and padding...({}/{})".format(row + 1, len(data["monster_hps"])))
		temp_hps[row, :len(data["monster_hps"][row])] = sorted(data["monster_hps"][row], reverse=True)

	# Create monster_hp_xxx column with sorting and padding
	monster_hps_column = ["monster_hp_" + str(num) for num in range(1, max_monsters_num + 1)]
	monster_hps = pd.DataFrame(temp_hps, columns=monster_hps_column)
	data = pd.concat([data, monster_hps], axis=1, ignore_index=False).drop(columns=["monster_hps", "monster_num"])
	data.drop_duplicates(inplace=True)

	return data
