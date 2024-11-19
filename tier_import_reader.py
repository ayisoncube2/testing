import streamlit as st
import pandas as pd
import random


class TierDataProcessor:
    def __init__(self):
        self._counter = 0
        self._import_file = None
        self.tier_df = None
        self.template = None

    def set_template_df(self, df):
        self.template = df

    def get_import_file(self):
        return self._import_file

    def set_import_file(self, template, import_file):
        self._import_file = import_file
        self.template = template

        if self.template is not None and self._import_file is not None:
            tier_data = pd.read_csv(self._import_file)
            self.tier_df = pd.merge(tier_data, self.template, on=['dataElement_uid', 'categoryOptionCombo_uid'],
                                    how='left')
            self.tier_df['supportType'] = self.tier_df['dataElement'].str.split(',').str[1].str.strip()

    def get_df(self):
        return self.tier_df

    def display_tier_import_uploader(self, template, label, key):
        key = f"{key}{self._counter}"
        import_file = st.file_uploader(label, type=["csv"], key=key)
        if import_file is not None:
            st.success(f"File '{import_file.name}' uploaded successfully!")
        self._counter += 1
        self.set_import_file(template, import_file)
