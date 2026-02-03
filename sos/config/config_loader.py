"""
Configuration loader for SOS (SKA Observation Simulator).

Supports YAML configuration files for flexible, reproducible simulations.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from sos.utils.logger import setup_logger
from sos.utils.validators import (
    validate_redshifts,
    validate_spectral_index,
    validate_config_file,
)

logger = setup_logger(__name__)


class ConfigLoader:
    """Load and validate SOS configuration from YAML files."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to YAML configuration file.
        """
        self.config_path = Path(config_path) if config_path else None
        self.config: Dict[str, Any] = {}

        if self.config_path:
            self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Configuration dictionary.

        Raises:
            FileNotFoundError: If config file not found.
            yaml.YAMLError: If YAML parsing fails.
        """
        if not self.config_path:
            raise ValueError("No config path specified")

        validate_config_file(self.config_path)

        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        logger.info(f"Configuration loaded from {self.config_path}")
        self._validate_config()

        return self.config

    def _validate_config(self) -> None:
        """Validate loaded configuration."""
        if not self.config:
            raise ValueError("Configuration is empty")

        # Validate simulation section
        if "simulation" in self.config:
            sim = self.config["simulation"]
            if "redshifts" in sim:
                validate_redshifts(sim["redshifts"])
            if "spectral_index" in sim:
                validate_spectral_index(sim["spectral_index"])

        logger.debug("Configuration validation passed")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports nested keys with dots).

        Args:
            key: Configuration key (e.g., "simulation.redshifts").
            default: Default value if key not found.

        Returns:
            Configuration value.
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config


def create_default_config() -> Dict[str, Any]:
    """
    Create a default configuration dictionary.

    Returns:
        Default configuration structure.
    """
    return {
        "simulation": {
            "redshifts": [0.05, 0.1, 0.13, 0.15, 0.17, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1.0],
            "spectral_index": -1.6,
            "channels": 1,
            "frequency_resolution_mhz": 50.0,
            "integration_time": "1s",
        },
        "source": {
            "linear_size_mpc": 0.5,
            "flux_density_jy": 0.6,
            "source_type": 1,  # 1=extended, 2=point, 3=mixed
        },
        "image": {
            "cell_size": "0.01arcsec",
            "image_size": 7200,
            "reference_frequency": "9.2GHz",
        },
        "telescope": {
            "config_file": "ska_mid197_new.cfg",
            "elevation_limit": 17.0,
        },
        "observation": {
            "rise_time": "56839.0d",
            "num_scans": 1,
            "start_time_sec": 1.0,
            "scan_duration_sec": 2.0,
            "scan_gap_sec": 0.0,
        },
    }
