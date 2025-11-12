import click
import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.circuit.random import random_circuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qutip import Qobj

from quantomo.utils.logging import setup_logger
from quantomo.circuits.experiments import Experimentalist


N = 4  # number of qubits
DEPTH = 3
SHOTS = 1024

SEED = 42

random.seed(SEED)


def get_densitymatrix(qc):
    statevector = Statevector.from_instruction(qc)
    density_matrix = DensityMatrix(statevector)

    return density_matrix


def simulate(qc):
    simulator = AerSimulator()
    # transpile the circuit for the simulator
    transpiled_qc = transpile(qc, simulator)

    # Run the simulation
    job = simulator.run(transpiled_qc, shots=SHOTS)
    result = job.result()
    counts = result.get_counts()

    return counts


@click.command()
def main():
    logger = setup_logger()
    
    logger.info(f"\n\n{'='*10} STARTING EXPERIMENT {'='*10}\n\n")
    
    experimenter = Experimentalist()
    experimenter.run_experiment()
    experimenter.save_results()

    logger.info(f"\n\n{'='*17} END {'='*17}\n\n")

    return None


if __name__ == "__main__":
    main()



