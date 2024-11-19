import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'PMTCT_STAT'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(PMTCT_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, PMTCT_STAT, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, PMTCT_STAT, summary_df, step):

    if step == 'Tier Import':
        # Write Main sheet
        PMTCT_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_2_check_df = PMTCT_STAT[PMTCT_STAT['Level 2 Check:  PMTCT_STAT N > PMTCT_STAT D'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_STAT N > PMTCT_STAT D', index=False)

        support_typecheck = PMTCT_STAT[PMTCT_STAT['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        PMTCT_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_Genie = PMTCT_STAT[PMTCT_STAT['Import File vs Genie_PMTCT_STAT_D'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_PMTCT_STAT_D', index=False)

        Import_vs_Genie = PMTCT_STAT[PMTCT_STAT['Import File vs Genie_PMTCT_STAT_N'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_PMTCT_STAT_N', index=False)

        level_2_check_df = PMTCT_STAT[PMTCT_STAT['Level 2 Check:  PMTCT_STAT N > PMTCT_STAT D'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_STAT N > PMTCT_STAT D', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_pmtct_stat_data(mfl, first_genie, user_inputs, non_tier, new_genie_df):

    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()  # select correct year for this semi
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr() # select correct qtr for this semi
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        # PMTCT_STAT
        PMTCT_STAT_genie = first_genie[
            (first_genie['numeratordenom'] == 'D') & (first_genie['indicator'] == 'PMTCT_STAT') & (
                        first_genie['fiscal_year'] == fiscal_year_1stG) & (first_genie['source_name'] == 'DATIM')]
        PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                        values=_1stG_curr_qtr, aggfunc='sum')
        PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()
        PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT': 'Previous_QTR_PMTCT_STAT_D'})

        # merge with first genie
        PMTCT_STAT = pd.merge(mfl, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        PMTCT_STAT = PMTCT_STAT.drop(columns='orgunituid')

        # PMTCT_STAT
        PMTCT_STAT_genie = first_genie[
            (first_genie['numeratordenom'] == 'N') & (first_genie['indicator'] == 'PMTCT_STAT') & (
                        first_genie['fiscal_year'] == fiscal_year_1stG) & (first_genie['source_name'] == 'DATIM')]
        PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                        values=_1stG_curr_qtr, aggfunc='sum')
        PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()
        PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT': 'Previous_QTR_PMTCT_STAT_N'})

        # merge with first genie
        PMTCT_STAT = pd.merge(PMTCT_STAT, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        PMTCT_STAT = PMTCT_STAT.drop(columns='orgunituid')

        if step == 'Tier Import':
            PMTCT_STAT = run_tier(PMTCT_STAT, non_tier)

            # step 4 output
            summary_cols = ['Import File_PMTCT_STAT_D', 'Import File_PMTCT_STAT_N']

            summary_df = PMTCT_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            PMTCT_STAT = run_new_genie(PMTCT_STAT, non_tier, new_genie_df, fiscal_year_2ndG, _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Import File_PMTCT_STAT_D', 'Import File_PMTCT_STAT_N', 'Genie_PMTCT_STAT_D',
                            'Genie_PMTCT_STAT_N']

            summary_df = PMTCT_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_tier(PMTCT_STAT, non_tier):
    PMTCT_STAT_D_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_STAT (D')]

    PMTCT_STAT_D_tier['dataElement'] = PMTCT_STAT_D_tier['dataElement'].apply(
        lambda x: 'PMTCT_STAT_D' if x.startswith('PMTCT_STAT') else x)

    PMTCT_STAT_D_tier = PMTCT_STAT_D_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                      values='value', aggfunc='sum')

    PMTCT_STAT_D_tier = pd.DataFrame(PMTCT_STAT_D_tier).reset_index()

    PMTCT_STAT_D_tier = PMTCT_STAT_D_tier.rename(columns={'PMTCT_STAT_D': 'Import File_PMTCT_STAT_D'})

    PMTCT_STAT = pd.merge(PMTCT_STAT, PMTCT_STAT_D_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PMTCT_STAT = PMTCT_STAT.drop(columns=['orgUnit_uid'])

    PMTCT_STAT_N_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_STAT (N')]

    PMTCT_STAT_N_tier['dataElement'] = PMTCT_STAT_N_tier['dataElement'].apply(
        lambda x: 'PMTCT_STAT_N' if x.startswith('PMTCT_STAT') else x)

    PMTCT_STAT_N_tier = PMTCT_STAT_N_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                      aggfunc='sum')

    PMTCT_STAT_N_tier = pd.DataFrame(PMTCT_STAT_N_tier).reset_index()

    PMTCT_STAT_N_tier = PMTCT_STAT_N_tier.rename(columns={'PMTCT_STAT_N': 'Import File_PMTCT_STAT_N'})

    PMTCT_STAT = pd.merge(PMTCT_STAT, PMTCT_STAT_N_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PMTCT_STAT = PMTCT_STAT.drop(columns=['orgUnit_uid'])

    PMTCT_STAT['Support Type Check'] = (PMTCT_STAT['DSD/TA'] == PMTCT_STAT['supportType']) | (
                PMTCT_STAT['supportType'].isna() | (PMTCT_STAT['supportType'] == ''))

    PMTCT_STAT['Level 2 Check:  PMTCT_STAT N > PMTCT_STAT D'] = PMTCT_STAT['Import File_PMTCT_STAT_N'] > PMTCT_STAT[
        'Import File_PMTCT_STAT_D']

    PMTCT_STAT['% Coverage'] = (
                (PMTCT_STAT['Import File_PMTCT_STAT_N'] / PMTCT_STAT['Import File_PMTCT_STAT_D']) * 100).round(2)

    def check_coverage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low HIV testing coverage"
        elif pd.notna(value) and value > 100:
            return "Data quality issue"
        else:
            return ""

    PMTCT_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = PMTCT_STAT[
        '% Coverage'].apply(check_coverage)

    return PMTCT_STAT


def run_new_genie(PMTCT_STAT, non_tier, second_genie, fiscal_year_2ndG, _2ndG_curr_qtr):
    # run tier step
    PMTCT_STAT = run_tier(PMTCT_STAT, non_tier)

    # PMTCT_STAT
    PMTCT_STAT_genie = second_genie[
        (second_genie['numeratordenom'] == 'D') & (second_genie['indicator'] == 'PMTCT_STAT') & (
                    second_genie['fiscal_year'] == fiscal_year_2ndG) & (second_genie['source_name'] == 'DATIM')]
    PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                    aggfunc='sum')
    PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()

    PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT': 'Genie_PMTCT_STAT_D'})

    # merge with first genie
    PMTCT_STAT = pd.merge(PMTCT_STAT, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    PMTCT_STAT = PMTCT_STAT.drop(columns='orgunituid')

    PMTCT_STAT['Import File vs Genie_PMTCT_STAT_D'] = (
                PMTCT_STAT['Import File_PMTCT_STAT_D'].eq(PMTCT_STAT['Genie_PMTCT_STAT_D']) | (
                    PMTCT_STAT['Import File_PMTCT_STAT_D'].isna() & PMTCT_STAT['Genie_PMTCT_STAT_D'].isna()))

    # PMTCT_STAT
    PMTCT_STAT_genie = second_genie[
        (second_genie['numeratordenom'] == 'N') & (second_genie['indicator'] == 'PMTCT_STAT') & (
                    second_genie['fiscal_year'] == fiscal_year_2ndG) & (second_genie['source_name'] == 'DATIM')]
    PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                    aggfunc='sum')
    PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()
    PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT': 'Genie_PMTCT_STAT_N'})

    # merge with first genie
    PMTCT_STAT = pd.merge(PMTCT_STAT, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    PMTCT_STAT = PMTCT_STAT.drop(columns='orgunituid')

    PMTCT_STAT['Import File vs Genie_PMTCT_STAT_N'] = (
                PMTCT_STAT['Import File_PMTCT_STAT_N'].eq(PMTCT_STAT['Genie_PMTCT_STAT_N']) | (
                    PMTCT_STAT['Import File_PMTCT_STAT_N'].isna() & PMTCT_STAT['Genie_PMTCT_STAT_N'].isna()))

    PMTCT_STAT['Level 2 Check:  PMTCT_STAT N > PMTCT_STAT D'] = PMTCT_STAT['Genie_PMTCT_STAT_N'] > PMTCT_STAT[
        'Genie_PMTCT_STAT_D']

    PMTCT_STAT['% Coverage'] = ((PMTCT_STAT['Genie_PMTCT_STAT_N'] / PMTCT_STAT['Genie_PMTCT_STAT_D']) * 100).round(2)

    def check_coverage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low HIV testing coverage"
        elif pd.notna(value) and value > 100:
            return "Data quality issue"
        else:
            return ""

    PMTCT_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = PMTCT_STAT[
        '% Coverage'].apply(check_coverage)

    return PMTCT_STAT