"""
Pytest configuration and shared fixtures for cricpy tests
"""
import pytest
import tempfile
import yaml
import os
from pathlib import Path


@pytest.fixture
def sample_match_data():
    """Provide a sample match data structure for testing"""
    return {
        'meta': {
            'data_version': '1.0.0',
            'created': '2024-01-01',
            'revision': 1
        },
        'info': {
            'city': 'Mumbai',
            'competition': 'IPL',
            'dates': ['2024-01-01'],
            'gender': 'male',
            'match_type': 'T20',
            'match_type_number': 1234,
            'outcome': {
                'winner': 'Mumbai Indians',
                'by': {'runs': 10}
            },
            'overs': 20,
            'player_of_match': ['Rohit Sharma'],
            'players': {
                'Mumbai Indians': ['Rohit Sharma', 'Suryakumar Yadav'],
                'Chennai Super Kings': ['MS Dhoni', 'Ravindra Jadeja']
            },
            'registry': {
                'people': {
                    'Rohit Sharma': 'abc123',
                    'MS Dhoni': 'def456'
                }
            },
            'season': '2024',
            'team_type': 'club',
            'teams': ['Mumbai Indians', 'Chennai Super Kings'],
            'toss': {
                'decision': 'bat',
                'winner': 'Mumbai Indians'
            },
            'umpires': ['Umpire 1', 'Umpire 2'],
            'venue': 'Wankhede Stadium'
        },
        'innings': [
            {
                '1st innings': {
                    'team': 'Mumbai Indians',
                    'deliveries': [
                        {
                            0.1: {
                                'batsman': 'Rohit Sharma',
                                'bowler': 'Deepak Chahar',
                                'non_striker': 'Suryakumar Yadav',
                                'runs': {
                                    'batsman': 0,
                                    'extras': 0,
                                    'total': 0
                                }
                            }
                        },
                        {
                            0.2: {
                                'batsman': 'Rohit Sharma',
                                'bowler': 'Deepak Chahar',
                                'non_striker': 'Suryakumar Yadav',
                                'runs': {
                                    'batsman': 4,
                                    'extras': 0,
                                    'total': 4
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }


@pytest.fixture
def sample_yaml_files(tmp_path):
    """Create sample YAML files in a temporary directory"""
    files_data = {
        'match1.yaml': {
            'info': {'match_type': 'T20', 'teams': ['Team A', 'Team B']},
            'innings': [{'1st innings': {'team': 'Team A', 'deliveries': []}}]
        },
        'match2.yaml': {
            'info': {'match_type': 'ODI', 'teams': ['Team C', 'Team D']},
            'innings': [{'1st innings': {'team': 'Team C', 'deliveries': []}}]
        },
        'match3.yml': {
            'info': {'match_type': 'Test', 'teams': ['Team E', 'Team F']},
            'innings': [{'1st innings': {'team': 'Team E', 'deliveries': []}}]
        }
    }
    
    for filename, content in files_data.items():
        filepath = tmp_path / filename
        with open(filepath, 'w') as f:
            yaml.dump(content, f)
    
    return tmp_path


@pytest.fixture
def invalid_yaml_file(tmp_path):
    """Create an invalid YAML file"""
    filepath = tmp_path / 'invalid.yaml'
    filepath.write_text('{ this is: invalid yaml syntax ][')
    return filepath


@pytest.fixture
def empty_yaml_file(tmp_path):
    """Create an empty YAML file"""
    filepath = tmp_path / 'empty.yaml'
    filepath.write_text('')
    return filepath


@pytest.fixture
def large_match_data():
    """Generate a large match data structure for performance testing"""
    deliveries = []
    for over in range(20):  # 20 overs
        for ball in range(6):  # 6 balls per over
            ball_number = over + (ball + 1) / 10  # e.g., 0.1, 0.2, ..., 19.6
            delivery = {
                ball_number: {
                    'batsman': f'Batsman {(over % 2) + 1}',
                    'bowler': f'Bowler {(over // 4) + 1}',
                    'runs': {
                        'batsman': ball % 3,
                        'extras': 0,
                        'total': ball % 3
                    }
                }
            }
            deliveries.append(delivery)
    
    return {
        'info': {
            'match_type': 'T20',
            'teams': ['Team A', 'Team B']
        },
        'innings': [
            {
                '1st innings': {
                    'team': 'Team A',
                    'deliveries': deliveries
                }
            }
        ]
    }


@pytest.fixture
def match_with_all_dismissal_types():
    """Create match data with all types of dismissals"""
    dismissal_types = [
        {'kind': 'bowled'},
        {'kind': 'caught', 'fielders': ['Fielder 1']},
        {'kind': 'lbw'},
        {'kind': 'run out', 'fielder': 'Fielder 2'},
        {'kind': 'stumped', 'fielder': 'Wicket Keeper'},
        {'kind': 'hit wicket'},
        {'kind': 'caught and bowled'},
        {'kind': 'retired hurt'},
        {'kind': 'retired out'},
        {'kind': 'obstructing the field'}
    ]
    
    deliveries = []
    for i, dismissal in enumerate(dismissal_types):
        delivery = {
            i + 0.1: {
                'batsman': f'Batsman {i+1}',
                'bowler': f'Bowler {i+1}',
                'runs': {'batsman': 0, 'extras': 0, 'total': 0},
                'wicket': dismissal
            }
        }
        deliveries.append(delivery)
    
    return {
        'innings': [
            {
                '1st innings': {
                    'team': 'Test Team',
                    'deliveries': deliveries
                }
            }
        ]
    }


@pytest.fixture
def match_with_all_extras_types():
    """Create match data with all types of extras"""
    extras_types = [
        {'wides': 1},
        {'noballs': 1},
        {'byes': 2},
        {'legbyes': 1},
        {'penalty': 5}
    ]
    
    deliveries = []
    for i, extra in enumerate(extras_types):
        extra_runs = list(extra.values())[0]
        delivery = {
            i + 0.1: {
                'batsman': 'Test Batsman',
                'bowler': 'Test Bowler',
                'runs': {
                    'batsman': 0,
                    'extras': extra_runs,
                    'total': extra_runs
                },
                'extras': extra
            }
        }
        deliveries.append(delivery)
    
    return {
        'innings': [
            {
                '1st innings': {
                    'team': 'Test Team',
                    'deliveries': deliveries
                }
            }
        ]
    }


# Performance testing fixtures
@pytest.fixture
def create_many_yaml_files():
    """Factory fixture to create many YAML files for performance testing"""
    def _create_files(directory, count=100):
        for i in range(count):
            content = {
                'info': {
                    'match_id': i,
                    'teams': [f'Team {2*i}', f'Team {2*i+1}']
                },
                'innings': []
            }
            filepath = directory / f'match_{i:04d}.yaml'
            with open(filepath, 'w') as f:
                yaml.dump(content, f)
        return directory
    
    return _create_files


# Utility functions for tests
def assert_dataframe_columns(df, expected_columns):
    """Helper to assert DataFrame has expected columns"""
    assert set(df.columns) == set(expected_columns)


def assert_no_missing_values(df, columns):
    """Helper to assert no missing values in specified columns"""
    for col in columns:
        assert not df[col].isna().any(), f"Column {col} has missing values"