import datetime
import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings
from qaurter_handler import get_six_months_ago

warnings.filterwarnings("ignore")

indicator_name = 'HTS_SELF'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(HTS_SELF, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, HTS_SELF, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, HTS_SELF, summary_df, step):
    if step == 'Tier Import':
        # Write Main sheet
        HTS_SELF.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        HTS_SELF.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_hts_self_data(mfl, first_genie, user_inputs, non_tier, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()  # select correct year for this semi
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()  # select correct qtr for this semi
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        HTS_SELF_genie = first_genie[
            (first_genie['indicator'] == 'HTS_SELF') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]
        HTS_SELF_genie = HTS_SELF_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                    aggfunc='sum')
        HTS_SELF_genie = pd.DataFrame(HTS_SELF_genie).reset_index()
        HTS_SELF_genie = HTS_SELF_genie.rename(columns={'HTS_SELF': 'Previous_QTR_HTS_SELF'})

        # merge with first genie
        HTS_SELF = pd.merge(mfl, HTS_SELF_genie, left_on='DATIM UID', right_on='orgunituid', how='left')

        HTS_SELF = HTS_SELF.drop(columns='orgunituid')

        if step == 'Tier Import':
            HTS_SELF = run_tier(HTS_SELF, non_tier)

            # step 4 output
            summary_cols = ['Previous_QTR_HTS_SELF', 'Import File_HTS_SELF']

            summary_df = HTS_SELF.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_SELF, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            HTS_SELF = run_new_genie(HTS_SELF, non_tier, new_genie_df, fiscal_year_2ndG, _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_HTS_SELF', 'Import File_HTS_SELF', 'Genie_HTS_SELF']

            summary_df = HTS_SELF.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_SELF, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_tier(HTS_SELF, non_tier):
    dataElementName = ['HTS_SELF (N, TA, Age/Sex/HIVSelfTest): HIV self test kits distributed',
                       'HTS_SELF (N, DSD, Age/Sex/HIVSelfTest): HIV self test kits distributed',
                       'HTS_SELF (N, TA, HIVSelfTestUser): HIV self test kits distributed',
                       'HTS_SELF (N, DSD, HIVSelfTestUser): HIV self test kits distributed']

    non_tier = non_tier[non_tier['dataElement'].isin(dataElementName)]

    non_tier = non_tier.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()
    non_tier = non_tier.rename(columns={'value': 'Import File_HTS_SELF'})

    HTS_SELF = pd.merge(HTS_SELF, non_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_SELF = HTS_SELF.drop(columns=['orgUnit_uid'])
    return HTS_SELF


def run_new_genie(HTS_SELF, non_tier, second_genie, fiscal_year_2ndG, _2ndG_curr_qtr):
    # run tier step
    HTS_SELF = run_tier(HTS_SELF, non_tier)

    HTS_SELF_genie = second_genie[
        (second_genie['indicator'] == 'HTS_SELF') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    HTS_SELF_genie = HTS_SELF_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                aggfunc='sum')
    HTS_SELF_genie = pd.DataFrame(HTS_SELF_genie).reset_index()
    HTS_SELF_genie = HTS_SELF_genie.rename(columns={'HTS_SELF': 'Genie_HTS_SELF'})

    # merge with first genie
    HTS_SELF = pd.merge(HTS_SELF, HTS_SELF_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    HTS_SELF = HTS_SELF.drop(columns='orgunituid')

    HTS_SELF['Import File vs Genie_HTS_SELF'] = (HTS_SELF['Import File_HTS_SELF'].eq(HTS_SELF['Genie_HTS_SELF']) | (
                HTS_SELF['Import File_HTS_SELF'].isna() & HTS_SELF['Genie_HTS_SELF'].isna()))

    return HTS_SELF
