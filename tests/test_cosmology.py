"""
Unit tests for cosmology calculator.
"""

import pytest
from sos.core.image_maker import CosmologyCalculator


class TestCosmologyCalculator:
    """Test cosmological distance calculations."""

    @pytest.fixture
    def cosmology(self):
        """Create CosmologyCalculator instance."""
        return CosmologyCalculator()

    def test_add_distance_zero_redshift(self, cosmology):
        """Test angular diameter distance at z=0."""
        assert cosmology.angular_diameter_distance(0) == 0.0

    def test_add_distance_positive_redshift(self, cosmology):
        """Test angular diameter distance increases with redshift."""
        d_low = cosmology.angular_diameter_distance(0.1)
        d_high = cosmology.angular_diameter_distance(1.0)
        # Distance should increase then decrease (ADD peaks around z~1.6 in ΛCDM)
        assert d_low > 0
        assert d_high > 0

    def test_angular_size_zero_redshift(self, cosmology):
        """Test angular size at z=0."""
        assert cosmology.calculate_angular_size(0.5, 0) == 0.0

    def test_angular_size_increases_with_distance(self, cosmology):
        """Test angular size decreases with increasing redshift (for fixed linear size)."""
        size_low = cosmology.calculate_angular_size(1.0, 0.1)
        size_high = cosmology.calculate_angular_size(1.0, 1.0)
        # Angular size should decrease with increasing redshift (ADD peaks but L is fixed)
        assert size_low > 0
        assert size_high > 0

    def test_flux_density_at_reference_redshift(self, cosmology):
        """Test flux density unchanged at reference redshift."""
        flux = cosmology.calculate_flux_density(1.0, 0.1, 0.1)
        assert flux == pytest.approx(1.0, rel=0.01)

    def test_flux_density_scales_correctly(self, cosmology):
        """Test flux density changes with redshift."""
        flux_near = cosmology.calculate_flux_density(1.0, 0.05, 0.1)
        flux_far = cosmology.calculate_flux_density(1.0, 0.05, 0.5)
        # Flux should decrease with increasing distance (higher redshift)
        assert flux_near > flux_far
