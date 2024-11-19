import pandas as pd
import streamlit as st


class MerFileReader:
    def __init__(self):
        self._mer_file = None
        self._df = None
        self._counter = 0

    def set_mer_file(self, file):
        self._mer_file = file
        self._df = pd.read_excel(file)

    def get_file(self):
        return self._mer_file

    def get_df(self):
        if self._df is not None:
            return self._df
        else:
            raise ValueError("MER file is not uploaded")

    def display_file_uploader(self, label, key_prefix):
        key = f"{key_prefix}{self._counter}"
        self._mer_file = st.file_uploader(label, type=["xlsx"], key=key)
        if self._mer_file is not None:
            st.success(f"File '{self._mer_file.name}' uploaded successfully!")
            self._df = pd.read_excel(self._mer_file)

        self._counter += 1
