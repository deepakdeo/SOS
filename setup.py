"""
SOS setup configuration file.

Defines package metadata, dependencies, and installation options.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="sos-ska",
    version="2.0.0",
    author="Deepak Deo",
    author_email="deepak@example.com",
    description="SKA Observation Simulator: Simulate SKA1_Mid visibility using CASA toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepakdeo/SOS",
    project_urls={
        "Documentation": "https://github.com/deepakdeo/SOS/wiki",
        "Source": "https://github.com/deepakdeo/SOS",
        "Tracker": "https://github.com/deepakdeo/SOS/issues",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "PyYAML>=5.3",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
        "casa": [
            # CASA toolkit (install separately in CASA environment)
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    keywords="ska simulation visibility radio astronomy",
    zip_safe=False,
)
