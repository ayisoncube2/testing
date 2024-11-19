import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_CURR'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_CURR, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_CURR, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_CURR[TX_CURR[
                                       'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_CURR'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_CURR', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_CURR < TX_NEW'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_CURR < TX_NEW', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_ML > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_ML > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_CURR[TX_CURR['MER report 1st submission vs 2nd submission_TX_CURR'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TX_CURR', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_CURR < TX_NEW'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_CURR < TX_NEW', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_ML > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_ML > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = TX_CURR[TX_CURR['MER report 2nd submission vs Import File_TX_CURR'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TX_CURR', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_CURR < TX_NEW'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_CURR < TX_NEW', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_ML > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_ML > TX_CURR', index=False)

        support_typecheck = TX_CURR[TX_CURR['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_CURR.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = TX_CURR[TX_CURR['Import File vs Genie_TX_CURR'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_TX_CURR', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_CURR < TX_NEW'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_CURR < TX_NEW', index=False)

        level_2_check_df = TX_CURR[TX_CURR['Level 2: TX_ML > TX_CURR'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 TX_ML > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_curr_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        TX_CURR_genie = first_genie[
            (first_genie['indicator'] == 'TX_CURR') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]
        TX_CURR_genie = TX_CURR_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                  aggfunc='sum')
        TX_CURR_genie = pd.DataFrame(TX_CURR_genie).reset_index()
        TX_CURR_genie = TX_CURR_genie.rename(columns={'TX_CURR': 'Previous_QTR_TX_CURR'})

        # merge with first genie
        TX_CURR = pd.merge(mfl, TX_CURR_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_CURR = TX_CURR.drop(columns='orgunituid')

        if step == 'MER File 1':
            TX_CURR = run_first_mer(TX_CURR, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_CURR', 'MER report 1st submission_TX_CURR']

            summary_df = TX_CURR.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TX_CURR = run_second_mer(TX_CURR, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TX_CURR', 'MER report 1st submission_TX_CURR',
                            'MER report 2nd submission_TX_CURR']

            summary_df = TX_CURR.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TX_CURR = run_tier(TX_CURR, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TX_CURR', 'MER report 1st submission_TX_CURR',
                            'MER report 2nd submission_TX_CURR', 'Import File_TX_CURR']

            summary_df = TX_CURR.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TX_CURR = run_new_genie(TX_CURR, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TX_CURR', 'MER report 1st submission_TX_CURR',
                            'MER report 2nd submission_TX_CURR',
                            'Import File_TX_CURR', 'Genie_TX_CURR']

            summary_df = TX_CURR.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_CURR, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TX_CURR, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_CURR')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_CURR'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    # Track Second Submission: TX_CURR
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_CURR'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_CURR'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_CURR[qtr_data_check] = TX_CURR.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    kp = pd.read_excel(mer_file1, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_NEW'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

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
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='TX_ML_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_ML')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_ML'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    TX_CURR['MER Report 1st Submission TX_NET_NEW'] = TX_CURR['MER report 1st submission_TX_CURR'] - TX_CURR[
        'Previous_QTR_TX_CURR']

    TX_CURR['MER Report 1st Submission TX_NET_NEW % Variance'] = ((TX_CURR['MER report 1st submission_TX_CURR'] -
                                                                   TX_CURR['Previous_QTR_TX_CURR']) / TX_CURR[
                                                                      'MER report 1st submission_TX_CURR']) * 100

    TX_CURR['MER Report 1st Submission TX_NET_NEW % Variance'] = TX_CURR[
        'MER Report 1st Submission TX_NET_NEW % Variance'].round(2)

    TX_CURR['MER Report 1st Submission Proxy Retention'] = ((TX_CURR['MER Report 1st Submission TX_NET_NEW'] / TX_CURR[
        'MER report 1st submission_TX_NEW']).round(2)) * 100

    TX_CURR['Level 2: TX_CURR < TX_NEW'] = TX_CURR['MER report 1st submission_TX_CURR'] < TX_CURR[
        'MER report 1st submission_TX_NEW']

    TX_CURR['Level 2: TX_ML > TX_CURR'] = TX_CURR['MER report 1st submission_TX_ML'] > TX_CURR[
        'MER report 1st submission_TX_CURR']

    cols_to_add = [
        'TX_CURR 90',
        'Level 2: MER Report > TX_CURR 90',
        'Daily TX_CURR',
        'Daily TX_CURR vs MER Report 1st Submission',
        'Daily TX_CURR vs MER Report 1st Submission comment',
        'Daily TX_CURR vs MER Report 2nd Submission',
        'Daily TX_CURR vs MER Report 2nd Submission comment'
    ]

    for col_name in cols_to_add:
        TX_CURR[col_name] = None

    TX_CURR["Calculated proxy TX_CURR"] = TX_CURR['Previous_QTR_TX_CURR'] + TX_CURR[
        'MER report 1st submission_TX_NEW'] + TX_CURR['MER report 1st submission_TX_RTT'] - TX_CURR[
                                              'MER report 1st submission_TX_ML']

    return TX_CURR


def run_second_mer(TX_CURR, mer_file1, mer_file2):
    # Run mer 1 step
    TX_CURR = run_first_mer(TX_CURR, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_CURR')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_CURR'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    TX_CURR['MER report 1st submission vs 2nd submission_TX_CURR'] = (
                TX_CURR['MER report 1st submission_TX_CURR'].eq(TX_CURR['MER report 2nd submission_TX_CURR']) | (
                    TX_CURR['MER report 1st submission_TX_CURR'].isna() & TX_CURR[
                'MER report 2nd submission_TX_CURR'].isna()))

    kp = pd.read_excel(mer_file1, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_NEW'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    TX_CURR['MER Report 2nd Submission TX_NET_NEW'] = TX_CURR['MER report 2nd submission_TX_CURR'] - TX_CURR[
        'Previous_QTR_TX_CURR']

    TX_CURR['MER Report 2nd Submission TX_NET_NEW % Variance'] = ((TX_CURR['MER report 2nd submission_TX_CURR'] -
                                                                   TX_CURR['Previous_QTR_TX_CURR']) / TX_CURR[
                                                                      'MER report 2nd submission_TX_CURR']) * 100

    TX_CURR['MER Report 2nd Submission TX_NET_NEW % Variance'] = TX_CURR[
        'MER Report 2nd Submission TX_NET_NEW % Variance'].round(2)

    TX_CURR['MER Report 2nd Submission Proxy Retention'] = (
                TX_CURR['MER Report 2nd Submission TX_NET_NEW'] / TX_CURR['MER report 2nd submission_TX_NEW']).round(2)

    TX_CURR['Level 2: TX_CURR < TX_NEW'] = TX_CURR['MER report 2nd submission_TX_CURR'] < TX_CURR[
        'MER report 2nd submission_TX_NEW']

    # kp = pd.read_excel(mer_file1, sheet_name='TX_RTT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_RTT')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_RTT'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='TX_ML_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_ML')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_ML'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_CURR = TX_CURR.drop(columns='UID')

    TX_CURR['Level 2: TX_ML > TX_CURR'] = TX_CURR['MER report 2nd submission_TX_ML'] > TX_CURR[
        'MER report 2nd submission_TX_CURR']

    TX_CURR["Calculated proxy TX_CURR"] = TX_CURR['Previous_QTR_TX_CURR'] + TX_CURR[
        'MER report 2nd submission_TX_NEW'] + TX_CURR['MER report 2nd submission_TX_RTT'] - TX_CURR[
                                              'MER report 2nd submission_TX_ML']

    return TX_CURR


def run_tier(TX_CURR, mer_file1, mer_file2, tier):
    # run the second mer
    TX_CURR = run_second_mer(TX_CURR, mer_file1, mer_file2)

    tx_curr_tier = tier[tier['dataElement'].str.startswith('TX_CURR')]

    tx_curr_tier['dataElement'] = tx_curr_tier['dataElement'].apply(
        lambda x: 'TX_CURR' if x.startswith('TX_CURR') else x)

    TX_CURR_tier = tx_curr_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                            aggfunc='sum')
    TX_CURR_tier = pd.DataFrame(TX_CURR_tier).reset_index()

    TX_CURR_tier = TX_CURR_tier.rename(columns={'TX_CURR': 'Import File_TX_CURR'})

    TX_CURR = pd.merge(TX_CURR, TX_CURR_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_CURR = TX_CURR.drop(columns=['orgUnit_uid'])

    TX_CURR['Support Type Check'] = (TX_CURR['DSD/TA'] == TX_CURR['supportType']) | (
                TX_CURR['supportType'].isna() | (TX_CURR['supportType'] == ''))

    TX_CURR['MER report 2nd submission vs Import File_TX_CURR'] = (
                TX_CURR['MER report 2nd submission_TX_CURR'].eq(TX_CURR['Import File_TX_CURR']) | (
                    TX_CURR['MER report 2nd submission_TX_CURR'].isna() & TX_CURR['Import File_TX_CURR'].isna()))

    tx_new_tier = tier[tier['dataElement'].str.startswith('TX_NEW')]

    tx_new_tier['dataElement'] = tx_new_tier['dataElement'].apply(lambda x: 'TX_NEW' if x.startswith('TX_NEW') else x)

    TX_NEW_tier = tx_new_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    TX_NEW_tier = pd.DataFrame(TX_NEW_tier).reset_index()

    TX_NEW_tier = TX_NEW_tier.rename(columns={'TX_NEW': 'Import File_TX_NEW'})

    TX_CURR = pd.merge(TX_CURR, TX_NEW_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_CURR = TX_CURR.drop(columns=['orgUnit_uid'])

    tx_rtt_tier = tier[tier['dataElement'].isin(['TX_RTT (N, DSD, ARTNoContactReasonIIT/HIVStatus): Restarted ARV',
                                                 'TX_RTT (N, TA, ARTNoContactReasonIIT/HIVStatus): Restarted ARV'])]

    tx_rtt_tier['dataElement'] = tx_rtt_tier['dataElement'].apply(lambda x: 'TX_RTT' if x.startswith('TX_RTT') else x)

    TX_RTT_tier = tx_rtt_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    TX_RTT_tier = pd.DataFrame(TX_RTT_tier).reset_index()

    TX_RTT_tier = TX_RTT_tier.rename(columns={'TX_RTT': 'Import File_TX_RTT'})

    TX_CURR = pd.merge(TX_CURR, TX_RTT_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_CURR = TX_CURR.drop(columns=['orgUnit_uid'])

    TX_ML_tier = tier[tier['dataElement'].str.startswith('TX_ML')]

    TX_ML_tier['dataElement'] = TX_ML_tier['dataElement'].apply(lambda x: 'TX_ML' if x.startswith('TX_ML') else x)

    TX_ML_tier = TX_ML_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    TX_ML_tier = pd.DataFrame(TX_ML_tier).reset_index()

    TX_ML_tier = TX_ML_tier.rename(columns={'TX_ML': 'Import File_TX_ML'})

    TX_CURR = pd.merge(TX_CURR, TX_ML_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_CURR = TX_CURR.drop(columns=['orgUnit_uid'])

    TX_CURR['Level 2: TX_CURR < TX_NEW'] = TX_CURR['Import File_TX_CURR'] < TX_CURR['Import File_TX_NEW']

    TX_CURR['Level 2: TX_ML > TX_CURR'] = TX_CURR['Import File_TX_ML'] > TX_CURR['Import File_TX_CURR']

    TX_CURR["Calculated proxy TX_CURR"] = TX_CURR['Previous_QTR_TX_CURR'] + TX_CURR['Import File_TX_NEW'] + TX_CURR[
        'Import File_TX_RTT'] - TX_CURR['Import File_TX_ML']

    return TX_CURR


def run_new_genie(TX_CURR, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TX_CURR = run_tier(TX_CURR, mer_file1, mer_file2, tier_df)

    TX_CURR_genie = second_genie[
        (second_genie['indicator'] == 'TX_CURR') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    TX_CURR_genie = TX_CURR_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    TX_CURR_genie = pd.DataFrame(TX_CURR_genie).reset_index()
    TX_CURR_genie = TX_CURR_genie.rename(columns={'TX_CURR': 'Genie_TX_CURR'})

    TX_CURR_genie = TX_CURR_genie.rename(columns={'TX_CURR': 'Genie_TX_CURR'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, TX_CURR_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_CURR = TX_CURR.drop(columns='orgunituid')

    TX_CURR['Import File vs Genie_TX_CURR'] = (TX_CURR['Import File_TX_CURR'].eq(TX_CURR['Genie_TX_CURR']) | (
                TX_CURR['Import File_TX_CURR'].isna() & TX_CURR['Genie_TX_CURR'].isna()))

    TX_NEW_genie = second_genie[
        (second_genie['indicator'] == 'TX_NEW') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    TX_NEW_genie = TX_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                            aggfunc='sum')
    TX_NEW_genie = pd.DataFrame(TX_NEW_genie).reset_index()
    TX_NEW_genie = TX_NEW_genie.rename(columns={'TX_NEW': 'Genie_TX_NEW'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, TX_NEW_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_CURR = TX_CURR.drop(columns='orgunituid')

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
    TX_CURR = pd.merge(TX_CURR, TX_RTT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_CURR = TX_CURR.drop(columns='orgunituid')

    TX_ML_genie = second_genie[
        (second_genie['indicator'] == 'TX_ML') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    TX_ML_genie = TX_ML_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                          aggfunc='sum')
    TX_ML_genie = pd.DataFrame(TX_ML_genie).reset_index()
    TX_ML_genie = TX_ML_genie.rename(columns={'TX_ML': 'Genie_TX_ML'})

    # merge with first genie
    TX_CURR = pd.merge(TX_CURR, TX_ML_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_CURR = TX_CURR.drop(columns='orgunituid')

    TX_CURR["Calculated proxy TX_CURR"] = TX_CURR['Previous_QTR_TX_CURR'] + TX_CURR['Genie_TX_NEW'] + TX_CURR[
        'Genie_TX_RTT'] - TX_CURR['Genie_TX_ML']

    TX_CURR['Level 2: TX_ML > TX_CURR'] = TX_CURR['Genie_TX_ML'] > TX_CURR['Genie_TX_CURR']

    TX_CURR['Level 2: TX_CURR < TX_NEW'] = TX_CURR['Genie_TX_CURR'] < TX_CURR['Genie_TX_NEW']

    ordered_cols = ['OU3name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'Previous_QTR_TX_CURR',
                    'MER report 1st submission_TX_CURR',
                    'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_CURR',
                    'MER report 2nd submission_TX_CURR',
                    'Import File_TX_CURR',
                    'MER report 1st submission vs 2nd submission_TX_CURR',
                    'MER report 2nd submission vs Import File_TX_CURR',
                    'Genie_TX_CURR',
                    # 'MER report 2nd submission vs Genie_TX_CURR',
                    'Import File vs Genie_TX_CURR',

                    'MER Report 1st Submission TX_NET_NEW',
                    'MER Report 1st Submission TX_NET_NEW % Variance',
                    'MER Report 1st Submission Proxy Retention',

                    'MER Report 2nd Submission TX_NET_NEW',
                    'MER Report 2nd Submission TX_NET_NEW % Variance',
                    'MER Report 2nd Submission Proxy Retention',

                    'TX_CURR 90',
                    'Level 2: MER Report > TX_CURR 90', 'Daily TX_CURR',
                    'Daily TX_CURR vs MER Report 1st Submission',
                    'Daily TX_CURR vs MER Report 1st Submission comment',
                    'Daily TX_CURR vs MER Report 2nd Submission',
                    'Daily TX_CURR vs MER Report 2nd Submission comment',

                    'MER report 1st submission_TX_NEW',
                    'MER report 2nd submission_TX_NEW',
                    'Import File_TX_NEW',
                    'Level 2: TX_CURR < TX_NEW',

                    'MER report 1st submission_TX_RTT',
                    'MER report 2nd submission_TX_RTT',
                    'Import File_TX_RTT',

                    'MER report 1st submission_TX_ML',
                    'MER report 2nd submission_TX_ML',
                    'Import File_TX_ML',
                    'Level 2: TX_ML > TX_CURR',

                    'Calculated proxy TX_CURR']

    TX_CURR = TX_CURR[ordered_cols]

    return TX_CURR
