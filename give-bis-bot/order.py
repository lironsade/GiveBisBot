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

        def __str__(self):
            return f"{self.item.__str__() + ', amount: ' + str(len(self.notes))}. \nYour notes:  {self.notes}. \n"

    def __init__(self, name, location, phone):
        self._name = name
        self._location = location
        self._phone = phone
        self.my_orders = {}

    def place_order(self, item, note):
        assert isinstance(item, FoodItem)
        if item.name not in self.my_orders:
            self.my_orders[item.name] = Order.FoodTypeOrder(item, note)
        else:
            self.my_orders[item.name].add_note(note)

    def remove_order(self, item):
        self.my_orders.pop(item)

    def total_cost(self):
        total = 0
        for key in self.my_orders:
            total += self.my_orders[key].item.price * len(self.my_orders[key].notes)
        return total

    def __repr__(self):
        reprs = ''
        for key in (self.my_orders.keys()):
            reprs += self.my_orders[key].__str__()
        reprs += f"Customer name: {self._name}.\nCustomer location: {self._location}.\nCustomer phone: {self._phone}."
        return f"{reprs}"

    def get_status(self):
        return self.__repr__()
