import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TB_STAT_POS_ART'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TB_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TB_STAT_POS_ART, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TB_STAT_POS_ART, summary_df, step):
    if step == 'MER File 1':

        # Write Main sheet
        TB_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TB_STAT_POS_ART[TB_STAT_POS_ART[
                                               'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_POS'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_STAT_POS', index=False)

        level_1_check_df = TB_STAT_POS_ART[TB_STAT_POS_ART[
                                               'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_ART'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_ART', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TB_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TB_STAT_POS_ART[
            TB_STAT_POS_ART['MER report 1st submission vs 2nd submission_TB_STAT_POS'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_STAT_POS', index=False)

        mer1_vs_mer2 = TB_STAT_POS_ART[TB_STAT_POS_ART['MER report 1st submission vs 2nd submission_TB_ART'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_ART', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TB_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_mer2 = TB_STAT_POS_ART[TB_STAT_POS_ART['MER report 2nd submission vs Import File_TB_STAT_POS'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_STAT_POS', index=False)

        imp_vs_mer2 = TB_STAT_POS_ART[TB_STAT_POS_ART['MER report 2nd submission vs Import File_TB_ART'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_ART', index=False)

        support_typecheck = TB_STAT_POS_ART[TB_STAT_POS_ART['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TB_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_genie = TB_STAT_POS_ART[TB_STAT_POS_ART['Import File vs Genie_TB_STAT_POS'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_STAT_POS', index=False)

        imp_vs_genie = TB_STAT_POS_ART[TB_STAT_POS_ART['Import File vs Genie_TB_ART'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_ART', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tb_stat_pos_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        TB_STAT_POS_genie = first_genie[
            (first_genie['indicator'] == 'TB_STAT_POS') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'Derived')]

        TB_STAT_POS_genie = TB_STAT_POS_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                          values=_1stG_curr_qtr, aggfunc='sum')
        TB_STAT_POS_genie = pd.DataFrame(TB_STAT_POS_genie).reset_index()

        TB_STAT_POS_genie = TB_STAT_POS_genie.rename(columns={'TB_STAT_POS': 'Previous_QTR_TB_STAT_POS'})

        # merge with first genie
        TB_STAT_POS_ART = pd.merge(mfl, TB_STAT_POS_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='orgunituid')

        TB_ART_genie = first_genie[
            (first_genie['indicator'] == 'TB_ART') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]

        TB_ART_genie = TB_ART_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                aggfunc='sum')
        TB_ART_genie = pd.DataFrame(TB_ART_genie).reset_index()

        TB_ART_genie = TB_ART_genie.rename(columns={'TB_ART': 'Previous_QTR_TB_ART'})

        # # merge with first genie
        TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, TB_ART_genie, left_on='DATIM UID', right_on='orgunituid',
                                   how='left')
        TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='orgunituid')

        if step == 'MER File 1':
            TB_STAT_POS_ART = run_first_mer(TB_STAT_POS_ART, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TB_STAT_POS', 'Previous_QTR_TB_ART',
                            'MER report 1st submission_TB_STAT_POS', 'MER report 1st submission_TB_ART']

            summary_df = TB_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TB_STAT_POS_ART = run_second_mer(TB_STAT_POS_ART, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TB_STAT_POS', 'Previous_QTR_TB_ART',
                            'MER report 1st submission_TB_STAT_POS', 'MER report 1st submission_TB_ART',
                            'MER report 2nd submission_TB_STAT_POS', 'MER report 2nd submission_TB_ART']

            summary_df = TB_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TB_STAT_POS_ART = run_tier(TB_STAT_POS_ART, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TB_STAT_POS', 'Previous_QTR_TB_ART',
                            'MER report 1st submission_TB_STAT_POS', 'MER report 1st submission_TB_ART',
                            'MER report 2nd submission_TB_STAT_POS', 'MER report 2nd submission_TB_ART',
                            'MER report 2nd submission vs Import File_TB_STAT_POS',
                            'MER report 2nd submission vs Import File_TB_ART']

            summary_df = TB_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TB_STAT_POS_ART = run_new_genie(TB_STAT_POS_ART, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TB_STAT_POS', 'Previous_QTR_TB_ART',
                            'MER report 1st submission_TB_STAT_POS', 'MER report 1st submission_TB_ART',
                            'MER report 2nd submission_TB_STAT_POS', 'MER report 2nd submission_TB_ART',
                            'MER report 2nd submission vs Import File_TB_STAT_POS',
                            'MER report 2nd submission vs Import File_TB_ART',
                            'Import File vs Genie_TB_STAT_POS', 'Import File vs Genie_TB_ART']

            summary_df = TB_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TB_STAT_POS_ART, mer_file1):

    non_kp = pd.read_excel(mer_file1, sheet_name='TB_STAT_Numer')
    non_kp = non_kp[non_kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['HIVStatus'].isin(['New Positive', 'Known Positive'])]

    mer = non_kp.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_STAT_POS'})

    # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_POS'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_STAT_POS'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_STAT_POS_ART[qtr_data_check] = TB_STAT_POS_ART.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    non_kp = pd.read_excel(mer_file1, sheet_name='TB_ART')
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer = non_kp.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_ART'})

    # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_ART'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_ART'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_STAT_POS_ART[qtr_data_check] = TB_STAT_POS_ART.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    TB_STAT_POS_ART['%Linkage'] = (TB_STAT_POS_ART['MER report 1st submission_TB_ART'] / TB_STAT_POS_ART[
        'MER report 1st submission_TB_STAT_POS']) * 100

    TB_STAT_POS_ART['Level 2 Check: %Linkage comment'] = TB_STAT_POS_ART['%Linkage'].apply(
        lambda x: 'Extremely low linkage' if x < 79 else ('Good linkage' if x > 90 else ''))

    return TB_STAT_POS_ART


def run_second_mer(TB_STAT_POS_ART, mer_file1, mer_file2):
    # run first mer
    TB_STAT_POS_ART = run_first_mer(TB_STAT_POS_ART, mer_file1)

    non_kp = pd.read_excel(mer_file2, sheet_name='TB_STAT_Numer')
    non_kp = non_kp[non_kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['HIVStatus'].isin(['New Positive', 'Known Positive'])]

    mer = non_kp.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_STAT_POS'})

    # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='UID')

    TB_STAT_POS_ART['MER report 1st submission vs 2nd submission_TB_STAT_POS'] = (
                TB_STAT_POS_ART['MER report 1st submission_TB_STAT_POS'].eq(
                    TB_STAT_POS_ART['MER report 2nd submission_TB_STAT_POS']) | (
                            TB_STAT_POS_ART['MER report 1st submission_TB_STAT_POS'].isna() & TB_STAT_POS_ART[
                        'MER report 2nd submission_TB_STAT_POS'].isna()))

    non_kp = pd.read_excel(mer_file2, sheet_name='TB_ART')
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer = non_kp.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_ART'})

    # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='UID')

    TB_STAT_POS_ART['MER report 1st submission vs 2nd submission_TB_ART'] = (
                TB_STAT_POS_ART['MER report 1st submission_TB_ART'].eq(
                    TB_STAT_POS_ART['MER report 2nd submission_TB_ART']) | (
                            TB_STAT_POS_ART['MER report 1st submission_TB_ART'].isna() & TB_STAT_POS_ART[
                        'MER report 2nd submission_TB_ART'].isna()))

    TB_STAT_POS_ART['%Linkage'] = (TB_STAT_POS_ART['MER report 2nd submission_TB_ART'] / TB_STAT_POS_ART[
        'MER report 2nd submission_TB_STAT_POS']) * 100

    TB_STAT_POS_ART['Level 2 Check: %Linkage comment'] = TB_STAT_POS_ART['%Linkage'].apply(
        lambda x: 'Extremely low linkage' if x < 79 else ('Good linkage' if x > 90 else ''))

    return TB_STAT_POS_ART


def run_tier(TB_STAT_POS_ART, mer_file1, mer_file2, tier):
    # run the second mer
    TB_STAT_POS_ART = run_second_mer(TB_STAT_POS_ART, mer_file1, mer_file2)

    TB_STAT_POS_tier = tier[tier['dataElement'].str.startswith('TB_STAT (N,')].drop(columns=['period'])

    TB_STAT_POS_tier = TB_STAT_POS_tier[
        TB_STAT_POS_tier['categoryOptionComboName'].str.contains('Known Positives|Newly Tested Positives')]

    TB_STAT_POS_tier['dataElement'] = TB_STAT_POS_tier['dataElement'].apply(
        lambda x: 'TB_STAT' if x.startswith('TB_STAT (N,') else x)

    TB_STAT_POS_tier = TB_STAT_POS_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                    values='value', aggfunc='sum')
    TB_STAT_POS_tier = pd.DataFrame(TB_STAT_POS_tier).reset_index()

    TB_STAT_POS_tier = TB_STAT_POS_tier.rename(columns={'TB_STAT': 'Import File_TB_STAT_POS'})

    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, TB_STAT_POS_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                               how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns=['orgUnit_uid'])

    TB_STAT_POS_ART['Support Type Check'] = (TB_STAT_POS_ART['DSD/TA'] == TB_STAT_POS_ART['supportType']) | (
                TB_STAT_POS_ART['supportType'].isna() | (TB_STAT_POS_ART['supportType'] == ''))

    TB_STAT_POS_ART['MER report 2nd submission vs Import File_TB_STAT_POS'] = (
                TB_STAT_POS_ART['MER report 2nd submission_TB_STAT_POS'].eq(
                    TB_STAT_POS_ART['Import File_TB_STAT_POS']) | (
                            TB_STAT_POS_ART['MER report 2nd submission_TB_STAT_POS'].isna() & TB_STAT_POS_ART[
                        'Import File_TB_STAT_POS'].isna()))

    TB_ART_tier = tier[tier['dataElement'].str.startswith('TB_ART (N,')].drop(columns=['period'])
    TB_ART_tier['dataElement'] = TB_ART_tier['dataElement'].apply(
        lambda x: 'TB_ART' if x.startswith('TB_ART (N,') else x)

    TB_ART_tier = TB_ART_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    TB_ART_tier = pd.DataFrame(TB_ART_tier).reset_index()

    TB_ART_tier = TB_ART_tier.rename(columns={'TB_ART': 'Import File_TB_ART'})

    if TB_ART_tier.shape[0] == 0:
        TB_STAT_POS_ART['Import File_TB_ART'] = 0
    else:
        TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, TB_ART_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                   how='left')
        TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns=['orgUnit_uid'])

    TB_STAT_POS_ART['MER report 2nd submission vs Import File_TB_ART'] = (
                TB_STAT_POS_ART['MER report 2nd submission_TB_ART'].eq(TB_STAT_POS_ART['Import File_TB_ART']) | (
                    TB_STAT_POS_ART['MER report 2nd submission_TB_ART'].isna() & TB_STAT_POS_ART[
                'Import File_TB_ART'].isna()))

    TB_STAT_POS_ART['%Linkage'] = (
                (TB_STAT_POS_ART['Import File_TB_ART'] / TB_STAT_POS_ART['Import File_TB_STAT_POS']) * 100).round(2)

    TB_STAT_POS_ART['Level 2 Check: %Linkage comment'] = TB_STAT_POS_ART['%Linkage'].apply(
        lambda x: 'Extremely low linkage' if x < 79 else ('Good linkage' if x > 90 else ''))

    return TB_STAT_POS_ART


