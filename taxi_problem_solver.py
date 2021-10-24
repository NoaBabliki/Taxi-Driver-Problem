import math
import random
import utils
import itertools


class TaxiProblemSolver:
    """
    General class that initializes the required parameters to solve the Taxi Problem
    """
    def __init__(self, list_of_passengers, taxi_start_position, initial_solution=None):
        """

        :param list_of_passengers: list of passengers to try find a good rout between
        :param taxi_start_position: the start position (coordinate) of the taxi driver
        :param initial_solution: a solution to the problem
        """
        self.list_of_passengers = list_of_passengers
        self.taxi_start_position = taxi_start_position
        self.initial_solution = initial_solution


class LocalSearchTaxiProblemSolver(TaxiProblemSolver):
    """
    An iterative algorithm that starts with an arbitrary solution to a problem, then attempts to find a better solution
    by making an incremental change to the solution (moves 1 station to a different legal location). If the change
    produces a better solution, another incremental change is made to the new solution, and so on until here is no
    further improvements.
    """

    def __str__(self):
        return 'Local Search'

    def solve(self):
        steps_for_demo = []
        solution = self.initial_solution  # list of [((x, y), passenger_id, is_destination), .. ]
        cur_dist = utils.get_solution_len(solution)
        steps_for_demo.append((solution, cur_dist))
        set_of_neighbors = utils.get_set_of_neighbors(solution)
        while len(set_of_neighbors) > 0:
            ind = random.randint(0, len(set_of_neighbors) - 1)
            cur_solution = set_of_neighbors[ind]
            del set_of_neighbors[ind]
            new_dist = utils.get_solution_len(cur_solution)
            if new_dist < cur_dist:
                cur_dist = new_dist
                solution = cur_solution
                steps_for_demo.append((solution, cur_dist))
                set_of_neighbors = utils.get_set_of_neighbors(solution)
        return solution, steps_for_demo


class HillClimbingTaxiProblemSolver(TaxiProblemSolver):
    """
    An iterative algorithm that starts with an arbitrary solution to a problem, then attempts to find a better solution
    by making an incremental change to the solution (moves 1 station to a different legal location). The algorithm takes
    all the possible changes and picks the best, then another incremental change is added to the new solution, and so on
    until here is no further improvements.
    """

    def __str__(self):
        return 'Hill Climbing'

    def solve(self):
        cur_solution = self.initial_solution  # list of [((x, y), passenger_id, is_destination), .. ]
        cur_dist = utils.get_solution_len(cur_solution)
        set_of_neighbors = utils.get_set_of_neighbors(cur_solution)
        while len(set_of_neighbors) > 0:
            min_dist = cur_dist
            opt_solution = cur_solution
            for new_solution in set_of_neighbors:
                new_solution_dist = utils.get_solution_len(new_solution)
                if new_solution_dist < min_dist:
                    min_dist = new_solution_dist
                    opt_solution = new_solution

            if cur_dist <= min_dist:
                break
            cur_solution = opt_solution
            cur_dist = min_dist
            set_of_neighbors = utils.get_set_of_neighbors(cur_solution)
        return cur_solution


class SimulatedAnnealingTaxiProblemSolver(TaxiProblemSolver):
    """
    An iterative algorithm that starts with an arbitrary solution to a problem, then attempts to find a better solution
    by making an incremental change to the solution (moves 1 station to a different legal location).
    the algorithm calculates energy (the distance of the current solution) and makes a move on a state.
    A move can be done if it improves the solution or else with decaying probability.
    """

    def __str__(self):
        return 'Simulated Annealing'

    def solve(self):
        solution = self.initial_solution  # list of [((x, y), passenger_id, is_destination), .. ]
        cur_dist = utils.get_solution_len(solution)
        set_of_neighbors = utils.get_set_of_neighbors(solution)
        alpha = 1 / 25
        t = 100
        rate_of_cooling = 0.995
        while t > 0.1:
            ind = random.randint(0, len(set_of_neighbors) - 1)
            cur_solution = set_of_neighbors[ind]
            new_dist = utils.get_solution_len(cur_solution)

            delta = new_dist - cur_dist
            try:
                prob = alpha * math.exp(-delta / t)
            except OverflowError:
                prob = 1
            if delta < 0 or random.random() < prob:
                cur_dist = new_dist
                solution = cur_solution
                set_of_neighbors = utils.get_set_of_neighbors(solution)

            t *= rate_of_cooling
        return solution


