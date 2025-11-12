import numpy as np
import matplotlib.pyplot as plt
import logging
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.circuit.random import random_circuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qutip import Qobj


logger = logging.getLogger(__name__)


N = 4  # number of qubits
DEPTH = 3
SHOTS = 1024

SEED = 42


class RandomCircuit:
    def __init__(self, n_qubits, depth, seed=42, verbose=False):
        self.n_qubits = n_qubits
        self.depth = depth
        self.seed = seed
        self.qc = random_circuit(n_qubits, depth, measure=False, seed=seed)
        # self.rng = np.random_generator(seed=seed)

        self.verbose = verbose
        if verbose:
            logging.info("Created Random Circuit:")
            logging.info(self.qc.draw('text'))
        self.dm = self.get_densitymatrix(self.qc)
        
        return

    def measure(self, pauli_basis):
        # Add the respective rotations to measure X or Y
        measure_qc = self.qc.copy()
        measure_qc.barrier()  # Add a visual barrier to separate the circuit and the measurements rotations

        for qubit, basis in enumerate(pauli_basis):
            if basis == 'X':
                # To measure in the X-basis, apply H
                measure_qc.h(qubit)
            elif basis == 'Y':
                # To measure in the Y-basis, apply S-dagger, than H
                measure_qc.sdg(qubit)
                measure_qc.h(qubit)
            elif basis == 'Z':
                # To measure Z nothing is required, or just I
                measure_qc.id(qubit)

        # Add measurements layer (by default on the Z-basis)
        measure_qc.measure_all()
        
        if self.verbose:
            logging.info("Final circuit with roatations and measurements:")
            logging.info(measure_qc.draw('text'))

        # Simulate qiskit_aer circuit
        counts = self.simulate(measure_qc)

        return counts


    @staticmethod
    def get_densitymatrix(qc):
        statevector = Statevector.from_instruction(qc)
        density_matrix = DensityMatrix(statevector)

        return density_matrix


    @staticmethod
    def simulate(qc):
        simulator = AerSimulator()
        # transpile the circuit for the simulator
        transpiled_qc = transpile(qc, simulator)

        # Run the simulation
        job = simulator.run(transpiled_qc, shots=SHOTS)
        result = job.result()
        counts = result.get_counts()

        return counts

