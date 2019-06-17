from fooditem import FoodItem

class Menu:
    def __init__(self, items=None):
        if items:
            self.items = dict()
        else:
            self.items = items

    def AddItem(self, fooditem):
        self.items.append(fooditem)

    def RemoveItem(self, fooditem):
        self.items.remove(fooditem)

    def GetItem(self, name):
        return self.items.get(name, None)

    def AllText(self):
        print([item.name for item in self.items.values()])
        return [item.name for item in self.items.values()]

sample_menu_dict = { 'Falafel' : FoodItem('Falafel', 15), 'Pizza': FoodItem('Pizza', 20) }
