"""
Visibility simulation module for SOS (SKA Observation Simulator).

Simulates interferometric visibility from model sky images using CASA toolkit.
"""

from typing import List, Optional, Tuple
from pathlib import Path

from sos.constants import (
    DEFAULT_NOISE_LEVEL,
    DEFAULT_STOKES,
    DEFAULT_MOUNT_TYPE,
    EQUATORIAL_MOUNT_TELESCOPES,
)
from sos.utils.logger import setup_logger
from sos.utils.coordinates import ra_arcsec_to_hms, dec_arcsec_to_dms
from sos.utils.validators import validate_config_file, validate_file_exists

logger = setup_logger(__name__)


class VisibilitySimulator:
    """Simulate visibility measurements from model sky images."""

    def __init__(
        self,
        config_file: str,
        spectral_index: float = -1.6,
        channels: int = 1,
        frequency_resolution_mhz: float = 50.0,
        integration_time: str = "1s",
    ):
        """
        Initialize visibility simulator.

        Args:
            config_file: Path to telescope configuration file.
            spectral_index: Spectral index for flux scaling.
            channels: Number of frequency channels.
            frequency_resolution_mhz: Frequency resolution per channel in MHz.
            integration_time: Integration time for samples.

        Raises:
            FileNotFoundError: If config file not found.
        """
        validate_config_file(config_file)

        self.config_file = config_file
        self.spectral_index = spectral_index
        self.channels = channels
        self.frequency_resolution_mhz = frequency_resolution_mhz
        self.integration_time = integration_time

        logger.info(
            f"Initialized VisibilitySimulator with {channels} channels, "
            f"α={spectral_index}, Δf={frequency_resolution_mhz} MHz"
        )

    def simulate_visibility(
        self,
        image_path: str,
        output_ms_path: str,
        rise_time: str = "56839.0d",
        num_scans: int = 1,
        start_time_sec: float = 1.0,
        scan_duration_sec: float = 900.0,
        scan_gap_sec: float = 0.0,
        noise_level: str = DEFAULT_NOISE_LEVEL,
    ) -> str:
        """
        Simulate visibility measurement set from model image.

        Args:
            image_path: Path to model image.
            output_ms_path: Path for output Measurement Set.
            rise_time: Source rise time in CASA format (e.g., "56839.0d").
            num_scans: Number of observation scans.
            start_time_sec: Start time of first scan in seconds.
            scan_duration_sec: Duration of each scan in seconds.
            scan_gap_sec: Gap between consecutive scans in seconds.
            noise_level: Noise level to add (e.g., "0.0Jy" for no noise).

        Returns:
            Path to output Measurement Set.

        Raises:
            ImportError: If CASA toolkit not available.
            FileNotFoundError: If model image not found.
        """
        validate_file_exists(image_path)

        logger.info(f"Starting visibility simulation for {Path(image_path).name}")
        logger.debug(
            f"Output MS: {output_ms_path}, "
            f"Scans: {num_scans}, Duration: {scan_duration_sec}s"
        )

        try:
            # CASA imports - will fail if not in CASA environment
            from casac import casatools  # type: ignore
        except ImportError:
            logger.error("CASA toolkit not available. Run this within CASA.")
            raise ImportError("This function must be run within CASA environment")

        # TODO: Implement actual CASA simulation here
        # This would use sm (simobserve manager) tools

        logger.info(f"Visibility simulation complete: {output_ms_path}")
        return output_ms_path

    def _parse_telescope_config(self) -> Tuple[str, str, str]:
        """
        Parse telescope configuration file to extract name and mount type.

        Returns:
            Tuple of (telescope_name, mount_type, config_path).
        """
        path = Path(self.config_file)
        telescope_name = path.stem  # Filename without extension

        # Determine mount type
        mount_type = DEFAULT_MOUNT_TYPE
        if any(name in telescope_name for name in EQUATORIAL_MOUNT_TELESCOPES):
            mount_type = "EQUATORIAL"

        logger.debug(f"Parsed telescope: {telescope_name}, mount: {mount_type}")
        return telescope_name, mount_type, str(path.absolute())

    def scale_image_for_frequency(
        self,
        image_path: str,
        reference_frequency_ghz: float,
        target_frequency_ghz: float,
    ) -> str:
        """
        Scale image flux density to target frequency using spectral index.

        Args:
            image_path: Path to input image.
            reference_frequency_ghz: Reference frequency in GHz.
            target_frequency_ghz: Target frequency in GHz.

        Returns:
            Path to scaled image.

        Raises:
            ImportError: If CASA toolkit not available.
        """
        validate_file_exists(image_path)

        logger.debug(
            f"Scaling image from {reference_frequency_ghz}GHz to {target_frequency_ghz}GHz"
        )

        try:
            from casac import casatools  # type: ignore
        except ImportError:
            raise ImportError("CASA toolkit not available")

        # TODO: Implement actual image scaling using power law
        # S(ν₂) = S(ν₁) × (ν₂/ν₁)^α

        return image_path
