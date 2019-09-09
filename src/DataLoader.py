"""Data loading class for Stanford SNAP Reddit Hyperlink data."""

import numpy as np

class DataLoader:

    def __init__(self, full_file=False, num_lines=10, cols_to_load=[]):
        self.filepath = "data/soc-redditHyperlinks-body.tsv"
        self.full_file = False
        self.num_lines = num_lines
        self.cols_to_load = cols_to_load

    def load(self):
        with open(self.filepath) as f:
            if not self.full_file:
                lines = []
                for __ in range(self.num_lines):
                    lines.append(f.readline())
            else:
                lines = f.readlines

        cleaned_lines = np.array(self.clean(lines))
        if not self.cols_to_load:
            return cleaned_lines
        else:
            cols_to_load_idx = []
            for i, val in enumerate(cleaned_lines[0]):
                if val in self.cols_to_load:
                    cols_to_load_idx.append(i)
            return cleaned_lines[:, cols_to_load_idx]
    
    def clean(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(line.replace('\n', '').split('\t'))
        
        return new_lines