import pandas as pd
import streamlit as st


class TierTemplateFileReader:
    def __init__(self, uploaded_file):
        self._df = None
        self._uploaded_file = uploaded_file

        self._cols = ['dataelementname', 'dataelement_uid', 'categoryoptioncomboname', 'categoryoptioncombo_uid']

        self._new_names = {'dataelementname': 'dataElement',
                           'dataelement_uid': 'dataElement_uid',
                           'categoryoptioncomboname': 'categoryOptionComboName',
                           'categoryoptioncombo_uid': 'categoryOptionCombo_uid'}

    # Getter for file content
    def get_df(self):
        if self._uploaded_file is not None:
            self._df = pd.read_excel(self._uploaded_file, sheet_name="dataelement_codelist").rename(
                columns=self._new_names)
            return self._df
        else:
            st.warning("No file uploaded yet.")

    # Getter for file name
    def get_uploaded_file(self):
        return self._uploaded_file
