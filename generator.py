import time
import wandb
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from os import makedirs, listdir, remove
from os.path import join, exists
from Environment import MonsterHunter
from binarySearch import binarySearch
from visualizeDataset import visualizeDataset
from utilities import getFileformat, getFilename, getFilepath, getUniquename


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
    BASE_DIR = "./Datasets/verysmall"

    data_size = 100
    max_hps = list(range(100, 1001, 5))
    max_monster_num = 1000
    max_damage_list = list(range(5, 51))

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

        # # Set configuration
        # config = {"data_size": data_size,
        #           "max_hp": max_hp,
        #           "max_monster_num": max_monster_num,
        #           "max_damage": max_damage}
        #
        # # Initial project
        # name = "dataset_{}_{}_{}_{}".format(max_hp, max_monster_num, max_damage, data_size)
        # wandb.init(project="binary_search_optimization", name=name, config=config, reinit=True)
        #
        # # Create environment
        # env = MonsterHunter()
        # env.max_hp = wandb.config.max_hp
        # env.max_monster_num = wandb.config.max_monster_num
        # env.max_focus_damage = wandb.config.max_damage
        #
        # # Generate
        # save_dir = "./Datasets/{}.pkl".format(name)
        # if exists(save_dir):
        #     remove(save_dir)
        #
        # dataset = generate(env, wandb.config.data_size, verbose=0, save_dir=save_dir)
        #
        # plot_columns = ["monster_num", "focus_damage", "aoe_damage", "attack_num"]
        # for i, col in enumerate(plot_columns):
        #     plt.hist(dataset[col])
        #     plt.title(col)
        #     wandb.log({col: plt})
        #     plt.clf()
