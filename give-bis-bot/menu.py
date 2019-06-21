from fooditem import FoodItem
import csv

ITEM_NAME, ITEM_PRICE = range(2)

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

    def crete_menu_from_csv_file(self, csv_reader):
        for row in csv_reader:
            self.items[row[ITEM_NAME]] = FoodItem(row[ITEM_NAME], row[ITEM_PRICE])
