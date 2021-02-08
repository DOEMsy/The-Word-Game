# 个位为 0 的为泛用标签，除个位外与之相同的所有标签都属于其子标签
# 例如 Humanoid（101）属于 OrdinaryCreatures（100）
Labels = {
    # --- 种族 ---
    # 普通生物 OrdinaryCreatures
    "普通生物": 100,
    "人类": 101,  # 人类
    "亚人": 102,  # 亚人
    "动物": 103,  # 动物

    # 不死者 UndeadCreatures
    "不死者": 200,
    "血族": 201,  # 血族
    "亡骸": 202,  # 亡骸

    # 高等生物 AdvancedCreature
    "高等生物": 300,
    "自然": 301,  # 自然
    "龙": 302,  # 龙
    "机械": 303,  # 机械
    "魔法生物": 304,  # 魔法

    # 彼世 OutsideWorldCreature
    "彼世生物": 400,
    "恶魔": 401,  # 恶魔
    "天使": 402,  # 天使
    "神明": 403,  # 神明
    "腐化": 404,  # 腐化

    # --- 特性 ---
    "界者": 501,

    # --- 组织 ---
    # 帝国
    "帝国": 30011,

    # 四学士
    "四学士": 31011,
    # 猎龙塞
    "猎龙塞": 31021,
    # 雾行者的匕首
    "雾行者的匕首": 31031,

    # --- 技能 ---
    # 计略
    "计略": 40011,
    # 魔法
    "魔法": 40021,
    # 禁咒
    "禁咒": 40031,
    # 圣吟
    "圣吟": 40041,
    # 神术
    "神术": 40051,

}

for key, value in list(Labels.items()):
    Labels[value] = key


# 卡牌是否具有标签
def Is(label, card) -> bool:
    if (card.Type in {"UnitCard", "SkillCard"}):
        if (type(label) == str):    label = Labels[label]
        # 查询泛用标签
        if (label % 10 == 0):
            for lb in card.Label:
                if (Labels[lb] // 10 == label):
                    return True
            return False
        # 查询准确标签
        else:
            return card.Label.get(label) != None
    else:
        return False


# 标签中是否拥有
def Has(label, labels) -> bool:
    return label in labels
