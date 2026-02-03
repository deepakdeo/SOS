"""
Unit tests for coordinate utilities.
"""

import pytest
from sos.utils.coordinates import (
    ra_arcsec_to_hms,
    dec_arcsec_to_dms,
    parse_ra_hms,
    parse_dec_dms,
    radians_to_arcsec,
)


class TestRaConversion:
    """Test Right Ascension conversions."""

    def test_ra_arcsec_to_hms_zero(self):
        """Test zero RA conversion."""
        assert ra_arcsec_to_hms(0) == "00h00m00.00s"

    def test_ra_arcsec_to_hms_basic(self):
        """Test basic RA conversion."""
        # 4 hours = 4 * 3600 * 15 arcsec = 216000 arcsec
        result = ra_arcsec_to_hms(216000)
        assert result == "04h00m00.00s"

    def test_ra_arcsec_to_hms_with_minutes_seconds(self):
        """Test RA with minutes and seconds."""
        # 4h30m15s = (4 + 30/60 + 15/3600) * 3600 * 15 arcsec
        result = ra_arcsec_to_hms(243900)
        # Should be approximately 04h30m15s
        assert "04h" in result
        assert "m" in result
        assert "s" in result

    def test_ra_negative_raises_error(self):
        """Test that negative RA raises ValueError."""
        with pytest.raises(ValueError):
            ra_arcsec_to_hms(-100)


class TestDecConversion:
    """Test Declination conversions."""

    def test_dec_arcsec_to_dms_zero(self):
        """Test zero DEC conversion."""
        result = dec_arcsec_to_dms(0)
        assert "+0d0m" in result

    def test_dec_arcsec_to_dms_positive(self):
        """Test positive DEC conversion."""
        # +45 degrees = 45 * 3600 arcsec = 162000 arcsec
        result = dec_arcsec_to_dms(162000)
        assert "+45d" in result

    def test_dec_arcsec_to_dms_negative(self):
        """Test negative DEC conversion."""
        # -20 degrees = -20 * 3600 arcsec = -72000 arcsec
        result = dec_arcsec_to_dms(-72000)
        assert "-20d" in result

    def test_dec_with_minutes_seconds(self):
        """Test DEC with minutes and seconds."""
        # -20d30m00s = -(20*3600 + 30*60) arcsec = -73800 arcsec
        result = dec_arcsec_to_dms(-73800)
        assert "-20d30m" in result


class TestRaHmsParsing:
    """Test RA HH:MM:SS string parsing."""

    def test_parse_ra_hms_basic(self):
        """Test basic RA parsing."""
        result = parse_ra_hms("04h30m15.50s")
        assert 4 < result < 5  # Should be between 4 and 5 hours

    def test_parse_ra_hms_zero(self):
        """Test zero RA parsing."""
        result = parse_ra_hms("00h00m00.00s")
        assert result == 0.0

    def test_parse_ra_hms_max(self):
        """Test maximum RA parsing."""
        result = parse_ra_hms("23h59m59.99s")
        assert 23.9 < result < 24.0


class TestDecDmsParsing:
    """Test DEC ±DD:MM:SS string parsing."""

    def test_parse_dec_dms_positive(self):
        """Test positive DEC parsing."""
        result = parse_dec_dms("+45d30m15.50s")
        assert 45 < result < 46

    def test_parse_dec_dms_negative(self):
        """Test negative DEC parsing."""
        result = parse_dec_dms("-20d30m45.50s")
        assert -21 < result < -20

    def test_parse_dec_dms_zero(self):
        """Test zero DEC parsing."""
        result = parse_dec_dms("+00d00m00.00s")
        assert result == 0.0


class TestAngleConversion:
    """Test angle unit conversions."""

    def test_radians_to_arcsec(self):
        """Test radian to arcsecond conversion."""
        # 1 radian should be approximately 206265 arcsec
        result = radians_to_arcsec(1.0)
        assert 206264 < result < 206265
