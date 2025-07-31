"""
Test suite for cricpy.parsers.cricsheet_parser module
"""
import pytest
import pandas as pd
from cricpy.parsers.cricsheet_parser import parse_match


class TestParseMatch:
    """Test cases for parse_match function"""
    
    def test_parse_basic_match(self):
        """Test parsing a basic match with minimal data"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'India',
                        'deliveries': [
                            {
                                0.1: {
                                    'batsman': 'Rohit Sharma',
                                    'bowler': 'Mitchell Starc',
                                    'runs': {'total': 1, 'batsman': 1, 'extras': 0}
                                }
                            },
                            {
                                0.2: {
                                    'batsman': 'Rohit Sharma',
                                    'bowler': 'Mitchell Starc',
                                    'runs': {'total': 0, 'batsman': 0, 'extras': 0}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 2
        assert df.iloc[0]['batsman'] == 'Rohit Sharma'
        assert df.iloc[0]['bowler'] == 'Mitchell Starc'
        assert df.iloc[0]['runs_total'] == 1
        assert df.iloc[0]['runs_batter'] == 1
        assert df.iloc[0]['inning'] == '1st innings'
        assert df.iloc[0]['batting_team'] == 'India'
    
    def test_parse_match_with_extras(self):
        """Test parsing deliveries with extras"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'Australia',
                        'deliveries': [
                            {
                                1.1: {
                                    'batsman': 'David Warner',
                                    'bowler': 'Jasprit Bumrah',
                                    'runs': {'total': 1, 'batsman': 0, 'extras': 1},
                                    'extras': {'wides': 1}
                                }
                            },
                            {
                                1.2: {
                                    'batsman': 'David Warner',
                                    'bowler': 'Jasprit Bumrah',
                                    'runs': {'total': 5, 'batsman': 0, 'extras': 5},
                                    'extras': {'noballs': 1}
                                }
                            },
                            {
                                1.3: {
                                    'batsman': 'David Warner',
                                    'bowler': 'Jasprit Bumrah',
                                    'runs': {'total': 2, 'batsman': 1, 'extras': 1},
                                    'extras': {'legbyes': 1}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 3
        assert df.iloc[0]['extras_type'] == 'wides'
        assert df.iloc[0]['runs_extras'] == 1
        assert df.iloc[1]['extras_type'] == 'noballs'
        assert df.iloc[2]['extras_type'] == 'legbyes'
    
    def test_parse_match_with_wickets(self):
        """Test parsing deliveries with wickets"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'England',
                        'deliveries': [
                            {
                                10.3: {
                                    'batsman': 'Joe Root',
                                    'bowler': 'Pat Cummins',
                                    'runs': {'total': 0, 'batsman': 0, 'extras': 0},
                                    'wicket': {
                                        'kind': 'bowled',
                                        'player_out': 'Joe Root'
                                    }
                                }
                            },
                            {
                                15.2: {
                                    'batsman': 'Ben Stokes',
                                    'bowler': 'Nathan Lyon',
                                    'runs': {'total': 0, 'batsman': 0, 'extras': 0},
                                    'wicket': {
                                        'kind': 'caught',
                                        'player_out': 'Ben Stokes',
                                        'fielders': ['Steve Smith', 'David Warner']
                                    }
                                }
                            },
                            {
                                18.5: {
                                    'batsman': 'Jos Buttler',
                                    'bowler': 'Mitchell Starc',
                                    'runs': {'total': 0, 'batsman': 0, 'extras': 0},
                                    'wicket': {
                                        'kind': 'run out',
                                        'player_out': 'Jos Buttler',
                                        'fielder': 'Marcus Stoinis'
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 3
        assert df.iloc[0]['dismissal'] == 'bowled'
        assert pd.isna(df.iloc[0]['fielder']) or df.iloc[0]['fielder'] == ''
        
        assert df.iloc[1]['dismissal'] == 'caught'
        assert df.iloc[1]['fielder'] == 'Steve Smith, David Warner'
        
        assert df.iloc[2]['dismissal'] == 'run out'
        assert df.iloc[2]['fielder'] == 'Marcus Stoinis'
    
    def test_parse_multiple_innings(self):
        """Test parsing match with multiple innings"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'India',
                        'deliveries': [
                            {0.1: {'batsman': 'Rohit', 'bowler': 'Starc', 'runs': {'total': 4}}}
                        ]
                    }
                },
                {
                    '2nd innings': {
                        'team': 'Australia',
                        'deliveries': [
                            {0.1: {'batsman': 'Warner', 'bowler': 'Bumrah', 'runs': {'total': 1}}},
                            {0.2: {'batsman': 'Warner', 'bowler': 'Bumrah', 'runs': {'total': 0}}}
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 3
        
        # Check first innings
        first_innings = df[df['inning'] == '1st innings']
        assert len(first_innings) == 1
        assert first_innings.iloc[0]['batting_team'] == 'India'
        
        # Check second innings
        second_innings = df[df['inning'] == '2nd innings']
        assert len(second_innings) == 2
        assert second_innings.iloc[0]['batting_team'] == 'Australia'
    
    def test_parse_empty_match(self):
        """Test parsing match with no innings"""
        match_dict = {}
        df = parse_match(match_dict)
        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)
        
        match_dict = {'innings': []}
        df = parse_match(match_dict)
        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)
    
    def test_parse_match_missing_fields(self):
        """Test parsing match with missing fields"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'Pakistan',
                        'deliveries': [
                            {
                                0.1: {
                                    'batsman': 'Babar Azam',
                                    'bowler': 'Trent Boult'
                                    # Missing 'runs' field
                                }
                            },
                            {
                                0.2: {
                                    'batsman': 'Babar Azam',
                                    'bowler': 'Trent Boult',
                                    'runs': {}  # Empty runs dict
                                }
                            },
                            {
                                0.3: {
                                    # Missing batsman and bowler
                                    'runs': {'total': 1}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 3
        # First delivery - missing runs should default to 0
        assert df.iloc[0]['runs_total'] == 0
        assert df.iloc[0]['runs_batter'] == 0
        assert df.iloc[0]['runs_extras'] == 0
        
        # Second delivery - empty runs dict
        assert df.iloc[1]['runs_total'] == 0
        
        # Third delivery - missing batsman/bowler
        assert pd.isna(df.iloc[2]['batsman']) or df.iloc[2]['batsman'] is None
        assert pd.isna(df.iloc[2]['bowler']) or df.iloc[2]['bowler'] is None
    
    def test_parse_match_with_unknown_team(self):
        """Test parsing match when team name is missing"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        # Missing 'team' field
                        'deliveries': [
                            {0.1: {'batsman': 'Player1', 'bowler': 'Player2', 'runs': {'total': 1}}}
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 1
        assert df.iloc[0]['batting_team'] == 'Unknown'
    
    def test_parse_match_column_names(self):
        """Test that all expected columns are present"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'Test Team',
                        'deliveries': [
                            {0.1: {'batsman': 'Test Player', 'bowler': 'Test Bowler', 'runs': {'total': 1}}}
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        expected_columns = [
            'inning', 'batting_team', 'ball', 'batsman', 'bowler',
            'runs_total', 'runs_batter', 'runs_extras', 'extras_type',
            'dismissal', 'fielder'
        ]
        
        for col in expected_columns:
            assert col in df.columns
    
    def test_parse_match_data_types(self):
        """Test that columns have appropriate data types"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'South Africa',
                        'deliveries': [
                            {
                                1.1: {
                                    'batsman': 'Quinton de Kock',
                                    'bowler': 'Josh Hazlewood',
                                    'runs': {'total': 4, 'batsman': 4, 'extras': 0}
                                }
                            },
                            {
                                1.2: {
                                    'batsman': 'Quinton de Kock',
                                    'bowler': 'Josh Hazlewood',
                                    'runs': {'total': 0, 'batsman': 0, 'extras': 0}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        # Numeric columns should be numeric
        assert pd.api.types.is_numeric_dtype(df['runs_total'])
        assert pd.api.types.is_numeric_dtype(df['runs_batter'])
        assert pd.api.types.is_numeric_dtype(df['runs_extras'])
        
        # Ball numbers should be float (e.g., 1.1, 1.2)
        assert df['ball'].dtype == float
    
    def test_parse_complex_match(self):
        """Test parsing a more complex match with various scenarios"""
        match_dict = {
            'innings': [
                {
                    '1st innings': {
                        'team': 'West Indies',
                        'deliveries': [
                            # Normal delivery
                            {0.1: {'batsman': 'Chris Gayle', 'bowler': 'Dale Steyn', 
                                  'runs': {'total': 6, 'batsman': 6, 'extras': 0}}},
                            # Wide ball
                            {0.2: {'batsman': 'Chris Gayle', 'bowler': 'Dale Steyn',
                                  'runs': {'total': 1, 'batsman': 0, 'extras': 1},
                                  'extras': {'wides': 1}}},
                            # No ball with runs
                            {0.3: {'batsman': 'Chris Gayle', 'bowler': 'Dale Steyn',
                                  'runs': {'total': 5, 'batsman': 4, 'extras': 1},
                                  'extras': {'noballs': 1}}},
                            # Wicket - bowled
                            {0.4: {'batsman': 'Chris Gayle', 'bowler': 'Dale Steyn',
                                  'runs': {'total': 0, 'batsman': 0, 'extras': 0},
                                  'wicket': {'kind': 'bowled', 'player_out': 'Chris Gayle'}}},
                            # Bye runs
                            {0.5: {'batsman': 'Marlon Samuels', 'bowler': 'Dale Steyn',
                                  'runs': {'total': 2, 'batsman': 0, 'extras': 2},
                                  'extras': {'byes': 2}}}
                        ]
                    }
                },
                {
                    '2nd innings': {
                        'team': 'South Africa',
                        'deliveries': [
                            # Caught with multiple fielders
                            {0.1: {'batsman': 'AB de Villiers', 'bowler': 'Kemar Roach',
                                  'runs': {'total': 0, 'batsman': 0, 'extras': 0},
                                  'wicket': {'kind': 'caught', 'player_out': 'AB de Villiers',
                                            'fielders': ['Chris Gayle']}}},
                            # Leg byes
                            {0.2: {'batsman': 'Hashim Amla', 'bowler': 'Kemar Roach',
                                  'runs': {'total': 3, 'batsman': 0, 'extras': 3},
                                  'extras': {'legbyes': 3}}}
                        ]
                    }
                }
            ]
        }
        
        df = parse_match(match_dict)
        
        assert len(df) == 7
        
        # Check specific deliveries
        # Six
        assert df.iloc[0]['runs_batter'] == 6
        assert df.iloc[0]['extras_type'] is None
        
        # Wide
        assert df.iloc[1]['extras_type'] == 'wides'
        assert df.iloc[1]['runs_extras'] == 1
        
        # No ball with runs
        assert df.iloc[2]['extras_type'] == 'noballs'
        assert df.iloc[2]['runs_batter'] == 4
        assert df.iloc[2]['runs_total'] == 5
        
        # Wicket
        assert df.iloc[3]['dismissal'] == 'bowled'
        
        # Different innings
        assert df.iloc[5]['inning'] == '2nd innings'
        assert df.iloc[5]['batting_team'] == 'South Africa'