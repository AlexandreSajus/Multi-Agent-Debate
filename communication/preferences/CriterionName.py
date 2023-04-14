#!/usr/bin/env python3

from enum import Enum


def criterion_find(criteria: str):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

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

    return criterion_name_dict[criteria]
