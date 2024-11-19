import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TB_STAT'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TB_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TB_STAT, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TB_STAT, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TB_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TB_STAT[TB_STAT[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_STAT_D', index=False)

        level_1_check_df = TB_STAT[TB_STAT[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_STAT_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TB_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TB_STAT[TB_STAT['MER report 1st submission vs 2nd submission_TB_STAT_D'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_STAT_D', index=False)

        mer1_vs_mer2 = TB_STAT[TB_STAT['MER report 1st submission vs 2nd submission_TB_STAT_N'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_STAT_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TB_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_mer2 = TB_STAT[TB_STAT['MER report 2nd submission vs Import File_TB_STAT_D'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_STAT_D', index=False)

        imp_vs_mer2 = TB_STAT[TB_STAT['MER report 2nd submission vs Import File_TB_STAT_N'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_STAT_N', index=False)

        support_typecheck = TB_STAT[TB_STAT['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TB_STAT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_genie = TB_STAT[TB_STAT['Import File vs Genie_TB_STAT_D'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_STAT_D', index=False)

        imp_vs_genie = TB_STAT[TB_STAT['Import File vs Genie_TB_STAT_N'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_STAT_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tb_stat_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        TB_STAT_N_genie = first_genie[
            (first_genie['indicator'] == 'TB_STAT') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'N')]

        TB_STAT_N_genie = TB_STAT_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TB_STAT_N_genie = pd.DataFrame(TB_STAT_N_genie).reset_index()
        TB_STAT_N_genie = TB_STAT_N_genie.rename(columns={'TB_STAT': 'Previous_QTR_TB_STAT_N'})

        # merge with first genie
        TB_STAT = pd.merge(mfl, TB_STAT_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TB_STAT = TB_STAT.drop(columns='orgunituid')

        TB_STAT_D_genie = first_genie[
            (first_genie['indicator'] == 'TB_STAT') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'D')]

        TB_STAT_D_genie = TB_STAT_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TB_STAT_D_genie = pd.DataFrame(TB_STAT_D_genie).reset_index()
        TB_STAT_D_genie = TB_STAT_D_genie.rename(columns={'TB_STAT': 'Previous_QTR_TB_STAT_D'})

        # merge with first genie
        TB_STAT = pd.merge(TB_STAT, TB_STAT_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TB_STAT = TB_STAT.drop(columns='orgunituid')

        if step == 'MER File 1':
            TB_STAT = run_first_mer(TB_STAT, mer_file1)

            summary_cols = ['Previous_QTR_TB_STAT_N', 'Previous_QTR_TB_STAT_D',
                            'MER report 1st submission_TB_STAT_D', 'MER report 1st submission_TB_STAT_N']

            summary_df = TB_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TB_STAT = run_second_mer(TB_STAT, mer_file1, mer_file2)

            summary_cols = ['Previous_QTR_TB_STAT_N', 'Previous_QTR_TB_STAT_D',
                            'MER report 1st submission_TB_STAT_D', 'MER report 1st submission_TB_STAT_N',
                            'MER report 2nd submission_TB_STAT_D', 'MER report 2nd submission_TB_STAT_N']

            summary_df = TB_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TB_STAT = run_tier(TB_STAT, mer_file1, mer_file2, tier_df)

            summary_cols = ['Previous_QTR_TB_STAT_N', 'Previous_QTR_TB_STAT_D',
                            'MER report 1st submission_TB_STAT_D', 'MER report 1st submission_TB_STAT_N',
                            'MER report 2nd submission_TB_STAT_D', 'MER report 2nd submission_TB_STAT_N',
                            'Import File_TB_STAT_D', 'Import File_TB_STAT_N']

            summary_df = TB_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TB_STAT = run_new_genie(TB_STAT, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TB_STAT_N', 'Previous_QTR_TB_STAT_D',
                            'MER report 1st submission_TB_STAT_D', 'MER report 1st submission_TB_STAT_N',
                            'MER report 2nd submission_TB_STAT_D', 'MER report 2nd submission_TB_STAT_N',
                            'Import File_TB_STAT_D', 'Import File_TB_STAT_N',
                            'Genie_TB_STAT_D', 'Genie_TB_STAT_N']

            summary_df = TB_STAT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TB_STAT, mer_file1):
    non_kp = pd.read_excel(mer_file1, sheet_name='TB_STAT_Numer')
    mer_appended = non_kp[non_kp['District'].isin(districts)]
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_STAT_N'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT = TB_STAT.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_STAT_N'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_STAT[qtr_data_check] = TB_STAT.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    non_kp = pd.read_excel(mer_file1, sheet_name='TB_STAT_Denom')
    mer_appended = non_kp[non_kp['District'].isin(districts)]
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_STAT_D'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT = TB_STAT.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_STAT_D'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_STAT[qtr_data_check] = TB_STAT.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    TB_STAT['%TB Coverage'] = (TB_STAT['MER report 1st submission_TB_STAT_N'] / TB_STAT[
        'MER report 1st submission_TB_STAT_D']) * 100

    def check_coverage(coverage):
        if coverage < 80:
            return "Extremely low HIV testing coverage"
        elif coverage > 100:
            return "Data quality issue"
        else:
            return ""

    # Apply the function to the '%TB Coverage' column
    TB_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = TB_STAT[
        '%TB Coverage'].apply(check_coverage)

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TB_STAT_D',
                    'MER report 1st submission_TB_STAT_D',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D',
                    'Previous_QTR_TB_STAT_N',
                    'MER report 1st submission_TB_STAT_N',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N',
                    '%TB Coverage',
                    'Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%',
                    ]
    TB_STAT = TB_STAT[ordered_cols]

    return TB_STAT


def run_second_mer(TB_STAT, mer_file1, mer_file2):
    # run first mer
    TB_STAT = run_first_mer(TB_STAT, mer_file1)

    non_kp = pd.read_excel(mer_file2, sheet_name='TB_STAT_Numer')
    mer_appended = non_kp[non_kp['District'].isin(districts)]
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_STAT_N'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT = TB_STAT.drop(columns='UID')

    TB_STAT['MER report 1st submission vs 2nd submission_TB_STAT_N'] = (
                TB_STAT['MER report 1st submission_TB_STAT_N'].eq(TB_STAT['MER report 2nd submission_TB_STAT_N']) | (
                    TB_STAT['MER report 1st submission_TB_STAT_N'].isna() & TB_STAT[
                'MER report 2nd submission_TB_STAT_N'].isna()))

    non_kp = pd.read_excel(mer_file2, sheet_name='TB_STAT_Denom')
    mer_appended = non_kp[non_kp['District'].isin(districts)]
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_STAT_D'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT = TB_STAT.drop(columns='UID')

    TB_STAT['MER report 1st submission vs 2nd submission_TB_STAT_D'] = (
                TB_STAT['MER report 1st submission_TB_STAT_D'].eq(TB_STAT['MER report 2nd submission_TB_STAT_D']) | (
                    TB_STAT['MER report 1st submission_TB_STAT_D'].isna() & TB_STAT[
                'MER report 2nd submission_TB_STAT_D'].isna()))

    TB_STAT['%TB Coverage'] = TB_STAT['MER report 2nd submission_TB_STAT_N'] / TB_STAT[
        'MER report 2nd submission_TB_STAT_D']

    def check_coverage(coverage):
        if coverage < 0.8:
            return "Extremely low HIV testing coverage"
        elif coverage > 1.0:
            return "Data quality issue"
        else:
            return ""

    # Apply the function to the '%TB Coverage' column
    TB_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = TB_STAT[
        '%TB Coverage'].apply(check_coverage)

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TB_STAT_D',
                    'MER report 1st submission_TB_STAT_D',
                    'MER report 2nd submission_TB_STAT_D',
                    'MER report 1st submission vs 2nd submission_TB_STAT_D',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D',
                    'Previous_QTR_TB_STAT_N',
                    'MER report 1st submission_TB_STAT_N',
                    'MER report 2nd submission_TB_STAT_N',
                    'MER report 1st submission vs 2nd submission_TB_STAT_N',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N',
                    '%TB Coverage',
                    'Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%',
                    ]
    TB_STAT = TB_STAT[ordered_cols]

    return TB_STAT


def run_tier(TB_STAT, mer_file1, mer_file2, tier):
    # run the second mer
    TB_STAT = run_second_mer(TB_STAT, mer_file1, mer_file2)

    TB_STAT_N_tier = tier[tier['dataElement'].str.startswith('TB_STAT (N,')].drop(columns=['period'])

    TB_STAT_N_tier['dataElement'] = TB_STAT_N_tier['dataElement'].apply(
        lambda x: 'TB_STAT' if x.startswith('TB_STAT (N,') else x)

    TB_STAT_N_tier = TB_STAT_N_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                values='value', aggfunc='sum')
    TB_STAT_N_tier = pd.DataFrame(TB_STAT_N_tier).reset_index()

    TB_STAT_N_tier = TB_STAT_N_tier.rename(columns={'TB_STAT': 'Import File_TB_STAT_N'})

    TB_STAT = pd.merge(TB_STAT, TB_STAT_N_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TB_STAT = TB_STAT.drop(columns=['orgUnit_uid'])

    TB_STAT['Support Type Check'] = (TB_STAT['DSD/TA'] == TB_STAT['supportType']) | (
                TB_STAT['supportType'].isna() | (TB_STAT['supportType'] == ''))

    TB_STAT['MER report 2nd submission vs Import File_TB_STAT_N'] = (
                TB_STAT['MER report 2nd submission_TB_STAT_N'].eq(TB_STAT['Import File_TB_STAT_N']) | (
                    TB_STAT['MER report 2nd submission_TB_STAT_N'].isna() & TB_STAT['Import File_TB_STAT_N'].isna()))

    TB_STAT_D_tier = tier[tier['dataElement'].str.startswith('TB_STAT (D,')].drop(columns=['period'])

    TB_STAT_D_tier['dataElement'] = TB_STAT_D_tier['dataElement'].apply(
        lambda x: 'TB_STAT' if x.startswith('TB_STAT (D,') else x)

    TB_STAT_D_tier = TB_STAT_D_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                aggfunc='sum')
    TB_STAT_D_tier = pd.DataFrame(TB_STAT_D_tier).reset_index()

    TB_STAT_D_tier = TB_STAT_D_tier.rename(columns={'TB_STAT': 'Import File_TB_STAT_D'})

    TB_STAT = pd.merge(TB_STAT, TB_STAT_D_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TB_STAT = TB_STAT.drop(columns=['orgUnit_uid'])

    TB_STAT['MER report 2nd submission vs Import File_TB_STAT_D'] = (
                TB_STAT['MER report 2nd submission_TB_STAT_D'].eq(TB_STAT['Import File_TB_STAT_D']) | (
                    TB_STAT['MER report 2nd submission_TB_STAT_D'].isna() & TB_STAT['Import File_TB_STAT_D'].isna()))

    TB_STAT['%TB Coverage'] = ((TB_STAT['Import File_TB_STAT_N'] / TB_STAT['Import File_TB_STAT_D']) * 100).round(0)

    def check_coverage(coverage):
        if coverage < 80:
            return "Extremely low HIV testing coverage"
        elif coverage > 100:
            return "Data quality issue"
        else:
            return ""

    # Apply the function to the '%TB Coverage' column
    TB_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = TB_STAT[
        '%TB Coverage'].apply(check_coverage)

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TB_STAT_D',
                    'MER report 1st submission_TB_STAT_D',
                    'MER report 2nd submission_TB_STAT_D',
                    'MER report 1st submission vs 2nd submission_TB_STAT_D',
                    'Import File_TB_STAT_D',
                    'MER report 2nd submission vs Import File_TB_STAT_D',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D',
                    'Previous_QTR_TB_STAT_N',
                    'MER report 1st submission_TB_STAT_N',
                    'MER report 2nd submission_TB_STAT_N',
                    'MER report 1st submission vs 2nd submission_TB_STAT_N',
                    'Import File_TB_STAT_N',
                    'MER report 2nd submission vs Import File_TB_STAT_N',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N',
                    '%TB Coverage',
                    'Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%',
                    'supportType', 'Support Type Check'
                    ]
    TB_STAT = TB_STAT[ordered_cols]

    return TB_STAT


def run_new_genie(TB_STAT, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TB_STAT = run_tier(TB_STAT, mer_file1, mer_file2, tier_df)

    TB_STAT_N_genie = second_genie[
        (second_genie['indicator'] == 'TB_STAT') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (second_genie['numeratordenom'] == 'N')]

    TB_STAT_N_genie = TB_STAT_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TB_STAT_N_genie = pd.DataFrame(TB_STAT_N_genie).reset_index()

    TB_STAT_N_genie = TB_STAT_N_genie.rename(columns={'TB_STAT': 'Genie_TB_STAT_N'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, TB_STAT_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TB_STAT = TB_STAT.drop(columns='orgunituid')

    TB_STAT['Import File vs Genie_TB_STAT_N'] = (TB_STAT['Import File_TB_STAT_N'].eq(TB_STAT['Genie_TB_STAT_N']) | (
                TB_STAT['Import File_TB_STAT_N'].isna() & TB_STAT['Genie_TB_STAT_N'].isna()))

    TB_STAT_D_genie = second_genie[
        (second_genie['indicator'] == 'TB_STAT') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (second_genie['numeratordenom'] == 'D')]

    TB_STAT_D_genie = TB_STAT_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TB_STAT_D_genie = pd.DataFrame(TB_STAT_D_genie).reset_index()

    TB_STAT_D_genie = TB_STAT_D_genie.rename(columns={'TB_STAT': 'Genie_TB_STAT_D'})

    # merge with first genie
    TB_STAT = pd.merge(TB_STAT, TB_STAT_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TB_STAT = TB_STAT.drop(columns='orgunituid')

    TB_STAT['Import File vs Genie_TB_STAT_D'] = (TB_STAT['Import File_TB_STAT_D'].eq(TB_STAT['Genie_TB_STAT_D']) | (
                TB_STAT['Import File_TB_STAT_D'].isna() & TB_STAT['Genie_TB_STAT_D'].isna()))

    TB_STAT['%TB Coverage'] = TB_STAT['Genie_TB_STAT_N'] / TB_STAT['Genie_TB_STAT_D']

    def check_coverage(coverage):
        if coverage < 0.8:
            return "Extremely low HIV testing coverage"
        elif coverage > 1.0:
            return "Data quality issue"
        else:
            return ""

    # Apply the function to the '%TB Coverage' column
    TB_STAT['Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%'] = TB_STAT[
        '%TB Coverage'].apply(check_coverage)

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TB_STAT_D',
                    'MER report 1st submission_TB_STAT_D',
                    'MER report 2nd submission_TB_STAT_D',
                    'MER report 1st submission vs 2nd submission_TB_STAT_D',
                    'Import File_TB_STAT_D',
                    'MER report 2nd submission vs Import File_TB_STAT_D',
                    'Genie_TB_STAT_D',
                    'Import File vs Genie_TB_STAT_D',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_D',
                    'Previous_QTR_TB_STAT_N',
                    'MER report 1st submission_TB_STAT_N',
                    'MER report 2nd submission_TB_STAT_N',
                    'MER report 1st submission vs 2nd submission_TB_STAT_N',
                    'Import File_TB_STAT_N',
                    'MER report 2nd submission vs Import File_TB_STAT_N',
                    'Genie_TB_STAT_N', 'Import File vs Genie_TB_STAT_N',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_N',
                    '%TB Coverage',
                    'Status Check: "Extremely low HIV testing coverage" <80%, "Data quality issue" >100%',
                    ]
    TB_STAT = TB_STAT[ordered_cols]

    return TB_STAT
