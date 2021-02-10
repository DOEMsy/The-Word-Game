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
    "幽灵": 203,

    # 高等生物 AdvancedCreature
    "高等生物": 300,
    "自然": 301,  # 自然
    "龙": 302,  # 龙
    "机械": 303,  # 机械
    "魔法生物": 304,  # 魔法
    "妖精": 305,

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
    # 特性，生物的固有属性
    "特性": 40061,
    # 计略，因高超的计略产生的效果
    "计略": 40011,
    # 魔法，简单方便的魔法产生的效果
    "魔法": 40021,
    # 禁咒，因邪恶的力量，或者牺牲换取的效果
    "禁咒": 40031,
    # 圣吟，因虔诚和祈祷，获取的带有神圣的效果
    "圣吟": 40041,
    # 神术，撼天动地的，轻易改变世间常理的效果
    "神术": 40051,

}

for key, value in list(Labels.items()):
    Labels[value] = key


# 卡牌是否具有标签
def Is(label, card) -> bool:
    if (card.Type in {"UnitCard", "SkillCard"}):
        lbnum = 0
        if (type(label) == str):    lbnum = Labels[label]
        else:   lbnum = label
        # 查询泛用标签
        if (lbnum % 10 == 0):
            for lb in card.Label:
                if (Labels[lb] // 10 * 10 == lbnum):
                    return True
            return False
        # 查询准确标签
        else:
            return label in card.Label
    else:
        return False


# 标签中是否拥有
def Has(label, labels) -> bool:
    return label in labels
