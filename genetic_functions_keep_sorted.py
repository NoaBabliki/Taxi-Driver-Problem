from random import random, choice
import utils


def sort_stations(p2, seq_from_p1, most_before, most_after, remainders):
    sorted_before, sorted_after = [], []
    for station in p2:
        if station in most_before:
            sorted_before.append(station)
            most_before.remove(station)
        if station in most_after:
            sorted_after.append(station)
        if station in remainders:
            # then, if there is still most_before we most sort, we insert the station in the
            # before list, else, we keep it sorted inside most_after
            if most_before:
                sorted_before.append(station)
            else:
                sorted_after.append(station)
    return sorted_before + seq_from_p1 + sorted_after


def crossover_keep_sorted(p1, p2):
    start_station, p1, p2 = p1[0], p1[1:], p2[1:]
    start, end = random(), random()
    start, end = min([start, end]), max([start, end])
    start, end = int(start*len(p1)), int(end*len(p1))+1
    seq_from_p1 = p1[start:end]

    take_passengers_id = [station[1] for station in seq_from_p1 if not station[2]]
    drop_passengers_id = [station[1] for station in seq_from_p1 if station[2]]

    most_before = {station for station in p1 if not station[2] and station[1] in drop_passengers_id
                   and station[1] not in take_passengers_id}
    most_after = {station for station in p1 if station[2] and station[1] in take_passengers_id
                  and station[1] not in drop_passengers_id}

    remainders = {station for station in p2 if station not in
                  set(seq_from_p1).union(most_before).union(most_after)}

    c = [start_station] + sort_stations(p2, seq_from_p1, most_before, most_after, remainders)
    return [c]


def mutation_keep_sorted(sol, mut_prob):
    if random() < mut_prob:
        return choice(utils.get_set_of_neighbors(sol))
    return sol
