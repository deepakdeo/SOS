"""
Example script: Using configuration files with SOS.

Demonstrates loading and using YAML configuration files for reproducible simulations.
"""

from sos.config.config_loader import ConfigLoader, create_default_config
from sos.core.image_maker import ImageMaker
from sos.utils.logger import setup_logger
import yaml

logger = setup_logger(__name__, log_file="example_config.log")

# Example 1: Create and save default config
print("=" * 60)
print("Example 1: Creating default configuration")
print("=" * 60)

default_config = create_default_config()

with open("sos_config_default.yaml", "w") as f:
    yaml.dump(default_config, f, default_flow_style=False)

logger.info("Default configuration saved to sos_config_default.yaml")

# Example 2: Load configuration from file
print("\n" + "=" * 60)
print("Example 2: Loading configuration from file")
print("=" * 60)

config_loader = ConfigLoader("sos_config_default.yaml")
config = config_loader.to_dict()

# Access nested configuration values
redshifts = config_loader.get("simulation.redshifts")
spectral_index = config_loader.get("simulation.spectral_index")
cell_size = config_loader.get("image.cell_size")

logger.info(f"Loaded redshifts: {redshifts}")
logger.info(f"Spectral index: {spectral_index}")
logger.info(f"Cell size: {cell_size}")

# Example 3: Create ImageMaker from configuration
print("\n" + "=" * 60)
print("Example 3: Creating ImageMaker from configuration")
print("=" * 60)

image_maker = ImageMaker(
    cell_size=config_loader.get("image.cell_size"),
    image_size=config_loader.get("image.image_size"),
    reference_frequency=config_loader.get("image.reference_frequency"),
)

logger.info("ImageMaker initialized from configuration")
