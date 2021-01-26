class Card(object):
    def __init__(self, name, desc):
        self.Name = name
        self.Desc = desc
        self.Type = "None"

    def OnHand(self):
        return 1

    def Play(self):
        return 1

    def Aban(self):
        return 1

    def __str__(self):
        return "[{},{},{}]".format(self.Name, self.Desc, self.Type)
