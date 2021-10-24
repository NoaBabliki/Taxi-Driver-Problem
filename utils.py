import math
import matplotlib.pyplot as plt

MAX_INT = float('inf')


def euclidean_distance(a, b):
    """calculates the euclidean distance between points a and b"""
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def check_solution(solution):
    """
    checks if the solution is legal,raise error if not
    :param solution: solution to check
    :return: None
    """
    passengers_on, passengers_off = set(), set()
    for i in range(1, len(solution)):
        loc, passengers_id, is_down_station = solution[i]
        if not is_down_station:
            if passengers_id in passengers_on:
                raise Exception('error')
            passengers_on.add(passengers_id)
        else:
            if passengers_id not in passengers_on:
                raise Exception('error')
            if passengers_id in passengers_off:
                raise Exception('error')
            passengers_off.add(passengers_id)


def get_solution_len(solution):
    """
    checks the length of the given solution
    :param solution: solution to check its length
    :return: the length
    """

    s = 0
    for i in range(1, len(solution)):
        s += euclidean_distance(solution[i - 1][0], solution[i][0])
    return s


def set_data_for_solution(solution):
    """arrange the solution's data before plot"""

    check_solution(solution)
    s = get_solution_len(solution)

    x, y = [p[0][0] for p in solution], [p[0][1] for p in solution]
    z = [p[1] for p in solution]

    return x, y, z, s


def plot_multiple_solutions(num_rows, num_cols, solutions, algs):
    """plot solutions of several algorithms in num_rows*num_cols subplots"""

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 6), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.001)

    for i in range(num_rows):
        for j in range(num_cols):
            x, y, z, s = set_data_for_solution(solutions[num_cols * i + j])
            axs[i, j].plot(x, y)

            axs[i, j].set_title(str(algs[num_cols * i + j]) + ": " + str(s))
            for k in range(len(x)):
                axs[i, j].annotate(str(z[k]), (x[k], y[k]),
                                   textcoords="offset points", xytext=(0, 5), ha='center')
    plt.show()


def get_other_station_from_solution(solution, passenger_id):
    """

    :param solution: a given solution of the problem without 1 station
    :param passenger_id: unique id of passenger
    :return: the second station that matches the id
    """

    for sid, s in enumerate(solution):
        if passenger_id == s[1]:
            return sid


def get_set_of_neighbors(solution):
    """

    :param solution: a given solution
    :return: a list of all neighbors for this solution
    """
    set_of_neighbors = []
    for station_id, station in enumerate(solution):
        if station_id == 0:
            continue
        if station[2]:  # it is a destination station
            neighbor_wo_dest = solution[:station_id] + solution[station_id + 1:]
            origin_station_id = get_other_station_from_solution(neighbor_wo_dest, station[1])
            for new_sid in range(origin_station_id + 1, len(neighbor_wo_dest) + 1):
                if new_sid == station_id:
                    continue
                new_nieghbor = neighbor_wo_dest[:new_sid] + [station] + neighbor_wo_dest[new_sid:]
                set_of_neighbors.append(new_nieghbor)
        else:  # it is an origin station
            neighbor_wo_origin = solution[:station_id] + solution[station_id + 1:]
            dest_station_id = get_other_station_from_solution(neighbor_wo_origin, station[1])
            for new_sid in range(1, dest_station_id + 1):
                if new_sid == station_id:
                    continue
                new_nieghbor = neighbor_wo_origin[:new_sid] + [station] + neighbor_wo_origin[new_sid:]
                set_of_neighbors.append(new_nieghbor)

    return set_of_neighbors
