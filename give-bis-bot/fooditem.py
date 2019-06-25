class FoodItem:
    def __init__(self, name, price, comment=None):
        self.name = name
        self.price = price
        self.comment = comment

    def __str__(self):
    if self.comment == None
        return f"{self.name} costs {self.price}"
    else:
        return f"{self.name} costs {self.price}: {self.comment}"
