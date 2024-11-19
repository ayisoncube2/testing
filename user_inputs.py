import streamlit as st

import indicator_handler
from indicator_handler import get_indicators


class UserInputs:
    def __init__(self):
        self._fiscal_year = None
        self._qtr = None
        self._indicator = None
        self._step_output = None
        self._first_genie_year = None
        self._first_genie_qtr = None

    def display_inputs(self):
        with st.expander("Need help?"):
            st.markdown('<p style="color:red;">Please make sure to provide <strong>accurate</strong> files.</p>',
                        unsafe_allow_html=True)
            st.markdown("There are only 2 Steps for non tier indicators", unsafe_allow_html=True)
            st.markdown("For semi indicators e.g. [TX_TB, SC_CURR, SC_ARVDISP, TB_PREV], choose Q2 or Q4 of the "
                        "fiscal year.", unsafe_allow_html=True)
            st.markdown("MFL sheet name: Use format MFL_FY24_Q2 to indicate the right FY and Q", unsafe_allow_html=True)
            st.markdown("Tier data: CSV format required.", unsafe_allow_html=True)
            st.markdown("Tier template: Excel format required.", unsafe_allow_html=True)
            st.markdown("Non-Tier data: Excel file required.", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            self._fiscal_year = st.selectbox("Select fiscal year", [2023, 2024, 2025, 2026, 2027, 2028], index=0)

        with col2:
            self._qtr = st.selectbox("Select Current QTR", ["qtr1", "qtr2", "qtr3", "qtr4"], index=0)

        with col3:
            self._first_genie_qtr = st.selectbox("Select Previous QTR", ["qtr1", "qtr2", "qtr3", "qtr4"], index=0)

        with col4:
            self._first_genie_year = st.selectbox("Select 1st Genie's Year", [2023, 2024, 2025, 2026, 2027, 2028], index=0)

        col5, col6 = st.columns(2)

        with col5:
            self._indicator = st.selectbox("Select your indicator", get_indicators(), index=0)

            non_tier_indicators = indicator_handler.get_non_tier_indicators()

            if self._indicator in non_tier_indicators:
                with col6:
                    self._step_output = st.selectbox("Select your step", ["Tier Import", "New Genie"], index=0)
            else:
                with col6:
                    self._step_output = st.selectbox("Select your step", ["MER File 1", "MER File 2",
                                                                  "Tier Import", "New Genie"], index=0)

    def get_fiscal_year(self):
        return self._fiscal_year

    def set_fiscal_year(self, fiscal_year):
        self._fiscal_year = fiscal_year

    def get_qtr(self):
        return self._qtr

    def set_qtr(self, qtr):
        self._qtr = qtr

    def get_indicator(self):
        return self._indicator

    def set_indicator(self, indicator):
        self._indicator = indicator

    def get_step_output(self):
        return self._step_output

    def set_step_output(self, step_output):
        self._step_output = step_output

    def get_first_genie_year(self):
        return self._first_genie_year

    def set_first_genie_year(self, first_genie_year):
        self._first_genie_year = first_genie_year

    def get_first_genie_qtr(self):
        return self._first_genie_qtr

    def set_first_genie_qtr(self, first_genie_qtr):
        self._first_genie_qtr = first_genie_qtr
