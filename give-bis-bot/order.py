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

    def total_cost(self):
        total = 0
        for key in self.my_orders:
            total += self.my_orders[key].item.price * len(self.my_orders[key].notes)
        return total

    def __repr__(self):
        reprs = ''
        for key in (order.my_orders.keys()):
            reprs += order.my_orders[key].__str__()
        return f"{reprs}"

    def get_status(self):
        return f"Name: {self._name} \n Location: {self._location} \n Payment: {self._payment}\n Order: {self.__str__()}"



if __name__ == '__main__':
    falafel = FoodItem('Falafel', 15)
    pizza = FoodItem('Pizza', 10)
    sabich = FoodItem('Sabich', 25)
    salad = FoodItem('Salad', 159)

    order = Order('liron', 'huji', 'chocolate bar')
    # order.place_order(falafel, "חומוס, צ'יפס, סלט עם קולה ובלי חריף דיר בלאק")
    # order.place_order(pizza, "פטריות ובצל. אה, מקמח מלא")
    # order.place_order(pizza, "פיצה רגילה")
    # order.place_order(sabich, "בטעות לחצתי על סביח אני בכלל לא אוהב את זה")
    # order.place_order(salad, "פלאפל, פיצה וסביח למה אני מת מרעב ואיתי אמר שסלט לא משביע ובפרט אוכל של בנות "
    #                          "ובנות לא שבעות הרי")

    order.place_order(falafel, "falafel")
    order.place_order(pizza, "pizza1")
    order.place_order(pizza, "pizza2")
    order.place_order(sabich, "sabich")
    order.place_order(salad, "salad")

    # for key in (order.my_orders.keys()):
    #     print(order.my_orders[key])
    print(order.__repr__())
