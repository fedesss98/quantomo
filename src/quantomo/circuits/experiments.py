import numpy as np
import matplotlib.pyplot as plt
import logging
import json
import pickle
from tqdm import tqdm

from quantomo.circuits.random_circuit import RandomCircuit
from quantomo import ROOT
from quantomo.utils.config import setup_config


logger = logging.getLogger(__name__)


class Experimentalist:
    def __init__(self, config=''):
        if isinstance(config, str):
            config = setup_config(config)
        elif not isinstance(config, dict):
            raise ValueError("`config` argument must be a file name or a dictionary")

        self.seed = config.get('seed', 42)
        self.rng = np.random.default_rng(seed=self.seed)
        self.verbose = config.get('verbose', False)
        self.name = config.get('name', 'Quantum-Tomography-1')
        if self.verbose:
            logger.info(f"Created the Experimentalist for experiment {self.name}")

        n_qubits = config['circuit'].get('n-qubits', 3)
        depth = config['circuit'].get('depth')
        shots = config['circuit'].get('shots')
        self.circuit = RandomCircuit(n_qubits, depth, seed=self.seed, verbose=self.verbose)

        if config['experiment'].get('pauli_basis'):
            self.pauli_basis = config['experiment']['pauli_basis']
            self.n_experiments = len(self.pauli_basis)
        else:
            self.n_measurements = config['experiment'].get('measurements', 1)
            self.pauli_basis = self.rng.choice(['X', 'Y', 'Z'], (self.n_measurements, n_qubits))

        self.experiment_results = {}

    def run_experiment(self, pauli_basis=[]):
        if not pauli_basis:
            pauli_basis = self.pauli_basis
        
        results = {}
        for i, basis in enumerate(tqdm(pauli_basis)):
            dm = self.circuit.dm
            counts = self.circuit.measure(basis)
            results[i] = {
                'density-matrix': dm.data.tolist(), 
                'measurement-basis': basis, 
                'measurement-statistics': counts
            }
        logger.info("Finished taking measurements.\n")

        self.experiment_results.update(results)

        return results

    def save_results(self, output_file=''):
        if not output_file:
            output_file = ROOT / f"experiments/{self.name}/data/results.pkl"

        with open(output_file, 'wb') as f:
            pickle.dump(self.experiment_results, f)

        logger.info(f"Successfully saved experiments' results in {output_file}")
        return


if __name__ == "__main__":
    config = dict()
    experimenter = Experimentalist()
    experimenter.run_experiment()
    experimenter.save_results()
