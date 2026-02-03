"""
Input validation utilities for SOS (SKA Observation Simulator).

Provides functions to validate configuration parameters, file paths,
and astronomical values before simulation.
"""

from pathlib import Path
from typing import List, Union
import re

from sos.constants import (
    MIN_REDSHIFT,
    MAX_REDSHIFT,
    MIN_SPECTRAL_INDEX,
    MAX_SPECTRAL_INDEX,
    MIN_FLUX_DENSITY_JY,
    MAX_FLUX_DENSITY_JY,
)


def validate_redshifts(redshifts: List[float]) -> bool:
    """
    Validate list of redshift values.

    Args:
        redshifts: List of redshift values.

    Returns:
        True if all redshifts are valid.

    Raises:
        ValueError: If any redshift is invalid.
    """
    if not isinstance(redshifts, list) or len(redshifts) == 0:
        raise ValueError("Redshifts must be a non-empty list")

    for z in redshifts:
        if not isinstance(z, (int, float)):
            raise ValueError(f"Redshift must be numeric, got {type(z)}")
        if not (MIN_REDSHIFT <= z <= MAX_REDSHIFT):
            raise ValueError(
                f"Redshift {z} out of range [{MIN_REDSHIFT}, {MAX_REDSHIFT}]"
            )

    return True


def validate_spectral_index(alpha: float) -> bool:
    """
    Validate spectral index value.

    Args:
        alpha: Spectral index (typically negative for radio sources).

    Returns:
        True if spectral index is valid.

    Raises:
        ValueError: If spectral index is invalid.
    """
    if not isinstance(alpha, (int, float)):
        raise ValueError(f"Spectral index must be numeric, got {type(alpha)}")
    if not (MIN_SPECTRAL_INDEX <= alpha <= MAX_SPECTRAL_INDEX):
        raise ValueError(
            f"Spectral index {alpha} out of range "
            f"[{MIN_SPECTRAL_INDEX}, {MAX_SPECTRAL_INDEX}]"
        )
    return True


def validate_flux_density(flux_jy: float) -> bool:
    """
    Validate flux density in Jy.

    Args:
        flux_jy: Flux density in Jansky (Jy).

    Returns:
        True if flux density is valid.

    Raises:
        ValueError: If flux density is invalid.
    """
    if not isinstance(flux_jy, (int, float)):
        raise ValueError(f"Flux density must be numeric, got {type(flux_jy)}")
    if not (MIN_FLUX_DENSITY_JY <= flux_jy <= MAX_FLUX_DENSITY_JY):
        raise ValueError(
            f"Flux density {flux_jy} Jy out of range "
            f"[{MIN_FLUX_DENSITY_JY}, {MAX_FLUX_DENSITY_JY}]"
        )
    return True


def validate_file_exists(file_path: Union[str, Path]) -> bool:
    """
    Validate that a file exists.

    Args:
        file_path: Path to file.

    Returns:
        True if file exists.

    Raises:
        FileNotFoundError: If file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path.absolute()}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path.absolute()}")
    return True


def validate_config_file(config_path: Union[str, Path]) -> bool:
    """
    Validate telescope configuration file format.

    Args:
        config_path: Path to .cfg configuration file.

    Returns:
        True if config file is valid.

    Raises:
        ValueError: If file is invalid.
    """
    validate_file_exists(config_path)

    path = Path(config_path)
    if path.suffix.lower() != ".cfg":
        raise ValueError(f"Configuration file must have .cfg extension, got {path.suffix}")

    # Basic sanity check: file should not be empty
    if path.stat().st_size == 0:
        raise ValueError(f"Configuration file is empty: {path}")

    return True


def validate_frequency(freq_value: float, freq_unit: str = "GHz") -> bool:
    """
    Validate frequency value and unit.

    Args:
        freq_value: Frequency value.
        freq_unit: Frequency unit (Hz, MHz, GHz).

    Returns:
        True if frequency is valid.

    Raises:
        ValueError: If frequency is invalid.
    """
    valid_units = ["Hz", "MHz", "GHz"]
    if freq_unit not in valid_units:
        raise ValueError(f"Invalid frequency unit: {freq_unit}. Must be one of {valid_units}")

    if not isinstance(freq_value, (int, float)) or freq_value <= 0:
        raise ValueError(f"Frequency must be positive numeric value, got {freq_value}")

    return True


def validate_coordinate_string(coord_string: str, coord_type: str = "ra") -> bool:
    """
    Validate RA/DEC coordinate string format.

    Args:
        coord_string: Coordinate string (e.g., "04h30m15.5s").
        coord_type: Type of coordinate ("ra" or "dec").

    Returns:
        True if coordinate string is valid.

    Raises:
        ValueError: If format is invalid.
    """
    if coord_type.lower() == "ra":
        # RA pattern: HHhMMmSS.Ss
        pattern = r"^(\d{1,2})h(\d{1,2})m(\d{1,2}(?:\.\d+)?)s$"
    elif coord_type.lower() == "dec":
        # DEC pattern: ±DDdMMmSS.Ss
        pattern = r"^([+-])?(\d{1,2})d(\d{1,2})m(\d{1,2}(?:\.\d+)?)s$"
    else:
        raise ValueError(f"Invalid coordinate type: {coord_type}")

    if not re.match(pattern, coord_string):
        raise ValueError(
            f"Invalid {coord_type.upper()} format: {coord_string}. "
            f"Expected format: {'HHhMMmSS.Ss' if coord_type.lower() == 'ra' else '±DDdMMmSS.Ss'}"
        )

    return True


def validate_image_parameters(
    cell_size: str,
    image_size: int,
    frequency: str
) -> bool:
    """
    Validate image creation parameters.

    Args:
        cell_size: Cell size (e.g., "0.01arcsec").
        image_size: Image size in pixels.
        frequency: Reference frequency (e.g., "9.2GHz").

    Returns:
        True if all parameters are valid.

    Raises:
        ValueError: If any parameter is invalid.
    """
    # Validate cell size format
    if not re.match(r"^\d+(?:\.\d+)?arcsec$", cell_size):
        raise ValueError(f"Invalid cell size format: {cell_size}. Expected 'NNarcsec'")

    # Validate image size
    if not isinstance(image_size, int) or image_size <= 0:
        raise ValueError(f"Image size must be positive integer, got {image_size}")

    # Validate frequency format
    if not re.match(r"^\d+(?:\.\d+)?GHz$", frequency):
        raise ValueError(f"Invalid frequency format: {frequency}. Expected 'NNGHz'")

    return True
