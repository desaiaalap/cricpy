"""
Setup configuration for cricpy package
"""
from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cricpy",
    version="0.1.0",  # Start with 0.1.0 for initial release
    author="Aalap Desai",  # TODO: Add your name
    author_email="aalapdesai0604@gmail.com",  # TODO: Add your email
    description="A Python package for parsing and analyzing Cricsheet cricket data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/desaiaalap/cricpy",  # TODO: Add your repo URL
    project_urls={
        "Bug Tracker": "https://github.com/desaiaalap/cricpy/issues",
        "Documentation": "https://cricpy.readthedocs.io",  # Optional
        "Source Code": "https://github.com/desaiaalap/cricpy",
    },
    packages=find_packages(exclude=["tests", "tests.*", "*.tests", "*.tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",  # Change to 4 - Beta or 5 - Production/Stable when ready
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",  # Or your chosen license
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Add any command-line scripts here
            # "cricpy=cricpy.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="cricket, sports, analytics, cricsheet, data analysis, T20, ODI, Test, cricket statistics",
)