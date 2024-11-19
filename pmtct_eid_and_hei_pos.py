import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'PMTCT_EID_HEI_POS'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(PMTCT_EID_HEI_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, PMTCT_EID_HEI_POS, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, PMTCT_EID_HEI_POS, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        PMTCT_EID_HEI_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS[
                                                 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_EID'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_PMTCT_EID', index=False)

        level_1_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS[
                                                 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_HEI_POS'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_PMTCT_HEI_POS', index=False)

        level_1_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS[
                                                 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_HEI_POS_ART'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_PMTCT_HEI_POS_ART', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] == False]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        PMTCT_EID_HEI_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_EID'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PMTCT_EID', index=False)

        mer1_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_HEI_POS'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PMTCT_HEI_POS', index=False)

        mer1_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_HEI_POS_ART'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer1 vs Mer2_PMTCT_HEI_POS_ART', index=False)

        mer1_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['<1 MER report 1st submission vs 2nd submission_TX_NEW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_<1 _TX_NEW', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] == False]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        PMTCT_EID_HEI_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_EID'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_PMTCT_EID', index=False)

        import_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_HEI_POS'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_PMTCT_HEI_POS', index=False)

        import_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_HEI_POS_ART'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import_Mer 2_PMTCT_HEI_POS_ART', index=False)

        import_vs_mer2 = PMTCT_EID_HEI_POS[
            PMTCT_EID_HEI_POS['<1 MER report 2nd submission vs Import File_TX_NEW'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_<1 _TX_NEW', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] == False]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        support_typecheck = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        PMTCT_EID_HEI_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_genie = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_EID'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import vs genie_PMTCT_EID', index=False)

        import_vs_genie = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_HEI_POS'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import vs genie_PMTCT_HEI_POS', index=False)

        import_vs_genie = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_HEI_POS_ART'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import_genie_PMTCT_HEI_POS_ART', index=False)

        import_vs_genie = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['<1 Genie vs Import File_TX_NEW'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import vs genie_<1 _TX_NEW', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] == True]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        level_2_check_df = PMTCT_EID_HEI_POS[PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] == False]
        level_2_check_df.to_excel(writer, sheet_name='PMTCT_HEI_ART >  PMTCT_HEI_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_pmtct_eid_hei_pos_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df, non_tier):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        PMTCT_EID_genie = first_genie[
            (first_genie['indicator'] == 'PMTCT_EID') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]
        PMTCT_EID_genie = PMTCT_EID_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        PMTCT_EID_genie = pd.DataFrame(PMTCT_EID_genie).reset_index()

        PMTCT_EID_genie = PMTCT_EID_genie.rename(columns={'PMTCT_EID': 'Previous_QTR_PMTCT_EID'})

        # merge with first genie
        PMTCT_EID_HEI_POS = pd.merge(mfl, PMTCT_EID_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

        PMTCT_HEI_POS_genie = first_genie[
            (first_genie['indicator'] == 'PMTCT_HEI_POS') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'Derived')]
        PMTCT_HEI_POS_genie = PMTCT_HEI_POS_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                              values=_1stG_curr_qtr, aggfunc='sum')
        PMTCT_HEI_POS_genie = pd.DataFrame(PMTCT_HEI_POS_genie).reset_index()

        PMTCT_HEI_POS_genie = PMTCT_HEI_POS_genie.rename(columns={'PMTCT_HEI_POS': 'Previous_QTR_PMTCT_HEI_POS'})

        # merge with first genie
        PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_genie, left_on='DATIM UID', right_on='orgunituid',
                                     how='left')
        PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

        PMTCT_HEI_POS_ART_genie = first_genie[
            (first_genie['indicator'] == 'PMTCT_HEI_POS_ART') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'Derived')]
        PMTCT_HEI_POS_ART_genie = PMTCT_HEI_POS_ART_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                                      values=_1stG_curr_qtr, aggfunc='sum')
        PMTCT_HEI_POS_ART_genie = pd.DataFrame(PMTCT_HEI_POS_ART_genie).reset_index()

        PMTCT_HEI_POS_ART_genie = PMTCT_HEI_POS_ART_genie.rename(
            columns={'PMTCT_HEI_POS_ART': 'Previous_QTR_PMTCT_HEI_POS_ART'})

        # merge with first genie
        PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_ART_genie, left_on='DATIM UID',
                                     right_on='orgunituid', how='left')
        PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

        TX_NEW_genie = first_genie[
            (first_genie['indicator'] == 'TX_NEW') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM') & first_genie['ageasentered'].str.contains('<01')]
        TX_NEW_genie = TX_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                aggfunc='sum')
        TX_NEW_genie = pd.DataFrame(TX_NEW_genie).reset_index()
        TX_NEW_genie = TX_NEW_genie.rename(columns={'TX_NEW': '<1 Previous_QTR_TX_NEW'})

        # merge with first genie
        PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, TX_NEW_genie, left_on='DATIM UID', right_on='orgunituid',
                                     how='left')
        PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

        if step == 'MER File 1':
            PMTCT_EID_HEI_POS = run_first_mer(PMTCT_EID_HEI_POS, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_PMTCT_EID', 'Previous_QTR_PMTCT_HEI_POS_ART', '<1 Previous_QTR_TX_NEW',
                            'MER report 1st submission_PMTCT_EID', 'MER report 1st submission_PMTCT_HEI_POS',
                            'MER report 1st submission_PMTCT_HEI_POS_ART', '<1 MER report 1st submission_TX_NEW']

            summary_df = PMTCT_EID_HEI_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_EID_HEI_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            PMTCT_EID_HEI_POS = run_second_mer(PMTCT_EID_HEI_POS, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_PMTCT_EID', 'Previous_QTR_PMTCT_HEI_POS_ART', '<1 Previous_QTR_TX_NEW',
                            'MER report 1st submission_PMTCT_EID', 'MER report 1st submission_PMTCT_HEI_POS',
                            'MER report 1st submission_PMTCT_HEI_POS_ART', '<1 MER report 1st submission_TX_NEW',
                            'MER report 2nd submission_PMTCT_EID',
                            'MER report 2nd submission_PMTCT_HEI_POS',
                            'MER report 2nd submission_PMTCT_HEI_POS_ART',
                            '<1 MER report 2nd submission_TX_NEW']

            summary_df = PMTCT_EID_HEI_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_EID_HEI_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            PMTCT_EID_HEI_POS = run_tier(PMTCT_EID_HEI_POS, mer_file1, mer_file2, tier_df, non_tier)

            # step 4 output
            summary_cols = ['Previous_QTR_PMTCT_EID', 'Previous_QTR_PMTCT_HEI_POS_ART', '<1 Previous_QTR_TX_NEW',
                            'MER report 1st submission_PMTCT_EID', 'MER report 1st submission_PMTCT_HEI_POS',
                            'MER report 1st submission_PMTCT_HEI_POS_ART', '<1 MER report 1st submission_TX_NEW',
                            'MER report 2nd submission_PMTCT_EID',
                            'MER report 2nd submission_PMTCT_HEI_POS',
                            'MER report 2nd submission_PMTCT_HEI_POS_ART',
                            '<1 MER report 2nd submission_TX_NEW',
                            'Import File_PMTCT_EID', 'Import File_PMTCT_HEI_POS_ART', 'Import File_PMTCT_HEI_POS',
                            '<1 Import File_TX_NEW'
                            ]

            summary_df = PMTCT_EID_HEI_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_EID_HEI_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            PMTCT_EID_HEI_POS = run_new_genie(PMTCT_EID_HEI_POS, mer_file1, mer_file2, tier_df, non_tier, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_PMTCT_EID', 'Previous_QTR_PMTCT_HEI_POS_ART', '<1 Previous_QTR_TX_NEW',
                            'MER report 1st submission_PMTCT_EID', 'MER report 1st submission_PMTCT_HEI_POS',
                            'MER report 1st submission_PMTCT_HEI_POS_ART', '<1 MER report 1st submission_TX_NEW',
                            'MER report 2nd submission_PMTCT_EID',
                            'MER report 2nd submission_PMTCT_HEI_POS',
                            'MER report 2nd submission_PMTCT_HEI_POS_ART',
                            '<1 MER report 2nd submission_TX_NEW',
                            'Import File_PMTCT_EID', 'Import File_PMTCT_HEI_POS_ART', 'Import File_PMTCT_HEI_POS',
                            '<1 Import File_TX_NEW', 'Genie_PMTCT_EID', 'Genie_PMTCT_HEI_POS_ART',
                            'Genie_PMTCT_HEI_POS', '<1 Genie_TX_NEW']

            summary_df = PMTCT_EID_HEI_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_EID_HEI_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(PMTCT_EID_HEI_POS, mer_file1):
    # kp = pd.read_excel(mer_file1, sheet_name='PMTCT_EID_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PMTCT_EID')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PMTCT_EID'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # Track Second Submission: PMTCT_EID
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_EID'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_PMTCT_EID'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PMTCT_EID_HEI_POS[qtr_data_check] = PMTCT_EID_HEI_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    # kp = pd.read_excel(mer_file1, sheet_name='PMTCT_HEI_POS_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PMTCT_HEI_POS')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PMTCT_HEI_POS'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # Track Second Submission: PMTCT_HEI_POS
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_HEI_POS'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_PMTCT_HEI_POS'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PMTCT_EID_HEI_POS[qtr_data_check] = PMTCT_EID_HEI_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    # kp = pd.read_excel(mer_file1, sheet_name='PMTCT_HEI_POS_ART_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PMTCT_HEI_POS_ART')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PMTCT_HEI_POS_ART'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # Track Second Submission: PMTCT_HEI_POS_ART
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PMTCT_HEI_POS_ART'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_PMTCT_HEI_POS_ART'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PMTCT_EID_HEI_POS[qtr_data_check] = PMTCT_EID_HEI_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    PMTCT_EID_HEI_POS['% Yield'] = ((PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS'] / PMTCT_EID_HEI_POS[
        'MER report 1st submission_PMTCT_EID']) * 100).round(1)

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] = PMTCT_EID_HEI_POS[
                                                                             'MER report 1st submission_PMTCT_HEI_POS_ART'] > \
                                                                         PMTCT_EID_HEI_POS[
                                                                             'MER report 1st submission_PMTCT_HEI_POS']

    PMTCT_EID_HEI_POS['Level 2: % Linkage'] = ((PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS_ART'] /
                                                PMTCT_EID_HEI_POS[
                                                    'MER report 1st submission_PMTCT_HEI_POS']) * 100).round(1)

    def calculate_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low LINKAGE"
        elif pd.notna(value) and value > 80:
            return "Good LINKAGE"
        else:
            return ""

    PMTCT_EID_HEI_POS['Level 2 Check: % Linkage status'] = PMTCT_EID_HEI_POS['Level 2: % Linkage'].apply(
        calculate_linkage)

    kp = pd.read_excel(mer_file1, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = mer_appended[mer_appended['FineAgeGroup'].str.contains('<1')]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': '<1 MER report 1st submission_TX_NEW'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # Track Second Submission: TX_NEW
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_NEW'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['<1 MER report 1st submission_TX_NEW'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PMTCT_EID_HEI_POS[qtr_data_check] = PMTCT_EID_HEI_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] = (
                PMTCT_EID_HEI_POS['<1 MER report 1st submission_TX_NEW'].eq(
                    PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS_ART']) | (
                            PMTCT_EID_HEI_POS['<1 MER report 1st submission_TX_NEW'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 1st submission_PMTCT_HEI_POS_ART'].isna()))

    return PMTCT_EID_HEI_POS


def run_second_mer(PMTCT_EID_HEI_POS, mer_file1, mer_file2):
    # run first mer
    PMTCT_EID_HEI_POS = run_first_mer(PMTCT_EID_HEI_POS, mer_file1)

    # kp = pd.read_excel(mer_file2, sheet_name='PMTCT_EID_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='PMTCT_EID')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PMTCT_EID'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # kp = pd.read_excel(mer_file2, sheet_name='PMTCT_HEI_POS_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='PMTCT_HEI_POS')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PMTCT_HEI_POS'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    # kp = pd.read_excel(mer_file2, sheet_name='PMTCT_HEI_POS_ART_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='PMTCT_HEI_POS_ART')

    # kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    # mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = non_kp

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PMTCT_HEI_POS_ART'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_EID'] = (
                PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_EID'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_EID']) | (
                            PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_EID'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_EID'].isna()))

    PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_HEI_POS'] = (
                PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS']) | (
                            PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_HEI_POS'].isna()))

    PMTCT_EID_HEI_POS['MER report 1st submission vs 2nd submission_PMTCT_HEI_POS_ART'] = (
                PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS_ART'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS_ART']) | (
                            PMTCT_EID_HEI_POS['MER report 1st submission_PMTCT_HEI_POS_ART'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_HEI_POS_ART'].isna()))

    PMTCT_EID_HEI_POS['% Yield'] = ((PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS'] / PMTCT_EID_HEI_POS[
        'MER report 2nd submission_PMTCT_EID']) * 100).round(1)

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] = PMTCT_EID_HEI_POS[
                                                                             'MER report 2nd submission_PMTCT_HEI_POS_ART'] > \
                                                                         PMTCT_EID_HEI_POS[
                                                                             'MER report 2nd submission_PMTCT_HEI_POS']

    PMTCT_EID_HEI_POS['Level 2: % Linkage'] = ((PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS_ART'] /
                                                PMTCT_EID_HEI_POS[
                                                    'MER report 2nd submission_PMTCT_HEI_POS']) * 100).round(1)

    def calculate_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low LINKAGE"
        elif pd.notna(value) and value > 80:
            return "Good LINKAGE"
        else:
            return ""

    PMTCT_EID_HEI_POS['Level 2 Check: % Linkage status'] = PMTCT_EID_HEI_POS['Level 2: % Linkage'].apply(
        calculate_linkage)

    kp = pd.read_excel(mer_file2, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = mer_appended[mer_appended['FineAgeGroup'].str.contains('<1')]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': '<1 MER report 2nd submission_TX_NEW'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='UID')

    PMTCT_EID_HEI_POS['<1 MER report 1st submission vs 2nd submission_TX_NEW'] = (
                PMTCT_EID_HEI_POS['<1 MER report 1st submission_TX_NEW'].eq(
                    PMTCT_EID_HEI_POS['<1 MER report 2nd submission_TX_NEW']) | (
                            PMTCT_EID_HEI_POS['<1 MER report 1st submission_TX_NEW'].isna() & PMTCT_EID_HEI_POS[
                        '<1 MER report 2nd submission_TX_NEW'].isna()))

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] = (
                PMTCT_EID_HEI_POS['<1 MER report 2nd submission_TX_NEW'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS_ART']) | (
                            PMTCT_EID_HEI_POS['<1 MER report 2nd submission_TX_NEW'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_HEI_POS_ART'].isna()))

    return PMTCT_EID_HEI_POS


def run_tier(PMTCT_EID_HEI_POS, mer_file1, mer_file2, tier, non_tier):
    # run the second mer
    PMTCT_EID_HEI_POS = run_second_mer(PMTCT_EID_HEI_POS, mer_file1, mer_file2)

    PMTCT_EID_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_EID')]

    PMTCT_EID_tier['dataElement'] = 'PMTCT_EID'

    PMTCT_EID_tier = PMTCT_EID_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                values='value', aggfunc='sum')

    PMTCT_EID_tier = pd.DataFrame(PMTCT_EID_tier).reset_index()

    PMTCT_EID_tier = PMTCT_EID_tier.rename(columns={'PMTCT_EID': 'Import File_PMTCT_EID'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_EID_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns=['orgUnit_uid'])

    PMTCT_EID_HEI_POS['Support Type Check'] = (PMTCT_EID_HEI_POS['DSD/TA'] == PMTCT_EID_HEI_POS['supportType']) | (
                PMTCT_EID_HEI_POS['supportType'].isna() | (PMTCT_EID_HEI_POS['supportType'] == ''))

    PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_EID'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_EID'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_EID']) | (
                            PMTCT_EID_HEI_POS['Import File_PMTCT_EID'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_EID'].isna()))

    PMTCT_HEI_POS_ART_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_HEI_POS_ART')]

    PMTCT_HEI_POS_ART_tier['dataElement'] = 'PMTCT_HEI_POS_ART'

    PMTCT_HEI_POS_ART_tier = PMTCT_HEI_POS_ART_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement',
                                                                values='value', aggfunc='sum')

    PMTCT_HEI_POS_ART_tier = pd.DataFrame(PMTCT_HEI_POS_ART_tier).reset_index()

    PMTCT_HEI_POS_ART_tier = PMTCT_HEI_POS_ART_tier.rename(
        columns={'PMTCT_HEI_POS_ART': 'Import File_PMTCT_HEI_POS_ART'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_ART_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns=['orgUnit_uid'])

    PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_HEI_POS_ART'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS_ART'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS_ART']) | (
                            PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS_ART'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_HEI_POS_ART'].isna()))

    c = ['PMTCT_HEI (N, TA, Age/Result): Infant Testing', 'PMTCT_HEI (N, DSD, Age/Result): Infant Testing']
    PMTCT_HEI_POS_tier = non_tier[
        non_tier['dataElement'].isin(c) & non_tier['categoryOptionComboName'].str.contains('Positive')]

    PMTCT_HEI_POS_tier['dataElement'] = 'PMTCT_HEI_POS'

    PMTCT_HEI_POS_tier = PMTCT_HEI_POS_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                        aggfunc='sum')

    PMTCT_HEI_POS_tier = pd.DataFrame(PMTCT_HEI_POS_tier).reset_index()

    PMTCT_HEI_POS_tier = PMTCT_HEI_POS_tier.rename(columns={'PMTCT_HEI_POS': 'Import File_PMTCT_HEI_POS'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns=['orgUnit_uid'])

    PMTCT_EID_HEI_POS['MER report 2nd submission vs Import File_PMTCT_HEI_POS'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS'].eq(
                    PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS']) | (
                            PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS'].isna() & PMTCT_EID_HEI_POS[
                        'MER report 2nd submission_PMTCT_HEI_POS'].isna()))

    tx_new_tier = tier[
        tier['dataElement'].str.startswith('TX_NEW') & tier['categoryOptionComboName'].str.contains('<1')]

    tx_new_tier['dataElement'] = tx_new_tier['dataElement'].apply(lambda x: 'TX_NEW' if x.startswith('TX_NEW') else x)

    TX_NEW_tier = tx_new_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    TX_NEW_tier = pd.DataFrame(TX_NEW_tier).reset_index()

    TX_NEW_tier = TX_NEW_tier.rename(columns={'TX_NEW': '<1 Import File_TX_NEW'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, TX_NEW_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns=['orgUnit_uid'])

    PMTCT_EID_HEI_POS['<1 MER report 2nd submission vs Import File_TX_NEW'] = (
                PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].eq(
                    PMTCT_EID_HEI_POS['<1 MER report 2nd submission_TX_NEW']) | (
                            PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].isna() & PMTCT_EID_HEI_POS[
                        '<1 MER report 2nd submission_TX_NEW'].isna()))

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] = (PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].eq(
        PMTCT_EID_HEI_POS['MER report 2nd submission_PMTCT_HEI_POS_ART']) | (PMTCT_EID_HEI_POS[
                                                                                 '<1 Import File_TX_NEW'].isna() &
                                                                             PMTCT_EID_HEI_POS[
                                                                                 'MER report 2nd submission_PMTCT_HEI_POS_ART'].isna()))

    PMTCT_EID_HEI_POS['% Yield'] = ((PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS'] / PMTCT_EID_HEI_POS[
        'Import File_PMTCT_EID']) * 100).round(1)

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] = PMTCT_EID_HEI_POS[
                                                                             'Import File_PMTCT_HEI_POS_ART'] > \
                                                                         PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS']

    PMTCT_EID_HEI_POS['Level 2: % Linkage'] = ((PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS_ART'] / PMTCT_EID_HEI_POS[
        'Import File_PMTCT_HEI_POS']) * 100).round(1)

    def calculate_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low LINKAGE"
        elif pd.notna(value) and value > 80:
            return "Good LINKAGE"
        else:
            return ""

    PMTCT_EID_HEI_POS['Level 2 Check: % Linkage status'] = PMTCT_EID_HEI_POS['Level 2: % Linkage'].apply(
        calculate_linkage)

    return PMTCT_EID_HEI_POS


