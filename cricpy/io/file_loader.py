import os
import yaml

def load_yaml(filepath):
    """
    Load a single Cricsheet YAML file and return a dictionary.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load file: {filepath} — {e}")
        return None


def load_all_yaml(folder_path):
    """
    Load all YAML files from a folder.
    Returns a list of (filename, match_dict) tuples.
    """
    matches = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            path = os.path.join(folder_path, filename)
            data = load_yaml(path)
            if data:
                matches.append((filename, data))
    return matches
