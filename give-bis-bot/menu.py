from fooditem import FoodItem

class Menu:
    def __init__(self, items=None):
        if items:
            self.items = items
        else:
            self.items = dict()

    def AddItem(self, fooditem):
        self.items.append(fooditem)

    def RemoveItem(self, fooditem):
        self.items.remove(fooditem)

    def GetItem(self, name):
        return self.items.get(name, None)

    def AllText(self):
        return list(self.items.keys())

sample_menu_dict = { 'Falafel' : FoodItem('Falafel', 15), 'Pizza': FoodItem('Pizza', 20) }
