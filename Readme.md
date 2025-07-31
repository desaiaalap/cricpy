# cricpy

A Python package for parsing and analyzing cricket data from Cricsheet.

[![PyPI version](https://badge.fury.io/py/cricpy.svg)](https://badge.fury.io/py/cricpy)
[![Python Support](https://img.shields.io/pypi/pyversions/cricpy.svg)](https://pypi.org/project/cricpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Parse Cricsheet YAML files into pandas DataFrames
- Support for all cricket formats (Test, ODI, T20, T10, The Hundred, etc.)
- Delivery-level data extraction
- Handle extras, wickets, and all match events
- Batch processing of multiple match files
- Easy-to-use API

## Installation

```bash
pip install cricpy
```

## Quick Start

``` python
from cricpy.io import file_loader
from cricpy.parsers import cricsheet_parser

# Load a single match
match_data = file_loader.load_yaml('path/to/match.yaml')

# Parse into a DataFrame
df = cricsheet_parser.parse_match(match_data)

# Load multiple matches
matches = file_loader.load_all_yaml('path/to/matches/folder')

# Process all matches
all_deliveries = []
for filename, match_data in matches:
    df = cricsheet_parser.parse_match(match_data)
    df['match_file'] = filename
    all_deliveries.append(df)

# Combine into a single DataFrame
import pandas as pd
all_matches_df = pd.concat(all_deliveries, ignore_index=True)
```

## Data Structure

The parsed DataFrame contains the following columns:

- `inning`: Inning identifier (e.g., '1st innings', '2nd innings')
- `batting_team`: Name of the batting team
- `ball`: Ball number (e.g., 0.1, 0.2, ..., 19.6)
- `batsman`: Batsman on strike
- `bowler`: Bowler
- `runs_total`: Total runs scored on that delivery
- `runs_batter`: Runs scored by the batsman
- `runs_extras`: Extra runs (wides, no-balls, byes, leg-byes)
- `extras_type`: Type of extras, if any
- `dismissal`: Type of dismissal if a wicket fell
- `fielder`: Fielder(s) involved in the dismissal

## Supported Formats

- **Test Cricket**: 5-day matches with up to 4 innings
- **ODI**: 50 overs per side
- **T20**: 20 overs per side
- **T10**: 10 overs per side
- **The Hundred**: 100 balls per side
- **First-class Cricket**: Multi-day matches
- **List A Cricket**: Limited overs cricket

## Examples

### Analyzing a T20 Match

```python
# Load and parse a T20 match
match_data = file_loader.load_yaml('t20_match.yaml')
df = cricsheet_parser.parse_match(match_data)

# Get batting statistics
batting_stats = df.groupby(['batting_team', 'batsman']).agg({
    'runs_batter': 'sum',
    'ball': 'count'
}).rename(columns={'ball': 'balls_faced'})

print(batting_stats)
```

### Finding All Wickets

```python
# Get all wickets
wickets = df[df['dismissal'].notna()]
print(f"Total wickets: {len(wickets)}")
print(wickets[['batsman', 'bowler', 'dismissal', 'fielder']])
```

### Analyzing Extras

```python
# Get extras breakdown
extras = df[df['extras_type'].notna()]
extras_summary = extras.groupby('extras_type')['runs_extras'].sum()
print(extras_summary)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=cricpy --cov-report=html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Cricsheet](https://cricsheet.org/) for providing cricket data in YAML format
- All contributors to this project

## Citation

If you use this package in your research, please cite:

```bibtex
@software{cricpy,
  title = {cricpy: A Python package for parsing Cricsheet cricket data},
  author = {Aalap Desai},
  year = {2025},
  url = {https://github.com/desaiaalap/cricpy}
}
```
