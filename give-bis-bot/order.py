from .fooditem import FoodItem

DEFAULT_PRICE = 50


class Order:
    class FoodTypeOrder:
        notes = []

        def __init__(self, item, notes=None):
            assert isinstance(item, FoodItem)
            self.item = item
            self.notes.append(notes)

        def add_note(self, note):
            self.notes.append(note)

        def delete_note(self, note):
            self.notes.remove(note)

        def __str__(self):
            return f"{self.item.__str__()}  \n Your notes:  {self.notes} \n"

    my_orders = []

    def __init__(self, name, location, payment):
        self._name = name
        self._location = location
        self._payment = payment

    def place(self, food_type):
        """
        place new order
        :type food_type: FoodType
        """
        assert isinstance(food_type, Order.FoodTypeOrder)
        self.my_orders.append(food_type)

    def __str__(self):
        return f"{food_order.__str__() for food_order in self.my_orders}"

    def get_status(self):
        return f"Name: {self._name} \n Location: {self._location} \n Payment: {self._payment}\n Order: {self.__str__()}"
