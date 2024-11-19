from datetime import datetime
import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_PVLS'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_PVLS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_PVLS, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_PVLS, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_PVLS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_PVLS[TX_PVLS[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_D'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_PVLS_D', index=False)

        level_1_check_df = TX_PVLS[TX_PVLS[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_N'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_PVLS_N', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_PVLS (N) > TX_PVLS (D)', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_CURR < TX_PVLS (D)', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_PVLS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_PVLS[TX_PVLS['MER report 1st submission vs 2nd submission_TX_PVLS_D'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_PVLS_D', index=False)

        mer1_vs_mer2 = TX_PVLS[TX_PVLS['MER report 1st submission vs 2nd submission_TX_PVLS_N'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TB_PVLS_N', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_PVLS (N) > TX_PVLS (D)', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_CURR < TX_PVLS (D)', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_PVLS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_mer2 = TX_PVLS[TX_PVLS['MER report 2nd submission vs Import File_TX_PVLS_D'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_PVLS_D', index=False)

        Import_vs_mer2 = TX_PVLS[TX_PVLS['MER report 2nd submission vs Import File_TX_PVLS_D'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TB_PVLS_N', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_PVLS (N) > TX_PVLS (D)', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_CURR < TX_PVLS (D)', index=False)

        support_typecheck = TX_PVLS[TX_PVLS['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_PVLS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_Genie = TX_PVLS[TX_PVLS['Import File vs Genie_TX_PVLS_D'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_TB_PVLS_D', index=False)

        Import_vs_Genie = TX_PVLS[TX_PVLS['Import File vs Genie_TX_PVLS_N'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_TB_PVLS_N', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_PVLS (N) > TX_PVLS (D)', index=False)

        level_2_check_df = TX_PVLS[TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] == True]
        level_2_check_df.to_excel(writer, sheet_name='TX_CURR < TX_PVLS (D)', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_pvls_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        current_year = datetime.now().year
        # Define the range of years for the dropdown
        year_options = list(range(2024 - 3, current_year + 1))

        # Create a selector for six_months_ago_yr
        six_months_ago_yr = st.selectbox('Select the year for six months ago TX_CURR:', options=year_options)

        # Define possible quarters
        quarters = ['qtr1', 'qtr2', 'qtr3', 'qtr4']

        # Create a selector for six_months_ago_tx_curr_qtr
        six_months_ago_tx_curr_qtr = st.selectbox('Select the quarter for six months ago TX_CURR:', options=quarters)

        # TX_CURR
        TX_CURR_genie = first_genie[
            (first_genie['indicator'] == 'TX_CURR') & (first_genie['fiscal_year'] == six_months_ago_yr) & (
                        first_genie['source_name'] == 'DATIM')]

        TX_CURR_genie = TX_CURR_genie.pivot_table(index='orgunituid', columns='indicator',
                                                  values=six_months_ago_tx_curr_qtr, aggfunc='sum')
        TX_CURR_genie = pd.DataFrame(TX_CURR_genie).reset_index()

        TX_CURR_genie = TX_CURR_genie.rename(columns={'TX_CURR': 'Previous_QTR_TX_CURR'})

        TX_PVLS = pd.merge(mfl, TX_CURR_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_PVLS = TX_PVLS.drop(columns='orgunituid')

        # merge with first genie
        TX_PVLS['Previous_QTR_TX_CURR'].sum()

        # TX_PVLS_D
        TX_PVLS_D_genie = first_genie[
            (first_genie['numeratordenom'] == 'D') & (first_genie['indicator'] == 'TX_PVLS') & (
                        first_genie['fiscal_year'] == fiscal_year_1stG) & (first_genie['source_name'] == 'DATIM')]
        TX_PVLS_D_genie = TX_PVLS_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TX_PVLS_D_genie = pd.DataFrame(TX_PVLS_D_genie).reset_index()

        TX_PVLS_D_genie = TX_PVLS_D_genie.rename(columns={'TX_PVLS': 'Previous_QTR_TX_PVLS_D'})

        # merge with first genie
        TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_PVLS = TX_PVLS.drop(columns='orgunituid')

        # TX_PVLS_N
        TX_PVLS_N_genie = first_genie[
            (first_genie['numeratordenom'] == 'N') & (first_genie['indicator'] == 'TX_PVLS') & (
                        first_genie['fiscal_year'] == fiscal_year_1stG) & (first_genie['source_name'] == 'DATIM')]
        TX_PVLS_N_genie = TX_PVLS_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        TX_PVLS_N_genie = pd.DataFrame(TX_PVLS_N_genie).reset_index()

        TX_PVLS_N_genie = TX_PVLS_N_genie.rename(columns={'TX_PVLS': 'Previous_QTR_TX_PVLS_N'})

        # merge with first genie
        TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_PVLS = TX_PVLS.drop(columns='orgunituid')

        if step == 'MER File 1':
            TX_PVLS = run_first_mer(TX_PVLS, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_CURR', 'Previous_QTR_TX_PVLS_D', 'Previous_QTR_TX_PVLS_N',
                            'MER report 1st submission_TX_PVLS_D', 'MER report 1st submission_TX_PVLS_N']

            summary_df = TX_PVLS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_PVLS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TX_PVLS = run_second_mer(TX_PVLS, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TX_CURR', 'Previous_QTR_TX_PVLS_D', 'Previous_QTR_TX_PVLS_N',
                            'MER report 1st submission_TX_PVLS_D', 'MER report 1st submission_TX_PVLS_N',
                            'MER report 2nd submission_TX_PVLS_D', 'MER report 2nd submission_TX_PVLS_N']

            summary_df = TX_PVLS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_PVLS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TX_PVLS = run_tier(TX_PVLS, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TX_CURR', 'Previous_QTR_TX_PVLS_D', 'Previous_QTR_TX_PVLS_N',
                            'MER report 1st submission_TX_PVLS_D', 'MER report 1st submission_TX_PVLS_N',
                            'MER report 2nd submission_TX_PVLS_D', 'MER report 2nd submission_TX_PVLS_N',
                            'Import File_TX_PVLS_D', 'Import File_TX_PVLS_N']

            summary_df = TX_PVLS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_PVLS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TX_PVLS = run_new_genie(TX_PVLS, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TX_CURR', 'Previous_QTR_TX_PVLS_D', 'Previous_QTR_TX_PVLS_N',
                            'MER report 1st submission_TX_PVLS_D', 'MER report 1st submission_TX_PVLS_N',
                            'MER report 2nd submission_TX_PVLS_D', 'MER report 2nd submission_TX_PVLS_N',
                            'Import File_TX_PVLS_D', 'Import File_TX_PVLS_N',
                            'Genie_TX_PVLS_N', 'Genie_TX_PVLS_D']

            summary_df = TX_PVLS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_PVLS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TX_PVLS, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Denom_KP').drop(columns=['KP_Type', 'KP_Location'])

    non_kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Denom')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_PVLS_D'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_PVLS = TX_PVLS.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Numer_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Numer')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_PVLS_N'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_PVLS = TX_PVLS.drop(columns='UID')

    # Track Second Submission: TX_PVLS_D
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_D'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_PVLS_D'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_PVLS[qtr_data_check] = TX_PVLS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    # Track Second Submission: TX_PVLS_N
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_N'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_PVLS_N'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_PVLS[qtr_data_check] = TX_PVLS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] = TX_PVLS['MER report 1st submission_TX_PVLS_N'] > TX_PVLS[
        'MER report 1st submission_TX_PVLS_D']

    TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] = TX_PVLS['Previous_QTR_TX_CURR'] < TX_PVLS[
        'MER report 1st submission_TX_PVLS_D']

    TX_PVLS['% VL Coverage'] = (
                (TX_PVLS['MER report 1st submission_TX_PVLS_D'] / TX_PVLS['Previous_QTR_TX_CURR']) * 100).round(0)

    TX_PVLS['Level 2 Check: %VL Coverage <65%, "Extremenly low coverage"'] = TX_PVLS['% VL Coverage'].apply(
        lambda x: 'Extremely low VLC' if x < 64 else ('Good VLC' if x > 90 else ''))

    TX_PVLS['% VL Suppression'] = ((TX_PVLS['MER report 1st submission_TX_PVLS_N'] / TX_PVLS[
        'MER report 1st submission_TX_PVLS_D']) * 100).round(0)

    TX_PVLS['Level 2 Check: %VL Suppression <80%, Extremenly low VLS'] = TX_PVLS['% VL Suppression'].apply(
        lambda x: 'Extremely low VLS' if x < 79 else ('Good VLS' if x > 90 else ''))

    return TX_PVLS


def run_second_mer(TX_PVLS, mer_file1, mer_file2):
    # run first mer
    TX_PVLS = run_first_mer(TX_PVLS, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Denom_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Denom')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_PVLS_D'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_PVLS = TX_PVLS.drop(columns='UID')

    kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Numer_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Numer')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_PVLS_N'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_PVLS = TX_PVLS.drop(columns='UID')

    TX_PVLS['MER report 1st submission vs 2nd submission_TX_PVLS_D'] = (
                TX_PVLS['MER report 1st submission_TX_PVLS_D'].eq(TX_PVLS['MER report 2nd submission_TX_PVLS_D']) | (
                    TX_PVLS['MER report 1st submission_TX_PVLS_D'].isna() & TX_PVLS[
                'MER report 2nd submission_TX_PVLS_D'].isna()))

    TX_PVLS['MER report 1st submission vs 2nd submission_TX_PVLS_N'] = (
                TX_PVLS['MER report 1st submission_TX_PVLS_N'].eq(TX_PVLS['MER report 2nd submission_TX_PVLS_N']) | (
                    TX_PVLS['MER report 1st submission_TX_PVLS_N'].isna() & TX_PVLS[
                'MER report 2nd submission_TX_PVLS_N'].isna()))
    TX_PVLS['Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)'] = TX_PVLS['MER report 2nd submission_TX_PVLS_N'] > TX_PVLS[
        'MER report 2nd submission_TX_PVLS_D']

    TX_PVLS['Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)'] = TX_PVLS['Previous_QTR_TX_CURR'] < TX_PVLS[
        'MER report 2nd submission_TX_PVLS_D']

    TX_PVLS['% VL Coverage'] = (TX_PVLS['MER report 2nd submission_TX_PVLS_D'] / TX_PVLS['Previous_QTR_TX_CURR']) * 100

    TX_PVLS['Level 2 Check: %VL Coverage <65%, "Extremenly low coverage"'] = TX_PVLS['% VL Coverage'].apply(
        lambda x: 'Extremely low VLC' if x < 64 else ('Good VLC' if x > 90 else ''))

    TX_PVLS['% VL Suppression'] = (TX_PVLS['MER report 2nd submission_TX_PVLS_N'] / TX_PVLS[
        'MER report 2nd submission_TX_PVLS_D']) * 100

    TX_PVLS['Level 2 Check: %VL Suppression <80%, Extremenly low VLS'] = TX_PVLS['% VL Suppression'].apply(
        lambda x: 'Extremely low VLS' if x < 79 else ('Good VLS' if x > 90 else ''))

    return TX_PVLS


def run_tier(TX_PVLS, mer_file1, mer_file2, tier):
    # run the second mer
    TX_PVLS = run_second_mer(TX_PVLS, mer_file1, mer_file2)

    TX_PVLS_D_tier = tier[tier['dataElement'].str.startswith('TX_PVLS (D')]

    TX_PVLS_D_tier['dataElement'] = TX_PVLS_D_tier['dataElement'].apply(
        lambda x: 'TX_PVLS_D' if x.startswith('TX_PVLS') else x)

    TX_PVLS_D_tier = TX_PVLS_D_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                values='value', aggfunc='sum')

    TX_PVLS_D_tier = pd.DataFrame(TX_PVLS_D_tier).reset_index()

    TX_PVLS_D_tier = TX_PVLS_D_tier.rename(columns={'TX_PVLS_D': 'Import File_TX_PVLS_D'})

    TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_D_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_PVLS = TX_PVLS.drop(columns=['orgUnit_uid'])

    TX_PVLS_N_tier = tier[tier['dataElement'].str.startswith('TX_PVLS (N')]

    TX_PVLS_N_tier['dataElement'] = TX_PVLS_N_tier['dataElement'].apply(
        lambda x: 'TX_PVLS_N' if x.startswith('TX_PVLS') else x)

    TX_PVLS_N_tier = TX_PVLS_N_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                aggfunc='sum')

    TX_PVLS_N_tier = pd.DataFrame(TX_PVLS_N_tier).reset_index()

    TX_PVLS_N_tier = TX_PVLS_N_tier.rename(columns={'TX_PVLS_N': 'Import File_TX_PVLS_N'})

    TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_N_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_PVLS = TX_PVLS.drop(columns=['orgUnit_uid'])

    TX_PVLS['MER report 2nd submission vs Import File_TX_PVLS_D'] = (
                TX_PVLS['MER report 2nd submission_TX_PVLS_D'].eq(TX_PVLS['Import File_TX_PVLS_D']) | (
                    TX_PVLS['MER report 2nd submission_TX_PVLS_D'].isna() & TX_PVLS['Import File_TX_PVLS_D'].isna()))
    TX_PVLS['MER report 2nd submission vs Import File_TX_PVLS_N'] = (
                TX_PVLS['MER report 2nd submission_TX_PVLS_N'].eq(TX_PVLS['Import File_TX_PVLS_N']) | (
                    TX_PVLS['MER report 2nd submission_TX_PVLS_N'].isna() & TX_PVLS['Import File_TX_PVLS_N'].isna()))

    TX_PVLS['Support Type Check'] = (TX_PVLS['DSD/TA'] == TX_PVLS['supportType']) | (
                TX_PVLS['supportType'].isna() | (TX_PVLS['supportType'] == ''))

    return TX_PVLS


def run_new_genie(TX_PVLS, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TX_PVLS = run_tier(TX_PVLS, mer_file1, mer_file2, tier_df)

    # TX_PVLS_D
    TX_PVLS_D_genie = second_genie[
        (second_genie['numeratordenom'] == 'D') & (second_genie['indicator'] == 'TX_PVLS') & (
                    second_genie['fiscal_year'] == fiscal_year_2ndG) & (second_genie['source_name'] == 'DATIM')]
    TX_PVLS_D_genie = TX_PVLS_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TX_PVLS_D_genie = pd.DataFrame(TX_PVLS_D_genie).reset_index()

    TX_PVLS_D_genie = TX_PVLS_D_genie.rename(columns={'TX_PVLS': 'Genie_TX_PVLS_D'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_PVLS = TX_PVLS.drop(columns='orgunituid')

    # TX_PVLS_N
    TX_PVLS_N_genie = second_genie[
        (second_genie['numeratordenom'] == 'N') & (second_genie['indicator'] == 'TX_PVLS') & (
                    second_genie['fiscal_year'] == fiscal_year_2ndG) & (second_genie['source_name'] == 'DATIM')]

    TX_PVLS_N_genie = TX_PVLS_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    TX_PVLS_N_genie = pd.DataFrame(TX_PVLS_N_genie).reset_index()

    TX_PVLS_N_genie = TX_PVLS_N_genie.rename(columns={'TX_PVLS': 'Genie_TX_PVLS_N'})

    # merge with first genie
    TX_PVLS = pd.merge(TX_PVLS, TX_PVLS_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_PVLS = TX_PVLS.drop(columns='orgunituid')

    TX_PVLS['Import File vs Genie_TX_PVLS_D'] = (TX_PVLS['Import File_TX_PVLS_D'].eq(TX_PVLS['Genie_TX_PVLS_D']) | (
                TX_PVLS['Import File_TX_PVLS_D'].isna() & TX_PVLS['Genie_TX_PVLS_D'].isna()))
    TX_PVLS['Import File vs Genie_TX_PVLS_N'] = (TX_PVLS['Import File_TX_PVLS_N'].eq(TX_PVLS['Genie_TX_PVLS_N']) | (
                TX_PVLS['Import File_TX_PVLS_N'].isna() & TX_PVLS['Genie_TX_PVLS_N'].isna()))

    ordered_cols = ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
                    'Previous_QTR_TX_CURR',
                    'Previous_QTR_TX_PVLS_D',
                    'MER report 1st submission_TX_PVLS_D',
                    'MER report 2nd submission_TX_PVLS_D',
                    'MER report 1st submission vs 2nd submission_TX_PVLS_D',
                    'Import File_TX_PVLS_D',
                    'MER report 2nd submission vs Import File_TX_PVLS_D',
                    'Genie_TX_PVLS_D',
                    'Import File vs Genie_TX_PVLS_D',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_D',
                    'Previous_QTR_TX_PVLS_N',
                    'MER report 1st submission_TX_PVLS_N',
                    'MER report 2nd submission_TX_PVLS_N',
                    'MER report 1st submission vs 2nd submission_TX_PVLS_N',
                    'Import File_TX_PVLS_N',
                    'MER report 2nd submission vs Import File_TX_PVLS_N',
                    'Genie_TX_PVLS_N',
                    'Import File vs Genie_TX_PVLS_N',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_PVLS_N',
                    'Level 2 Check:  TX_PVLS (N) > TX_PVLS (D)',
                    'Level 2 Check: TX_CURR 2 quarter ago < TX_PVLS (D)', '% VL Coverage',
                    'Level 2 Check: %VL Coverage <65%, "Extremenly low coverage"',
                    '% VL Suppression',
                    'Level 2 Check: %VL Suppression <80%, Extremenly low VLS'
                    ]
    TX_PVLS = TX_PVLS[ordered_cols]

    return TX_PVLS