class BeamLocalSearchTaxiProblemSolver(LocalSearchTaxiProblemSolver):
    """
    A version of the LocalSearch algorithm that holds a pool with a fixed size of solutions and add a solution instead
    of another iff the new solution is better.
    """
    def __init__(self, list_of_passengers, taxi_start_position, initial_solution):
        super().__init__(list_of_passengers, taxi_start_position, initial_solution)
        self.NUM_OF_BEAM = 100

    def __str__(self):
        return 'Beam Local Search'

    def solve(self):
        pool = []
        initial_solution = self.initial_solution
        for _ in range(self.NUM_OF_BEAM):
            pool.append([initial_solution,
                         utils.get_solution_len(initial_solution),
                         utils.get_set_of_neighbors(initial_solution)])
        found_improvement = True
        while found_improvement:
            found_improvement = False
            worst_index = max([k for k in range(len(pool))], key=lambda j: pool[j][1])
            worst_score = pool[worst_index][1]
            for i in range(len(pool)):
                solution, solution_score, solution_neighbors = pool[i]
                if not solution_neighbors:
                    continue
                ind = random.randint(0, len(solution_neighbors) - 1)
                new_solution = solution_neighbors[ind]
                del solution_neighbors[ind]
                new_dist = utils.get_solution_len(new_solution)
                if new_dist < worst_score:
                    pool[worst_index] = [new_solution, new_dist, utils.get_set_of_neighbors(new_solution)]
                    worst_index = max([k for k in range(len(pool))], key=lambda j: pool[j][1])
                    worst_score = pool[worst_index][1]
                    found_improvement = True
        return max(pool, key=lambda j: j[1])[0]


class MultipleLocalSearchTaxiProblemSolver(LocalSearchTaxiProblemSolver):
    """
    A version of the LocalSearch algorithm that runs LocalSearch a given number of times and takes the best result
    """

    def __init__(self, list_of_passengers, taxi_start_position, initial_solution, n_tries=35):
        super().__init__(list_of_passengers, taxi_start_position, initial_solution)
        self.n_tries = n_tries

    def __str__(self):
        return 'Multiple Local Search'

    def solve(self, iteration_dict=None):
        """ Finds the neighbor with the shortest route """
        best_solution, best_solution_dist = None, 10 ** 6
        for iter in range(self.n_tries):
            cur_solution = super().solve()[0]
            cur_dist = utils.get_solution_len(cur_solution)
            if cur_dist < best_solution_dist:
                best_solution = cur_solution
                best_solution_dist = cur_dist
            if iteration_dict and iteration_dict[iter]:
                iteration_dict[iter] += [best_solution_dist]
        return best_solution


class RandomTaxiProblemSolver(TaxiProblemSolver):
    """
    Finds a solution be creating a random legal path between all the passengers
    """

    def __str__(self):
        return 'Random'

    def solve(self):
        all_passengers = [[passenger, False] for passenger in self.list_of_passengers]
        cur_position = self.taxi_start_position
        solution = [(cur_position, 0)]
        while all_passengers:

            ind = random.randint(0, len(all_passengers) - 1)
            random_passenger = all_passengers[ind][0]

            if all_passengers[ind][1]:  # already on the vehicle
                solution.append((random_passenger.end, random_passenger.passenger_id, True))
                del all_passengers[ind]
            else:
                solution.append((random_passenger.start, random_passenger.passenger_id, False))
                all_passengers[ind][1] = True
        return solution


