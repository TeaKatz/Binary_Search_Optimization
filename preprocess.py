def preprocess(dataset, max_monster_num=1000):
	monster_hp_columns = ["monster_hp_" + str(num) for num in range(1, max_monster_num + 1)]
	
	temp_hps = np.zeros((dataset["monster_hps"].shape[0], max_monster_num), dtype=int)
	for row in range(len(dataset["monster_hps"])):
		# Sorted and padding
		temp_hps[row, :len(dataset["monster_hps"][row])] = sorted(dataset["monster_hps"][row], reverse=True)
		
	monster_hps = pd.DataFrame(temp_hps, columns=monster_hp_columns)
	dataset = pd.concat([loaded, monster_hps], axis=1, ignore_index=False).drop(columns="monster_hps")

	return dataset
