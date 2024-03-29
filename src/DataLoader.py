"""Data loading class for Stanford SNAP Reddit Hyperlink data."""

# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

import ast
import numpy as np
import pandas as pd

from src.property_names import PROPERTIES_COLUMN_NAMES

class DataLoader:
    """Helper class for loading Reddit Hyperlink data.

    Attributes
    ----------
    filepath : str
        Path to the data file.
    full_file : bool, optional
        Whether or not to load the full file.
        If this is set to true, then the num_lines
        argument is not used.
    num_lines : str
        How many lines of the file to load.
        Use this parameter if not loading the
        full file.
    cols_to_load : bool, optional
        Which columns in the data to load. Need
        to use the column names found in the raw data.
    """

    def __init__(self, filepath, full_file=False, num_lines=10, cols_to_load=[]):
        self.filepath = filepath
        self.full_file = full_file
        self.num_lines = num_lines
        self.cols_to_load = cols_to_load

    def load(self):
        """Load the data file and return the lines as a list."""
        with open(self.filepath) as f:
            if not self.full_file:
                lines = []
                for __ in range(self.num_lines):
                    lines.append(f.readline())
            else:
                lines = f.readlines()

        cleaned_lines = np.array(self._clean(lines))
        if not self.cols_to_load:
            return cleaned_lines
        else:
            cols_to_load_idx = []
            for i, val in enumerate(cleaned_lines[0]):
                if val in self.cols_to_load:
                    cols_to_load_idx.append(i)
            return cleaned_lines[:, cols_to_load_idx]
    
    def _clean(self, lines):
        """Splits lines on tabs and removes the extraneous new line sometimes found."""
        new_lines = []
        for line in lines:
            new_lines.append(line.replace('\n', '').split('\t'))
        
        return new_lines

class PandasDataLoader:
    """Helper class for loading Reddit Hyperlink data into pandas.

    Attributes
    ----------
    filepath1 : str
        Path to the data file.
    filepath2 : str, optional
        If filepath2 is passed, then another
        data file is loaded and combined with
        the first data file. The combined
        DataFrame is returned.
    """

    def __init__(self, filepath1, filepath2=None):
        self.filepath1 = filepath1
        self.filepath2 = filepath2
    
    def load(self):
        """Load one data file if only one filepath was passed, else load two and return combined."""
        df1 = pd.read_csv(self.filepath1, delimiter='\t')
        if not self.filepath2:
            return df1
        else:
            df2 = pd.read_csv(self.filepath2, delimiter='\t')
            df_combined = pd.concat([df1, df2])
            return df_combined
    
    @staticmethod
    def generate_properties_df(df):
        """Takes the 'PROPERTIES' column of the DataFrame and splits it into its 86 numeric columns.
        Returns a DataFrame of just these text properties."""
        text_properties = df.apply(lambda row: ast.literal_eval(row['PROPERTIES']), axis=1).values.tolist()
        df_properties = pd.DataFrame(text_properties, columns=PROPERTIES_COLUMN_NAMES)

        return df_properties