class GreedyTaxiProblemSolver:
    """
    Creates a solution by moving to the closest legal next station
    """

    def __init__(self, list_of_passengers, taxi_start_position):
        self.list_of_passengers = list_of_passengers
        self.taxi_start_position = taxi_start_position

    def __str__(self):
        return 'Greedy'

    def solve(self):
        set_of_passengers = {passenger: False for passenger in self.list_of_passengers}

        cur_position = self.taxi_start_position
        solution = [(cur_position, 0)]
        while set_of_passengers:
            closest_passenger, optimal_dist = None, 2000
            for passenger in set_of_passengers.keys():
                passenger_position = passenger.start if not set_of_passengers[passenger] else passenger.end
                cur_dist = utils.euclidean_distance(cur_position, passenger_position)
                if cur_dist < optimal_dist:
                    closest_passenger = passenger
                    optimal_dist = cur_dist

            if set_of_passengers[closest_passenger]:
                cur_position = closest_passenger.end
                solution.append((closest_passenger.end, closest_passenger.passenger_id, True))
                del set_of_passengers[closest_passenger]
            else:
                cur_position = closest_passenger.start
                solution.append((closest_passenger.start, closest_passenger.passenger_id, False))
                set_of_passengers[closest_passenger] = True
        return solution


class BruteForceSolver:
    """
    Find the optimal solution by running over all the possible solutions
    """
    def __init__(self, list_of_passengers, taxi_start_position):
        self.list_of_passengers = list_of_passengers
        self.taxi_start_position = taxi_start_position

    def __str__(self):
        return 'brute force'

    def solve(self):
        all_points = [(passenger.start, passenger.passenger_id, False) for passenger in self.list_of_passengers]\
                     + [(passenger.end, passenger.passenger_id, True) for passenger in self.list_of_passengers]
        possible_paths = [[(passenger.start, passenger.passenger_id, False),
                           (passenger.end, passenger.passenger_id, True)]
                          for passenger in self.list_of_passengers]
        permutations = self.permutation(all_points, possible_paths)
        return min(permutations, key=lambda p: utils.get_solution_len(p))

    def permutation(self, points, constraints):
        all_permutations = itertools.permutations(points, len(points))
        permutations = [list(p) for p in all_permutations if
                        all(p.index(constraints[i][0]) < p.index(constraints[i][1])
                            for i in range(len(constraints)))]
        for p in permutations:
            p.insert(0, (self.taxi_start_position, 0))
        return permutations


class BruteForcePruningSolver:
    """
    Finds the optimal solution in  a more efficient way. This algorithm builds the solutions recursively and stops build
    a solution if it is illegal or if it is longer than a given solution.
    """
    def __init__(self, list_of_passengers, taxi_start_position, best_dist=utils.MAX_INT, best_solution=None):
        """

        :param list_of_passengers: list of passengers to try find a good rout between
        :param taxi_start_position: the start position (coordinate) of the taxi driver
        :param best_dist: the best distance so far for a solution. If the length of a partial solution is bigger than
        this number then the algorithm stops building it.
        :param best_solution: keep track of the best solution so far
        """
        self.list_of_passengers = list_of_passengers
        self.taxi_start_position = taxi_start_position
        self.best_dist = best_dist
        self.best_solution = best_solution

    def __str__(self):
        return 'brute force with pruning'

    def solve(self, solution):
        options = self.get_options(solution, self.list_of_passengers)
        if len(options) == 0:
            candidate = utils.get_solution_len(solution)
            if candidate < self.best_dist:
                self.best_dist = candidate
                self.best_solution = solution
            return
        if utils.get_solution_len(solution) >= self.best_dist:
            return
        for opt in options:
            self.solve(solution + [opt])

    def get_options(self, solution, passengers):
        options = []
        for i, p in enumerate(passengers, 1):
            optpick = (p.start, i, False)
            optdrop = (p.end, i, True)
            if optpick not in solution:
                options.append(optpick)
            elif optdrop not in solution:
                options.append(optdrop)
        return options