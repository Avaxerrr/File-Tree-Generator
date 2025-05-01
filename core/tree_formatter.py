# tree_formatter.py

# v1.0.0

from typing import Dict, List, Optional


class TreeFormatter:
    def __init__(self, use_box_drawing: bool = False):
        self.use_box_drawing = use_box_drawing
        # Set up the characters based on the chosen style
        if use_box_drawing:
            self.branch = "├── "
            self.pipe = "│   "
            self.last_branch = "└── "
            self.empty = "    "
        else:
            self.branch = "+--- "
            self.pipe = "|    "
            self.last_branch = "\\--- "  # Changed to backslash for last item
            self.empty = "     "

    def format_tree(self, tree_data: Dict, include_comments: bool = False) -> str:
        """
        Format the directory tree into a string representation
        """
        lines = []
        # Add the root directory name with trailing slash
        root_name = tree_data['name']
        if not root_name.endswith('/'):
            root_name += '/'
        lines.append(root_name)

        # Format the children
        self._format_children(tree_data['children'], [], lines, include_comments)

        return '\n'.join(lines)

    def _format_children(self, children: List[Dict], prefix_parts: List[bool], lines: List[str],
                         include_comments: bool, comments: Optional[Dict] = None):
        """
        Recursively format the children of a directory
        """
        if not children:
            return

        # If comments not provided, initialize as empty dict
        if comments is None:
            comments = {}

        for i, item in enumerate(children):
            is_last = i == len(children) - 1

            # Build prefix string with proper spacing and pipes
            prefix = ''
            for has_more_siblings in prefix_parts:
                prefix += self.pipe if has_more_siblings else self.empty

            # Choose the appropriate branch character
            branch_char = self.last_branch if is_last else self.branch

            # Format the current item
            item_line = f"{prefix}{branch_char}{item['name']}"

            # Add comment if available and enabled
            if include_comments and item['name'] in comments:
                item_line += f"    # {comments[item['name']]}"

            lines.append(item_line)

            # Recursively process subdirectories
            if item['is_dir'] and 'children' in item:
                # For next level, add True if not last (has more siblings), else False
                new_prefix_parts = prefix_parts + [not is_last]
                self._format_children(item['children'], new_prefix_parts, lines, include_comments, comments)

                # Add empty line with just pipes for spacing between directory sections
                if not is_last and item['children']:
                    separator_prefix = ''
                    for j, has_more_siblings in enumerate(prefix_parts):
                        separator_prefix += self.pipe if has_more_siblings else self.empty
                    # Add pipe at the current level if not the last item
                    separator_prefix += self.pipe
                    lines.append(f"{separator_prefix}")
