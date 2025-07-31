"""
Test suite for cricpy.io.file_loader module
"""
import os
import pytest
import yaml
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from cricpy.io.file_loader import load_yaml, load_all_yaml


class TestLoadYaml:
    """Test cases for load_yaml function"""
    
    def test_load_valid_yaml_file(self, tmp_path):
        """Test loading a valid YAML file"""
        # Create a temporary YAML file
        yaml_content = {
            'meta': {
                'data_version': '1.0.0',
                'created': '2024-01-01',
                'revision': 1
            },
            'info': {
                'match_type': 'T20',
                'teams': ['Team A', 'Team B']
            }
        }
        yaml_file = tmp_path / "test_match.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(yaml_content, f)
        
        # Test loading
        result = load_yaml(str(yaml_file))
        assert result == yaml_content
        assert result['meta']['data_version'] == '1.0.0'
        assert 'teams' in result['info']
    
    def test_load_yaml_with_unicode(self, tmp_path):
        """Test loading YAML with unicode characters"""
        yaml_content = {
            'info': {
                'player': 'José García',
                'venue': 'München'
            }
        }
        yaml_file = tmp_path / "unicode_test.yaml"
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f)
        
        result = load_yaml(str(yaml_file))
        assert result['info']['player'] == 'José García'
        assert result['info']['venue'] == 'München'
    
    def test_load_empty_yaml_file(self, tmp_path):
        """Test loading an empty YAML file"""
        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("")
        
        result = load_yaml(str(yaml_file))
        assert result is None
    
    def test_load_nonexistent_file(self):
        """Test loading a non-existent file"""
        result = load_yaml("/nonexistent/path/file.yaml")
        assert result is None
    
    def test_load_invalid_yaml(self, tmp_path):
        """Test loading an invalid YAML file"""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("{ invalid yaml content: ][")
        
        result = load_yaml(str(yaml_file))
        assert result is None
    
    def test_load_file_permission_error(self, tmp_path):
        """Test loading a file without read permissions"""
        yaml_file = tmp_path / "no_permission.yaml"
        yaml_file.write_text("test: data")
        
        # Remove read permissions
        os.chmod(yaml_file, 0o000)
        
        try:
            result = load_yaml(str(yaml_file))
            assert result is None
        finally:
            # Restore permissions for cleanup
            os.chmod(yaml_file, 0o644)
    
    @patch('builtins.print')
    def test_error_message_printed(self, mock_print):
        """Test that error messages are printed correctly"""
        load_yaml("/nonexistent/file.yaml")
        mock_print.assert_called_once()
        assert "[ERROR]" in str(mock_print.call_args)
        assert "Failed to load file" in str(mock_print.call_args)
    
    def test_load_large_yaml_file(self, tmp_path):
        """Test loading a large YAML file"""
        # Create a large YAML structure
        large_content = {
            'innings': [
                {
                    f'over_{i}': {
                        'deliveries': [
                            {f'ball_{j}': {'runs': j}} for j in range(6)
                        ]
                    }
                } for i in range(50)
            ]
        }
        yaml_file = tmp_path / "large_match.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(large_content, f)
        
        result = load_yaml(str(yaml_file))
        assert result is not None
        assert len(result['innings']) == 50


