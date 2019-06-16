
class Order:

    def __init__(self, food_type, food_note, name, location, payment):
        self._food_type = food_type
        self._food_note = food_note
        self._name = name
        self._location = location
        self._payment = payment

    def get_status(self):
        pass

    def __str__(self):
        pass

