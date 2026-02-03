# SOS: SKA Observation Simulator

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simulate SKA1_Mid visibility (radio observations) using CASA toolkit. Create synthetic radio sky models at arbitrary redshifts and simulate realistic interferometric observations.

<p align="center">
  <img src="ska_uv.png" alt="SKA UV Coverage" width="500"/>
  <br>
  <em>Figure: UV coverage from 15 min of simulated observation with SKA1_Mid.</em>
</p>

## Features

- **Radio Sky Modeling**: Create synthetic radio halo models at multiple redshifts
- **Cosmological Calculations**: K-corrections and angular diameter distances using ΛCDM cosmology (Planck 2015)
- **Visibility Simulation**: Simulate interferometric measurements using CASA toolkit
- **Flexible Configuration**: YAML-based configuration for reproducible simulations
- **Well-Tested Code**: Comprehensive unit tests for all utilities
- **Modern Python**: Python 3.8+ with full type hints and documentation
- **Clean Architecture**: Modular package structure for maintainability

## Requirements

- **Python**: 3.8 or higher
- **CASA**: 4.7.2 or higher (for visibility simulations)
- **Dependencies**: See [requirements.txt](requirements.txt)

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/deepakdeo/SOS.git
cd SOS

# Install package
pip install -e .

# For development (includes testing tools)
pip install -e ".[dev]"
```

### Basic Usage

#### 1. Creating Model Sky Images

```python
from sos.core.image_maker import ImageMaker, CosmologyCalculator
from sos.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)

# Create image maker
image_maker = ImageMaker(
    cell_size="0.01arcsec",
    image_size=7200,
    reference_frequency="9.2GHz",
)

# Create models at multiple redshifts
images = image_maker.create_model_sky(
    redshifts=[0.1, 0.5, 1.0],
    linear_size_mpc=0.5,
    reference_flux_jy=0.6,
    spectral_index=-1.6,
)
```

#### 2. Using Configuration Files

```python
from sos.config.config_loader import ConfigLoader

# Load configuration from YAML
config = ConfigLoader("config.yaml")

# Access values with dot notation
redshifts = config.get("simulation.redshifts")
spectral_index = config.get("simulation.spectral_index")
```

#### 3. Simulating Visibility (in CASA)

```python
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
```

## Project Structure

```
SOS/
├── sos/                          # Main package
│   ├── __init__.py
│   ├── constants.py              # Global constants
│   ├── core/                     # Core simulation modules
│   │   ├── image_maker.py        # Sky model creation
│   │   └── visibility_sim.py     # Visibility simulation
│   ├── config/                   # Configuration management
│   │   └── config_loader.py      # YAML config handling
│   └── utils/                    # Utility functions
│       ├── coordinates.py        # RA/DEC conversions
│       ├── logger.py             # Logging setup
│       └── validators.py         # Input validation
├── tests/                        # Unit tests
├── examples/                     # Example scripts & configs
├── setup.py                      # Setup configuration
├── pyproject.toml               # Project metadata
├── requirements.txt             # Runtime dependencies
├── README.md                    # This file
└── ska_uv.png                  # Sample UV coverage
```

## Contents

1. **make_img.py** : Creates toy-model radio sky based on inputs provided
2. **SOS.py** : Simulates SKA visibility when a radio sky and SKA configuration file is provided
3. **ska_mid197.cfg** : Configuration file with 197 antennas (including MeerKAT)
4. **ska_mid133.cfg** : Configuration file with 133 antennas (excluding MeerKAT)
5. **SOSv2.py** : SKA simulation for CASA versions > 4.7.2
6. **ska_mid197_new.cfg** : New configuration for CASA 4.7.2+ (197 antennas)
7. **ska_mid133_new.cfg** : New configuration for CASA 4.7.2+ (133 antennas)
8. **ska_uv.png** : Sample UV coverage (15-min observation)

*SOS works with CASA 4.7.2 or earlier*  
*SOSv2.py requires CASA versions > 4.7.2*

## Configuration

Create a `config.yaml` file to customize your simulation:

```yaml
simulation:
  redshifts: [0.05, 0.1, 0.5, 1.0]
  spectral_index: -1.6
  channels: 1
  frequency_resolution_mhz: 50.0

source:
  linear_size_mpc: 0.5
  reference_flux_jy: 0.6
  source_type: 1  # 1=extended, 2=point, 3=mixed

image:
  cell_size: "0.01arcsec"
  image_size: 7200
  reference_frequency: "9.2GHz"

telescope:
  config_file: "ska_mid197_new.cfg"
  elevation_limit: 17.0
```

See [examples/config_example.yaml](examples/config_example.yaml) for full configuration options.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sos

# Run tests in parallel
pytest -n auto
```

## Module Overview

### sos.constants
Global constants used throughout the package:
- Coordinate conversion factors
- Astronomy constants (speed of light, Planck 2015 cosmology)
- Telescope and observation defaults
- Source model parameters

### sos.core.image_maker
- **CosmologyCalculator**: ΛCDM distance and angular size calculations
- **ImageMaker**: Create synthetic radio sky models

### sos.core.visibility_sim
- **VisibilitySimulator**: Simulate interferometric visibility measurements

### sos.config.config_loader
- **ConfigLoader**: Load and validate YAML configurations
- Nested key access with dot notation

### sos.utils.coordinates
Consolidated coordinate conversion functions:
- `ra_arcsec_to_hms()` - RA to HH:MM:SS format
- `dec_arcsec_to_dms()` - DEC to ±DD:MM:SS format
- `parse_ra_hms()` - Parse RA string to decimal
- `parse_dec_dms()` - Parse DEC string to decimal

### sos.utils.validators
Comprehensive input validation:
- Redshift ranges and spectral index bounds
- File existence and format checking
- Coordinate string format validation
- Image parameter validation

### sos.utils.logger
Centralized logging with console and file output.

## Improvements from Original

✅ **Modular Architecture**: Well-organized package structure  
✅ **No Duplication**: Consolidated duplicate functions  
✅ **Type Hints**: Full Python 3.8+ annotations  
✅ **Configuration Files**: YAML-based configuration system  
✅ **Comprehensive Logging**: Professional logging throughout  
✅ **Input Validation**: Early error detection  
✅ **Unit Tests**: 25+ comprehensive tests  
✅ **Better Documentation**: Examples and API docs  

## Troubleshooting

**CASA Not Found**
```
ImportError: CASA toolkit not available
```
Solution: Run SOS scripts within CASA environment:
```bash
casa -c "execfile('script.py')"
```

**Configuration File Not Found**
```
FileNotFoundError: File not found: config.yaml
```
Solution: Specify full path or ensure file exists in current directory.

**Coordinate Conversion Errors**
Check coordinate string format:
- RA: `"HHhMMmSS.Ss"` (e.g., `"04h30m15.50s"`)
- DEC: `"±DDdMMmSS.Ss"` (e.g., `"-20d30m45.50s"`)

## Examples

See [examples/](examples/) directory for complete examples:
1. `example_image_maker.py` - Create model images with cosmological scaling
2. `example_config.py` - Load and use YAML configurations
3. `config_example.yaml` - Complete configuration template

## References

- **SKA**: Square Kilometre Array - https://www.skao.org/
- **CASA**: Common Astronomy Software Applications - https://casa.nrao.edu/

## License

MIT License - See [LICENSE](LICENSE) file

## Authors

- **Deepak Deo**
- **Dr. Ruta Kale** (NCRA-TIFR)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Version 1.0 (refactored) | Updated February 2026*
