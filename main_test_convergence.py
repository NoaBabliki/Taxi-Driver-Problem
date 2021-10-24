import taxi_problem_solver as tps
import build_map
import genetic_algorithm_solver as gf
from genetic_funcs_interface import GeneticFuncsInterface
import genetic_functions_keep_seq as gf_keep_seq
import genetic_functions_keep_sorted as gf_keep_sorted
import utils
import random

import matplotlib.pyplot as plt


RANDOM = tps.RandomTaxiProblemSolver

GENETIC = gf.GeneticTaxiProblemSolver



NUM_OF_PASSENGERS = 10
ITERATION_TEST_MULTIPLE = 100

def test_m_local_search_with_greedy_as_baseline(iteration_dict):
    passengers = build_map.build_map_of_passengers(NUM_OF_PASSENGERS)
    greedy = tps.GreedyTaxiProblemSolver(passengers, (0, 0))
    solution_greedy = greedy.solve()

    local_search = tps.MultipleLocalSearchTaxiProblemSolver(passengers, (0, 0), solution_greedy, ITERATION_TEST_MULTIPLE)
    solution_local_search = local_search.solve(iteration_dict)


# def test_m_local_search_with_random_as_baseline(iteration_dict):
#     passengers = build_map.build_map_of_passengers(NUM_OF_PASSENGERS)
#
#     rand = tps.RandomTaxiProblemSolver(passengers, (0, 0), None)
#     solution_random = rand.solve()
#
#     local_search = tps.MultipleLocalSearchTaxiProblemSolver(passengers, (0, 0), solution_random)
#     solution_local_search = local_search.solve()


def main_multiple():

    iteration = {}
    iters = list(range(1, ITERATION_TEST_MULTIPLE+1))
    for i in iters:
        iteration[i] = []
    seed_first = 200
    seed_len = 5
    for seed in range(seed_first, seed_first + seed_len):
        random.seed(seed)
        test_m_local_search_with_greedy_as_baseline(iteration)
    average_per_iter = []
    for i in iters:
        average = sum(iteration[i]) / ITERATION_TEST_MULTIPLE
        average_per_iter.append(average)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(iters, average_per_iter, 'b-')


    plt.show()




if __name__ == "__main__":
    main_multiple()
