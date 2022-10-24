class Player:
    def __init__(self,
                 player_id: int,
                 name: str,
                 background: str,
                 group: str,
                 race: str,
                 hp: float,
                 lvl: int,
                 ep: float,
                 stats: dict):
        self.player_id = player_id
        self.name = name
        self.background = background
        self.group = group
        self.race = race
        self.hp = hp
        self.lvl = lvl
        self.ep = ep
        self.stats = stats
        self.dead = False

        if self.ep >= 100:
            self.ep = self.ep - 100
            self.lvl = self.lvl + 1

    def getDmg(self, dmg: float):
        self.hp = self.hp - dmg
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            print('you are dead')
        else:
            print(self.hp)

    def export(self):
        dnd_char = {
            '_id': self.player_id,
            'name': self.name,
            'background': self.background,
            'hp': self.hp,
            'stats': self.stats,
            'dead': self.dead
        }
        return dnd_char
