""" Orders and creates the criterias """

STOPPING_POWER = 0
FIRE_RATE = 3
RANGE = 1
CAPACITY = 4
MOBILITY = 2
PRICE = 5

# Create a dict
criterion_name_dict = {
    "STOPPING_POWER": STOPPING_POWER,
    "FIRE_RATE": FIRE_RATE,
    "RANGE": RANGE,
    "CAPACITY": CAPACITY,
    "MOBILITY": MOBILITY,
    "PRICE": PRICE,
}

reverse_criterion_name_dict = {
    STOPPING_POWER: "STOPPING_POWER",
    FIRE_RATE: "FIRE_RATE",
    RANGE: "RANGE",
    CAPACITY: "CAPACITY",
    MOBILITY: "MOBILITY",
    PRICE: "PRICE",
}


def criterion_find(criteria: str):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

    return criterion_name_dict[criteria]


def criterion_name(criteria_value: int):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

    return reverse_criterion_name_dict[criteria_value]
