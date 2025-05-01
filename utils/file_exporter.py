# file_exporter.py

# v0.7

import os


class FileExporter:
    @staticmethod
    def export_to_text(content: str, file_path: str) -> bool:
        """
        Export the formatted tree to a text file

        Args:
            content: The formatted tree content
            file_path: Path to save the file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        except Exception as e:
            print(f"Error exporting to file: {e}")
            return False
