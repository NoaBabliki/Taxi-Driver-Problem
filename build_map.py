import random


class Passenger:
    """
    Class that represents a passenger in the Taxi Driver Problem. Each passenger has a unique id, a pick up point
    (start) and a drop point (end)
    """
    def __init__(self, passenger_id, start, end):
        self.passenger_id = passenger_id
        self.start = start
        self.end = end

    def __str__(self):
        return 'passenger id ' + str(self.passenger_id) + ': start: ' + str(self.start) + ', end: ' + str(self.end)


def build_map_of_passengers(num_of_passengers):
    """
    build a list of 'num_of_passengers' randomly initialized passengers (random pick up and drop stations)
    :param num_of_passengers:
    :return: a list of passengers
    """
    list_of_passengers = []
    for i in range(1, num_of_passengers + 1):
        start = (random.randint(0, 1000), random.randint(0, 1000))
        end = (random.randint(0, 1000), random.randint(0, 1000))
        list_of_passengers.append(Passenger(i, start, end))

    return list_of_passengers
