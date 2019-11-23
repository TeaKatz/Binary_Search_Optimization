import time
import shutil
import pandas as pd
from os import makedirs, listdir
from os.path import join, exists
from Environment import MonsterHunter
from binarySearch import binarySearch
from utilities import getFileformat, getFilename, getFilepath, getUniquename


def generate(env, save_dir, iter, verbose=0):
    dataset = {"monster_num": [],
               "focus_damage": [],
               "aoe_damage": [],
               "monster_hps": [],
               "attack_num": []}
            
    # Create directory if it does not exist
    filepath = getFilepath(save_dir)
    if not exists(filepath):
        makedirs(filepath)
        
    # Create unique name for save file
    save_dir = getUniquename(save_dir)

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
                
    # Save dataset
    dataset = pd.DataFrame(dataset)
    dataset.to_pickle(save_dir)
    
    print("Total time: {:.2f}".format(time.time() - total_time))


if __name__ == "__main__":
    # Get save directory
    dataset_size = 10000
    df_min = 10
    df_max = 100
    df_step = 10
    hp_min = 1000
    hp_max = 10000
    hp_step = 100
    
    for hp in range(hp_min, hp_max + 1, hp_step):
        for df in range(df_min, df_max + 1, df_step):
            env = MonsterHunter()
            env.max_hp = hp
            env.max_focus_damage = df
            env.min_focus_damage = max(2, env.max_focus_damage - df_step)
            
            dataset_dir = "./Datasets/Dataset_medium_df{}-{}_hp{}-{}".format(df_min, df_max, hp_min, hp_max)
            save_name = "dataset_{}_df{}_hp{}.pkl".format(dataset_size, df, hp)
            save_dir = join(dataset_dir, save_name)
            if not exists(save_dir):
                generate(env, save_dir, dataset_size, verbose=0)
            else:
                print("Skip {}".format(save_name))
