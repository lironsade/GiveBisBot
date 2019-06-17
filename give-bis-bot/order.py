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
            return f"{self.item.__str__()}  \n Your notes:  {self.notes} \n"

    my_orders = {}

    def __init__(self, name, location, payment):
        self._name = name
        self._location = location
        self._payment = payment

    def place_order(self, item, note):
        assert isinstance(item, FoodItem)
        if item.name not in self.my_orders:
            self.my_orders[item.name] = Order.FoodTypeOrder(item, '(1) ' + note)
        else:
            self.my_orders[item.name].add_note("(" + str(1 + len(self.my_orders[item.name].notes)) + ") " + note)

    def remove_order(self, item):
        self.my_orders.pop(item)

    def __repr__(self):
        reprs = ''
        for key in (order.my_orders.keys()):
            reprs += order.my_orders[key].__str__()
        return f"{reprs}"

    def get_status(self):
        return f"Name: {self._name} \n Location: {self._location} \n Payment: {self._payment}\n Order: {self.__str__()}"
