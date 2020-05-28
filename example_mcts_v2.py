import random
import numpy as np
from typing import Dict
from functions import costfunction
from models import Schedule
from mcts import MCTSAgent


def systems():
    # create a python dictionary
    variables: Dict = {}
    # number of systems
    variables['no_plants']: int = 5
    # number of channels
    variables['no_channels']: int = 2
    # System 1
    variables['A1'] = np.matrix([[0.8114, 0.3277], [0.4478, 0.8819]])
    variables['B1'] = np.matrix([[0.6651], [0.8834]])
    variables['C1'] = np.matrix([[0.7117, 0.6653]])
    variables['Q1'] = np.matrix(
        [[1.2146, 0.2539], [0.2539, 1.4417]])                   # state cost
    variables['R1'] = np.matrix(
        [[0.6676]])                                             # control cost
    # covariance of process noise
    variables['W1'] = np.matrix([[1.0324, 0.1464], [0.1464, 0.7221]])
    # covariance of measurement noise
    variables['V1'] = np.matrix([[0.7158]])
    # System 2
    variables['A2'] = np.matrix([[0.6538, 0.6301], [0.5739, 0.7875]])
    variables['B2'] = np.matrix([[0.1314], [0.1582]])
    variables['C2'] = np.matrix([[0.9958, 0.9315]])
    variables['Q2'] = np.matrix(
        [[0.9600, 0.4860], [0.4860, 1.2684]])                   # state cost
    variables['R2'] = np.matrix(
        [[1.0161]])                                             # control cost
    # covariance of process noise
    variables['W2'] = np.matrix(
        [[0.8992, -0.4091], [-0.4091, 1.2267]])
    # covariance of measurement noise
    variables['V2'] = np.matrix([[0.9359]])
    # System 3
    variables['A3'] = np.matrix([[0.3502, 0.6309], [0.2857, 0.8476]])
    variables['B3'] = np.matrix([[0.7238], [0.3317]])
    variables['C3'] = np.matrix([[1.2116, 0.9824]])
    variables['Q3'] = np.matrix(
        [[0.3773, 0.1158], [0.1158, 0.4689]])                   # state cost
    variables['R3'] = np.matrix(
        [[1.4400]])                                             # control cost
    # covariance of process noise
    variables['W3'] = np.matrix(
        [[0.6642, -0.1361], [-0.1361, 0.2247]])
    # covariance of measurement noise
    variables['V3'] = np.matrix([[1.2732]])
    # System 4
    variables['A4'] = np.matrix([[0.9231, 0.2357], [0.6234, 0.1020]])
    variables['B4'] = np.matrix([[0.1236], [0.4864]])
    variables['C4'] = np.matrix([[0.2137, 0.4623]])
    variables['Q4'] = np.matrix(
        [[1.7395, 0.5339], [0.5339, 2.4417]])                   # state cost
    # control cost
    variables['R4'] = np.matrix([[0.8543]])
    # covariance of process noise
    variables['W4'] = np.matrix([[1.5225, 0.3215], [0.3215, 0.9335]])
    # covariance of measurement noise
    variables['V4'] = np.matrix([[0.4325]])
    # System 5
    variables['A5'] = np.matrix([[0.3926, 0.0125], [1.0375, 1.3194]])
    variables['B5'] = np.matrix([[0.6147], [0.8327]])
    variables['C5'] = np.matrix([[1.2945, 0.6459]])
    variables['Q5'] = np.matrix(
        [[2.3610, 0.8236], [0.8236, 1.7546]])                   # state cost
    variables['R5'] = np.matrix(
        [[3.1228]])                                             # control cost
    # covariance of process noise
    variables['W5'] = np.matrix(
        [[1.002, 0.6723], [0.6723, 2.2877]])
    # covariance of measurement noise
    variables['V5'] = np.matrix([[0.3249]])
    return variables


if __name__ == "__main__":
    # Set the random seeds for reproducibility
    random.seed(50)
    # Create a set of feedback control systems
    variables = systems()
    # Construct a cost function
    costfunc = costfunction(variables)
    # Create an instant for schedule
    schedule = Schedule(
        [],
        costfunc,
        9,
        variables['no_plants'],
        variables['no_channels'])
    # Create a scheduling bot
    bot = MCTSAgent(500000, temperature=1.2)
    # Search for the near-optimal schedule
    cost, sequence = bot.select_action(schedule)
    # Print the near-optimal schedule and the associated cost
    print("The near-optimal sequence is {} and its associated cost is {:3.4f}.".format(sequence, cost))
