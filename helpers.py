import random


def helper_random_fieldpoint(corner1, corner2):
    """
    Function to return random point in field

    :param corner1: the bottom left corner of the field
    :type corner1: dict

    :param corner2: the top right corner of the field
    :type corner2: dict

    :return: returns a lat/long in the field
    :rtype: dict
    """

    x = random.uniform(corner1['lat'], corner2['lat'])
    y = random.uniform(corner1['lng'], corner2['lng'])
    point = {'lat': x, 'lng': y}

    return point


def helper_random_gate(corner1, corner2):
    """
    Function to return random gate in field

    :param corner1: the bottom left corner of the field
    :type corner1: dict

    :param corner2: the top right corner of the field
    :type corner2: dict

    :return: returns a lat/long in the field
    :rtype: dict
    """

    side = random.randint(1, 4)

    if side == 1:
        gatex = random.uniform(corner1['lat'], corner2['lat'])
        gatey = corner2['lng']
    elif side == 2:
        gatey = random.uniform(corner1['lng'], corner2['lng'])
        gatex = corner2['lat']
    elif side == 3:
        gatex = random.uniform(corner1['lat'], corner2['lat'])
        gatey = corner1['lng']
    elif side == 4:
        gatey = random.uniform(corner1['lng'], corner2['lng'])
        gatex = corner1['lat']

    point = {'lat': gatex, 'lng': gatey}

    return point


def helper_random_soiltype():
    """
    Function to returns a random soil type

    :return: returns a soiltype field
    :rtype: str
    """
    return random.choice(["Sand",
                          "LoamySand",
                          "SandyLoam",
                          "SandyClayLoam",
                          "MediumLoam",
                          "SandyClay",
                          "ClayLoam",
                          "Clay",
                          "SiltyClay",
                          "SiltyClayLoam",
                          "SiltyLoam",
                          "Silt",
                          "Unknown"])


if __name__ == "__main__":
    print(helper_random_soiltype())
