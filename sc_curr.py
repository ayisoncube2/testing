import datetime
import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings
from  qaurter_handler import get_six_months_ago

warnings.filterwarnings("ignore")

indicator_name = 'SC_CURR'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(SC_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, SC_CURR, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, SC_CURR, summary_df, step):

    if step == 'Tier Import':
        # Write Main sheet
        SC_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Write Level 1 Check sheet
        level_1_check_df = SC_CURR[SC_CURR[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_SC_CURR'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check', index=False)

        support_typecheck = SC_CURR[SC_CURR['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        SC_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_genie = SC_CURR[SC_CURR['Import File vs Genie_SC_CURR'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import vs Genie_SC_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_sc_curr_data(mfl, first_genie, user_inputs, non_tier, new_genie_df):

    step = user_inputs.get_step_output()
    fiscal_year_1stG_semi = user_inputs.get_first_genie_year()  # select correct year for this semi
    _1stG_curr_qtr_semi = user_inputs.get_first_genie_qtr() # select correct qtr for this semi
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        genie = first_genie[
            (first_genie['indicator'] == 'SC_CURR') & (first_genie['fiscal_year'] == fiscal_year_1stG_semi) & (
                        first_genie['source_name'] == 'DATIM')]

        genie = genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr_semi, aggfunc='sum')
        genie = pd.DataFrame(genie).reset_index()
        genie = genie.rename(columns={'SC_CURR': 'Previous_SC_CURR'})

        SC_CURR = pd.merge(mfl, genie, left_on='DATIM UID', right_on='orgunituid', how='left')

        if step == 'Tier Import':
            SC_CURR = run_tier(SC_CURR, non_tier)

            summary_df = SC_CURR.groupby('OU3name')[['Previous_SC_CURR', 'Import File_SC_CURR']].sum().reset_index()

            total_row = summary_df[['Previous_SC_CURR', 'Import File_SC_CURR']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            SC_CURR = run_new_genie(SC_CURR, non_tier, new_genie_df, fiscal_year_2ndG, _2ndG_curr_qtr)

            summary_df = SC_CURR.groupby('OU3name')[['Previous_SC_CURR', 'Import File_SC_CURR']].sum().reset_index()

            total_row = summary_df[['Previous_SC_CURR', 'Import File_SC_CURR']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_tier(SC_CURR, non_tier):
    SC_CURR_tier = non_tier[non_tier['dataElement'].str.startswith('SC_CURR')]

    SC_CURR_tier['dataElement'] = SC_CURR_tier['dataElement'].apply(
        lambda x: 'SC_CURR' if x.startswith('SC_CURR') else x)

    SC_CURR_tier = SC_CURR_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                            aggfunc='sum')
    SC_CURR_tier = pd.DataFrame(SC_CURR_tier).reset_index()

    SC_CURR_tier = SC_CURR_tier.rename(columns={'SC_CURR': 'Import File_SC_CURR'})

    SC_CURR = pd.merge(SC_CURR, SC_CURR_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    SC_CURR = SC_CURR.drop(columns=['orgUnit_uid'])

    SC_CURR['Support Type Check'] = (SC_CURR['DSD/TA'] == SC_CURR['supportType']) | (
                SC_CURR['supportType'].isna() | (SC_CURR['supportType'] == ''))

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_SC_CURR'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['Import File_SC_CURR'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    SC_CURR[qtr_data_check] = SC_CURR.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    return SC_CURR


def run_new_genie(SC_CURR, non_tier, second_genie, fiscal_year_2ndG, _2ndG_curr_qtr):
    # run tier step
    SC_CURR = run_tier(SC_CURR, non_tier)

    genie = second_genie[
        (second_genie['indicator'] == 'SC_CURR') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    genie = genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr, aggfunc='sum')
    genie = pd.DataFrame(genie).reset_index()

    genie = genie.rename(columns={'SC_CURR': 'Genie_SC_CURR'})

    # merge with first genie
    SC_CURR = pd.merge(SC_CURR, genie, left_on='DATIM UID', right_on='orgunituid', how='left')

    SC_CURR['Import File vs Genie_SC_CURR'] = (SC_CURR['Import File_SC_CURR'].eq(SC_CURR['Genie_SC_CURR']) | (
                SC_CURR['Import File_SC_CURR'].isna() & SC_CURR['Genie_SC_CURR'].isna()))

    SC_CURR.drop(columns=['orgunituid_x', 'orgunituid_y'], inplace=True)

    return SC_CURR
