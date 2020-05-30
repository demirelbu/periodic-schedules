import numpy as np
import scipy.linalg as la
from typing import Dict


def systems(n: int, m: int, p: int, nUsers: int, nChannels: int, seed: int = 20) -> Dict:
    # Set the random seeds for reproducibility
    np.random.seed(seed)
    # Create a python dictionary
    variables: Dict = {}
    # Set number of systems
    variables['no_plants']: int = nUsers
    # Set number of channels
    variables['no_channels']: int = nChannels
    for index in range(1, nUsers + 1):
        # System variables
        variables['A' + str(index)] = generateSquareMatrix(n, False)
        variables['B' + str(index)] = generateAnyMatrix(n, m)
        variables['C' + str(index)] = generateAnyMatrix(p, n)
        # Performance indices
        variables['Q' + str(index)] = generateSPDmatrix(n)
        variables['R' + str(index)] = generateSPDmatrix(m)
        # Covariance of process noise
        variables['W' + str(index)] = generateSPDmatrix(n)
        # Covariance of measurement noise
        variables['V' + str(index)] = generateSPDmatrix(p)
    return variables


def generateSquareMatrix(n: int, stable: bool = True):
    "This function generates a dense n x n matrix."
    for _ in range(9999):
        M = np.matrix(np.random.rand(n, n))
        eigvals, _ = la.eig(M)
        flag = True if np.max(eigvals) < 1 else False
        if flag == stable:
            return M


def generateAnyMatrix(n: int, m: int):
    "This function generates a dense n x m matrix."
    return np.matrix(np.random.rand(n, m))


def generateSPDmatrix(n: int):
    "This function generates a dense n x n symmetric, positive definite matrix."
    M = np.matrix(np.random.rand(n, n))
    return 0.5 * (M + M.transpose()) + n * np.eye(n)