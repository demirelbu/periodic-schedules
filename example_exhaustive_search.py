from models import systems
from functions import *


if __name__ == "__main__":
    # Create a set of feedback control systems
    variables = systems(2, 1, 1, 3, 1, 20)
    # Construct a cost function
    costfunc = costfunction(variables)
    # Find the all allocation options
    all_scheduling_options = find_all_allocation_options(
        variables['no_plants'], variables['no_channels'])
    # Compute the cardinality of the sequence of the all possible allocation
    cardinality = len(all_scheduling_options)
    for period in range(3, 13):  # period length
        # Create a complete search tree (that includes only indices)
        sequences = create_complete_search_tree(cardinality, period)
        # Create a list to gather the costs associated with schedules
        cost_list = []
        # Compute the costs associated with schedules
        for sequence in sequences:
            cost_list.append(costfunc(sequence))
        # Print the period, the lowest cost, the corresponding schedule
        print("Period: {}, Min cost: {:3.4f}, Sequence: {}.".format(period,
                                                                    min(cost_list),
                                                                    index2schedule(sequences[cost_list.index(min(cost_list))],
                                                                                   variables['no_plants'],
                                                                                   variables['no_channels'])))
