""" Implements an argument: criteria and value"""

from communication.preferences.CriterionName import criterion_name


class CoupleValue:
    """CoupleValue class .
    This class implements a couple value used in argument object .

    attr :
    criterion_name :
    value :
    """

    def __init__(self, criterion_name, value):
        """Creates a new couple value ."""
        self.criterion_name = criterion_name
        self.value = value

    # print function
    def __str__(self):
        return (
            "Argument : "
            + str(criterion_name(self.criterion_name))
            + " = "
            + str(self.value)
        )
