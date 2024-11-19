import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_RTT'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_RTT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_RTT, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_RTT, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_RTT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_RTT[TX_RTT[
                                      'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_RTT'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_RTT', index=False)

        level_2_check_df = TX_RTT[TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 Check TX_RTT > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_RTT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_RTT[TX_RTT['MER report 1st submission vs 2nd submission_TX_RTT'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TX_RTT', index=False)

        level_2_check_df = TX_RTT[TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 Check TX_RTT > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_RTT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = TX_RTT[TX_RTT['MER report  2nd submission vs Import File_TX_RTT'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TX_RTT', index=False)

        level_2_check_df = TX_RTT[TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 Check TX_RTT > TX_CURR', index=False)

        support_typecheck = TX_RTT[TX_RTT['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_RTT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = TX_RTT[TX_RTT['Import File vs Genie_TX_RTT'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_TX_RTT', index=False)

        level_2_check_df = TX_RTT[TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 Check TX_RTT > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_rtt_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        TX_RTT_genie = first_genie[
            (first_genie['indicator'] == 'TX_RTT') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'DATIM')]

        # remove these rows for rtt in categoryoptioncomboname
        rtt_out_rows = ['No Contact Outcome - Interruption in Treatment (<3 Months Interruption), Positive',
                        'No Contact Outcome - Interruption In Treatment (6+ Months Interruption), Positive',
                        'No Contact Outcome - Interruption in Treatment (3-5 Months Interruption), Positive', 'default']
        TX_RTT_genie = TX_RTT_genie[~TX_RTT_genie['categoryoptioncomboname'].isin(rtt_out_rows)]

        TX_RTT_genie = TX_RTT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                aggfunc='sum')
        TX_RTT_genie = pd.DataFrame(TX_RTT_genie).reset_index()
        TX_RTT_genie = TX_RTT_genie.rename(columns={'TX_RTT': 'Previous_QTR_TX_RTT'})

        # merge with first genie
        TX_RTT = pd.merge(mfl, TX_RTT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_RTT = TX_RTT.drop(columns='orgunituid')

        if step == 'MER File 1':
            TX_RTT = run_first_mer(TX_RTT, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_RTT', 'MER report 1st submission_TX_RTT']

            summary_df = TX_RTT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_RTT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TX_RTT = run_second_mer(TX_RTT, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TX_RTT', 'MER report 1st submission_TX_RTT',
                            'MER report 2nd submission_TX_RTT']

            summary_df = TX_RTT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_RTT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TX_RTT = run_tier(TX_RTT, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TX_RTT', 'MER report 1st submission_TX_RTT',
                            'MER report 2nd submission_TX_RTT', 'Import File_TX_RTT']

            summary_df = TX_RTT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_RTT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TX_RTT = run_new_genie(TX_RTT, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TX_RTT', 'MER report 1st submission_TX_RTT',
                            'MER report 2nd submission_TX_RTT', 'Import File_TX_RTT', 'Genie_TX_RTT']

            summary_df = TX_RTT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_RTT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TX_RTT, mer_file1):
    # kp = pd.read_excel(mer_file1, sheet_name='TX_RTT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_RTT')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_RTT'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_RTT = TX_RTT.drop(columns='UID')

    # Track Second Submission: TX_RTT
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_RTT'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_RTT'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_RTT[qtr_data_check] = TX_RTT.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    kp = pd.read_excel(mer_file1, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_CURR')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_CURR'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_RTT = TX_RTT.drop(columns='UID')

    TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] = TX_RTT['Previous_QTR_TX_RTT'] > TX_RTT[
        'MER report 1st submission_TX_CURR']

    return TX_RTT


def run_second_mer(TX_RTT, mer_file1, mer_file2):
    # run first mer
    TX_RTT = run_first_mer(TX_RTT, mer_file1)

    # kp = pd.read_excel(mer_file2, sheet_name='TX_RTT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_RTT')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_RTT'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_RTT = TX_RTT.drop(columns='UID')

    TX_RTT['MER report 1st submission vs 2nd submission_TX_RTT'] = (
            TX_RTT['MER report 1st submission_TX_RTT'].eq(TX_RTT['MER report 2nd submission_TX_RTT']) | (
            TX_RTT['MER report 1st submission_TX_RTT'].isna() & TX_RTT[
        'MER report 2nd submission_TX_RTT'].isna()))

    kp = pd.read_excel(mer_file2, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_CURR')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_CURR'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_RTT = TX_RTT.drop(columns='UID')

    TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] = TX_RTT['Previous_QTR_TX_RTT'] > TX_RTT[
        'MER report 2nd submission_TX_CURR']

    return TX_RTT


def run_tier(TX_RTT, mer_file1, mer_file2, tier):
    # run the second mer
    TX_RTT = run_second_mer(TX_RTT, mer_file1, mer_file2)

    tx_rtt_tier = tier[tier['dataElement'].isin(['TX_RTT (N, DSD, ARTNoContactReasonIIT/HIVStatus): Restarted ARV',
                                                 'TX_RTT (N, TA, ARTNoContactReasonIIT/HIVStatus): Restarted ARV'])]

    tx_rtt_tier['dataElement'] = tx_rtt_tier['dataElement'].apply(lambda x: 'TX_RTT' if x.startswith('TX_RTT') else x)

    TX_RTT_tier = tx_rtt_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                          aggfunc='sum')
    TX_RTT_tier = pd.DataFrame(TX_RTT_tier).reset_index()

    TX_RTT_tier = TX_RTT_tier.rename(columns={'TX_RTT': 'Import File_TX_RTT'})

    TX_RTT = pd.merge(TX_RTT, TX_RTT_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_RTT = TX_RTT.drop(columns=['orgUnit_uid'])

    TX_CURR_tier = tier[tier['dataElement'].str.startswith('TX_CURR')]

    TX_CURR_tier['dataElement'] = TX_CURR_tier['dataElement'].apply(
        lambda x: 'TX_CURR' if x.startswith('TX_CURR') else x)

    TX_CURR_tier = TX_CURR_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')

    TX_CURR_tier = pd.DataFrame(TX_CURR_tier).reset_index()

    TX_CURR_tier = TX_CURR_tier.rename(columns={'TX_CURR': 'Import File_TX_CURR'})

    TX_RTT = pd.merge(TX_RTT, TX_CURR_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_RTT = TX_RTT.drop(columns=['orgUnit_uid'])

    TX_RTT['MER report  2nd submission vs Import File_TX_RTT'] = (
            TX_RTT['MER report 2nd submission_TX_RTT'].eq(TX_RTT['Import File_TX_RTT']) | (
            TX_RTT['MER report 2nd submission_TX_RTT'].isna() & TX_RTT['Import File_TX_RTT'].isna()))

    TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] = TX_RTT['Import File_TX_RTT'] > TX_RTT['Import File_TX_CURR']

    TX_RTT['Support Type Check'] = (TX_RTT['DSD/TA'] == TX_RTT['supportType']) | (
            TX_RTT['supportType'].isna() | (TX_RTT['supportType'] == ''))

    return TX_RTT


def run_new_genie(TX_RTT, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TX_RTT = run_tier(TX_RTT, mer_file1, mer_file2, tier_df)

    # remove these rows for rtt in categoryoptioncomboname
    rtt_out_rows = ['No Contact Outcome - Interruption in Treatment (<3 Months Interruption), Positive',
                    'No Contact Outcome - Interruption In Treatment (6+ Months Interruption), Positive',
                    'No Contact Outcome - Interruption in Treatment (3-5 Months Interruption), Positive', 'default']

    TX_RTT_genie = second_genie[
        (second_genie['indicator'] == 'TX_RTT') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'DATIM')]
    TX_RTT_genie = TX_RTT_genie[~TX_RTT_genie['categoryoptioncomboname'].isin(rtt_out_rows)]
    TX_RTT_genie = TX_RTT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                            aggfunc='sum').reset_index()

    TX_RTT_genie = TX_RTT_genie.rename(columns={'TX_RTT': 'Genie_TX_RTT'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, TX_RTT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_RTT = TX_RTT.drop(columns='orgunituid')

    TX_CURR_genie = second_genie[
        (second_genie['indicator'] == 'TX_CURR') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'DATIM')]
    TX_CURR_genie = TX_CURR_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum').reset_index()

    TX_CURR_genie = TX_CURR_genie.rename(columns={'TX_CURR': 'Genie_TX_CURR'})

    # merge with first genie
    TX_RTT = pd.merge(TX_RTT, TX_CURR_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_RTT = TX_RTT.drop(columns='orgunituid')

    TX_RTT['Import File vs Genie_TX_RTT'] = (TX_RTT['Import File_TX_RTT'].eq(TX_RTT['Genie_TX_RTT']) | (
            TX_RTT['Import File_TX_RTT'].isna() & TX_RTT['Genie_TX_RTT'].isna()))

    TX_RTT['Level 2 Check: TX_RTT > TX_CURR'] = TX_RTT['Genie_TX_RTT'] > TX_RTT['Genie_TX_CURR']

    return TX_RTT
