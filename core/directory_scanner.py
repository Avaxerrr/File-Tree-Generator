# directory_scanner.py

# v0.7

import os
from pathlib import Path
from typing import Dict, List, Optional


class DirectoryScanner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.exclusion_manager = None

    def set_exclusion_manager(self, exclusion_manager):
        """Set the exclusion manager for filtering paths"""
        self.exclusion_manager = exclusion_manager

    def scan(self) -> Dict:
        """
        Scan the directory structure and return a nested dictionary representation
        """
        if not self.root_path.exists() or not self.root_path.is_dir():
            raise ValueError(f"Path does not exist or is not a directory: {self.root_path}")

        return self._scan_directory(self.root_path)

    def _scan_directory(self, directory: Path) -> Dict:
        """
        Recursively scan a directory and return its structure
        """
        result = {
            'name': directory.name or directory.as_posix(),  # Use path string for root
            'is_dir': True,
            'children': []
        }

        try:
            # Get all items in the directory
            items = []
            for item in directory.iterdir():
                # Skip excluded paths if exclusion manager is set
                if self.exclusion_manager and self.exclusion_manager.should_exclude(item):
                    continue
                items.append(item)

            # Sort items: directories first, then files, all alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

            for item in items:
                if item.is_dir():
                    # Recursively scan subdirectories
                    result['children'].append(self._scan_directory(item))
                else:
                    # Add files
                    result['children'].append({
                        'name': item.name,
                        'is_dir': False
                    })

            return result

        except PermissionError:
            # Handle permission errors gracefully
            result['children'].append({
                'name': "[Permission Denied]",
                'is_dir': False
            })
            return result
