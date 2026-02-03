"""
SOS: SKA Observation Simulator

A Python package for simulating SKA1_Mid visibility (radio observations)
using CASA toolkit. Includes model sky generation and visibility simulation.

Version: 2.0.0
Author: Deepak Deo, Dr. Ruta Kale (NCRA-TIFR)
"""

__version__ = "2.0.0"
__author__ = "Deepak Deo, Dr. Ruta Kale"
__email__ = "deepak@example.com"

from sos.utils.logger import setup_logger, get_logger

__all__ = [
    "setup_logger",
    "get_logger",
    "__version__",
    "__author__",
]
