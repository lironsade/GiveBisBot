# restaurant object

class Restaurant:

    def __init__(self, food, contact_man, contact_phone, min_order=1):
        assert isinstance(contact_man, str)
        self.contact_man = contact_man
        assert isinstance(contact_phone, str)
        self.contact_phone = contact_phone
        self.min_order = min_order
        self.food = food
