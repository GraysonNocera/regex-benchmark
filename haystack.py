import os
from typing import List

class Haystack:
    def __init__(self, paths: List[str], split_file: bool):
        self.paths = self.transform_paths(paths)
        self.validate_paths()
        self.path_index = 0
        self.line_index = 0
        self.split_file = split_file
        self.temp_file = os.path.join("haystacks", "temp")
        self.f = open(self.paths[self.path_index], "r") if self.split_file else None

    @property
    def current_path(self):
        return self.paths[self.path_index]
    
    @property
    def num_haystacks(self):
        if self.split_file:
            return self.get_num_lines()
        return len(self.paths)
    
    def get_num_lines(self):
        return sum([sum(1 for line in open(path)) for path in self.paths])
    
    def __len__(self):
        return self.num_haystacks

    def transform_paths(self, paths):
        paths = [os.path.join("haystacks", path) for path in paths]
        return paths

    def validate_paths(self):
        is_valid = [os.path.exists(path) for path in self.paths]
        if not all(is_valid):
            raise Exception("Invalid haystack paths")
        
    def reset(self):
        self.path_index = 0
        self.line_index = 0
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        self.f = open(self.paths[self.path_index], "r") if self.split_file else None

    def get_one_haystack(self):
        """Returns a path to a haystack file"""
        if self.split_file:
            line = self.get_line()
            return line
        
        if self.path_index >= len(self.paths):
            return None
        
        path = self.paths[self.path_index]
        self.path_index += 1
        return path
    
    def get_line(self):
        """gets a line, writes it to a temp file, and returns the file"""

        if not self.f: 
            return None

        line = self.f.readline()
        if not line and self.path_index == len(self.paths) - 1:
            self.f.close()
            self.f = None
            return None
        
        if not line:
            self.f.close()
            self.path_index += 1
            self.f = open(self.paths[self.path_index], "r")
            line = self.f.readline()

        line = line.strip("\n")
        with open(self.temp_file, "w") as f:
            f.write(line)

        self.line_index += 1
        return self.temp_file


if __name__ == "__main__":
  haystack = Haystack(["email_regex_text.txt", "testing.txt"], False)
  line = haystack.get_one_haystack()
  while line:
    print(line)
    line = haystack.get_one_haystack()