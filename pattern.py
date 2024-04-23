import os
from typing import List

class Pattern:
    def __init__(self, patterns: List[str], in_file: bool):
        if in_file:
            paths = self.transform_patterns(patterns)
            self.validate_paths(paths)
            self.patterns = self.unpack_patterns(paths)
        else:
            self.patterns = patterns

        self.index = 0

    def transform_patterns(self, patterns):
        paths = [os.path.join("patterns", pattern) for pattern in patterns]
        return paths
    
    def validate_paths(self, paths):
        is_valid = [os.path.exists(path) for path in paths]
        if not all(is_valid):
            raise Exception("Invalid pattern paths")
        
    def reset(self):
        self.index = 0

    def unpack_patterns(self, paths):
        patterns = []
        for file in paths:
            with open(file, "r") as f:
                patterns_one_file = [x.strip("\n") for x in f.readlines()]
                patterns += patterns_one_file
        return patterns

    def get_one_pattern(self):
        """Returns a pattern"""
        if self.index >= len(self.patterns):
            return None
        
        pattern = self.patterns[self.index]
        self.index += 1
        return pattern
    
if __name__ == "__main__":
    p = Pattern([r"email_regex.txt"], True)
    pattern = p.get_one_pattern()
    while pattern:
        print(pattern)
        print()
        pattern = p.get_one_pattern()