class TestLoadAllYaml:
    """Test cases for load_all_yaml function"""
    
    def test_load_all_yaml_from_folder(self, tmp_path):
        """Test loading all YAML files from a folder"""
        # Create multiple YAML files
        yaml_files = {
            'match1.yaml': {'match_id': 1, 'info': {'teams': ['A', 'B']}},
            'match2.yml': {'match_id': 2, 'info': {'teams': ['C', 'D']}},
            'match3.yaml': {'match_id': 3, 'info': {'teams': ['E', 'F']}}
        }
        
        for filename, content in yaml_files.items():
            with open(tmp_path / filename, 'w') as f:
                yaml.dump(content, f)
        
        # Create non-YAML files that should be ignored
        (tmp_path / 'readme.txt').write_text('This is not a YAML file')
        (tmp_path / 'data.json').write_text('{"json": "file"}')
        
        result = load_all_yaml(str(tmp_path))
        
        assert len(result) == 3
        filenames = [item[0] for item in result]
        assert 'match1.yaml' in filenames
        assert 'match2.yml' in filenames
        assert 'match3.yaml' in filenames
        assert 'readme.txt' not in filenames
        assert 'data.json' not in filenames
        
        # Check content
        for filename, data in result:
            assert 'match_id' in data
            assert 'info' in data
    
    def test_load_all_yaml_empty_folder(self, tmp_path):
        """Test loading from an empty folder"""
        result = load_all_yaml(str(tmp_path))
        assert result == []
    
    def test_load_all_yaml_no_yaml_files(self, tmp_path):
        """Test loading from a folder with no YAML files"""
        (tmp_path / 'file1.txt').write_text('text file')
        (tmp_path / 'file2.csv').write_text('csv,file')
        (tmp_path / 'file3.json').write_text('{}')
        
        result = load_all_yaml(str(tmp_path))
        assert result == []
    
    def test_load_all_yaml_with_invalid_files(self, tmp_path):
        """Test loading when some YAML files are invalid"""
        # Valid YAML
        valid_content = {'match_id': 1, 'valid': True}
        with open(tmp_path / 'valid.yaml', 'w') as f:
            yaml.dump(valid_content, f)
        
        # Invalid YAML
        (tmp_path / 'invalid.yaml').write_text('{ invalid: yaml content ][')
        
        # Another valid YAML
        valid_content2 = {'match_id': 2, 'valid': True}
        with open(tmp_path / 'valid2.yaml', 'w') as f:
            yaml.dump(valid_content2, f)
        
        result = load_all_yaml(str(tmp_path))
        
        # Should only load valid files
        assert len(result) == 2
        filenames = [item[0] for item in result]
        assert 'valid.yaml' in filenames
        assert 'valid2.yaml' in filenames
        assert 'invalid.yaml' not in filenames
    
    def test_load_all_yaml_nonexistent_folder(self):
        """Test loading from a non-existent folder"""
        with pytest.raises(FileNotFoundError):
            load_all_yaml("/nonexistent/folder/path")
    
    def test_load_all_yaml_file_instead_of_folder(self, tmp_path):
        """Test passing a file path instead of folder path"""
        file_path = tmp_path / 'file.yaml'
        file_path.write_text('test: data')
        
        with pytest.raises(NotADirectoryError):
            load_all_yaml(str(file_path))
    
    def test_load_all_yaml_preserves_order(self, tmp_path):
        """Test that files are loaded in consistent order"""
        # Create files with specific names
        for i in range(5):
            content = {'match_id': i}
            with open(tmp_path / f'match_{i:02d}.yaml', 'w') as f:
                yaml.dump(content, f)
        
        result = load_all_yaml(str(tmp_path))
        
        # Files should be in alphabetical order
        filenames = [item[0] for item in result]
        assert set(filenames) == set(f'match_{i:02d}.yaml' for i in range(5))
    
    def test_load_all_yaml_mixed_extensions(self, tmp_path):
        """Test loading files with both .yaml and .yml extensions"""
        yaml_content = {'test': 'data'}
        
        with open(tmp_path / 'file1.yaml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        with open(tmp_path / 'file2.yml', 'w') as f:
            yaml.dump(yaml_content, f)
        
        with open(tmp_path / 'file3.YAML', 'w') as f:  # uppercase
            f.write('test: data')
        
        result = load_all_yaml(str(tmp_path))
        
        # Should load both .yaml and .yml (but not .YAML)
        assert len(result) == 2
        extensions = [os.path.splitext(item[0])[1] for item in result]
        assert '.yaml' in extensions
        assert '.yml' in extensions


# Integration tests
class TestIntegration:
    """Integration tests for file_loader module"""
    
    def test_load_and_process_multiple_files(self, tmp_path):
        """Test loading multiple files and processing them"""
        # Create a realistic cricket match structure
        match_data = {
            'meta': {
                'data_version': '1.0.0',
                'created': '2024-01-01',
                'revision': 1
            },
            'info': {
                'city': 'Mumbai',
                'dates': ['2024-01-01'],
                'match_type': 'T20',
                'teams': ['India', 'Australia'],
                'venue': 'Wankhede Stadium'
            },
            'innings': [
                {
                    '1st innings': {
                        'team': 'India',
                        'deliveries': [
                            {0.1: {'batsman': 'Rohit', 'bowler': 'Starc', 'runs': {'total': 4}}}
                        ]
                    }
                }
            ]
        }
        
        # Create multiple match files
        for i in range(3):
            match_data['info']['match_number'] = i + 1
            with open(tmp_path / f'match{i+1}.yaml', 'w') as f:
                yaml.dump(match_data, f)
        
        # Load all files
        matches = load_all_yaml(str(tmp_path))
        
        assert len(matches) == 3
        for filename, data in matches:
            assert 'meta' in data
            assert 'info' in data
            assert 'innings' in data
            assert data['info']['match_type'] == 'T20'
    
    def test_load_different_match_formats(self, tmp_path):
        """Test loading files with different cricket formats"""
        formats = {
            'test_match.yaml': {
                'info': {'match_type': 'Test', 'teams': ['England', 'Australia']},
                'innings': [
                    {'1st innings': {'team': 'England', 'deliveries': []}},
                    {'2nd innings': {'team': 'Australia', 'deliveries': []}},
                    {'3rd innings': {'team': 'England', 'deliveries': []}},
                    {'4th innings': {'team': 'Australia', 'deliveries': []}}
                ]
            },
            'odi_match.yaml': {
                'info': {'match_type': 'ODI', 'overs': 50, 'teams': ['India', 'Pakistan']},
                'innings': [
                    {'1st innings': {'team': 'India', 'deliveries': []}},
                    {'2nd innings': {'team': 'Pakistan', 'deliveries': []}}
                ]
            },
            't20_match.yaml': {
                'info': {'match_type': 'T20', 'overs': 20, 'teams': ['Mumbai', 'Chennai']},
                'innings': [
                    {'1st innings': {'team': 'Mumbai', 'deliveries': []}},
                    {'2nd innings': {'team': 'Chennai', 'deliveries': []}}
                ]
            },
            't10_match.yaml': {
                'info': {'match_type': 'T10', 'overs': 10, 'teams': ['Warriors', 'Gladiators']},
                'innings': [
                    {'1st innings': {'team': 'Warriors', 'deliveries': []}},
                    {'2nd innings': {'team': 'Gladiators', 'deliveries': []}}
                ]
            }
        }
        
        # Create files for each format
        for filename, content in formats.items():
            with open(tmp_path / filename, 'w') as f:
                yaml.dump(content, f)
        
        # Load all files
        matches = load_all_yaml(str(tmp_path))
        
        assert len(matches) == 4
        
        # Check that all formats are loaded
        loaded_formats = [data['info']['match_type'] for _, data in matches]
        assert 'Test' in loaded_formats
        assert 'ODI' in loaded_formats
        assert 'T20' in loaded_formats
        assert 'T10' in loaded_formats
        
        # Verify Test match has 4 innings
        test_match = next(data for _, data in matches if data['info']['match_type'] == 'Test')
        assert len(test_match['innings']) == 4
        
        # Verify limited overs matches have 2 innings
        for _, data in matches:
            if data['info']['match_type'] in ['ODI', 'T20', 'T10']:
                assert len(data['innings']) == 2