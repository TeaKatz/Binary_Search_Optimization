import time
import pandas as pd
from os import makedirs
from os.path import join, exists
from environments.monster_hunter import MonsterHunter
from datasets.visualizeDataset import visualizeDataset
from utilities import getFilepath, getUniquename, binarySearch


def generate(env, iter, verbose=0, save_dir=None):
    dataset = {"monster_num": [],
               "focus_damage": [],
               "aoe_damage": [],
               "monster_hps": [],
               "attack_num": []}

    # Init start time
    total_time = time.time()
    epoch_time = time.time()
    for epoch in range(iter):
        env.reset()

        attack_num = binarySearch(env.max_hp, 1, env.action)
        
        if attack_num is not None:
            # Update to dataset
            dataset["monster_num"].append(env.monster_num)
            dataset["focus_damage"].append(env.focus_damage)
            dataset["aoe_damage"].append(env.aoe_damage)
            dataset["monster_hps"].append(env.monster_hps)
            dataset["attack_num"].append(attack_num)
            
            if verbose > 0:
                if (epoch + 1) % verbose == 0:
                    # Show run time
                    print("Epoch: {} Time: {:.2f}".format(epoch + 1, time.time() - epoch_time))
                    # Reset start time
                    epoch_time = time.time()

    if save_dir is not None:
        # Create directory if it does not exist
        filepath = getFilepath(save_dir)
        if not exists(filepath):
            makedirs(filepath)

        # Create unique name for save file
        save_dir = getUniquename(save_dir)

        # Save dataset
        dataset = pd.DataFrame(dataset)
        dataset.to_pickle(save_dir)
    
    print("Total time: {:.2f}".format(time.time() - total_time))
    
    return dataset


if __name__ == "__main__":
    BASE_DIR = "./verysmall_hp100000_num10000"

    data_size = 100
    max_hps = list(range(100, 100001, 500))
    max_monster_num = 10000
    max_damage_list = list(range(5, 101, 2))

    for max_hp in max_hps:
        folder = str(max_hp)
        for max_damage in max_damage_list:
            # Create environment
            env = MonsterHunter()
            env.max_hp = max_hp
            env.max_monster_num = max_monster_num
            env.max_focus_damage = max_damage

            # Generate
            name = "dataset_{}_{}_{}_{}".format(max_hp, max_monster_num, max_damage, data_size)
            save_dir = join(BASE_DIR, folder, name + ".pkl")
            if not exists(save_dir):
                print("Generating: {}...".format(save_dir))
                dataset = generate(env, data_size, verbose=0, save_dir=save_dir)

                # Visualize
                plot_columns = ["monster_num", "focus_damage", "aoe_damage", "attack_num"]
                visualizeDataset(save_dir, plot_columns, save_dir=join(BASE_DIR, folder, name + ".png"))
            else:
                print("Skip: {}".format(save_dir))

        plot_columns = ["monster_num", "focus_damage", "aoe_damage", "attack_num"]
        visualizeDataset(join(BASE_DIR, folder), plot_columns, save_dir=join(BASE_DIR, folder + ".png"))
