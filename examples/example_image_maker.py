"""
Example script: Creating a model sky image with SOS.

This example demonstrates how to use the refactored SOS package
to create a synthetic radio sky model at multiple redshifts.
"""

from sos.core.image_maker import ImageMaker, CosmologyCalculator
from sos.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__, log_file="example_image_maker.log")

# Define simulation parameters
REDSHIFTS = [0.1, 0.5, 1.0]
LINEAR_SIZE_MPC = 0.5
REFERENCE_FLUX_JY = 0.6
SPECTRAL_INDEX = -1.6

# Initialize image maker
image_maker = ImageMaker(
    cell_size="0.01arcsec",
    image_size=7200,
    reference_frequency="9.2GHz",
)

# Create model sky images
try:
    images = image_maker.create_model_sky(
        redshifts=REDSHIFTS,
        linear_size_mpc=LINEAR_SIZE_MPC,
        reference_flux_jy=REFERENCE_FLUX_JY,
        spectral_index=SPECTRAL_INDEX,
    )

    logger.info(f"Created {len(images)} model images:")
    for img in images:
        logger.info(f"  - {img}")

except ImportError as e:
    logger.error(f"Error: {e}")
    logger.info("Note: This example must be run within CASA environment.")

# Example: Inspect cosmological parameters
print("\n--- Cosmological Calculations ---")
cosmology = CosmologyCalculator()

for z in REDSHIFTS:
    d_a = cosmology.angular_diameter_distance(z)
    angular_size = cosmology.calculate_angular_size(LINEAR_SIZE_MPC, z)
    flux = cosmology.calculate_flux_density(
        REFERENCE_FLUX_JY, REDSHIFTS[0], z, SPECTRAL_INDEX
    )

    print(f"z = {z}:")
    print(f"  D_A = {d_a:.1f} Mpc")
    print(f"  Angular size = {angular_size:.3f} arcmin")
    print(f"  Flux density = {flux:.3f} Jy")
