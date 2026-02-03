"""
Global constants for SOS (SKA Observation Simulator).

This module centralizes all magic numbers and configuration constants used
throughout the SOS package to ensure maintainability and consistency.
"""

# ============================================================================
# Coordinate Conversion Constants
# ============================================================================

# Conversion factors for coordinate systems
ARCSEC_PER_RADIAN = 206264.81
"""Arcseconds per radian for coordinate conversions."""

ARCMIN_PER_RADIAN = 3437.75
"""Arcminutes per radian for angular size calculations."""

RA_ARCSEC_PER_SECOND = 15.0
"""Right Ascension: arcseconds per RA second (1 RA sec = 15 arcsec)."""

DEGREES_PER_RA_HOUR = 15.0
"""Degrees per hour of Right Ascension."""

# ============================================================================
# Astronomy & Cosmology Constants
# ============================================================================

SPEED_OF_LIGHT_KM_S = 299792.458
"""Speed of light in km/s."""

# Planck 2015 ΛCDM parameters
HUBBLE_CONSTANT = 67.8
"""Hubble constant H₀ in km/s/Mpc (Planck 2015 results)."""

MATTER_DENSITY_PARAMETER = 0.308
"""Matter density parameter Ω_m from Planck 2015 ΛCDM cosmology."""

# ============================================================================
# Telescope & Observation Parameters
# ============================================================================

TELESCOPE_ELEVATION_LIMIT = 17.0
"""Default elevation limit in degrees for telescope observations."""

TELESCOPE_SHADOW_LIMIT = 0.001
"""Default shadow limit (unit in image pixels) for antenna masking."""

DEFAULT_NOISE_LEVEL = "0.0Jy"
"""Default noise level for visibility simulations (0 = no noise)."""

DEFAULT_STOKES = "RR LL"
"""Default Stokes parameters for visibility simulations."""

DEFAULT_MOUNT_TYPE = "alt-az"
"""Default telescope mount type (alt-az or equatorial)."""

# Equatorial mount telescopes
EQUATORIAL_MOUNT_TELESCOPES = ["DRAO", "WSRT", "ASKAP"]
"""Telescopes with equatorial mounts."""

# ============================================================================
# Frequency & Channel Parameters
# ============================================================================

DEFAULT_FREQUENCY_RESOLUTION_MHZ = 50.0
"""Default frequency resolution per channel in MHz."""

DEFAULT_INTEGRATION_TIME = "1s"
"""Default integration time for visibility samples."""

# ============================================================================
# Image & Sky Model Parameters
# ============================================================================

DEFAULT_CELL_SIZE = "0.01arcsec"
"""Default pixel cell size for image creation."""

DEFAULT_IMAGE_SIZE = 7200
"""Default image size in pixels (for SKA beam coverage)."""

DEFAULT_BRIGHTNESS_UNIT = "Jy/pixel"
"""Default brightness unit for model images."""

DEFAULT_FREQUENCY_INCREMENT = "0.5GHz"
"""Default frequency increment in spectral coordinate system."""

# ============================================================================
# Source Model Parameters
# ============================================================================

SOURCE_TYPE_EXTENDED = 1
"""Source type code: extended source (radio halo)."""

SOURCE_TYPE_POINT = 2
"""Source type code: point source."""

SOURCE_TYPE_MIXED = 3
"""Source type code: extended + point sources."""

# Point source beam properties
DEFAULT_POINT_SOURCE_SIZE_ARCSEC = 3.0
"""Default Gaussian beam size for point sources in arcsec."""

DEFAULT_POSITION_ANGLE = "45.0deg"
"""Default position angle for Gaussian source components."""

# Random source parameters
RANDOM_SOURCE_REGION_SIZE = 47
"""Region size for random point source placement (in units)."""

NUM_RANDOM_POINT_SOURCES = 5
"""Number of random point sources to generate."""

# ============================================================================
# Log File Names
# ============================================================================

LOGFILE_EXTENDED = "logbookE.txt"
"""Log file for extended source simulations."""

LOGFILE_POINT = "logbookP.txt"
"""Log file for point source simulations."""

LOGFILE_MIXED = "logbookEnP.txt"
"""Log file for mixed (extended + point) source simulations."""

# ============================================================================
# File & Format Parameters
# ============================================================================

CONFIG_FILE_EXTENSION = ".cfg"
"""Telescope configuration file extension."""

IMAGE_EXTENSION = ".im"
"""CASA image extension."""

FITS_EXTENSION = ".fits"
"""FITS format image extension."""

MS_EXTENSION = ".ms"
"""CASA Measurement Set extension."""

# ============================================================================
# Error & Validation Parameters
# ============================================================================

MIN_REDSHIFT = 0.0
"""Minimum valid redshift value."""

MAX_REDSHIFT = 10.0
"""Maximum valid redshift value."""

MIN_SPECTRAL_INDEX = -5.0
"""Minimum reasonable spectral index for radio sources."""

MAX_SPECTRAL_INDEX = 0.0
"""Maximum reasonable spectral index for radio sources."""

MIN_FLUX_DENSITY_JY = 0.0
"""Minimum valid flux density in Jy."""

MAX_FLUX_DENSITY_JY = 1e6
"""Maximum reasonable flux density in Jy."""
