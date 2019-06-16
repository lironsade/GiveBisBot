import numpy as np
import pandas as pd

food_types = ['Pizza', 'Falafel', 'Sushi', 'Hamburger', 'Shawarma', 'Humus']
restaurant_info = ['contact man', 'contact phone', 'minimum orders']
foodDB = pd.DataFrame(index=food_types, columns=restaurant_info)


def add_food_type(new_food):
    """
    Add another food option. Updates the DB as well as the list of foods
    :param new_food: string. New food type to add.
    """
    if new_food not in food_types:
        # todo: check for bad append because of bad spelling ?
        food_types.append(new_food)
        foodDB.append(new_food)


# restaurant object

class Restaurant:

    def __init__(self, food, contact_man, contact_phone, min_order=1):
        """

        :param food:
        :param contact_man:
        :param contact_phone:
        :param min_order:
        """
        assert isinstance(contact_man, str)
        self.contact_man = contact_man
        assert isinstance(contact_phone, str)
        self.contact_phone = contact_phone
        self.min_order = min_order
        self.food = food
