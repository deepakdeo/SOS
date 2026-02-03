# SOS: SKA Observation Simulator v2.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simulate SKA1_Mid visibility (radio observations) using CASA toolkit. Create synthetic radio sky models at arbitrary redshifts and simulate realistic interferometric observations.

## 🌟 Features

- **Radio Sky Modeling**: Create synthetic radio halo models at multiple redshifts
- **Cosmological Calculations**: K-corrections and angular diameter distances using ΛCDM cosmology (Planck 2015)
- **Visibility Simulation**: Simulate interferometric measurements using CASA toolkit
- **Flexible Configuration**: YAML-based configuration for reproducible simulations
- **Well-Tested Code**: Comprehensive unit tests for coordinate utilities and validators
- **Python 3.8+**: Modern Python wi- **Python 3.8+**: Modern Python wi-
- **Modular Architecture**: Clean separation of concerns for maintainability

## 📋 Requirements

- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations- *- *- *- *- *- *- *- *- *-sh
- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations- *- *- *- \`\`- *- *- *- *- *sag- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulatport- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations- *- *- *- *- *- *- *- *- *- er- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulations-",- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *- *-  simulatiltiple redshifts
images = image_maker.create_model_sky(
    redshifts=[0.1, 0.5, 1.0],
    li    li    li    li    li    li    li    li    li    li    li    li    
)
\`\`\`

#### 2. Using Configuration Files

\`\`\`python
from sos.config.config_loader import ConfigLoader

# Load configuration from YAML
config = ConfigLoader("config.yaml")

# Access values with dot notation
redshifts = config.get("simulation.redshifts")
spectral_index = config.get("simulation.spectral_index")
\`\`\`

#### 3. Simulating Visibility (in CASA)

\`\`\`python
from sos.core.visibility_sim import VisibilitySimulator

# Within CASA environment
simulator = VisibilitySimulator(
    config_file="ska_mid197_new.cfg",
    spectral_index=-1.6,
    channels=1,
)

# Simulate visibility
ms_path = simulator.simulate_visibility(
    image_path="modelsky_0.1.im",
    output_ms_path="visibility_0.1.ms",
    num_scans=1,
    scan_duration_sec=900.0,
)
\`\`\`

## 📁 Project Structure

\`\`\`
SOS/
├── sos/                          # Main package
│   ├── __init__.py
│   ├── constants.py              # Global const│   ├── constants.py              # Global const│   ├── con�   │   ├── image_maker.py        # Sky│   ├eati│   ├── constants.py              # G  # Vi│   ├── constants.py ── config/                   # Confi│   ├── ent
│   │   └── config_loader.py      # YAML config handling
│   └── utils/                    # Utility functions
│       ├── coordinates.py        # RA/DEC conversions
│       ├── logger.py             # Logging setup
│       └── validators.py         # Input validation
├── tests/       �                # Unit tests
├── examples/                     # Example scripts & configs
├── setup.py                      # Setup configuration
├── pyproject.toml               # Project metadata
├── requirements.txt             # Runtime dependencies
└── README.md                    # This file
\`\`\`

## 🧪 Testing

\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`\\`pe annotations
✅ **Configuration Files**: YAML-based config system
✅ **Comprehensive Logging**: Replaced print statements
✅ **Input Validation**: Validates all inputs before processing
✅ **Unit Tests**: 25+ tests for core functionality
✅ **Py✅ **Py✅ **Py✅ **Py✅ **Py✅ **Py✅ **Py✅ **Py✅io✅ **Py✅ **Py✅ **Py✅ **Py✅ **Py✅ **ples
- - - - - - - - - - - - - - - - - - - - - - - - - - -at)
- Configurati- Configurati- Configurati- Configurati- Configurati- Configex- Configurati- Configurati- Configurati- Configuratiuthors- Configurati- Configurati- Configurati- Configurati- ConfiNCR- Configurati- Configurati- Configurati- Configur.0-  **Upd- Configuratuary 2026
