import pandas as pd
import streamlit as st


class GenieHandler:
    def __init__(self):
        self._genie_file = None
        self._genie_df = None
        self._columns_to_read = ['indicator', 'standardizeddisaggregate', 'orgunituid', 'categoryoptioncomboname',
                                 'sex', 'ageasentered', 'fiscal_year', 'qtr1', 'qtr2', 'qtr3', 'qtr4', 'source_name',
                                 'numeratordenom', 'statushiv']

    # def set_genie_file(self, file):
    #     self._genie_file = file
    #     self.set_genie_df(file)

    def get_file(self):
        if self._genie_file is None:
            return None
        else:
            return self._genie_file

    # def set_genie_df(self, file):
    #     self._genie_df = pd.read_csv(self._genie_file, sep='\t', usecols=columns_to_read)

    def get_df(self):
        if self._genie_file is not None:
            return self._genie_df
        else:
            raise ValueError("Genie file is not set")

    def display_file_uploader(self, label, key):
        self._genie_file = st.file_uploader(label, type=["txt"], key=key)
        if self._genie_file is not None:
            st.success(f"File '{self._genie_file.name}' uploaded successfully!")
            self._genie_df = pd.read_csv(self._genie_file, sep='\t', usecols=self._columns_to_read)