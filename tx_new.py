import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_NEW'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_NEW, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_NEW, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_NEW[TX_NEW[
                                      'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_NEW'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_NEW', index=False)

        level_1_check_df = TX_NEW[TX_NEW[
                                      'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST_POS'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_NEW[TX_NEW['MER report 1st submission vs 2nd submission_TX_NEW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TX_NEW', index=False)

        mer1_vs_mer2 = TX_NEW[TX_NEW['MER report 1st submission vs 2nd submission_HTS_TST_POS'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_mer2 = TX_NEW[TX_NEW['MER report 2nd submission vs Import File_TX_NEW'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TX_NEW', index=False)

        Import_vs_mer2 = TX_NEW[TX_NEW['MER report 2nd submission vs Import File_HTS_TST_POS'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_HTS_TST_POS', index=False)

        support_typecheck = TX_NEW[TX_NEW['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_mer2 = TX_NEW[TX_NEW['Import File vs Genie_TX_NEW'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_TX_NEW', index=False)

        Import_vs_mer2 = TX_NEW[TX_NEW['Import File vs Genie_HTS_TST_POS'] == False]
        Import_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_new_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df, non_tier):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        TX_NEW_genie = first_genie[
            (first_genie['indicator'] == 'TX_NEW') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]
        TX_NEW_genie = TX_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                aggfunc='sum')
        TX_NEW_genie = pd.DataFrame(TX_NEW_genie).reset_index()
        TX_NEW_genie = TX_NEW_genie.rename(columns={'TX_NEW': 'Previous_QTR_TX_NEW'})

        # merge with first genie
        TX_NEW = pd.merge(mfl, TX_NEW_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_NEW = TX_NEW.drop(columns='orgunituid')

        HTS_TST_POS_genie = first_genie[
            (first_genie['indicator'] == 'HTS_TST_POS') & (first_genie['fiscal_year'] == fiscal_year_1stG)]
        HTS_TST_POS_genie = HTS_TST_POS_genie[
            (HTS_TST_POS_genie['standardizeddisaggregate'] == 'Modality/Age/Sex/Result') & (
                        HTS_TST_POS_genie['statushiv'] == 'Positive')]

        HTS_TST_POS_genie = HTS_TST_POS_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                          values=_1stG_curr_qtr, aggfunc='sum')
        HTS_TST_POS_genie = pd.DataFrame(HTS_TST_POS_genie).reset_index()

        HTS_TST_POS_genie = HTS_TST_POS_genie.rename(columns={'HTS_TST_POS': 'Previous_QTR_HTS_TST_POS'})

        TX_NEW = pd.merge(TX_NEW, HTS_TST_POS_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_NEW = TX_NEW.drop(columns=['orgunituid'])

        TX_NEW['% Linkage'] = ((TX_NEW['Previous_QTR_HTS_TST_POS'] / TX_NEW['Previous_QTR_TX_NEW']) * 100).round(2)
        TX_NEW['Level 2 Check: % Linkage  status'] = TX_NEW['% Linkage'].apply(
            lambda x: "Extremely low LINKAGE" if x < 80 else ("Good LINKAGE" if x >= 80 else ''))

        if step == 'MER File 1':
            TX_NEW = run_first_mer(TX_NEW, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_NEW', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_TX_NEW', 'MER report 1st submission_HTS_TST_POS']

            summary_df = TX_NEW.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TX_NEW = run_second_mer(TX_NEW, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TX_NEW', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_TX_NEW', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_TX_NEW', 'MER report 2nd submission_HTS_TST_POS']

            summary_df = TX_NEW.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TX_NEW = run_tier(TX_NEW, mer_file1, mer_file2, tier_df, non_tier, mfl)

            # step 4 output
            summary_cols = ['Previous_QTR_TX_NEW', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_TX_NEW', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_TX_NEW', 'MER report 2nd submission_HTS_TST_POS',
                            'Import File_TX_NEW', 'Import File_HTS_TST_POS']

            summary_df = TX_NEW.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TX_NEW = run_new_genie(TX_NEW, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr, non_tier, mfl)

            # step 5 output
            summary_cols = ['Previous_QTR_TX_NEW', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_TX_NEW', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_TX_NEW', 'MER report 2nd submission_HTS_TST_POS',
                            'Import File_TX_NEW', 'Import File_HTS_TST_POS',
                            'Genie_TX_NEW', 'Genie_HTS_TST_POS']

            summary_df = TX_NEW.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TX_NEW, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_NEW'})

    # merge with first genie
    TX_NEW = pd.merge(TX_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_NEW = TX_NEW.drop(columns='UID')

    # Track Second Submission: TX_NEW
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_NEW'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_NEW'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_NEW[qtr_data_check] = TX_NEW.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    mer1_hts_tst = read_and_filter_data(mer_file1, 'HTS_TST',
                                        ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup'], 'HIVTestResult',
                                        districts)
    mer1_hts_tstkp = read_and_filter_data(mer_file1, 'HTS_TST_KP',
                                          ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup', 'KP_Location',
                                           'KP_Type'
                                           ], 'HIVTestResult', districts)

    appended_df_mer1 = pd.concat([mer1_hts_tst, mer1_hts_tstkp], ignore_index=True)

    mer1_hts_tst_pos = appended_df_mer1.pivot_table(index='UID', values='Total', aggfunc='sum').reset_index().rename(
        columns={'Total': 'MER report 1st submission_HTS_TST_POS'})

    TX_NEW = pd.merge(TX_NEW, mer1_hts_tst_pos, left_on='OU5uid', right_on='UID', how='left')
    TX_NEW = TX_NEW.drop(columns='UID')

    # Track Second Submission: HTS_TST_POS
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST_POS'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_HTS_TST_POS'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_NEW[qtr_data_check] = TX_NEW.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    TX_NEW['% Linkage'] = ((TX_NEW['MER report 1st submission_HTS_TST_POS'] / TX_NEW[
        'MER report 1st submission_TX_NEW']) * 100).round(2)
    TX_NEW['Level 2 Check: % Linkage  status'] = TX_NEW['% Linkage'].apply(
        lambda x: "Extremely low LINKAGE" if x < 80 else ("Good LINKAGE" if x >= 80 else ''))

    return TX_NEW


def run_second_mer(TX_NEW, mer_file1, mer_file2):
    # run first mer
    TX_NEW = run_first_mer(TX_NEW, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='TX_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_NEW'})

    # merge with first genie
    TX_NEW = pd.merge(TX_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_NEW = TX_NEW.drop(columns='UID')

    TX_NEW['MER report 1st submission vs 2nd submission_TX_NEW'] = (
                TX_NEW['MER report 1st submission_TX_NEW'].eq(TX_NEW['MER report 2nd submission_TX_NEW']) | (
                    TX_NEW['MER report 1st submission_TX_NEW'].isna() & TX_NEW[
                'MER report 2nd submission_TX_NEW'].isna()))

    mer2_hts_tst = read_and_filter_data(mer_file2, 'HTS_TST',
                                        ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup'], 'HIVTestResult',
                                        districts)
    mer2_hts_tstkp = read_and_filter_data(mer_file2, 'HTS_TST_KP',
                                          ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup', 'KP_Location',
                                           'KP_Type'
                                           ], 'HIVTestResult', districts)

    appended_df_mer2 = pd.concat([mer2_hts_tst, mer2_hts_tstkp], ignore_index=True)

    mer2_hts_tst_pos = appended_df_mer2.pivot_table(index='UID', values='Total', aggfunc='sum').reset_index().rename(
        columns={'Total': 'MER report 2nd submission_HTS_TST_POS'})

    TX_NEW = pd.merge(TX_NEW, mer2_hts_tst_pos, left_on='OU5uid', right_on='UID', how='left')
    TX_NEW = TX_NEW.drop(columns='UID')

    TX_NEW['MER report 1st submission vs 2nd submission_HTS_TST_POS'] = (
                TX_NEW['MER report 1st submission_HTS_TST_POS'].eq(TX_NEW['MER report 2nd submission_HTS_TST_POS']) | (
                    TX_NEW['MER report 1st submission_HTS_TST_POS'].isna() & TX_NEW[
                'MER report 2nd submission_HTS_TST_POS'].isna()))

    TX_NEW['% Linkage'] = ((TX_NEW['MER report 2nd submission_HTS_TST_POS'] / TX_NEW[
        'MER report 2nd submission_TX_NEW']) * 100).round(2)
    TX_NEW['Level 2 Check: % Linkage  status'] = TX_NEW['% Linkage'].apply(
        lambda x: "Extremely low LINKAGE" if x < 80 else ("Good LINKAGE" if x >= 80 else ''))

    return TX_NEW


def run_tier(TX_NEW, mer_file1, mer_file2, tier, non_tier, mfl):
    # run the second mer
    TX_NEW = run_second_mer(TX_NEW, mer_file1, mer_file2)

    tx_new_tier = tier[tier['dataElement'].str.startswith('TX_NEW')]

    tx_new_tier['dataElement'] = tx_new_tier['dataElement'].apply(lambda x: 'TX_NEW' if x.startswith('TX_NEW') else x)

    TX_NEW_tier = tx_new_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                          aggfunc='sum')
    TX_NEW_tier = pd.DataFrame(TX_NEW_tier).reset_index()

    TX_NEW_tier = TX_NEW_tier.rename(columns={'TX_NEW': 'Import File_TX_NEW'})

    TX_NEW = pd.merge(TX_NEW, TX_NEW_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_NEW = TX_NEW.drop(columns=['orgUnit_uid'])

    TX_NEW['MER report 2nd submission vs Import File_TX_NEW'] = (
                TX_NEW['MER report 2nd submission_TX_NEW'].eq(TX_NEW['Import File_TX_NEW']) | (
                    TX_NEW['MER report 2nd submission_TX_NEW'].isna() & TX_NEW['Import File_TX_NEW'].isna()))

    TX_NEW['Support Type Check'] = (TX_NEW['DSD/TA'] == TX_NEW['supportType']) | (
                TX_NEW['supportType'].isna() | (TX_NEW['supportType'] == ''))

    non_kp = pd.read_excel(mer_file2, sheet_name='TB_STAT_Numer')
    non_kp = non_kp[non_kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['HIVStatus'] == 'New Positive']

    tb_Stat_num = non_kp.pivot_table(index='UID', values='Total', aggfunc='sum').reset_index().rename(
        columns={'Total': 'Mer 2'})

    tb_Stat = pd.merge(tb_Stat_num, mfl[['DATIM UID', 'OU5uid']], left_on='UID', right_on='OU5uid',
                       how='right')  # .drop(columns=['UID','OU5uid'])

    dataElementName = ['HTS_TST (N, TA, PMTCT PostANC1 Pregnant-L&D/Age/Sex/Result): HTS received results',
                       'HTS_TST (N, DSD, PMTCT PostANC1 Pregnant-L&D/Age/Sex/Result): HTS received results',
                       'HTS_INDEX (N, TA, Index/Age/Sex/Result): HTS Result',
                       'HTS_INDEX (N, DSD, Index/Age/Sex/Result): HTS Result',
                       'PMTCT_STAT (N, TA, Age/Sex/KnownNewResult): Known Results',
                       'PMTCT_STAT (N, DSD, Age/Sex/KnownNewResult): Known Results',
                       # 'HTS_INDEX (N, DSD, IndexMod/Age/Sex/Result): HTS Result',
                       'HTS_TST (N, TA, OtherPITC/Age/Sex/Result): HTS received results',
                       'HTS_TST (N, DSD, OtherPITC/Age/Sex/Result): HTS received results',
                       # 'HTS_TST (N, DSD, MobileMod/Age/Sex/Result): HTS received results'
                       ]

    import_df = non_tier[non_tier['dataElement'].isin(dataElementName)]

    import_df = import_df[import_df['categoryOptionComboName'].str.contains('Positive')]

    import_df = import_df[~import_df['categoryOptionComboName'].str.contains('Known Positives')]

    import_df['dataElement'] = 'HTS_TST_POS'

    import_df = import_df.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')

    import_df = pd.merge(import_df, mfl[['DATIM UID']], left_on='orgUnit_uid', right_on='DATIM UID', how='right')

    import_non_tier = pd.merge(tb_Stat, import_df, on='DATIM UID')
    import_non_tier['Mer 2'] = import_non_tier['Mer 2'].fillna(0)
    import_non_tier['HTS_TST_POS'] = import_non_tier['HTS_TST_POS'].fillna(0)

    import_non_tier['Import File_HTS_TST_POS'] = import_non_tier['Mer 2'] + import_non_tier['HTS_TST_POS']
    import_non_tier = import_non_tier.drop(columns=['Mer 2', 'HTS_TST_POS'])

    import_non_tier['Import File_HTS_TST_POS'].sum()
    import_non_tier = import_non_tier.drop(columns=['UID', 'OU5uid'])
    TX_NEW = pd.merge(TX_NEW, import_non_tier, on='DATIM UID', how='left')

    TX_NEW['MER report 2nd submission vs Import File_HTS_TST_POS'] = (
                TX_NEW['MER report 2nd submission_HTS_TST_POS'].eq(TX_NEW['Import File_HTS_TST_POS']) | (
                    TX_NEW['MER report 2nd submission_HTS_TST_POS'].isna() & TX_NEW['Import File_HTS_TST_POS'].isna()))

    TX_NEW.drop_duplicates(subset=['OU5name'], inplace=True)

    TX_NEW['% Linkage'] = ((TX_NEW['Import File_HTS_TST_POS'] / TX_NEW['Import File_TX_NEW']) * 100).round(2)
    TX_NEW['Level 2 Check: % Linkage  status'] = TX_NEW['% Linkage'].apply(
        lambda x: "Extremely low LINKAGE" if x < 80 else ("Good LINKAGE" if x >= 80 else ''))

    return TX_NEW


def run_new_genie(TX_NEW, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr, non_tier, mfl):  # df is new genie
    # run tier step
    TX_NEW = run_tier(TX_NEW, mer_file1, mer_file2, tier_df, non_tier, mfl)

    TX_NEW_genie = second_genie[
        (second_genie['indicator'] == 'TX_NEW') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    TX_NEW_genie = TX_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                            aggfunc='sum')
    TX_NEW_genie = pd.DataFrame(TX_NEW_genie).reset_index()
    TX_NEW_genie = TX_NEW_genie.rename(columns={'TX_NEW': 'Genie_TX_NEW'})

    # merge with first genie
    TX_NEW = pd.merge(TX_NEW, TX_NEW_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_NEW = TX_NEW.drop(columns='orgunituid')

    TX_NEW['Import File vs Genie_TX_NEW'] = (TX_NEW['Import File_TX_NEW'].eq(TX_NEW['Genie_TX_NEW']) | (
                TX_NEW['Import File_TX_NEW'].isna() & TX_NEW['Genie_TX_NEW'].isna()))

    HTS_TST_POS_genie = second_genie[
        (second_genie['indicator'] == 'HTS_TST_POS') & (second_genie['fiscal_year'] == fiscal_year_2ndG)]

    HTS_TST_POS_genie = HTS_TST_POS_genie[
        (HTS_TST_POS_genie['standardizeddisaggregate'] == 'Modality/Age/Sex/Result') & (
                    HTS_TST_POS_genie['statushiv'] == 'Positive')]

    HTS_TST_POS_genie = HTS_TST_POS_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                      aggfunc='sum')
    HTS_TST_POS_genie = pd.DataFrame(HTS_TST_POS_genie).reset_index()

    HTS_TST_POS_genie = HTS_TST_POS_genie.rename(columns={'HTS_TST_POS': 'Genie_HTS_TST_POS'})

    TX_NEW = pd.merge(TX_NEW, HTS_TST_POS_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_NEW = TX_NEW.drop(columns=['orgunituid'])

    TX_NEW['Import File vs Genie_HTS_TST_POS'] = (TX_NEW['Import File_HTS_TST_POS'].eq(TX_NEW['Genie_HTS_TST_POS']) | (
                TX_NEW['Import File_HTS_TST_POS'].isna() & TX_NEW['Genie_HTS_TST_POS'].isna()))

    TX_NEW['% Linkage'] = ((TX_NEW['Genie_HTS_TST_POS'] / TX_NEW['Genie_TX_NEW']) * 100).round(2)
    TX_NEW['Level 2 Check: % Linkage  status'] = TX_NEW['% Linkage'].apply(
        lambda x: "Extremely low LINKAGE" if x < 80 else ("Good LINKAGE" if x >= 80 else ''))

    return TX_NEW


def read_and_filter_data(file_path, sheet_name, columns_to_drop, filter_column, districts):
    df = pd.read_excel(file_path, sheet_name=sheet_name).drop(columns=columns_to_drop)
    filtered_df = df[(df[filter_column] == 'Positive (Reactive)') & df['District'].isin(districts)]
    filtered_df = filtered_df.drop(columns=['District', 'HIVTestResult', 'Facility', 'HIVTestOfferedIn'])
    return filtered_df
