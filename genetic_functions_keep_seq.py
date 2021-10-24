from random import random, randint, choice

import utils


def get_other_station_from_solution(solution, passenger_id):
    for sid, s in enumerate(solution):
        if passenger_id == s[1]:
            return sid


def find_matches(p1, p2):
    matches = [False] * len(p1)
    for i in range(1, len(p1) - 1):
        if (p1[i] == p2[i]) & (p1[i + 1] == p2[i + 1]):
            matches[i], matches[i + 1] = True, True

    return matches


def _copy_until_crossover_point(c, matches, cross_point):
    inx = 0
    while cross_point != 0:
        if not matches[inx]:
            matches[inx] = True
            cross_point -= 1
        inx += 1

    return [v if matches[i] else None for i, v in enumerate(c)], {(v[1], v[2]) for i, v in enumerate(c) if
                                                                  not matches[i]}


def _complete_solution(sol, matches, missing_points):
    if not missing_points:
        return matches

    inx = 0
    for i in range(1, len(sol)):
        while matches[inx] is not None:
            if inx == len(sol) - 1:
                break
            inx += 1
        if (sol[i][1], sol[i][2]) in missing_points:
            matches[inx] = sol[i]

    return matches


def crossover(p1, p2):
    """

    :param p1: first parent
    :param p2: second parent
    :param cross_prob: probability to execute cross
    :return: two children
    """

    c1, c2 = p1.copy(), p2.copy()
    matches = find_matches(p1, p2)
    matches2 = matches.copy()

    cross_inx = len(p1) - matches.count(True)
    cross_point = randint(1, cross_inx)

    c1, missing_points1 = _copy_until_crossover_point(c1, matches, cross_point)
    c2, missing_points2 = _copy_until_crossover_point(c2, matches2, cross_point)

    c1 = _complete_solution(p2, c1, missing_points1)
    c2 = _complete_solution(p1, c2, missing_points2)

    if None in c1 or None in c2:
        c1 = _complete_solution(p2, c1, missing_points1)
        c2 = _complete_solution(p1, c2, missing_points2)

    return c1, c2


def mutation_keep_sorted(sol, mut_prob):
    if random() < mut_prob:
        return choice(utils.get_set_of_neighbors(sol))
    return sol