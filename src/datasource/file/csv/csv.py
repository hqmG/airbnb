"""
Class script for interacting with CSV file.
"""
# Modules
import os
import pandas


class CSV(object):
    """
    Class for interacting with CSV file.
    """
    def __init__(
        self,
        filepath: str,
    ) -> None:
        """
        Initiating CSV class.

        Attributes:
            filepath: Path to file.
        """
        # Parameters
        self.filepath = filepath

    def load(self) -> pandas.DataFrame:
        """
        Loading CSV file as pandas dataframe.

        Returns:
            Pandas dataframe.
        """
        # Loading data
        return pandas.read_csv(self.filepath)

    def save(
        self,
        df: pandas.DataFrame,
    ) -> None:
        """
        Saving pandas dataframe as CSV file.

        Args:
            df: pandas dataframe.0
        """
        # Deleting existing data
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        # Saving data
        df.to_csv(self.filepath)
