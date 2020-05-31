import random
from functions import costfunction
from models import Schedule, systems
from mcts import MCTSAgent


if __name__ == "__main__":
    # Set the random seeds for reproducibility
    random.seed(40)
    # Create a set of feedback control systems
    variables = systems(2, 1, 1, 3, 1, 20)
    # Construct a cost function
    costfunc = costfunction(variables)
    # Create an instant for schedule
    schedule = Schedule(
        [],
        costfunc,
        10,
        variables['no_plants'],
        variables['no_channels'])
    # Create a scheduling bot
    bot = MCTSAgent(50000, temperature=1.2)
    # Search for the near-optimal schedule
    cost, sequence = bot.select_action(schedule)
    # Print the near-optimal schedule and the associated cost
    print("The near-optimal sequence is {} and its associated cost is {:3.4f}.".format(sequence, cost))
