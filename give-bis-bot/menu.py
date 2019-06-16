from fooditem import FoodItem

class Menu:
    
    def __init__(self, items=[]):
        self.items = items

    def AddItem(self, fooditem):
        self.items.append(fooditem)

    def RemoveItem(self, fooditem):
        self.items.remove(fooditem)

