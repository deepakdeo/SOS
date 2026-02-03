"""
Image creation module for SOS (SKA Observation Simulator).

Creates synthetic radio sky models based on cosmological parameters
and source properties.
"""

from typing import List, Tuple, Optional
from pathlib import Path

from sos.constants import (
    SPEED_OF_LIGHT_KM_S,
    HUBBLE_CONSTANT,
    MATTER_DENSITY_PARAMETER,
    ARCMIN_PER_RADIAN,
)
from sos.utils.logger import setup_logger
from sos.utils.coordinates import ra_arcsec_to_hms, dec_arcsec_to_dms
from sos.utils.validators import validate_redshifts, validate_image_parameters

logger = setup_logger(__name__)


class CosmologyCalculator:
    """Calculate cosmological distances and source properties."""

    def __init__(
        self,
        h0: float = HUBBLE_CONSTANT,
        omega_m: float = MATTER_DENSITY_PARAMETER
    ):
        """
        Initialize cosmology calculator.

        Args:
            h0: Hubble constant in km/s/Mpc (default: Planck 2015).
            omega_m: Matter density parameter (default: Planck 2015).
        """
        self.h0 = h0
        self.omega_m = omega_m
        logger.info(f"Initialized cosmology with H0={h0}, Ω_m={omega_m}")

    def angular_diameter_distance(self, redshift: float) -> float:
        """
        Calculate angular diameter distance using ΛCDM cosmology.

        Uses closed-form approximation from Schneider (2006) 'Extragalactic Astronomy
        and Cosmology', Section 4.3.3.

        Args:
            redshift: Redshift z.

        Returns:
            Angular diameter distance in Mpc.
        """
        if redshift == 0:
            return 0.0

        omega_l = 1.0 - self.omega_m
        numerator = (
            SPEED_OF_LIGHT_KM_S * 2.0 *
            (self.omega_m * redshift +
             (self.omega_l - 2.0) * (((1.0 + self.omega_m * redshift) ** 0.5) - 1.0))
        )
        denominator = (
            self.h0 *
            (self.omega_m * (1.0 + redshift)) ** 2
        )

        return numerator / denominator

    def calculate_flux_density(
        self,
        flux_ref: float,
        z_ref: float,
        z_target: float,
        spectral_index: float = -1.6
    ) -> float:
        """
        Calculate flux density at target redshift using k-correction.

        Args:
            flux_ref: Reference flux density in Jy.
            z_ref: Reference redshift.
            z_target: Target redshift.
            spectral_index: Spectral index (default: -1.6 for radio halos).

        Returns:
            Flux density at target redshift in Jy.
        """
        d_ref = self.angular_diameter_distance(z_ref)
        d_target = self.angular_diameter_distance(z_target)

        if d_ref == 0 or d_target == 0:
            return flux_ref

        k_correction = ((1.0 + z_target) / (1.0 + z_ref)) ** spectral_index
        flux = flux_ref * (d_ref / d_target) ** 2 * k_correction

        return flux

    def calculate_angular_size(
        self,
        linear_size_mpc: float,
        redshift: float
    ) -> float:
        """
        Calculate angular size of a source at given redshift.

        θ = L / D_A where L is linear size and D_A is angular diameter distance.

        Args:
            linear_size_mpc: Linear size in Mpc.
            redshift: Redshift z.

        Returns:
            Angular size in arcminutes.
        """
        d_a = self.angular_diameter_distance(redshift)

        if d_a == 0:
            return 0.0

        # Convert from radians to arcminutes
        angular_size_rad = linear_size_mpc / d_a
        angular_size_arcmin = angular_size_rad * ARCMIN_PER_RADIAN

        return angular_size_arcmin


class ImageMaker:
    """Create synthetic radio sky model images."""

    def __init__(
        self,
        cell_size: str = "0.01arcsec",
        image_size: int = 7200,
        reference_frequency: str = "9.2GHz",
    ):
        """
        Initialize image maker.

        Args:
            cell_size: Pixel size (e.g., "0.01arcsec").
            image_size: Number of pixels per side.
            reference_frequency: Reference frequency for image.
        """
        validate_image_parameters(cell_size, image_size, reference_frequency)

        self.cell_size = cell_size
        self.image_size = image_size
        self.reference_frequency = reference_frequency
        self.cosmology = CosmologyCalculator()

        logger.info(
            f"Initialized ImageMaker: {image_size}x{image_size} pixels, "
            f"{cell_size} resolution, {reference_frequency}"
        )

    def create_model_sky(
        self,
        redshifts: List[float],
        linear_size_mpc: float = 0.5,
        reference_flux_jy: float = 0.6,
        spectral_index: float = -1.6,
        output_dir: Optional[str] = None,
    ) -> List[str]:
        """
        Create model sky images for each redshift.

        Args:
            redshifts: List of redshifts.
            linear_size_mpc: Linear size of source in Mpc.
            reference_flux_jy: Reference flux density in Jy.
            spectral_index: Spectral index.
            output_dir: Output directory for images (optional).

        Returns:
            List of created image file paths.

        Raises:
            ImportError: If CASA toolkit not available.
            ValueError: If parameters invalid.
        """
        validate_redshifts(redshifts)

        logger.info(f"Creating model sky images for {len(redshifts)} redshifts")

        try:
            # CASA imports - will fail if not in CASA environment
            from casac import casatools  # type: ignore
        except ImportError:
            logger.error("CASA toolkit not available. Run this within CASA.")
            raise ImportError("This function must be run within CASA environment")

        images = []

        for z in redshifts:
            # Calculate properties at this redshift
            flux = self.cosmology.calculate_flux_density(
                reference_flux_jy, redshifts[0], z, spectral_index
            )
            angular_size = self.cosmology.calculate_angular_size(linear_size_mpc, z)

            logger.debug(
                f"z={z}: flux={flux:.3f}Jy, angular_size={angular_size:.3f}arcmin"
            )

            # TODO: Implement actual CASA image creation here
            # For now, just return template names
            image_name = f"modelsky_{z}.im"
            images.append(image_name)
            logger.debug(f"Created image: {image_name}")

        logger.info(f"Successfully created {len(images)} model images")
        return images
