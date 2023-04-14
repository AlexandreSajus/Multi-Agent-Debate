""" Module for generating Arguments """

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item


class Argument:
    """Argument class .
    This class implements an argument used during the interaction .

    attr :
    decision :
    item :
    comparison_list :
    couple_values_list :
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument ."""
        self.decision = boolean_decision
        self.item = item
        self.comparison_list = []
        self.couple_values_list = []

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list ."""
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list ."""
        self.couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to support an item
        : param item : Item - name of the item
        : return : list of all premisses PRO (value over 5) an item ( sorted by order of importance
        based on agent ’s preferences )
        """
        premisses = []
        for criterion in preferences.get_criterion_name_list():
            if preferences.get_value(item, criterion) > 4:
                premisses.append(
                    CoupleValue(criterion, preferences.get_value(item, criterion))
                )
        return premisses

    def list_attacking_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to attack an item
        : param item : Item - name of the item
        : return : list of all premisses CON (value under 5) an item ( sorted by order of importance
        based on preferences )
        """
        premisses = []
        for criterion in preferences.criterion_name_list:
            if preferences.get_criterion_value(item, criterion).value < 5:
                premisses.append(
                    CoupleValue(criterion, preferences.get_value(item, criterion))
                )
        return premisses
