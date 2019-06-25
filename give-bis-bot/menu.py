from fooditem import FoodItem
import csv

NUM_OF_ITEMS = 2

ITEM_NAME, ITEM_PRICE = range(NUM_OF_ITEMS)

class Menu:
    def __init__(self, items=None):
        if items:
            self.items = items
        else:
            self.items = {}

    def AddItem(self, fooditem):
        self.items.append(fooditem)

    def RemoveItem(self, fooditem):
        self.items.remove(fooditem)

    def GetItem(self, name):
        return self.items.get(name, None)

    def AllText(self):
        return [self.items.keys()]

    def crete_menu_from_csv_file(self, csv_reader):
        for row in csv_reader:
            self.items[row[ITEM_NAME]] = FoodItem(row[ITEM_NAME], row[ITEM_PRICE])
