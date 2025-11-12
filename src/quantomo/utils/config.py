from quantomo import ROOT
import yaml

def setup_config(config_file='') -> dict:
    if not config_file:
        config_file = ROOT / 'configs/config.yaml'

    with open(config_file, "r", encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Create experiment folder
    experiment_name = config.get('name', 'Quantum-Tomography-1')
    experiment_root = ROOT / f"experiments/{experiment_name}/"
    experiment_root.mkdir(parents=True, exist_ok=True)

    (experiment_root / "visualization").mkdir(parents=True, exist_ok=True)
    (experiment_root / "data/measurements").mkdir(parents=True, exist_ok=True)

    # Copy the configuration file in the new folder
    with open(experiment_root / "config.yaml", 'w', encoding='utf-8') as f:
        yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)

    return config

