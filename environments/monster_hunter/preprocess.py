import numpy as np
import pandas as pd


def preprocess(data, max_monsters_num=1000, truncate_mode="cut"):
	truncate_mode = truncate_mode.lower()
	assert truncate_mode == "cut" or truncate_mode == "avg" or truncate_mode == "max", "truncate_mode must be either 'cut', 'avg' or 'max'."
	# Create monster_hps_xxx column
	mask_hps = np.zeros((data["monster_hps"].shape[0], max_monsters_num), dtype=int)
	for row in range(len(data["monster_hps"])):
		# Report
		if (row + 1) % 10000 == 0:
			print("Sorting and padding...({}/{})".format(row + 1, len(data["monster_hps"])))
		# Sorted and padding
		sorted_data = np.array(sorted(data["monster_hps"][row], reverse=True))
		if sorted_data.shape[0] > max_monsters_num:
			if truncate_mode == "cut":
				# Truncate sorted_data by cut exceed index off
				mask_hps[row, :max_monsters_num] = sorted_data[:max_monsters_num]
			elif truncate_mode == "avg":
				# Average group of sorted_data to reduce length of it
				# Calculate group size and last group size
				group_size = round(len(sorted_data) / max_monsters_num)
				last_group_size = len(sorted_data) % group_size
				# group contain indexes of sorted_data in each group
				group = [list(range(i, i + group_size)) for i in range(0, len(sorted_data), group_size)]
				if last_group_size != 0:
					# correct last group length
					group[-1] = group[-1][:last_group_size]
				# Get truncated sorted_data
				truncated_data = np.array([sum(sorted_data[index]/len(group)) for index in group])
				if truncated_data.shape[0] > max_monsters_num:
					# If truncated_data length exceed maximum, average them together
					truncated_data = truncated_data[:max_monsters_num]
				mask_hps[row, :truncated_data.shape[0]] = truncated_data
			else:
				# Pick maximum value from group of sorted_data to reduce length of it
				# Calculate group size and last group size
				group_size = round(len(sorted_data) / max_monsters_num)
				last_group_size = len(sorted_data) % group_size
				# group contain indexes of sorted_data in each group
				group = [list(range(i, i + group_size)) for i in range(0, len(sorted_data), group_size)]
				if last_group_size != 0:
					# correct last group length
					group[-1] = group[-1][:last_group_size]
				# Get truncated sorted_data
				truncated_data = np.array([max(sorted_data[index]) for index in group])
				if truncated_data.shape[0] > max_monsters_num:
					# If truncated_data length exceed maximum, cut them out because they're less than last element anyway
					truncated_data = truncated_data[:max_monsters_num]
				mask_hps[row, :truncated_data.shape[0]] = truncated_data
		else:
			# If sorted_data is smaller than maximum, it will be padded automatically by mask
			mask_hps[row, :sorted_data.shape[0]] = sorted_data

	# Create monster_hp_xxx column with sorting and padding
	monster_hps_column = ["monster_hp_" + str(num) for num in range(1, max_monsters_num + 1)]
	monster_hps = pd.DataFrame(mask_hps, columns=monster_hps_column)
	data = pd.concat([data, monster_hps], axis=1, ignore_index=False).drop(columns=["monster_hps", "monster_num"])
	data.drop_duplicates(inplace=True)

	return data
