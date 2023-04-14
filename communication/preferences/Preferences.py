""" Module to generate Preferences """

import pandas as pd

from communication.preferences.CriterionName import criterion_find
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object."""
        self.__criterion_name_list = []
        self.__criterion_value_list = []

    def get_criterion_name_list(self):
        """Returns the list of criterion name."""
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value."""
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name."""
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list."""
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name."""
        values = self.get_criterion_value_list()
        for value in values:
            if (
                value.get_item() == item
                and value.get_criterion_name() == criterion_name
            ):
                return value.get_value()

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2."""
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2."""
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list):
        """Returns the most preferred item from a list."""
        item_list.sort(key=lambda x: x.get_score(self), reverse=True)
        return item_list[0]

    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        item_list.sort(key=lambda x: x.get_score(self), reverse=True)
        top_20_percent = int(len(item_list) * 0.1)
        return item in item_list[:top_20_percent]


if __name__ == "__main__":
    DATASET_PATH = "weapons_dataset.csv"
    preferences = Preferences()

    # Read the dataset
    dataset = pd.read_csv(DATASET_PATH, sep=";")

    preferences.set_criterion_name_list(
        [criterion_find(column) for column in dataset.columns if column != "WEAPON"]
    )

    # Add values
    items = []
    for _, row in dataset.iterrows():
        new_item = Item(row["WEAPON"], "")
        items.append(new_item)
        for column in dataset.columns:
            if column != "WEAPON":
                preferences.add_criterion_value(
                    CriterionValue(
                        new_item,
                        criterion_find(column),
                        row[column],
                    )
                )

    print(items[0])
    print(items[1])
    print(items[0].get_value(preferences, criterion_find("PRICE")))
    print(
        preferences.is_preferred_criterion(
            criterion_find("PRICE"), criterion_find("STOPPING_POWER")
        )
    )
    print(f"0 > 1 : {preferences.is_preferred_item(items[0], items[1])}")
    print(f"1 > 0 : {preferences.is_preferred_item(items[1], items[0])}")
    print(f"0 (for agent 1) = {items[0].get_score(preferences)}")
    print(f"1 (for agent 1) = {items[1].get_score(preferences)}")
    print("Most preferred item is : ")
    print(preferences.most_preferred([items[1], items[0]]).get_name())
