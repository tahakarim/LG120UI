import random


def helper_random_fieldpoint(corner1, corner2):
    """
    Function to return random point in field

    :param corner1: the bottom left corner of the field
    :type corner1: tuple

    :param corner2: the top right corner of the field
    :type corner2: tuple

    :return: returns a lat/long in the field
    :rtype: tuple
    """

    x = random.uniform(corner1[0], corner2[0])
    y = random.uniform(corner1[1], corner2[1])
    point = (x, y)

    return point


def helper_random_gate(corner1, corner2):
    """
    Function to return random point in field

    :param corner1: the bottom left corner of the field
    :type corner1: tuple

    :param corner2: the top right corner of the field
    :type corner2: tuple

    :return: returns a lat/long in the field
    :rtype: tuple
    """

    side = random.randint(1, 4)

    if side == 1:
        gatex = random.uniform(corner1[0], corner2[0])
        gatey = corner2[1]
    elif side == 2:
        gatey = random.uniform(corner1[1], corner2[1])
        gatex = corner2[0]
    elif side == 3:
        gatex = random.uniform(corner1[0], corner2[0])
        gatey = corner1[1]
    elif side == 4:
        gatey = random.uniform(corner1[1], corner2[1])
        gatex = corner1[0]

    point = (gatex, gatey)

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
