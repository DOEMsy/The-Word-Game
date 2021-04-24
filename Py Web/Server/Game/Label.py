# 个位为 0 的为泛用标签，除个位外与之相同的所有标签都属于其子标签
# 例如 Humanoid（101）属于 OrdinaryCreatures（100）
Labels = {
    # --- 种族 ---
    # 普通生物 OrdinaryCreatures
    "普通生物": 100,
    "人类": 101,  # 人类
    "亚人": 102,  # 亚人
    "动物": 103,  # 动物
    "虫": 104,

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
    "宝具": 502,

    # --- 组织 ---
    # 帝国
    "帝国": 30011,
    # 神圣教国
    "神圣教国": 30021,

    # 四学士
    "四学士": 31011,
    # 猎龙塞
    "猎龙塞": 31021,
    # 雾行者的匕首
    "雾行者的匕首": 31031,

    # --- 技能 ---

    # 特性，生物的固有属性
    "特性": 40011,

    # 计略，因高超的计略产生的效果
    "计略": 40021,

    # 物理，因为强大的能量或物理打击造成的效果，通常表示伤害
    "物理": 40031,

    # 魔法，简单方便的魔法产生的效果
    "魔法": 40040,
    # 禁咒，因邪恶的力量，或者牺牲换取的效果，属于魔法
    "禁咒": 40041,
    # 圣吟，因虔诚和祈祷，获取的带有神圣的效果，属于魔法
    "圣吟": 40042,

    # 天气，因为恶劣的天气环境产生的效果
    "天气": 40050,
    "寒霜": 40051,
    "烈日": 40052,
    "血月": 40053,
    "暴雨": 40054,

    # 神术，撼天动地的，轻易改变世间常理的效果
    "神术": 40061,

}

for key, value in list(Labels.items()):
    Labels[value] = key


# 卡牌是否具有标签
def Is(label, card) -> bool:
    # 普通生物优先级最低，普通生物只能是普通生物，不能是不死者，或其他生物
    if (label == "普通生物"):
        return _is("普通生物", card) and not _is("不死者", card) and not _is("高等生物", card) and not _is(
            "彼世生物", card)
    # 高等生物其次，高等生物可以是不死者，不死者可以是高等生物
    elif (label == "高等生物"):
        return _is("高等生物", card) and not _is("彼世生物", card)
    # 彼世生物 优先级最高
    elif (label == "彼世生物"):
        return _is("彼世生物", card)
    # 不死者 可与 彼世生物，高等生物并列存在
    elif (label == "不死者"):
        return _is("不死者", card)
    # 单标签查询
    else:
        return _is(label, card)

    # 保证特指性效果可以对实际标签起作用，例如一个同时拥有龙和虫属性的单位可以受到指定虫属性的效果
    # 保证泛指性效果只对优先级最高的标签起作用，例如一个对普通生物的效果无法作用对上述单位，因为该单位拥有龙属性属于高等生物
    # 即泛用标签中存在覆盖关系，彼世生物>高等生物>普通生物，不死者>普通生物，不死者与彼世生物或高等生物可以同时存在
    # 保证指定不死者的效果一定生效，任何泛用标签都无法覆盖不死者


def _is(label, card) -> bool:
    if (card.Type in {"UnitCard", "SkillCard"}):
        lbnum = 0
        if (type(label) == str):
            lbnum = Labels[label]
        else:
            lbnum = label
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


# 标签中否具有标签
def Has(label, labels) -> bool:
    lbnum = 0
    if (type(label) == str):
        lbnum = Labels[label]
    else:
        lbnum = label
    # 查询泛用标签
    if (lbnum % 10 == 0):
        for lb in labels:
            if (Labels[lb] // 10 * 10 == lbnum):
                return True
        return False
    # 查询准确标签
    else:
        return label in labels
