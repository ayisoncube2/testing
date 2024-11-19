import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TB_PREV'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TB_PREV, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TB_PREV, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TB_PREV, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TB_PREV.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TB_PREV[TB_PREV[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_PREV_D', index=False)

        level_1_check_df = TB_PREV[TB_PREV[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TB_PREV_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TB_PREV.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TB_PREV[TB_PREV['MER report 1st submission vs 2nd submission_TB_PREV_D'] == 'FALSE']
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_PREV_D', index=False)

        mer1_vs_mer2 = TB_PREV[TB_PREV['MER report 1st submission vs 2nd submission_TB_PREV_N'] == 'FALSE']
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_PREV_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TB_PREV.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_mer2 = TB_PREV[TB_PREV['MER report  2nd submission vs Import File_TB_PREV_D'] == 'FALSE']
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_PREV_D', index=False)

        imp_vs_mer2 = TB_PREV[TB_PREV['MER report  2nd submission vs Import File_TB_PREV_N'] == 'FALSE']
        imp_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_PREV_N', index=False)

        support_typecheck = TB_PREV[TB_PREV['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TB_PREV.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_genie = TB_PREV[TB_PREV['Import File vs Genie_TB_PREV_D'] == 'FALSE']
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_PREV_D', index=False)

        imp_vs_genie = TB_PREV[TB_PREV['Import File vs Genie_TB_PREV_N'] == 'FALSE']
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_TB_PREV_N', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tb_prev_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()  # this is a semi - select even quarters
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        TB_PREV_N_genie = first_genie[
            (first_genie['indicator'] == 'TB_PREV') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'N')]

        TB_PREV_N_genie = TB_PREV_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TB_PREV_N_genie = pd.DataFrame(TB_PREV_N_genie).reset_index()
        TB_PREV_N_genie = TB_PREV_N_genie.rename(columns={'TB_PREV': 'Previous_QTR_TB_PREV_N'})

        # merge with first genie
        TB_PREV = pd.merge(mfl, TB_PREV_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TB_PREV = TB_PREV.drop(columns='orgunituid')

        TB_PREV_D_genie = first_genie[
            (first_genie['indicator'] == 'TB_PREV') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'D')]

        TB_PREV_D_genie = TB_PREV_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TB_PREV_D_genie = pd.DataFrame(TB_PREV_D_genie).reset_index()
        TB_PREV_D_genie = TB_PREV_D_genie.rename(columns={'TB_PREV': 'Previous_QTR_TB_PREV_D'})

        # merge with first genie
        TB_PREV = pd.merge(TB_PREV, TB_PREV_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TB_PREV = TB_PREV.drop(columns='orgunituid')

        if step == 'MER File 1':
            TB_PREV = run_first_mer(TB_PREV, mer_file1)

            # step 2 output
            summary_df = TB_PREV.groupby('OU3name')[
                ['Previous_QTR_TB_PREV_N', 'Previous_QTR_TB_PREV_D', 'MER report 1st submission_TB_PREV_D',
                 'MER report 1st submission_TB_PREV_N']].sum().reset_index()

            total_row = summary_df[
                ['Previous_QTR_TB_PREV_N', 'Previous_QTR_TB_PREV_D', 'MER report 1st submission_TB_PREV_D',
                 'MER report 1st submission_TB_PREV_N']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_PREV, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TB_PREV = run_second_mer(TB_PREV, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TB_PREV_N', 'Previous_QTR_TB_PREV_D',
                            'MER report 1st submission_TB_PREV_D', 'MER report 1st submission_TB_PREV_N',
                            'MER report 2nd submission_TB_PREV_D', 'MER report 2nd submission_TB_PREV_N']

            summary_df = TB_PREV.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_PREV, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TB_PREV = run_tier(TB_PREV, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TB_PREV_N', 'Previous_QTR_TB_PREV_D',
                            'MER report 1st submission_TB_PREV_D', 'MER report 1st submission_TB_PREV_N',
                            'MER report 2nd submission_TB_PREV_D', 'MER report 2nd submission_TB_PREV_N',
                            'Import File_TB_PREV_D', 'Import File_TB_PREV_N']

            summary_df = TB_PREV.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_PREV, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TB_PREV = run_new_genie(TB_PREV, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TB_PREV_N', 'Previous_QTR_TB_PREV_D',
                            'MER report 1st submission_TB_PREV_D', 'MER report 1st submission_TB_PREV_N',
                            'MER report 2nd submission_TB_PREV_D', 'MER report 2nd submission_TB_PREV_N',
                            'Import File_TB_PREV_D', 'Import File_TB_PREV_N',
                            'Genie_TB_PREV_D', 'Genie_TB_PREV_N']

            summary_df = TB_PREV.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TB_PREV, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TB_PREV, mer_file1):
    # kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Numer').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Numer')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_PREV_N'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_PREV = TB_PREV.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_PREV_N'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_PREV[qtr_data_check] = TB_PREV.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    # kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Denom').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Denom')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TB_PREV_D'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_PREV = TB_PREV.drop(columns='UID')

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TB_PREV_D'] > 0:
            return "Data Reported"
        else:
            return "No data reported"

    TB_PREV[qtr_data_check] = TB_PREV.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    TB_PREV['%TPT Completion'] = ((TB_PREV['MER report 1st submission_TB_PREV_N'] / TB_PREV[
        'MER report 1st submission_TB_PREV_D']) * 100).round(0)

    TB_PREV['Level 2 Check: %TPT Completion'] = TB_PREV['%TPT Completion'].apply(
        lambda x: 'Extremely low completion' if x < 79 else ('Good Completion' if x > 90 else ''))

    ordered_cols = [
        'OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
        'Previous_QTR_TB_PREV_D',
        'MER report 1st submission_TB_PREV_D',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D',
        'Previous_QTR_TB_PREV_N',
        'MER report 1st submission_TB_PREV_N',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N',
        '%TPT Completion', 'Level 2 Check: %TPT Completion']
    TB_PREV = TB_PREV[ordered_cols]

    return TB_PREV


def run_second_mer(TB_PREV, mer_file1, mer_file2):
    # run first mer
    TB_PREV = run_first_mer(TB_PREV, mer_file1)

    # kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Numer').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TB_PREV_Numer')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_PREV_N'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_PREV = TB_PREV.drop(columns='UID')

    TB_PREV['MER report 1st submission vs 2nd submission_TB_PREV_N'] = (
                TB_PREV['MER report 1st submission_TB_PREV_N'].eq(TB_PREV['MER report 2nd submission_TB_PREV_N']) | (
                    TB_PREV['MER report 1st submission_TB_PREV_N'].isna() & TB_PREV[
                'MER report 2nd submission_TB_PREV_N'].isna()))
    # kp = pd.read_excel(mer_file1, sheet_name='TB_PREV_Denom').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TB_PREV_Denom')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TB_PREV_D'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, mer, left_on='OU5uid', right_on='UID', how='left')
    TB_PREV = TB_PREV.drop(columns='UID')

    TB_PREV['MER report 1st submission vs 2nd submission_TB_PREV_D'] = (
                TB_PREV['MER report 1st submission_TB_PREV_D'].eq(TB_PREV['MER report 2nd submission_TB_PREV_D']) | (
                    TB_PREV['MER report 1st submission_TB_PREV_D'].isna() & TB_PREV[
                'MER report 2nd submission_TB_PREV_D'].isna()))

    TB_PREV['%TPT Completion'] = TB_PREV['MER report 2nd submission_TB_PREV_N'] / TB_PREV[
        'MER report 2nd submission_TB_PREV_D']

    TB_PREV['Level 2 Check: %TPT Completion'] = TB_PREV['%TPT Completion'].apply(
        lambda x: 'Extremely low completion' if x < 79 else ('Good Completion' if x > 90 else ''))

    ordered_cols = [
        'OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
        'Previous_QTR_TB_PREV_D',
        'MER report 1st submission_TB_PREV_D',
        'MER report 2nd submission_TB_PREV_D',
        'MER report 1st submission vs 2nd submission_TB_PREV_D',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D',
        'Previous_QTR_TB_PREV_N',
        'MER report 1st submission_TB_PREV_N',
        'MER report 2nd submission_TB_PREV_N',
        'MER report 1st submission vs 2nd submission_TB_PREV_N',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N',
        '%TPT Completion', 'Level 2 Check: %TPT Completion']
    TB_PREV = TB_PREV[ordered_cols]

    return TB_PREV


def run_tier(TB_PREV, mer_file1, mer_file2, tier):

    TB_PREV = run_second_mer(TB_PREV, mer_file1, mer_file2)

    TB_PREV_N_tier = tier[tier['dataElement'].str.startswith('TB_PREV (N,')].drop(columns=['period'])

    TB_PREV_N_tier['dataElement'] = TB_PREV_N_tier['dataElement'].apply(
        lambda x: 'TB_PREV' if x.startswith('TB_PREV (N,') else x)

    TB_PREV_N_tier = TB_PREV_N_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                values='value', aggfunc='sum')
    TB_PREV_N_tier = pd.DataFrame(TB_PREV_N_tier).reset_index()

    TB_PREV_N_tier = TB_PREV_N_tier.rename(columns={'TB_PREV': 'Import File_TB_PREV_N'})

    TB_PREV = pd.merge(TB_PREV, TB_PREV_N_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TB_PREV = TB_PREV.drop(columns=['orgUnit_uid'])

    TB_PREV['Support Type Check'] = (TB_PREV['DSD/TA'] == TB_PREV['supportType']) | (
                TB_PREV['supportType'].isna() | (TB_PREV['supportType'] == ''))

    TB_PREV['MER report  2nd submission vs Import File_TB_PREV_N'] = (
                TB_PREV['MER report 2nd submission_TB_PREV_N'].eq(TB_PREV['Import File_TB_PREV_N']) | (
                    TB_PREV['MER report 2nd submission_TB_PREV_N'].isna() & TB_PREV['Import File_TB_PREV_N'].isna()))

    TB_PREV_D_tier = tier[tier['dataElement'].str.startswith('TB_PREV (D,')].drop(columns=['period'])

    TB_PREV_D_tier['dataElement'] = TB_PREV_D_tier['dataElement'].apply(
        lambda x: 'TB_PREV' if x.startswith('TB_PREV (D,') else x)

    TB_PREV_D_tier = TB_PREV_D_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                aggfunc='sum')
    TB_PREV_D_tier = pd.DataFrame(TB_PREV_D_tier).reset_index()

    TB_PREV_D_tier = TB_PREV_D_tier.rename(columns={'TB_PREV': 'Import File_TB_PREV_D'})

    TB_PREV = pd.merge(TB_PREV, TB_PREV_D_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TB_PREV = TB_PREV.drop(columns=['orgUnit_uid'])

    TB_PREV['MER report  2nd submission vs Import File_TB_PREV_D'] = (
                TB_PREV['MER report 2nd submission_TB_PREV_D'].eq(TB_PREV['Import File_TB_PREV_D']) | (
                    TB_PREV['MER report 2nd submission_TB_PREV_D'].isna() & TB_PREV['Import File_TB_PREV_D'].isna()))

    TB_PREV['%TPT Completion'] = TB_PREV['Import File_TB_PREV_N'] / TB_PREV['Import File_TB_PREV_D']

    TB_PREV['Level 2 Check: %TPT Completion'] = TB_PREV['%TPT Completion'].apply(
        lambda x: 'Extremely low completion' if x < 79 else ('Good Completion' if x > 90 else ''))

    ordered_cols = [
        'OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
        'Previous_QTR_TB_PREV_D',
        'MER report 1st submission_TB_PREV_D',
        'MER report 2nd submission_TB_PREV_D',
        'MER report 1st submission vs 2nd submission_TB_PREV_D',
        'Import File_TB_PREV_D',
        'MER report  2nd submission vs Import File_TB_PREV_D',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D',
        'Previous_QTR_TB_PREV_N',
        'MER report 1st submission_TB_PREV_N',
        'MER report 2nd submission_TB_PREV_N',
        'MER report 1st submission vs 2nd submission_TB_PREV_N',
        'Import File_TB_PREV_N',
        'MER report  2nd submission vs Import File_TB_PREV_N',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N',
        '%TPT Completion', 'Level 2 Check: %TPT Completion', 'supportType', 'Support Type Check']
    TB_PREV = TB_PREV[ordered_cols]

    return TB_PREV


def run_new_genie(TB_PREV, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TB_PREV = run_tier(TB_PREV, mer_file1, mer_file2, tier_df)

    TB_PREV_N_genie = second_genie[
        (second_genie['indicator'] == 'TB_PREV') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (second_genie['numeratordenom'] == 'N')]

    TB_PREV_N_genie = TB_PREV_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TB_PREV_N_genie = pd.DataFrame(TB_PREV_N_genie).reset_index()

    TB_PREV_N_genie = TB_PREV_N_genie.rename(columns={'TB_PREV': 'Genie_TB_PREV_N'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, TB_PREV_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TB_PREV = TB_PREV.drop(columns='orgunituid')

    TB_PREV['Import File vs Genie_TB_PREV_N'] = (TB_PREV['Import File_TB_PREV_N'].eq(TB_PREV['Genie_TB_PREV_N']) | (
                TB_PREV['Import File_TB_PREV_N'].isna() & TB_PREV['Genie_TB_PREV_N'].isna()))

    TB_PREV_D_genie = second_genie[
        (second_genie['indicator'] == 'TB_PREV') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (second_genie['numeratordenom'] == 'D')]

    TB_PREV_D_genie = TB_PREV_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TB_PREV_D_genie = pd.DataFrame(TB_PREV_D_genie).reset_index()

    TB_PREV_D_genie = TB_PREV_D_genie.rename(columns={'TB_PREV': 'Genie_TB_PREV_D'})

    # merge with first genie
    TB_PREV = pd.merge(TB_PREV, TB_PREV_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TB_PREV = TB_PREV.drop(columns='orgunituid')

    TB_PREV['Import File vs Genie_TB_PREV_D'] = (TB_PREV['Import File_TB_PREV_D'].eq(TB_PREV['Genie_TB_PREV_D']) | (
                TB_PREV['Import File_TB_PREV_D'].isna() & TB_PREV['Genie_TB_PREV_D'].isna()))

    TB_PREV['%TPT Completion'] = TB_PREV['Genie_TB_PREV_N'] / TB_PREV['Genie_TB_PREV_D']

    TB_PREV['Level 2 Check: %TPT Completion'] = TB_PREV['%TPT Completion'].apply(
        lambda x: 'Extremely low completion' if x < 79 else ('Good Completion' if x > 90 else ''))

    ordered_cols = [
        'OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
        'Previous_QTR_TB_PREV_D',
        'MER report 1st submission_TB_PREV_D',
        'MER report 2nd submission_TB_PREV_D',
        'MER report 1st submission vs 2nd submission_TB_PREV_D',
        'Import File_TB_PREV_D',
        'MER report  2nd submission vs Import File_TB_PREV_D',
        'Genie_TB_PREV_D',
        'Import File vs Genie_TB_PREV_D',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_D',
        'Previous_QTR_TB_PREV_N',
        'MER report 1st submission_TB_PREV_N',
        'MER report 2nd submission_TB_PREV_N',
        'MER report 1st submission vs 2nd submission_TB_PREV_N',
        'Import File_TB_PREV_N',
        'MER report  2nd submission vs Import File_TB_PREV_N',
        'Genie_TB_PREV_N',
        'Import File vs Genie_TB_PREV_N',
        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TB_PREV_N',
        '%TPT Completion', 'Level 2 Check: %TPT Completion']

    TB_PREV = TB_PREV[ordered_cols]

    return TB_PREV
