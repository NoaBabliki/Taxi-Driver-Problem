import itertools
import random
import utils
import taxi_problem_solver as tps
from genetic_funcs_interface import GeneticFuncsInterface

SIZE_OF_POPULATION = 20  # must be an even number


class GeneticTaxiProblemSolver:
    """
    A heuristic optimization method which operates through nondeterministic, randomized search. The set of possible
    solutions for the optimization problem is considered as a population of individuals.
    The degree of adaptation of an individual to its environment is specified by its fitness.
    """

    def __init__(self, list_of_passengers, taxi_start_position, funcs: GeneticFuncsInterface):
        """

        :param list_of_passengers: list of passengers to try find a good rout between
        :param taxi_start_position: the start position (coordinate) of the taxi driver
        :param funcs: interface that include crossover function and mutation function
        """
        self.list_of_passengers = list_of_passengers
        self.taxi_start_position = taxi_start_position
        self._funcs = funcs

    def __str__(self):
        return 'Genetic Algorithm'

    def init_population(self):
        """

        :return: a list of random solution
        """
        population = []
        for i in range(SIZE_OF_POPULATION):
            rand = tps.RandomTaxiProblemSolver(self.list_of_passengers, (0, 0), None)
            solution_random = rand.solve()
            population.append(solution_random)
        return population

    def solve(self, num_iteration=400, prob_to_mut=0.05):
        """

        :param num_iteration: how many generation to run before the algorithm stops
        :param prob_to_cross: probability to execute cross between 2 parents
        :param prob_to_mut: probability to execute mutation on a child
        :return: the best path and its length
        """
        population = self.init_population()
        best_sol, best_length = population[0], utils.MAX_INT
        for generation in range(num_iteration):
            lengths = [utils.get_solution_len(sol) for sol in population]  # lengths of all solutions
            lengths.sort()
            if (max(lengths) / min(lengths)) < 1.02:
                break
            for i in range(SIZE_OF_POPULATION):
                if lengths[i] < best_length:
                    best_sol, best_length = population[i], lengths[i]

            # selected = [selection(population, lengths) for _ in range(SIZE_OF_POPULATION)]
            inx = list(itertools.combinations(range(SIZE_OF_POPULATION), 2))
            random.shuffle(inx)

            children = list()
            for i in range(0, SIZE_OF_POPULATION):
                p1, p2 = population[inx[i][0]], population[inx[i][1]]
                for child in self._funcs.crossover(p1, p2):
                    child = self._funcs.mutation(child, prob_to_mut)
                    children.append(child)

            population += children
            population.sort(key=lambda x: utils.get_solution_len(x))
            tmp, cur_len = [population[0]], utils.get_solution_len(population[0])
            for candidate in population:
                candidate_len = utils.get_solution_len(candidate)
                if candidate_len != cur_len:
                    cur_len = candidate_len
                    tmp.append(candidate)
            population = tmp[:SIZE_OF_POPULATION]

        return best_sol, best_length
