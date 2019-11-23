import numpy as np


class MonsterHunter:
    def __init__(self, min_monster_num=1, max_monster_num=1e3, min_focus_damage=2, max_focus_damage=1e3, min_aoe_damage=1, min_hp=1, max_hp=1e3):
        self.min_monster_num = min_monster_num
        self.max_monster_num = max_monster_num
        self.min_focus_damage = min_focus_damage
        self.max_focus_damage = max_focus_damage
        self.min_aoe_damage = min_aoe_damage
        self.min_hp = min_hp
        self.max_hp = max_hp
        self.monster_num = None
        self.focus_damage = None
        self.aoe_damage = None
        self.monster_hps = None
        
    @property
    def parameters(self):
        parameters = {}
        parameters["monster_num"] = self.monster_num
        parameters["focus_damage"] = self.focus_damage
        parameters["aoe_damage"] = self.aoe_damage
        parameters["monster_hps"] = self.monster_hps
        
        return parameters

    def reset(self):
        """ Initial environment parameters. """
        self.monster_num = np.random.randint(self.min_monster_num, self.max_monster_num)
        self.focus_damage = np.random.randint(self.min_focus_damage, self.max_focus_damage)
        self.aoe_damage = np.random.randint(self.min_aoe_damage, self.focus_damage)
        self.monster_hps = np.random.randint(self.min_hp, self.max_hp, size=(self.monster_num, ))

    def action(self, attack_num):
        """
        This method check whether with the given attack number will all the monsters die.
        Return: True if all monsters die.
                False otherwise.
        """
        # Fetch monster hps
        t_monster_hps = self.monster_hps.copy()

        # Calculate aoe attack all
        aoe_damage_all = self.aoe_damage * attack_num

        # Attack all monster with aoe damage
        for i in range(len(t_monster_hps)):
            if aoe_damage_all > t_monster_hps[i]:
                t_monster_hps[i] = 0
            else:
                t_monster_hps[i] -= aoe_damage_all

        # Calculate how many focus attack needed to kill all remain monster
        focus_attack_num = 0
        damage = self.focus_damage - self.aoe_damage
        for i in range(len(t_monster_hps)):
            if t_monster_hps[i] > 0:
                if t_monster_hps[i] % damage == 0:
                    focus_attack_num += t_monster_hps[i] // damage
                else:
                    focus_attack_num += t_monster_hps[i] // damage + 1

        # Return
        if focus_attack_num <= attack_num:
            return True
        else:
            return False
