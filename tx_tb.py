import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_TB'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_TB, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_TB, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_TB, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_TB.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_TB[TX_TB['Level 1 Check: No data in current quarter_TX_TB_Denom'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_TB_Denom', index=False)

        level_1_check_df = TX_TB[
            TX_TB['Level 1 Check: No data in current quarter_TX_TB_Denom_TestType'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 TX_TB_Denom_TestType', index=False)

        level_1_check_df = TX_TB[
            TX_TB['Level 1 Check: No data in current quarter_TX_TB_Denom_Pos'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 TX_TB_Denom_Pos', index=False)

        level_1_check_df = TX_TB[TX_TB['Level 1 Check: No data in current quarter_TX_TB_Numer'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_TB_Numer', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_TB.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_TB[TX_TB['MER report 1st submission vs 2nd submission_TX_CURR'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1 vs Mer2_TX_CURR', index=False)

        mer1_vs_mer2 = TX_TB[TX_TB['MER report 1st submission vs 2nd submission_TX_TB_Denom'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1_vs_2_TX_TB_Denom', index=False)

        mer1_vs_mer2 = TX_TB[TX_TB['MER report 1st submission vs 2nd submission_TX_TB_Denom_TestType'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1_vs_2_TX_TB_D_TestType', index=False)

        mer1_vs_mer2 = TX_TB[TX_TB['MER report 2nd submission_TX_TB_Denom_Pos'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1_vs_2_TX_TB_Denom_Pos', index=False)

        mer1_vs_mer2 = TX_TB[TX_TB['MER report 1st submission vs 2nd submission_TX_TB_Numer'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1_vs_2_TX_TB_Numer', index=False)

        # level_2_check_df = TX_TB[TX_TB['Level 2 Check: TX_TB > TX_CURR'] == True]
        # level_2_check_df.to_excel(writer, sheet_name='Level 2 Check TX_TB > TX_CURR', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_TB.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_mer2 = TX_TB[TX_TB['MER report  2nd submission vs Import File_TX_CURR'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer2_TX_CURR', index=False)

        Import_vs_mer2 = TX_TB[TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import_vs_Mer2_TX_TB_Denom', index=False)

        Import_vs_mer2 = TX_TB[TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom_TestType'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import_vs_Mer2_TX_TB_D_TestType', index=False)

        Import_vs_mer2 = TX_TB[TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom_Pos'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import_vs_Mer2_TX_TB_Denom_Pos', index=False)

        Import_vs_mer2 = TX_TB[TX_TB['MER report  2nd submission vs Import File_TX_TB_Numer'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import_vs_Mer2_TX_TB_Numer', index=False)

        support_typecheck = TX_TB[TX_TB['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_TB.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_Genie = TX_TB[TX_TB['Genie vs Import File_TX_CURR'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_TX_CURR', index=False)

        Import_vs_Genie = TX_TB[TX_TB['Genie vs Import File_TX_TB_Denom'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import_vs_Genie_TX_TB_Denom', index=False)

        Import_vs_Genie = TX_TB[TX_TB['Genie vs Import File_TX_TB_Denom_TestType'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Imp_vs_Genie_TX_TB_D_TestType', index=False)

        Import_vs_Genie = TX_TB[TX_TB['Genie vs Import File_TX_TB_Denom_Pos'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import_vs_Genie_TX_TB_Denom_Pos', index=False)

        Import_vs_Genie = TX_TB[TX_TB['Genie vs Import File_TX_TB_Numer'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import_vs_Genie_TX_TB_Numer', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_tb_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    tb_yr = fiscal_year_1stG
    tb_qtr = _1stG_curr_qtr

    if (first_genie is not None) & (mfl is not None):

        TX_TB_D_genie = first_genie[(first_genie['indicator'] == 'TX_TB') & (first_genie['fiscal_year'] == tb_yr) & (
                    first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'D')]

        TX_TB_D_genie = TX_TB_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=tb_qtr,
                                                  aggfunc='sum')
        TX_TB_D_genie = pd.DataFrame(TX_TB_D_genie).reset_index()
        TX_TB_D_genie = TX_TB_D_genie.rename(columns={'TX_TB': 'Previous_QTR_TX_TB_D'})

        # merge with first genie
        TX_TB = pd.merge(mfl, TX_TB_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_TB = TX_TB.drop(columns='orgunituid')

        TX_TB_N_genie = first_genie[(first_genie['indicator'] == 'TX_TB') & (first_genie['fiscal_year'] == tb_yr) & (
                    first_genie['source_name'] == 'DATIM') & (first_genie['numeratordenom'] == 'N')]

        TX_TB_N_genie = TX_TB_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=tb_qtr,
                                                  aggfunc='sum')
        TX_TB_N_genie = pd.DataFrame(TX_TB_N_genie).reset_index()
        TX_TB_N_genie = TX_TB_N_genie.rename(columns={'TX_TB': 'Previous_QTR_TX_TB_N'})

        # merge
        TX_TB = pd.merge(TX_TB, TX_TB_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_TB = TX_TB.drop(columns='orgunituid')

        art_mer_q1_file = st.file_uploader("Upload Previous Qtr ART MER file", type=["xlsx", "xls"])

        if step == 'MER File 1':
            TX_TB = run_first_mer(TX_TB, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_TB_D',
                            'Previous_QTR_TX_TB_N',
                            'MER report 1st submission_TX_TB_Denom',
                            'MER report 1st submission_TX_TB_Denom_TestType',
                            'MER report 1st submission_TX_TB_Denom_Pos',
                            'MER report 1st submission_TX_TB_Numer']

            summary_df = TX_TB.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_TB, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':

            if art_mer_q1_file is not None:

                TX_TB = run_second_mer(TX_TB, mer_file1, mer_file2, art_mer_q1_file)

                # step 3 output
                summary_cols = ['Previous_QTR_TX_TB_D','Previous_QTR_TX_TB_N',
                                'MER report 1st submission_TX_TB_Denom',
                                'MER report 1st submission_TX_TB_Denom_TestType',
                                'MER report 1st submission_TX_TB_Denom_Pos',
                                'MER report 1st submission_TX_TB_Numer',
                                'MER report 2nd submission_TX_TB_Denom',
                                'MER report 2nd submission_TX_TB_Denom_TestType',
                                'MER report 2nd submission_TX_TB_Denom_Pos',
                                'MER report 2nd submission_TX_TB_Numer']

                summary_df = TX_TB.groupby('OU3name')[summary_cols].sum().reset_index()

                total_row = summary_df[summary_cols].sum().tolist()
                total_row.insert(0, 'Total')
                summary_df.loc[len(summary_df)] = total_row

                # Button to trigger download
                download_excel(TX_TB, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

                return

        elif step == 'Tier Import':
            if art_mer_q1_file is not None:
                TX_TB = run_tier(TX_TB, mer_file1, mer_file2, tier_df, art_mer_q1_file)

                summary_cols = ['Previous_QTR_TX_TB_D', 'Previous_QTR_TX_TB_N',
                                'MER report 1st submission_TX_TB_Denom',
                                'MER report 1st submission_TX_TB_Denom_TestType',
                                'MER report 1st submission_TX_TB_Denom_Pos',
                                'MER report 1st submission_TX_TB_Numer',
                                'MER report 2nd submission_TX_TB_Denom',
                                'MER report 2nd submission_TX_TB_Denom_TestType',
                                'MER report 2nd submission_TX_TB_Denom_Pos',
                                'MER report 2nd submission_TX_TB_Numer',
                                'Import File_TX_CURR',
                                'Import File_TX_TB_Denom',
                                'Import File_TX_TB_Denom_TestType',
                                'Import File_TX_TB_Denom_Pos',
                                'Import File_TX_TB_Numer']

                summary_df = TX_TB.groupby('OU3name')[summary_cols].sum().reset_index()

                total_row = summary_df[summary_cols].sum().tolist()
                total_row.insert(0, 'Total')
                summary_df.loc[len(summary_df)] = total_row

                # Button to trigger download
                download_excel(TX_TB, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

                return

        elif step == 'New Genie':
            if art_mer_q1_file is not None:

                TX_TB = run_new_genie(TX_TB, mer_file1, mer_file2, tier_df, art_mer_q1_file, new_genie_df, fiscal_year_2ndG,
                                       _2ndG_curr_qtr)

                # step 5 output
                summary_cols = ['Previous_QTR_TX_TB_D', 'Previous_QTR_TX_TB_N',
                                'MER report 1st submission_TX_TB_Denom',
                                'MER report 1st submission_TX_TB_Denom_TestType',
                                'MER report 1st submission_TX_TB_Denom_Pos',
                                'MER report 1st submission_TX_TB_Numer',
                                'MER report 2nd submission_TX_TB_Denom',
                                'MER report 2nd submission_TX_TB_Denom_TestType',
                                'MER report 2nd submission_TX_TB_Denom_Pos',
                                'MER report 2nd submission_TX_TB_Numer',
                                'Import File_TX_CURR',
                                'Import File_TX_TB_Denom',
                                'Import File_TX_TB_Denom_TestType',
                                'Import File_TX_TB_Denom_Pos',
                                'Import File_TX_TB_Numer',
                                'Genie_TX_CURR',
                                'Genie_TX_TB_Denom',
                                'Genie_TX_TB_Denom_TestType',
                                'Genie_TX_TB_Denom_Pos',
                                'Genie_TX_TB_Numer']

                summary_df = TX_TB.groupby('OU3name')[summary_cols].sum().reset_index()

                total_row = summary_df[summary_cols].sum().tolist()
                total_row.insert(0, 'Total')
                summary_df.loc[len(summary_df)] = total_row

                # Button to trigger download
                download_excel(TX_TB, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

                return
        else:
            st.write("No step was selected")


def run_first_mer(TX_TB, mer_file1):
    s = pd.ExcelFile(mer_file1)
    elements = s.sheet_names
    tb_elements = [elem for elem in elements if elem.startswith("TX_TB")]

    kp = pd.read_excel(mer_file1, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_CURR')

    # select the districts
    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # append the kp and non kps
    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_CURR'})

    TX_TB = pd.merge(TX_TB, mer, left_on='OU5uid', right_on='UID', how='left')

    def process_sheet(sheet_name, total_column_name, new_column_name, TX_TB, mer_file, districts):
        mer = pd.read_excel(mer_file, sheet_name=sheet_name)
        mer = mer[mer['District'].isin(districts)]
        mer = mer.pivot_table(index=['UID'], values=total_column_name, aggfunc='sum')
        mer = pd.DataFrame(mer).reset_index()
        mer = mer.rename(columns={total_column_name: new_column_name})
        TX_TB = pd.merge(TX_TB, mer, on='UID', how='left')
        return TX_TB

    new_columns = []
    total_columns = []

    # create columns
    for item in tb_elements:
        new_columns.append('MER report 1st submission_' + item)

    # create totals
    for item in tb_elements:
        total_columns.append('Total')

    # use the function
    for sheet, total_col, new_col in zip(tb_elements, total_columns, new_columns):
        TX_TB = process_sheet(sheet, total_col, new_col, TX_TB, mer_file1, districts)

    # Track Second Submission
    def prev_qtr_data_no_current_qtr_check(row, el):
        if row['MER report 1st submission_' + el] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    for el in tb_elements:
        qtr_data_check = 'Level 1 Check: No data in current quarter_' + el
        TX_TB[qtr_data_check] = TX_TB.apply(prev_qtr_data_no_current_qtr_check, args=(el,), axis=1)

    TX_TB['% TX_TB Screening Rate'] = ((TX_TB['MER report 1st submission_TX_TB_Denom'] / TX_TB[
        'MER report 1st submission_TX_CURR']) * 100).round(0)

    TX_TB['% TB Treatment initiation rate'] = ((TX_TB['MER report 1st submission_TX_TB_Numer'] / TX_TB[
        'MER report 1st submission_TX_TB_Denom_Pos']) * 100).round(0)

    return TX_TB


def run_second_mer(TX_TB, mer_file1, mer_file2, art_mer_q1_file):
    # run first mer
    TX_TB = run_first_mer(TX_TB, mer_file1)

    # TX CURR
    kp = pd.read_excel(mer_file2, sheet_name='TX_CURR_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_CURR')

    # select the districts
    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # append the kp and non kps
    mer1_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer1 = mer1_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer1 = pd.DataFrame(mer1).reset_index()

    mer1 = mer1.rename(columns={'Total': 'MER report 2nd submission_TX_CURR'})

    TX_TB = pd.merge(TX_TB, mer1, on='UID', how='left')

    # OTHERS
    def process_sheet(sheet_name, total_column_name, new_column_name, TX_TB, mer_file, districts):
        mer = pd.read_excel(mer_file, sheet_name=sheet_name)
        mer = mer[mer['District'].isin(districts)]
        mer = mer.pivot_table(index=['UID'], values=total_column_name, aggfunc='sum')
        mer = pd.DataFrame(mer).reset_index()
        mer = mer.rename(columns={total_column_name: new_column_name})
        TX_TB = pd.merge(TX_TB, mer, on='UID', how='left')
        return TX_TB

    new_columns = []
    total_columns = []

    # TODO change to mer file 2
    elements = pd.ExcelFile(mer_file2).sheet_names
    tb_elements = [elem for elem in elements if elem.startswith("TX_TB")]

    # create columns
    for item in tb_elements:
        new_columns.append('MER report 2nd submission_' + item)

    # create totals
    for item in tb_elements:
        total_columns.append('Total')

    # use the function
    for sheet, total_col, new_col in zip(tb_elements, total_columns, new_columns):
        TX_TB = process_sheet(sheet, total_col, new_col, TX_TB, mer_file2, districts)

    # q1
    q1_art = pd.read_excel(art_mer_q1_file, sheet_name='TB_ART')
    q1_art = q1_art[q1_art['District'].isin(districts)]
    q1_art = q1_art.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    q1_art = pd.DataFrame(q1_art).reset_index()
    q1_art = q1_art.rename(columns={'Total': 'Q1 Total'})

    # q2 file - second mer file
    q2_art = pd.read_excel(mer_file2, sheet_name='TB_ART')
    q2_art = q2_art[q2_art['District'].isin(districts)]
    q2_art = q2_art.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    q2_art = pd.DataFrame(q2_art).reset_index()
    q2_art = q2_art.rename(columns={'Total': 'Q2 Total'})

    art = pd.merge(q1_art, q2_art)
    art['Expected TX_TB (N)'] = art['Q1 Total'] + art['Q2 Total']
    art = art.drop(columns=['Q1 Total', 'Q2 Total'])

    TX_TB = pd.merge(TX_TB, art, on='UID', how='left')

    TX_TB['% TX_TB Screening Rate'] = ((TX_TB['MER report 2nd submission_TX_TB_Denom'] / TX_TB[
        'MER report 2nd submission_TX_CURR']) * 100).round(0)

    TX_TB['% TB Treatment initiation rate'] = ((TX_TB['MER report 2nd submission_TX_TB_Numer'] / TX_TB[
        'MER report 2nd submission_TX_TB_Denom_Pos']) * 100).round(0)

    TX_TB['MER report 1st submission vs 2nd submission_TX_CURR'] = (TX_TB['MER report 1st submission_TX_CURR'] == TX_TB[
        'MER report 2nd submission_TX_CURR']) | (TX_TB['MER report 1st submission_TX_CURR'].eq('') & TX_TB[
        'MER report 2nd submission_TX_CURR'].eq(''))

    for e in tb_elements:
        TX_TB['MER report 1st submission vs 2nd submission_' + e] = (TX_TB['MER report 1st submission_' + e] == TX_TB[
            'MER report 2nd submission_' + e]) | (TX_TB['MER report 1st submission_' + e].eq('') & TX_TB[
            'MER report 2nd submission_' + e].eq(''))

    return TX_TB


def run_tier(TX_TB, mer_file1, mer_file2, tier, art_mer_q1_file):
    # run the second mer
    TX_TB = run_second_mer(TX_TB, mer_file1, mer_file2, art_mer_q1_file)

    # TX_CURR
    tier_c = tier[tier['dataElement'].isin(['TX_CURR (N, DSD, Age/Sex/HIVStatus): Receiving ART',
                                            'TX_CURR (N, TA, Age/Sex/HIVStatus): Receiving ART'])]  # TODO add other elements

    tier_c['dataElement'] = tier_c['dataElement'].apply(lambda x: 'TX_CURR' if x.startswith('TX_CURR') else x)

    tier_c = tier_c.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    tier_c = pd.DataFrame(tier_c).reset_index()

    tier_c = tier_c.rename(columns={'TX_CURR': 'Import File_TX_CURR'})

    TX_TB = pd.merge(TX_TB, tier_c, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_TB = TX_TB.drop(columns=['orgUnit_uid'])
    TX_TB.head(2)

    # TX_TB_Denom
    tier_c = tier[tier['dataElement'].isin(['TX_TB (D, TA, Age/Sex/TBScreen/NewExistingART/HIVStatus): TB Screening',
                                            'TX_TB (D, DSD, Age/Sex/TBScreen/NewExistingART/HIVStatus): TB Screening'])]  # TODO add other elements

    tier_c['dataElement'] = tier_c['dataElement'].apply(lambda x: 'TX_TB_Denom' if x.startswith('TX_TB (D') else x)

    tier_c = tier_c.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                aggfunc='sum')
    tier_c = pd.DataFrame(tier_c).reset_index()

    tier_c = tier_c.rename(columns={'TX_TB_Denom': 'Import File_TX_TB_Denom'})

    TX_TB = pd.merge(TX_TB, tier_c, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_TB = TX_TB.drop(columns=['orgUnit_uid'])
    TX_TB.head(2)

    # TX_TB_Denom_TestType
    tier_c = tier[tier['dataElement'].isin(['TX_TB (D, TA, TB Test Type/HIVStatus): TB Screening',
                                            'TX_TB (D, DSD, TB Test Type/HIVStatus): TB Screening'])]  # TODO add other elements

    tier_c['dataElement'] = tier_c['dataElement'].apply(
        lambda x: 'TX_TB_Denom_TestType' if x.startswith('TX_TB (D') else x)

    tier_c = tier_c.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    tier_c = pd.DataFrame(tier_c).reset_index()

    tier_c = tier_c.rename(columns={'TX_TB_Denom_TestType': 'Import File_TX_TB_Denom_TestType'})

    TX_TB = pd.merge(TX_TB, tier_c, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_TB = TX_TB.drop(columns=['orgUnit_uid'])
    TX_TB.head(2)

    # TX_TB_Denom_Pos
    tier_c = tier[tier['dataElement'].isin(['TX_TB (D, TA, Specimen Return/HIVStatus): TB Screening',
                                            'TX_TB (D, DSD, Specimen Return/HIVStatus): TB Screening'])]  # TODO add other elements

    tier_c['dataElement'] = tier_c['dataElement'].apply(lambda x: 'TX_TB_Denom_Pos' if x.startswith('TX_TB (D') else x)

    tier_c = tier_c.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    tier_c = pd.DataFrame(tier_c).reset_index()

    tier_c = tier_c.rename(columns={'TX_TB_Denom_Pos': 'Import File_TX_TB_Denom_Pos'})

    TX_TB = pd.merge(TX_TB, tier_c, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_TB = TX_TB.drop(columns=['orgUnit_uid'])
    TX_TB.head(2)
    # TX_TB_Numer
    tier_c = tier[tier['dataElement'].isin(['TX_TB (N, TA, Age/Sex/NewExistingArt/HIVStatus): TB Treatment',
                                            'TX_TB (N, DSD, Age/Sex/NewExistingArt/HIVStatus): TB Treatment'])]  # TODO add other elements

    tier_c['dataElement'] = tier_c['dataElement'].apply(lambda x: 'TX_TB_Numer' if x.startswith('TX_TB (N') else x)

    tier_c = tier_c.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    tier_c = pd.DataFrame(tier_c).reset_index()

    tier_c = tier_c.rename(columns={'TX_TB_Numer': 'Import File_TX_TB_Numer'})

    TX_TB = pd.merge(TX_TB, tier_c, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_TB = TX_TB.drop(columns=['orgUnit_uid'])
    TX_TB.head(2)

    TX_TB['% TX_TB Screening Rate'] = ((TX_TB['Import File_TX_TB_Denom'] / TX_TB['Import File_TX_CURR']) * 100).round(0)

    TX_TB['MER report  2nd submission vs Import File_TX_CURR'] = (
                TX_TB['MER report 2nd submission_TX_CURR'].eq(TX_TB['Import File_TX_CURR']) | (
                    TX_TB['MER report 2nd submission_TX_CURR'].isna() & TX_TB['Import File_TX_CURR'].isna()))

    TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom'] = (
                TX_TB['MER report 2nd submission_TX_TB_Denom'].eq(TX_TB['Import File_TX_TB_Denom']) | (
                    TX_TB['MER report 2nd submission_TX_TB_Denom'].isna() & TX_TB['Import File_TX_TB_Denom'].isna()))

    TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom_TestType'] = (
                TX_TB['MER report 2nd submission_TX_TB_Denom_TestType'].eq(
                    TX_TB['Import File_TX_TB_Denom_TestType']) | (
                            TX_TB['MER report 2nd submission_TX_TB_Denom_TestType'].isna() & TX_TB[
                        'Import File_TX_TB_Denom_TestType'].isna()))

    TX_TB['MER report  2nd submission vs Import File_TX_TB_Denom_Pos'] = (
                TX_TB['MER report 2nd submission_TX_TB_Denom_Pos'].eq(TX_TB['Import File_TX_TB_Denom_Pos']) | (
                    TX_TB['MER report 2nd submission_TX_TB_Denom_Pos'].isna() & TX_TB[
                'Import File_TX_TB_Denom_Pos'].isna()))

    TX_TB['MER report  2nd submission vs Import File_TX_TB_Numer'] = (
                TX_TB['MER report 2nd submission_TX_TB_Numer'].eq(TX_TB['Import File_TX_TB_Numer']) | (
                    TX_TB['MER report 2nd submission_TX_TB_Numer'].isna() & TX_TB['Import File_TX_TB_Numer'].isna()))

    TX_TB['Support Type Check'] = (TX_TB['DSD/TA'] == TX_TB['supportType']) | (
                TX_TB['supportType'].isna() | (TX_TB['supportType'] == ''))

    return TX_TB


def run_new_genie(TX_TB, mer_file1, mer_file2, tier_df, art_mer_q1_file, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TX_TB = run_tier(TX_TB, mer_file1, mer_file2, tier_df, art_mer_q1_file)

    # Run the CURR
    tx_curr = second_genie[
        (second_genie['indicator'] == 'TX_CURR') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    tx_curr = tx_curr.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr, aggfunc='sum')
    tx_curr = pd.DataFrame(tx_curr).reset_index()
    tx_curr = tx_curr.rename(columns={'TX_CURR': 'Genie_TX_CURR'})

    TX_TB = pd.merge(TX_TB, tx_curr, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_TB = TX_TB.drop(columns='orgunituid')

    els = second_genie['indicator'].unique().tolist()
    genie_elements = [elem for elem in els if elem.startswith("TX_TB")]

    TX_TB_D_genie = second_genie[
        (second_genie['indicator'] == 'TX_TB') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (
                    second_genie['standardizeddisaggregate'] == 'Age/Sex/TBScreen/NewExistingART/HIVStatus')]

    TX_TB_D_genie = TX_TB_D_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    TX_TB_D_genie = pd.DataFrame(TX_TB_D_genie).reset_index()
    TX_TB_D_genie = TX_TB_D_genie.rename(columns={'TX_TB': 'Genie_TX_TB_Denom'})

    # merge with first genie
    TX_TB = pd.merge(TX_TB, TX_TB_D_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_TB = TX_TB.drop(columns='orgunituid')

    TX_TB_D_Type_genie = second_genie[
        (second_genie['indicator'] == 'TX_TB') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (
                    second_genie['standardizeddisaggregate'] == 'TB Test Type/HIVStatus')]

    TX_TB_D_Type_genie = TX_TB_D_Type_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                        values=_2ndG_curr_qtr, aggfunc='sum')
    TX_TB_D_Type_genie = pd.DataFrame(TX_TB_D_Type_genie).reset_index()
    TX_TB_D_Type_genie = TX_TB_D_Type_genie.rename(columns={'TX_TB': 'Genie_TX_TB_Denom_TestType'})

    # merge with first genie
    TX_TB = pd.merge(TX_TB, TX_TB_D_Type_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_TB = TX_TB.drop(columns='orgunituid')

    TX_TB_N_genie = second_genie[
        (second_genie['indicator'] == 'TX_TB') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (second_genie['numeratordenom'] == 'N')]

    TX_TB_N_genie = TX_TB_N_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    TX_TB_N_genie = pd.DataFrame(TX_TB_N_genie).reset_index()
    TX_TB_N_genie = TX_TB_N_genie.rename(columns={'TX_TB': 'Genie_TX_TB_Numer'})

    # merge with first genie
    TX_TB = pd.merge(TX_TB, TX_TB_N_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_TB = TX_TB.drop(columns='orgunituid')

    TX_TB_D_Pos_genie = second_genie[
        (second_genie['indicator'] == 'TX_TB') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & (
                    second_genie['standardizeddisaggregate'] == 'Specimen Return/HIVStatus')]

    TX_TB_D_Pos_genie = TX_TB_D_Pos_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                      aggfunc='sum')
    TX_TB_D_Pos_genie = pd.DataFrame(TX_TB_D_Pos_genie).reset_index()

    TX_TB_D_Pos_genie = TX_TB_D_Pos_genie.rename(columns={'TX_TB': 'Genie_TX_TB_Denom_Pos'})

    # merge with first genie
    TX_TB = pd.merge(TX_TB, TX_TB_D_Pos_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_TB = TX_TB.drop(columns='orgunituid')

    TX_TB['% TX_TB Screening Rate'] = ((TX_TB['Genie_TX_TB_Denom'] / TX_TB['Genie_TX_CURR']) * 100).round(0)

    TX_TB['Genie vs Import File_TX_CURR'] = (TX_TB['Genie_TX_CURR'].eq(TX_TB['Import File_TX_CURR']) | (
                TX_TB['Genie_TX_CURR'].isna() & TX_TB['Import File_TX_CURR'].isna()))

    TX_TB['Genie vs Import File_TX_TB_Denom'] = (TX_TB['Genie_TX_TB_Denom'].eq(TX_TB['Import File_TX_TB_Denom']) | (
                TX_TB['Genie_TX_TB_Denom'].isna() & TX_TB['Import File_TX_TB_Denom'].isna()))

    TX_TB['Genie vs Import File_TX_TB_Denom_Pos'] = (
                TX_TB['Genie_TX_TB_Denom_Pos'].eq(TX_TB['Import File_TX_TB_Denom_Pos']) | (
                    TX_TB['Genie_TX_TB_Denom_Pos'].isna() & TX_TB['Import File_TX_TB_Denom_Pos'].isna()))

    TX_TB['Genie vs Import File_TX_TB_Numer'] = (TX_TB['Genie_TX_TB_Numer'].eq(TX_TB['Import File_TX_TB_Numer']) | (
                TX_TB['Genie_TX_TB_Numer'].isna() & TX_TB['Import File_TX_TB_Numer'].isna()))

    TX_TB['Genie vs Import File_TX_TB_Denom_TestType'] = (
                TX_TB['Genie_TX_TB_Denom_TestType'].eq(TX_TB['Import File_TX_TB_Denom_TestType']) | (
                    TX_TB['Genie_TX_TB_Denom_TestType'].isna() & TX_TB['Import File_TX_TB_Denom_TestType'].isna()))

    return TX_TB