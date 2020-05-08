import numpy as np
from typing import Dict
from functions import costfunction
from models import Schedule
from mcts import MCTSAgent


# create a python dictionary
variables: Dict = {}
# number of systems
variables['no_plants']: int = 3
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


if __name__ == "__main__":
    # construct the cost function
    costfunc = costfunction(variables)
    # create an instant for schedule
    schedule = Schedule([], costfunc, 7, 3)
    # ...
    bot = MCTSAgent(100, temperature=2.0)
    #
    move = bot.select_move(schedule)