def run_new_genie(TB_STAT_POS_ART, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TB_STAT_POS_ART = run_tier(TB_STAT_POS_ART, mer_file1, mer_file2, tier_df)

    TB_STAT_POS_genie = second_genie[
        (second_genie['indicator'] == 'TB_STAT_POS') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'Derived')]

    TB_STAT_POS_genie = TB_STAT_POS_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                      aggfunc='sum')
    TB_STAT_POS_genie = pd.DataFrame(TB_STAT_POS_genie).reset_index()

    TB_STAT_POS_genie = TB_STAT_POS_genie.rename(columns={'TB_STAT_POS': 'Genie_TB_STAT_POS'})

    # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, TB_STAT_POS_genie, left_on='DATIM UID', right_on='orgunituid',
                               how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='orgunituid')

    TB_STAT_POS_ART['Import File vs Genie_TB_STAT_POS'] = (
                TB_STAT_POS_ART['Import File_TB_STAT_POS'].eq(TB_STAT_POS_ART['Genie_TB_STAT_POS']) | (
                    TB_STAT_POS_ART['Import File_TB_STAT_POS'].isna() & TB_STAT_POS_ART['Genie_TB_STAT_POS'].isna()))

    TB_ART_genie = second_genie[
        (second_genie['indicator'] == 'TB_ART') & (second_genie['fiscal_year'] == fiscal_year_2ndG)]
    TB_ART_genie = TB_ART_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                            aggfunc='sum')
    TB_ART_genie = pd.DataFrame(TB_ART_genie).reset_index()

    TB_ART_genie = TB_ART_genie.rename(columns={'TB_ART': 'Genie_TB_ART'})

    # # merge with first genie
    TB_STAT_POS_ART = pd.merge(TB_STAT_POS_ART, TB_ART_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TB_STAT_POS_ART = TB_STAT_POS_ART.drop(columns='orgunituid')

    TB_STAT_POS_ART['Import File vs Genie_TB_ART'] = (
                TB_STAT_POS_ART['Import File_TB_ART'].eq(TB_STAT_POS_ART['Genie_TB_ART']) | (
                    TB_STAT_POS_ART['Import File_TB_ART'].isna() & TB_STAT_POS_ART['Genie_TB_ART'].isna()))

    TB_STAT_POS_ART['%Linkage'] = TB_STAT_POS_ART['Genie_TB_ART'] / TB_STAT_POS_ART['Genie_TB_STAT_POS']

    TB_STAT_POS_ART['Level 2 Check: %Linkage comment'] = TB_STAT_POS_ART['%Linkage'].apply(
        lambda x: 'Extremely low linkage' if x < 79 else ('Good linkage' if x > 90 else ''))

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TB_STAT_POS',
                    'MER report 1st submission_TB_STAT_POS',
                    'MER report 2nd submission_TB_STAT_POS',
                    'MER report 1st submission vs 2nd submission_TB_STAT_POS',
                    'Import File_TB_STAT_POS',
                    'MER report 2nd submission vs Import File_TB_STAT_POS',
                    'Genie_TB_STAT_POS',
                    'Import File vs Genie_TB_STAT_POS',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_STAT_POS',

                    'Previous_QTR_TB_ART',
                    'MER report 1st submission_TB_ART',
                    'MER report 2nd submission_TB_ART',
                    'MER report 1st submission vs 2nd submission_TB_ART',
                    'Import File_TB_ART',
                    'MER report 2nd submission vs Import File_TB_ART',
                    'Genie_TB_ART',
                    'Import File vs Genie_TB_ART',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_ART',
                    '%Linkage',
                    'Level 2 Check: %Linkage comment'
                    ]
    TB_STAT_POS_ART = TB_STAT_POS_ART[ordered_cols]

    return TB_STAT_POS_ART