def run_new_genie(PMTCT_EID_HEI_POS, mer_file1, mer_file2, tier_df, non_tier, second_genie, fiscal_year_2ndG, _2ndG_curr_qtr):  # df is new genie
    # run tier step
    PMTCT_EID_HEI_POS = run_tier(PMTCT_EID_HEI_POS, mer_file1, mer_file2, tier_df, non_tier)

    # PMTCT_EID
    PMTCT_EID_genie = second_genie[
        (second_genie['indicator'] == 'PMTCT_EID') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    PMTCT_EID_genie = PMTCT_EID_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    PMTCT_EID_genie = pd.DataFrame(PMTCT_EID_genie).reset_index()

    PMTCT_EID_genie = PMTCT_EID_genie.rename(columns={'PMTCT_EID': 'Genie_PMTCT_EID'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_EID_genie, left_on='DATIM UID', right_on='orgunituid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

    # PMTCT_HEI_POS_ART
    PMTCT_HEI_POS_ART_genie = second_genie[
        (second_genie['indicator'] == 'PMTCT_HEI_POS_ART') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'Derived')]
    PMTCT_HEI_POS_ART_genie = PMTCT_HEI_POS_ART_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                                  values=_2ndG_curr_qtr, aggfunc='sum')
    PMTCT_HEI_POS_ART_genie = pd.DataFrame(PMTCT_HEI_POS_ART_genie).reset_index()

    PMTCT_HEI_POS_ART_genie = PMTCT_HEI_POS_ART_genie.rename(columns={'PMTCT_HEI_POS_ART': 'Genie_PMTCT_HEI_POS_ART'})

    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_ART_genie, left_on='DATIM UID', right_on='orgunituid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

    # PMTCT_HEI_POS
    PMTCT_HEI_POS_genie = second_genie[
        (second_genie['indicator'] == 'PMTCT_HEI') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    PMTCT_HEI_POS_genie = PMTCT_HEI_POS_genie[
        PMTCT_HEI_POS_genie['categoryoptioncomboname'].str.contains('<= 2 months, Positive|2 - 12 months, Positive')]

    PMTCT_HEI_POS_genie = PMTCT_HEI_POS_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                          values=_2ndG_curr_qtr, aggfunc='sum')
    PMTCT_HEI_POS_genie = pd.DataFrame(PMTCT_HEI_POS_genie).reset_index()

    if PMTCT_HEI_POS_genie.shape[0] == 0:
        PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS'] = ''
    else:
        PMTCT_HEI_POS_genie = PMTCT_HEI_POS_genie.rename(columns={'PMTCT_HEI': 'Genie_PMTCT_HEI_POS'})

        PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, PMTCT_HEI_POS_genie, left_on='DATIM UID', right_on='orgunituid',
                                     how='left')
        PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

    TX_NEW_genie = second_genie[
        (second_genie['indicator'] == 'TX_NEW') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM') & second_genie['ageasentered'].str.contains('<01')]
    TX_NEW_genie = TX_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                            aggfunc='sum')
    TX_NEW_genie = pd.DataFrame(TX_NEW_genie).reset_index()
    TX_NEW_genie = TX_NEW_genie.rename(columns={'TX_NEW': '<1 Genie_TX_NEW'})

    # merge with first genie
    PMTCT_EID_HEI_POS = pd.merge(PMTCT_EID_HEI_POS, TX_NEW_genie, left_on='DATIM UID', right_on='orgunituid',
                                 how='left')
    PMTCT_EID_HEI_POS = PMTCT_EID_HEI_POS.drop(columns='orgunituid')

    PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_EID'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_EID'].eq(PMTCT_EID_HEI_POS['Genie_PMTCT_EID']) | (
                    PMTCT_EID_HEI_POS['Import File_PMTCT_EID'].isna() & PMTCT_EID_HEI_POS['Genie_PMTCT_EID'].isna()))

    PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_HEI_POS_ART'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS_ART'].eq(PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS_ART']) | (
                    PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS_ART'].isna() & PMTCT_EID_HEI_POS[
                'Genie_PMTCT_HEI_POS_ART'].isna()))

    PMTCT_EID_HEI_POS['Genie vs Import File_PMTCT_HEI_POS'] = (
                PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS'].eq(PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS']) | (
                    PMTCT_EID_HEI_POS['Import File_PMTCT_HEI_POS'].isna() & PMTCT_EID_HEI_POS[
                'Genie_PMTCT_HEI_POS'].isna()))

    PMTCT_EID_HEI_POS['<1 Genie vs Import File_TX_NEW'] = (
                PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].eq(PMTCT_EID_HEI_POS['<1 Genie_TX_NEW']) | (
                    PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].isna() & PMTCT_EID_HEI_POS['<1 Genie_TX_NEW'].isna()))

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_POS_ART = TX_NEW <1'] = (
                PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].eq(PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS_ART']) | (
                    PMTCT_EID_HEI_POS['<1 Import File_TX_NEW'].isna() & PMTCT_EID_HEI_POS[
                'Genie_PMTCT_HEI_POS_ART'].isna()))

    PMTCT_EID_HEI_POS['% Yield'] = (
                (PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS'] / PMTCT_EID_HEI_POS['Genie_PMTCT_EID']) * 100).round(1)

    PMTCT_EID_HEI_POS['Level 2 Check: PMTCT_HEI_ART >  PMTCT_HEI_POS'] = PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS_ART'] > \
                                                                         PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS']

    PMTCT_EID_HEI_POS['Level 2: % Linkage'] = (
                (PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS_ART'] / PMTCT_EID_HEI_POS['Genie_PMTCT_HEI_POS']) * 100).round(
        1)

    def calculate_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low LINKAGE"
        elif pd.notna(value) and value > 80:
            return "Good LINKAGE"
        else:
            return ""

    PMTCT_EID_HEI_POS['Level 2 Check: % Linkage status'] = PMTCT_EID_HEI_POS['Level 2: % Linkage'].apply(
        calculate_linkage)

    return PMTCT_EID_HEI_POS
