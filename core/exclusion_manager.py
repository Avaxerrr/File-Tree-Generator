#exclusion_manager.py

# v1.0.0

import re
from typing import Set
from pathlib import Path


class ExclusionManager:
    """Manages patterns of files and directories to exclude from tree generation"""

    def __init__(self):
        self.patterns = set()  # Set of patterns to exclude
        self.use_common_exclusions = True  # Whether to use common exclusions

    def add_pattern(self, pattern: str):
        """Add a pattern to exclude"""
        if pattern:
            self.patterns.add(pattern)

    def remove_pattern(self, pattern: str):
        """Remove a pattern from exclusions"""
        if pattern in self.patterns:
            self.patterns.remove(pattern)

    def clear_patterns(self):
        """Clear all exclusion patterns"""
        self.patterns.clear()

    def set_use_common_exclusions(self, use: bool):
        """Set whether to use common exclusions"""
        self.use_common_exclusions = use

    def get_common_exclusions(self) -> Set[str]:
        """Get the set of common exclusion patterns"""
        return {
            ".git", ".github", ".gitignore", ".idea", ".vscode",
            "__pycache__", ".venv", "node_modules", "build", "dist",
            "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.exe",
            "*.obj", "*.o", "*.a", "*.lib", "*.out", "*.log",
            ".DS_Store", "Thumbs.db"
        }

    def should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded based on patterns"""
        # Convert to string for pattern matching
        path_str = str(path)
        path_name = path.name

        # Check common exclusions if enabled
        if self.use_common_exclusions:
            exclusions = self.get_common_exclusions()
            if path_name in exclusions:
                return True

            # Check file extensions for patterns like "*.pyc"
            for pattern in exclusions:
                if pattern.startswith("*.") and path_name.endswith(pattern[1:]):
                    return True

        # Check custom patterns
        for pattern in self.patterns:
            if self._matches_pattern(path_str, path_name, pattern):
                return True

        return False

    def _matches_pattern(self, path_str: str, path_name: str, pattern: str) -> bool:
        """Check if a path matches a pattern"""
        if pattern.startswith("*."):
            # Simple extension matching
            return path_name.endswith(pattern[1:])
        elif "*" in pattern or "?" in pattern:
            # Convert glob pattern to regex
            regex_pattern = self._glob_to_regex(pattern)
            return re.search(regex_pattern, path_str) is not None
        else:
            # Direct substring matching
            return pattern in path_str or pattern == path_name

    def _glob_to_regex(self, pattern: str) -> str:
        """Convert a glob pattern to a regex pattern"""
        # Escape special regex characters
        regex = re.escape(pattern)
        # Convert glob wildcards to regex wildcards
        regex = regex.replace(r'\*', '.*').replace(r'\?', '.')
        return f"^{regex}$"
