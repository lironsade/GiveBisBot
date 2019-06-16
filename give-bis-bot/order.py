from fooditem import FoodItem


class Order:
    class FoodTypeOrder:

        def __init__(self, item, notes=None):
            if notes is None:
                self.notes = []
            else:
                self.notes = [notes]
            assert isinstance(item, FoodItem)
            self.item = item

        def add_note(self, note):
            self.notes.append(note)

        # def delete_note(self, note):
        #     self.notes.remove(note)

        def __str__(self):
            return f"{self.item.__str__()}  \n Your notes:  {self.notes} \n"

    my_orders = {}

    def __init__(self, name, location, payment):
        self._name = name
        self._location = location
        self._payment = payment

    def place_order(self, item, note):
        if item not in self.my_orders.keys():
            self.my_orders[item] = Order.FoodTypeOrder(item, note)
        else:
            self.my_orders[item].add_note(note)

    def remove_order(self, item):
        self.my_orders.pop(item)

    def __str__(self):

        return f"{list(food_order.__str__() for food_order in self.my_orders.values())}"

    def get_status(self):
        return f"Name: {self._name} \n Location: {self._location} \n Payment: {self._payment}\n Order: {self.__str__()}"
