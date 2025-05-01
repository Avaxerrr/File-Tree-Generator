import os
import json
import sys

def get_config_path():
    """Return the path to config.json in the executable's directory."""
    if getattr(sys, 'frozen', False):
        # Running as a packaged executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as a script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to project root if in utils/
        base_dir = os.path.abspath(os.path.join(base_dir, '..'))
    return os.path.join(base_dir, "config.json")

def load_exclusion_config():
    """Load exclusion patterns and use_common flag from config.json"""
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                patterns = data.get("patterns", [])
                use_common = data.get("use_common", True)
                return {"patterns": patterns, "use_common": use_common}
        except Exception:
            pass
    # Defaults if not found or error
    return {"patterns": [], "use_common": True}

def save_exclusion_config(patterns, use_common):
    """Save exclusion patterns and use_common flag to config.json"""
    config_path = get_config_path()
    data = {
        "patterns": patterns,
        "use_common": use_common
    }
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save exclusion config: {e}")
