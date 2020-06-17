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
    for period in range(3, 13):  # period length
        # Create an instant for schedule
        schedule = Schedule(
            [],
            costfunc,
            period,
            variables['no_plants'],
            variables['no_channels'])
        # Set the number of iterations
        no_iterations = {
            "3": 25,
            "4": 75,
            "5": 125,
            "6": 300,
            "7": 900,
            "8": 1800,
            "9": 4000,
            "10": 6000,
            "11": 15000,
            "12": 40000}
        # Create a scheduling bot
        bot = MCTSAgent(no_iterations[str(period)], temperature=1.2)
        # Search for the near-optimal schedule
        cost, sequence = bot.select_action(schedule)
        # Print the near-optimal schedule and the associated cost
        print("Period: {}, Near-optimal cost: {:3.4f}, Sequence: {}.".format(period, cost, sequence))
