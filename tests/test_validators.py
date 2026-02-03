"""
Unit tests for input validators.
"""

import pytest
from pathlib import Path
import tempfile

from sos.utils.validators import (
    validate_redshifts,
    validate_spectral_index,
    validate_flux_density,
    validate_file_exists,
    validate_frequency,
    validate_coordinate_string,
)


class TestRedshiftValidation:
    """Test redshift validation."""

    def test_valid_redshifts(self):
        """Test valid redshift list."""
        assert validate_redshifts([0.1, 0.5, 1.0]) is True

    def test_empty_redshifts_raises_error(self):
        """Test empty list raises error."""
        with pytest.raises(ValueError):
            validate_redshifts([])

    def test_negative_redshift_raises_error(self):
        """Test negative redshift raises error."""
        with pytest.raises(ValueError):
            validate_redshifts([-0.1, 0.5])

    def test_very_high_redshift_raises_error(self):
        """Test redshift beyond physical limit raises error."""
        with pytest.raises(ValueError):
            validate_redshifts([0.1, 100.0])  # 100 is unreasonably high


class TestSpectralIndexValidation:
    """Test spectral index validation."""

    def test_valid_spectral_index(self):
        """Test valid spectral index."""
        assert validate_spectral_index(-1.6) is True

    def test_positive_spectral_index_raises_error(self):
        """Test positive spectral index raises error."""
        with pytest.raises(ValueError):
            validate_spectral_index(1.0)

    def test_extreme_negative_raises_error(self):
        """Test extremely negative spectral index raises error."""
        with pytest.raises(ValueError):
            validate_spectral_index(-10.0)


class TestFluxDensityValidation:
    """Test flux density validation."""

    def test_valid_flux_density(self):
        """Test valid flux density."""
        assert validate_flux_density(0.6) is True

    def test_negative_flux_raises_error(self):
        """Test negative flux raises error."""
        with pytest.raises(ValueError):
            validate_flux_density(-0.1)

    def test_very_large_flux_raises_error(self):
        """Test unreasonably large flux raises error."""
        with pytest.raises(ValueError):
            validate_flux_density(1e10)


class TestFileValidation:
    """Test file validation."""

    def test_file_exists_passes(self):
        """Test validation passes for existing file."""
        with tempfile.NamedTemporaryFile() as tmp:
            assert validate_file_exists(tmp.name) is True

    def test_missing_file_raises_error(self):
        """Test missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            validate_file_exists("/nonexistent/path/file.txt")

    def test_directory_raises_error(self):
        """Test directory path raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError):
                validate_file_exists(tmpdir)


class TestFrequencyValidation:
    """Test frequency validation."""

    def test_valid_frequency(self):
        """Test valid frequency."""
        assert validate_frequency(9.2, "GHz") is True

    def test_negative_frequency_raises_error(self):
        """Test negative frequency raises error."""
        with pytest.raises(ValueError):
            validate_frequency(-1.0, "GHz")

    def test_invalid_unit_raises_error(self):
        """Test invalid unit raises error."""
        with pytest.raises(ValueError):
            validate_frequency(9.2, "TeraHz")


class TestCoordinateValidation:
    """Test coordinate string validation."""

    def test_valid_ra_string(self):
        """Test valid RA coordinate."""
        assert validate_coordinate_string("04h30m15.50s", "ra") is True

    def test_valid_dec_string(self):
        """Test valid DEC coordinate."""
        assert validate_coordinate_string("+45d30m15.50s", "dec") is True
        assert validate_coordinate_string("-20d30m45.50s", "dec") is True

    def test_invalid_ra_format_raises_error(self):
        """Test invalid RA format raises error."""
        with pytest.raises(ValueError):
            validate_coordinate_string("4:30:15.5", "ra")

    def test_invalid_dec_format_raises_error(self):
        """Test invalid DEC format raises error."""
        with pytest.raises(ValueError):
            validate_coordinate_string("45:30:15.5", "dec")
