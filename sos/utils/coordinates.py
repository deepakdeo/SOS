"""
Coordinate conversion utilities for SOS (SKA Observation Simulator).

Consolidates all coordinate transformation functions (RA, DEC, etc.) into
a single, tested module. Previously these were duplicated across multiple files.
"""

from typing import Tuple
from sos.constants import (
    RA_ARCSEC_PER_SECOND,
    ARCSEC_PER_RADIAN,
    DEGREES_PER_RA_HOUR
)


def ra_arcsec_to_hms(ra_arcsec: float) -> str:
    """
    Convert Right Ascension from arcseconds to HH:MM:SS.S format.

    Args:
        ra_arcsec: Right Ascension in arcseconds.

    Returns:
        RA as string in format "HHhMMmSS.Ss" (e.g., "04h30m15.50s").

    Raises:
        ValueError: If ra_arcsec is negative.

    Example:
        >>> ra_arcsec_to_hms(67815.0)  # 04:30:15
        '04h30m15.00s'
    """
    if ra_arcsec < 0:
        raise ValueError(f"RA in arcseconds must be non-negative, got {ra_arcsec}")

    # Convert arcsec to RA hours (1 RA hour = 3600 arcsec * 15)
    ra_hours = ra_arcsec / (3600.0 * RA_ARCSEC_PER_SECOND)

    hours = int(ra_hours)
    remainder = 60.0 * (ra_hours - hours)
    minutes = int(remainder)
    seconds = 60.0 * (remainder - minutes)
    seconds = float(f"{seconds:.2f}")

    return f"{hours:02d}h{minutes:02d}m{seconds:05.2f}s"


def dec_arcsec_to_dms(dec_arcsec: float) -> str:
    """
    Convert Declination from arcseconds to ±DD:MM:SS.S format.

    Args:
        dec_arcsec: Declination in arcseconds (can be negative).

    Returns:
        DEC as string in format "±DDdMMmSS.Ss" (e.g., "-20d30m45.50s", "+45d15m00.00s").

    Example:
        >>> dec_arcsec_to_dms(-73800.0)  # -20:30:00
        '-20d30m00.00s'
        >>> dec_arcsec_to_dms(162000.0)  # +45:00:00
        '+45d00m00.00s'
    """
    deg_value = dec_arcsec / 3600.0

    if deg_value < 0.0:
        # Negative declination
        degrees = int(abs(deg_value))
        remainder = 60.0 * (deg_value + degrees)  # Still negative
        arcminutes = int(abs(remainder))
        arcseconds = abs(60.0 * (remainder + arcminutes))
        arcseconds = float(f"{arcseconds:.2f}")
        return f"-{degrees}d{arcminutes}m{arcseconds:05.2f}s"
    else:
        # Positive declination
        degrees = int(deg_value)
        remainder = 60.0 * (deg_value - degrees)
        arcminutes = int(remainder)
        arcseconds = 60.0 * (remainder - arcminutes)
        arcseconds = float(f"{arcseconds:.2f}")
        return f"+{degrees}d{arcminutes}m{arcseconds:05.2f}s"


def radians_to_arcsec(radians: float) -> float:
    """
    Convert angle from radians to arcseconds.

    Args:
        radians: Angle in radians.

    Returns:
        Angle in arcseconds.
    """
    return radians * ARCSEC_PER_RADIAN


def parse_ra_hms(ra_string: str) -> float:
    """
    Parse RA string (HH:MM:SS.S format) to decimal hours.

    Args:
        ra_string: RA string (e.g., "04h30m15.50s" or "04:30:15.50").

    Returns:
        RA in decimal hours.

    Raises:
        ValueError: If string format is invalid.
    """
    # Remove common separators
    ra_string = ra_string.replace("h", ":").replace("m", ":").replace("s", "")

    parts = ra_string.split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid RA format: {ra_string}. Expected HH:MM:SS.S")

    try:
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
    except ValueError as e:
        raise ValueError(f"Could not parse RA components: {e}")

    if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
        raise ValueError(f"RA values out of range: {hours}h{minutes}m{seconds}s")

    return hours + minutes / 60.0 + seconds / 3600.0


def parse_dec_dms(dec_string: str) -> float:
    """
    Parse DEC string (±DD:MM:SS.S format) to decimal degrees.

    Args:
        dec_string: DEC string (e.g., "-20d30m45.50s" or "+45:15:00").

    Returns:
        DEC in decimal degrees.

    Raises:
        ValueError: If string format is invalid.
    """
    # Handle sign
    sign = 1.0
    if dec_string.startswith("-"):
        sign = -1.0
        dec_string = dec_string[1:]
    elif dec_string.startswith("+"):
        dec_string = dec_string[1:]

    # Remove common separators
    dec_string = dec_string.replace("d", ":").replace("m", ":").replace("s", "")

    parts = dec_string.split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid DEC format. Expected ±DD:MM:SS.S")

    try:
        degrees = float(parts[0])
        arcminutes = float(parts[1])
        arcseconds = float(parts[2])
    except ValueError as e:
        raise ValueError(f"Could not parse DEC components: {e}")

    if not (0 <= degrees < 360 and 0 <= arcminutes < 60 and 0 <= arcseconds < 60):
        raise ValueError(f"DEC values out of range")

    dec_decimal = degrees + arcminutes / 60.0 + arcseconds / 3600.0
    return sign * dec_decimal


def get_ra_dec_tuple(ra_string: str, dec_string: str) -> Tuple[float, float]:
    """
    Parse and return (RA, DEC) as decimal degrees (RA already in hours).

    Args:
        ra_string: RA in format "HHhMMmSS.Ss".
        dec_string: DEC in format "±DDdMMmSS.Ss".

    Returns:
        Tuple of (ra_decimal_hours, dec_decimal_degrees).
    """
    ra_hours = parse_ra_hms(ra_string)
    dec_degrees = parse_dec_dms(dec_string)
    return (ra_hours, dec_degrees)
