import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'HTS_TST_POS'
districts = get_districts()
is_HTS_TST_POS_reported = True


# Function to download the Indicator Excel File
def download_excel(HTS_TST_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, HTS_TST_POS, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, HTS_TST_POS, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        HTS_TST_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)  # Write Level 1 Check sheet

        level_1_check_df = HTS_TST_POS[HTS_TST_POS[
                                           'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_HTS_TST', index=False)

        level_1_check_df = HTS_TST_POS[HTS_TST_POS[
                                           'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST_POS'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        HTS_TST_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = HTS_TST_POS[HTS_TST_POS['MER report 1st submission vs 2nd submission_HTS_TST'] == 'FALSE']
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_HTS_TST', index=False)

        mer1_vs_mer2 = HTS_TST_POS[HTS_TST_POS['MER report 1st submission vs 2nd submission_HTS_TST_POS'] == 'FALSE']
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        HTS_TST_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = HTS_TST_POS[HTS_TST_POS['MER report 2nd submission vs Import File_HTS_TST'] == 'FALSE']
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_HTS_TST', index=False)

        import_vs_mer2 = HTS_TST_POS[HTS_TST_POS['MER report 2nd submission vs Import File_HTS_TST_POS'] == 'FALSE']
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        HTS_TST_POS.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_genie = HTS_TST_POS[HTS_TST_POS['Import File vs Genie_HTS_TST'] == 'FALSE']
        import_vs_genie.to_excel(writer, sheet_name='Import vs genie_HTS_TST', index=False)

        import_vs_genie = HTS_TST_POS[HTS_TST_POS['Import File vs Genie_HTS_TST_POS'] == 'FALSE']
        import_vs_genie.to_excel(writer, sheet_name='Import vs genie_HTS_TST_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_hts_tst_pos_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, non_tier, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        HTS_TST_genie = first_genie[
            (first_genie['indicator'] == 'HTS_TST') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'Derived')]
        HTS_TST_genie = HTS_TST_genie[(HTS_TST_genie['standardizeddisaggregate'] == 'Modality/Age/Sex/Result') & (
                HTS_TST_genie['statushiv'] == 'Positive')]

        HTS_TST_genie = HTS_TST_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                  aggfunc='sum')
        HTS_TST_genie = pd.DataFrame(HTS_TST_genie).reset_index()
        HTS_TST_genie = HTS_TST_genie.rename(columns={'HTS_TST': 'Previous_QTR_HTS_TST'})

        # merge with first genie
        HTS_TST_POS = pd.merge(mfl, HTS_TST_genie, left_on='DATIM UID', right_on='orgunituid', how='left')

        HTS_TST_POS = HTS_TST_POS.drop(columns='orgunituid')

        HTS_TST_POS_genie = first_genie[
            (first_genie['indicator'] == 'HTS_TST_POS') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'Derived')]
        HTS_TST_POS_genie = HTS_TST_POS_genie[HTS_TST_POS_genie['categoryoptioncomboname'] == 'default']
        HTS_TST_POS_genie = HTS_TST_POS_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                          values=_1stG_curr_qtr, aggfunc='sum')
        HTS_TST_POS_genie = pd.DataFrame(HTS_TST_POS_genie).reset_index()

        HTS_TST_POS_genie = HTS_TST_POS_genie.rename(columns={'HTS_TST_POS': 'Previous_QTR_HTS_TST_POS'})

        HTS_TST_POS = pd.merge(HTS_TST_POS, HTS_TST_POS_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        HTS_TST_POS = HTS_TST_POS.drop(columns='orgunituid')

        if step == 'MER File 1':

            HTS_TST_POS = run_first_mer(HTS_TST_POS, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_HTS_TST', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_HTS_TST', 'MER report 1st submission_HTS_TST_POS']

            summary_df = HTS_TST_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_TST_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            HTS_TST_POS = run_second_mer(HTS_TST_POS, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_HTS_TST', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_HTS_TST', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_HTS_TST', 'MER report 2nd submission_HTS_TST_POS']

            summary_df = HTS_TST_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_TST_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            HTS_TST_POS = run_non_tier(HTS_TST_POS, mer_file1, mer_file2, non_tier, mfl)

            # step 4 output
            summary_cols = ['Previous_QTR_HTS_TST', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_HTS_TST', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_HTS_TST', 'MER report 2nd submission_HTS_TST_POS',
                            'Import File_HTS_TST_POS', 'Import File_HTS_TST']

            summary_df = HTS_TST_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_TST_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            HTS_TST_POS = run_new_genie(HTS_TST_POS, mer_file1, mer_file2, non_tier, new_genie_df, fiscal_year_2ndG,
                                        _2ndG_curr_qtr, mfl)
            #
            # step 5 output
            summary_cols = ['Previous_QTR_HTS_TST', 'Previous_QTR_HTS_TST_POS',
                            'MER report 1st submission_HTS_TST', 'MER report 1st submission_HTS_TST_POS',
                            'MER report 2nd submission_HTS_TST', 'MER report 2nd submission_HTS_TST_POS',
                            'Import File_HTS_TST_POS', 'Import File_HTS_TST',
                            'Genie_HTS_TST_POS', 'Genie_HTS_TST']

            summary_df = HTS_TST_POS.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(HTS_TST_POS, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(HTS_TST_POS, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='HTS_TST_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='HTS_TST')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_HTS_TST'})

    # # merge with first genie
    HTS_TST_POS = pd.merge(HTS_TST_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='UID')

    # Track Second Submission: HTS_TST
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_HTS_TST'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    HTS_TST_POS[qtr_data_check] = HTS_TST_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    kp = pd.read_excel(mer_file1, sheet_name='HTS_TST_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='HTS_TST')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer_appended = mer_appended[
        (mer_appended['HIVTestResult'] == 'Positive (Reactive)') & mer_appended['District'].isin(districts)]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_HTS_TST_POS'})

    # merge with first genie
    HTS_TST_POS = pd.merge(HTS_TST_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='UID')

    # Track Second Submission: HTS_TST_POS
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_HTS_TST_POS'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_HTS_TST_POS'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    HTS_TST_POS[qtr_data_check] = HTS_TST_POS.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    HTS_TST_POS['% Yield'] = ((HTS_TST_POS['MER report 1st submission_HTS_TST_POS'] / HTS_TST_POS[
        'MER report 1st submission_HTS_TST']) * 100).round(0)

    def check_linkage(percentage):
        try:
            if len(percentage) == 1:
                if percentage[0] < 80:
                    return "Extremely Low Yield"
                elif percentage[0] >= 80:
                    return "Good Yield"
            return ""
        except:
            return ""

    # Apply the function to each row and store the result in a new column
    HTS_TST_POS['Level 2 Check: % Yield status'] = HTS_TST_POS['% Yield'].apply(lambda x: check_linkage([x]))

    return HTS_TST_POS


def run_second_mer(HTS_TST_POS, mer_file1, mer_file2):
    # run first mer
    HTS_TST_POS = run_first_mer(HTS_TST_POS, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='HTS_TST_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='HTS_TST')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_HTS_TST'})

    # # merge with first genie
    HTS_TST_POS = pd.merge(HTS_TST_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='UID')

    HTS_TST_POS['MER report 1st submission vs 2nd submission_HTS_TST'] = (
            HTS_TST_POS['MER report 1st submission_HTS_TST'].eq(
                HTS_TST_POS['MER report 2nd submission_HTS_TST']) | (
                    HTS_TST_POS['MER report 1st submission_HTS_TST'].isna() & HTS_TST_POS[
                        'MER report 2nd submission_HTS_TST'].isna()))

    kp = pd.read_excel(mer_file2, sheet_name='HTS_TST_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='HTS_TST')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer_appended = mer_appended[
        (mer_appended['HIVTestResult'] == 'Positive (Reactive)') & mer_appended['District'].isin(districts)]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_HTS_TST_POS'})

    # merge with first genie
    HTS_TST_POS = pd.merge(HTS_TST_POS, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='UID')

    HTS_TST_POS['MER report 1st submission vs 2nd submission_HTS_TST_POS'] = (
            HTS_TST_POS['MER report 1st submission_HTS_TST_POS'].eq(
                HTS_TST_POS['MER report 2nd submission_HTS_TST_POS']) | (
                    HTS_TST_POS['MER report 1st submission_HTS_TST_POS'].isna() & HTS_TST_POS[
                        'MER report 2nd submission_HTS_TST_POS'].isna()))

    HTS_TST_POS['% Yield'] = ((HTS_TST_POS['MER report 2nd submission_HTS_TST_POS'] / HTS_TST_POS[
        'MER report 2nd submission_HTS_TST']) * 100).round(0)

    def check_linkage(percentage):
        try:
            if len(percentage) == 1:
                if percentage[0] < 80:
                    return "Extremely Low Yield"
                elif percentage[0] > 80:
                    return "Good Yield"
            return ""
        except:
            return ""

    # Apply the function to each row and store the result in a new column
    HTS_TST_POS['Level 2 Check: % Yield status'] = HTS_TST_POS['% Yield'].apply(lambda x: check_linkage([x]))

    return HTS_TST_POS


