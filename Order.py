from .fooditem import FoodItem

DEFAULT_PRICE = 50


class Order:
    class FoodType:
        def __init__(self, name, price, notes=None):
            self.type = FoodItem(name, price)
            self.notes = notes

        def add_note(self, note):
            self.notes += note

        def delete_note(self, note):
            self.notes = self.notes.replace(note, "")

        def __str__(self):
            return f"{self.type.__str__()}  \n Your notes:  {self.notes}"

    _food_type = [FoodType('Falafel',DEFAULT_PRICE), FoodType('Pizza',DEFAULT_PRICE)]

    def __init__(self, food_type, food_note, name, location, payment):
        self._food_note = food_note
        self._name = name
        self._location = location
        self._payment = payment

    def add_food_type(self, new_food_type):
        self._food_type.append(new_food_type)

    def get_status(self):
        pass

    def __str__(self):
        pass
