Labels = {
    # 普通生物 OrdinaryCreatures
    "OrdinaryCreatures": 100,
    "Humanoid": 101,  # 人类、亚人
    "Animal": 102,  # 动物

    # 不死者 UndeadCreatures
    "UndeadCreatures": 200,
    "Vampire": 201,  # 血族
    "Undead": 202,  # 亡灵

    # 高等生物 AdvancedCreature
    "AdvancedCreature": 300,
    "Natural": 301,  # 自然
    "Dragon": 302,  # 龙
    "Mechanical": 303,  # 机械
    "MagicCreature": 304,  # 魔0法生物

    # 彼世 OutsideWorldCreature
    "OutsideWorldCreature": 400,
    "Demon": 401,  # 恶魔
    "Apostle": 402,  # 天使
    "Deity": 403,  # 神明
    "Corrupt": 404,  # 腐化
}

for key, value in Labels:
    Labels[value] = key


def Is(label, card):
    if (card.Type == "UnitCard"):
        if (type(label) == str):    label = Labels[label]
        if (label % 10 == 0):
            for i in range(1, 10):
                lab = Labels[label + i]
                if (card.Label.get(lab) != None):
                    return True
            return False
        else:
            return card.Label.get(label) != None
    elif (card.Type == "SkillCard"):
        pass