def run_non_tier(HTS_TST_POS, mer_file1, mer_file2, non_tier, mfl):
    HTS_TST_POS = run_second_mer(HTS_TST_POS, mer_file1, mer_file2)

    def read_and_filter_data(file_path, sheet_name, columns_to_drop, filter_column, districts_ls):
        df = pd.read_excel(file_path, sheet_name=sheet_name).drop(columns=columns_to_drop)
        filtered_df = df[(df[filter_column] == 'New Positive') & df['District'].isin(districts_ls)]
        filtered_df = filtered_df.drop(columns=['District', 'HIVStatus', 'Facility'])
        return filtered_df

    mer1 = read_and_filter_data(mer_file1, 'TB_STAT_Numer', ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup'],
                                'HIVStatus', districts)
    mer2 = read_and_filter_data(mer_file2, 'TB_STAT_Numer', ['Province', 'Sub District', 'Code', 'Sex', 'FineAgeGroup'],
                                'HIVStatus', districts)

    mer1_pivot_df = mer1.pivot_table(index='UID', values='Total', aggfunc='sum').reset_index().rename(
        columns={'Total': 'Mer 1'})
    mer2_pivot_df = mer2.pivot_table(index='UID', values='Total', aggfunc='sum').reset_index().rename(
        columns={'Total': 'Mer 2'})
    tb_Stat_num = mer1_pivot_df.merge(mer2_pivot_df)

    tb_Stat = pd.merge(tb_Stat_num, mfl[['DATIM UID', 'OU5uid']], left_on='UID', right_on='OU5uid', how='right').drop(
        columns=['UID', 'OU5uid'])

    dataElementName = ['HTS_TST (N, TA, PMTCT PostANC1 Pregnant-L&D/Age/Sex/Result): HTS received results',
                       'HTS_TST (N, DSD, PMTCT PostANC1 Pregnant-L&D/Age/Sex/Result): HTS received results',
                       'HTS_INDEX (N, TA, Index/Age/Sex/Result): HTS Result',
                       'HTS_INDEX (N, DSD, Index/Age/Sex/Result): HTS Result',
                       'PMTCT_STAT (N, TA, Age/Sex/KnownNewResult): Known Results',
                       'PMTCT_STAT (N, DSD, Age/Sex/KnownNewResult): Known Results',
                       'HTS_INDEX (N, DSD, IndexMod/Age/Sex/Result): HTS Result',
                       'HTS_TST (N, TA, OtherPITC/Age/Sex/Result): HTS received results',
                       'HTS_TST (N, DSD, OtherPITC/Age/Sex/Result): HTS received results',
                       'HTS_TST (N, DSD, MobileMod/Age/Sex/Result): HTS received results']

    import_df = non_tier[non_tier['dataElement'].isin(dataElementName)]

    import_df = import_df[import_df['categoryOptionComboName'].str.contains('Positive')]

    import_df = import_df[~import_df['categoryOptionComboName'].str.contains('Known Positives')]

    import_df['dataElement'] = 'HTS_TST_POS'

    import_df = import_df.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')

    import_non_tier = pd.merge(tb_Stat, import_df, left_on='DATIM UID', right_on='orgUnit_uid', how='left')

    import_non_tier['Import File_HTS_TST_POS'] = import_non_tier['Mer 2'] + import_non_tier['HTS_TST_POS']
    import_non_tier = import_non_tier.drop(columns=['Mer 1', 'Mer 2', 'HTS_TST_POS'])

    HTS_TST_POS = pd.merge(HTS_TST_POS, import_non_tier, on='DATIM UID', how='left')

    HTS_TST_POS['MER report 2nd submission vs Import File_HTS_TST_POS'] = (
            HTS_TST_POS['MER report 2nd submission_HTS_TST_POS'].eq(HTS_TST_POS['Import File_HTS_TST_POS']) | (
                HTS_TST_POS['MER report 2nd submission_HTS_TST_POS'].isna() & HTS_TST_POS[
                    'Import File_HTS_TST_POS'].isna()))

    hts_tier = non_tier[non_tier['dataElement'].isin(dataElementName)]
    hts_tier['dataElement'] = 'HTS_TST'

    hts_tier = hts_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')
    hts_tier = pd.DataFrame(hts_tier).reset_index()

    hts_tier = hts_tier.rename(columns={'HTS_TST': 'Import File_HTS_TST'})
    HTS_TST_POS = pd.merge(HTS_TST_POS, hts_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns=['orgUnit_uid'])

    HTS_TST_POS['MER report 2nd submission vs Import File_HTS_TST'] = (
            HTS_TST_POS['MER report 2nd submission_HTS_TST'].eq(HTS_TST_POS['Import File_HTS_TST']) | (
                HTS_TST_POS['MER report 2nd submission_HTS_TST'].isna() & HTS_TST_POS[
                    'Import File_HTS_TST'].isna()))

    HTS_TST_POS['% Yield'] = HTS_TST_POS['Import File_HTS_TST_POS'] / HTS_TST_POS['Import File_HTS_TST']

    def check_linkage(percentage):
        try:
            if len(percentage) == 1:
                if percentage[0] < 80:
                    return "Extremely Low Yield"
                elif percentage[0] > 80:
                    return "Good Yield"
            return ""
        except:
            return ""

    # Apply the function to each row and store the result in a new column
    HTS_TST_POS['Level 2 Check: % Yield status'] = HTS_TST_POS['% Yield'].apply(lambda x: check_linkage([x]))

    return HTS_TST_POS


