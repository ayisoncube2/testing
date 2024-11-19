import pandas as pd
import streamlit as st
from districts import get_districts
from qaurter_handler import get_fy_qtr_suffix


class MFLHandler:
    def __init__(self):
        self._file = None
        self._sheet_name = None

    def set_file(self, file):
        self._file = file

    def get_file(self):
        return self._file

    def set_sheet_name(self, sheet_name):
        self._sheet_name = sheet_name

    def get_sheet_name(self):
        return self._sheet_name

    def get_df(self):
        if self._file is not None and self._sheet_name is not None:
            df = pd.read_excel(self._file, sheet_name=self._sheet_name)
            st.write("Number of facilities found: ", df.shape[0])
            return df
        else:
            raise ValueError("File or sheet name is not set")

    def get_processed_mfl(self):
        try:
            df = pd.read_excel(self._file, sheet_name=self._sheet_name)
            df = df[['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'New_OU5 Code', 'DATIM UID', 'DSD/TA', 'Eligibility to Report']]
            df = df[df['OU3name'].isin(get_districts())]  # select districts
            #df = df[df['Eligibility to Report'].isin(['Both', 'Non-Tier', 'Tier'])]  # choose eligibility
            df = df.drop(columns=['Eligibility to Report'])
            return df
        except ValueError as e:
            st.error(f"Error: {str(e)}. Please select the correct sheet name.")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None

    def get_sheet_names(self, year, qtr):
        if self._file is not None:
            # Format the sheet name
            sheet_name = "MFL_FY" + get_fy_qtr_suffix(year, qtr)
            return [sheet_name]
        else:
            raise ValueError("File is not set")
