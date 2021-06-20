from copy import deepcopy
from random import sample, choice, randint
import numpy as np
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import NoSpell, ConcretizationCard

# --------------- 克拉肯 -----------------

class Kraken(UnitCard):
    def __init__(self):
        super().__init__(
            name="克拉肯",
            desc="在深不可测的海底，北海巨妖正在沉睡，它已经沉睡了数个世纪，并将继续安枕在巨大的海虫身上，直到有一天海虫的火焰将海底温暖，人和天使都将目睹它带着怒吼从海底升起，海面上的一切将毁于一旦\n"
                 "◇潮渊之境的怪兽：这家伙是个远古生物\n"
                 "◇触手：" # 记得先实现一个召唤物机制  2021.6.1
                 "".format(),
            combat=28,
            level=4,
            label={
                "远古生物"
            },
            canto={1},
        )