def run_new_genie(HTS_TST_POS, mer_file1, mer_file2, non_tier, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr, mfl):  # df is new genie
    # run tier step
    HTS_TST_POS = run_non_tier(HTS_TST_POS, mer_file1, mer_file2, non_tier, mfl)

    HTS_TST_genie = second_genie[
        (second_genie['indicator'] == 'HTS_TST') & (second_genie['fiscal_year'] == fiscal_year_2ndG)]

    HTS_TST_genie = HTS_TST_genie[(HTS_TST_genie['standardizeddisaggregate'] == 'Modality/Age/Sex/Result') & (
            HTS_TST_genie['statushiv'] == 'Positive')]

    HTS_TST_genie = HTS_TST_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    HTS_TST_genie = pd.DataFrame(HTS_TST_genie).reset_index()
    HTS_TST_genie = HTS_TST_genie.rename(columns={'HTS_TST': 'Genie_HTS_TST'})

    # merge with first genie
    HTS_TST_POS = pd.merge(HTS_TST_POS, HTS_TST_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='orgunituid')

    HTS_TST_POS['Import File vs Genie_HTS_TST'] = (
            HTS_TST_POS['Import File_HTS_TST'].eq(HTS_TST_POS['Genie_HTS_TST']) | (
                HTS_TST_POS['Import File_HTS_TST'].isna() & HTS_TST_POS['Genie_HTS_TST'].isna()))

    HTS_TST_POS_genie = second_genie[
        (second_genie['indicator'] == 'HTS_TST_POS') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'Derived')]
    HTS_TST_POS_genie = HTS_TST_POS_genie[HTS_TST_POS_genie['categoryoptioncomboname'] == 'default']
    HTS_TST_POS_genie = HTS_TST_POS_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                      aggfunc='sum')
    HTS_TST_POS_genie = pd.DataFrame(HTS_TST_POS_genie).reset_index()

    HTS_TST_POS_genie = HTS_TST_POS_genie.rename(columns={'HTS_TST_POS': 'Genie_HTS_TST_POS'})

    HTS_TST_POS = pd.merge(HTS_TST_POS, HTS_TST_POS_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    HTS_TST_POS = HTS_TST_POS.drop(columns='orgunituid')

    HTS_TST_POS['Import File vs Genie_HTS_TST_POS'] = (
            HTS_TST_POS['Import File_HTS_TST_POS'].eq(HTS_TST_POS['Genie_HTS_TST_POS']) | (
                HTS_TST_POS['Import File_HTS_TST_POS'].isna() & HTS_TST_POS['Genie_HTS_TST_POS'].isna()))

    HTS_TST_POS['% Yield'] = HTS_TST_POS['Genie_HTS_TST_POS'] / HTS_TST_POS['Genie_HTS_TST']

    def check_linkage(percentage):
        try:
            if len(percentage) == 1:
                if percentage[0] < 80:
                    return "Extremely Low Yield"
                elif percentage[0] > 80:
                    return "Good Yield"
            return ""
        except:
            return ""

    # Apply the function to each row and store the result in a new column
    HTS_TST_POS['Level 2 Check: % Yield status'] = HTS_TST_POS['% Yield'].apply(lambda x: check_linkage([x]))

    return HTS_TST_POS
