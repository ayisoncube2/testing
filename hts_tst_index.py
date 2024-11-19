import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'HTS_TST_INDEX'
districts = get_districts()
is_HTS_TST_INDEX_reported = True


# Function to download the Indicator Excel File
def download_excel(HTS_TST_INDEX, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, HTS_TST_INDEX, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, HTS_TST_INDEX, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        HTS_TST_INDEX.to_excel(writer, sheet_name='Main', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        HTS_TST_INDEX.to_excel(writer, sheet_name='Main', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        HTS_TST_INDEX.to_excel(writer, sheet_name='Main', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        HTS_TST_INDEX.to_excel(writer, sheet_name='Main', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_hts_tst_index_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, non_tier, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        HTS_Index_genie = first_genie[first_genie['standardizeddisaggregate'] == '4:Age/Sex/Result']

        Index_HTS_TST = HTS_Index_genie[
            HTS_Index_genie['categoryoptioncomboname'].str.contains('Newly Tested Positives|New Negatives')]

        Index_HTS_TST_POS = HTS_Index_genie[
            HTS_Index_genie['categoryoptioncomboname'].str.contains('Newly Tested Positives')]

        Index_Known_HTS_TST_POS = HTS_Index_genie[
            HTS_Index_genie['categoryoptioncomboname'].str.contains('Known Positives')]

        Index_HTS_TST = Index_HTS_TST.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                                  values=_1stG_curr_qtr,
                                                  aggfunc='sum')
        Index_HTS_TST = pd.DataFrame(Index_HTS_TST).reset_index()
        Index_HTS_TST = Index_HTS_TST.rename(columns={'4:Age/Sex/Result': 'Previous_Index_HTS_TST'})

        Index_HTS_TST_POS = Index_HTS_TST_POS.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                                          values=_1stG_curr_qtr,
                                                          aggfunc='sum')
        Index_HTS_TST_POS = pd.DataFrame(Index_HTS_TST_POS).reset_index()
        Index_HTS_TST_POS = Index_HTS_TST_POS.rename(columns={'4:Age/Sex/Result': 'Previous_Index_HTS_TST_POS'})

        Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.pivot_table(index=['orgunituid'],
                                                                      columns=['standardizeddisaggregate'],
                                                                      values=_1stG_curr_qtr,
                                                                      aggfunc='sum')
        Index_Known_HTS_TST_POS = pd.DataFrame(Index_Known_HTS_TST_POS).reset_index()
        Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.rename(
            columns={'4:Age/Sex/Result': 'Previous_Index_Known_HTS_TST_POS'})

        HTS_Index = pd.merge(mfl, Index_HTS_TST, left_on='DATIM UID', right_on='orgunituid', how='left')
        HTS_Index = HTS_Index.drop(columns='orgunituid')

        HTS_Index = pd.merge(HTS_Index, Index_HTS_TST_POS, left_on='DATIM UID', right_on='orgunituid', how='left')
        HTS_Index = HTS_Index.drop(columns='orgunituid')

        HTS_Index = pd.merge(HTS_Index, Index_Known_HTS_TST_POS, left_on='DATIM UID', right_on='orgunituid', how='left')
        HTS_Index = HTS_Index.drop(columns='orgunituid')

        HTS_Index_genie = first_genie.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                                  values=_1stG_curr_qtr,
                                                  aggfunc='sum')
        HTS_Index_genie = pd.DataFrame(HTS_Index_genie).reset_index()

        HTS_Index_genie = HTS_Index_genie.rename(
            columns={'1:Age/Sex/IndexCasesOffered': 'Previous_Cases Offered Index Services',
                     '2:Age/Sex/IndexCasesAccepted': 'Previous_Cases Accepted Index Services',
                     '3:Age Aggregated/Sex/Contacts': 'Previous_Contacts Elicited'})

        HTS_Index_genie = HTS_Index_genie.drop(columns=['4:Age/Sex/Result'])

        # merge with first genie
        HTS_TST_INDEX = pd.merge(HTS_Index, HTS_Index_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgunituid')

        HTS_TST_INDEX = HTS_TST_INDEX[['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA',
         'Previous_Index_HTS_TST', 'Previous_Index_HTS_TST_POS',
         'Previous_Index_Known_HTS_TST_POS',
         'Previous_Cases Offered Index Services',
         'Previous_Cases Accepted Index Services', 'Previous_Contacts Elicited']]

        if step == 'MER File 1':

            HTS_TST_INDEX = run_first_mer(HTS_TST_INDEX, mer_file1)

            summary_df = None

            # Button to trigger download
            download_excel(HTS_TST_INDEX, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            HTS_TST_INDEX = run_second_mer(HTS_TST_INDEX, mer_file1, mer_file2)

            summary_df = None

            # Button to trigger download
            download_excel(HTS_TST_INDEX, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            HTS_TST_INDEX = run_non_tier(HTS_TST_INDEX, mer_file1, mer_file2, non_tier, mfl)

            summary_df = None

            # Button to trigger download
            download_excel(HTS_TST_INDEX, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':

            HTS_TST_INDEX = run_new_genie(HTS_TST_INDEX, mer_file1, mer_file2, non_tier, new_genie_df, fiscal_year_2ndG,
                                          _2ndG_curr_qtr, mfl)
            summary_df = None

            # # Button to trigger download
            download_excel(HTS_TST_INDEX, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return
        else:
            st.write("No step was selected")


def run_first_mer(HTS_TST_INDEX, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Denom_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Denom')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_PVLS_D'})
    # merge with first genie
    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Numer_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_PVLS_Numer')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_PVLS_N'})

    # merge with first genie
    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='UID')

    HTS_TST_INDEX['uVL'] = HTS_TST_INDEX['MER report 1st submission_TX_PVLS_D'] - HTS_TST_INDEX[
        'MER report 1st submission_TX_PVLS_N']

    return HTS_TST_INDEX


def run_second_mer(HTS_TST_INDEX, mer_file1, mer_file2):
    # run first mer
    HTS_TST_INDEX = run_first_mer(HTS_TST_INDEX, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Denom_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Denom')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_PVLS_D'})

    # merge with first genie
    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='UID')

    kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Numer_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_PVLS_Numer')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_PVLS_N'})

    # merge with first genie
    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, mer, left_on='OU5uid', right_on='UID', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='UID')

    HTS_TST_INDEX['uVL'] = HTS_TST_INDEX['MER report 2nd submission_TX_PVLS_D'] - HTS_TST_INDEX[
        'MER report 2nd submission_TX_PVLS_N']

    return HTS_TST_INDEX


def run_non_tier(HTS_TST_INDEX, mer_file1, mer_file2, non_tier, mfl):
    HTS_TST_INDEX = run_second_mer(HTS_TST_INDEX, mer_file1, mer_file2)

    def read_and_filter_data(file_path, sheet_name, columns_to_drop, filter_column, districts):
        df = pd.read_excel(file_path, sheet_name=sheet_name).drop(columns=columns_to_drop)
        filtered_df = df[(df[filter_column] == 'New Positive') & df['District'].isin(districts)]
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
    # tb_Stat_num.head(2)

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

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, import_non_tier, on='DATIM UID', how='left')

    HTS_TST_INDEX['Pool'] = HTS_TST_INDEX['uVL'] + HTS_TST_INDEX['Import File_HTS_TST_POS']

    non_tier_CasesOffered = non_tier[non_tier['dataElement'].str.contains('CasesOffered')]

    casesOffered = non_tier_CasesOffered.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()

    casesOffered = casesOffered.rename(columns={'value': 'Cases Offered Index Services'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, casesOffered, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    casesAccepted_tier = non_tier[non_tier['dataElement'].str.contains('CasesAccepted')]

    casesAccepted = casesAccepted_tier.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()

    casesAccepted = casesAccepted.rename(columns={'value': 'Cases Accepted Index Services'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, casesAccepted, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    contacts_tier = non_tier[non_tier['dataElement'].str.contains('Contacts')]

    contacts = contacts_tier.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()

    contacts = contacts.rename(columns={'value': 'Contacts Elicited'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, contacts, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    sel = ['HTS_INDEX (N, TA, Index/Age/Sex/Result): HTS Result',
           'HTS_INDEX (N, DSD, Index/Age/Sex/Result): HTS Result']
    Index_HTS_TST = non_tier[non_tier['dataElement'].isin(sel)]

    Index_HTS_TST = Index_HTS_TST[
        Index_HTS_TST['categoryOptionComboName'].str.contains('Newly Tested Positives') | Index_HTS_TST[
            'categoryOptionComboName'].str.contains('New Negatives')]

    Index_HTS_TST = Index_HTS_TST.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()

    Index_HTS_TST = Index_HTS_TST.rename(columns={'value': 'Index_HTS_TST'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, Index_HTS_TST, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    Index_HTS_TST_POS = non_tier[non_tier['dataElement'].isin(sel)]
    Index_HTS_TST_POS = Index_HTS_TST_POS[
        Index_HTS_TST_POS['categoryOptionComboName'].str.contains('Newly Tested Positives')]

    Index_HTS_TST_POS = Index_HTS_TST_POS.pivot_table(index='orgUnit_uid', values='value', aggfunc='sum').reset_index()

    Index_HTS_TST_POS = Index_HTS_TST_POS.rename(columns={'value': 'Index_HTS_TST_POS'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, Index_HTS_TST_POS, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    Index_Known_HTS_TST_POS = non_tier[non_tier['dataElement'].isin(sel)]
    Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS[
        Index_Known_HTS_TST_POS['categoryOptionComboName'].str.contains('Known Positives')]

    Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.pivot_table(index='orgUnit_uid', values='value',
                                                                  aggfunc='sum').reset_index()

    Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.rename(columns={'value': 'Index_Known_HTS_TST_POS'})

    HTS_TST_INDEX = pd.merge(HTS_TST_INDEX, Index_Known_HTS_TST_POS, left_on='DATIM UID', right_on='orgUnit_uid',
                             how='left')
    HTS_TST_INDEX = HTS_TST_INDEX.drop(columns='orgUnit_uid')

    HTS_TST_INDEX['Client Offer Rate (%) (pool of uVl +HTS_TST_POS)'] = HTS_TST_INDEX['Contacts Elicited'] / \
                                                                        HTS_TST_INDEX['Pool']

    HTS_TST_INDEX['Client Offer Rate (%) (HTS_TST_POS)'] = HTS_TST_INDEX['Contacts Elicited'] / HTS_TST_INDEX[
        'Import File_HTS_TST_POS']

    HTS_TST_INDEX['Client Acceptance Rate (%)'] = HTS_TST_INDEX['Cases Accepted Index Services'] / HTS_TST_INDEX[
        'Cases Offered Index Services']

    HTS_TST_INDEX['Contacts Elicited Rate'] = HTS_TST_INDEX['Contacts Elicited'] / HTS_TST_INDEX[
        'Cases Accepted Index Services']

    HTS_TST_INDEX['Contact Test Rate (%)'] = HTS_TST_INDEX['Index_HTS_TST'] / HTS_TST_INDEX['Contacts Elicited']

    HTS_TST_INDEX['%Yield '] = HTS_TST_INDEX['Index_HTS_TST_POS'] / HTS_TST_INDEX['Index_HTS_TST']

    HTS_TST_INDEX['Level 2 Check: Pool<Index_offered'] = HTS_TST_INDEX['Pool'] < HTS_TST_INDEX['Contacts Elicited']

    HTS_TST_INDEX['Level 2 Check: Index_offered<Index_accepted'] = HTS_TST_INDEX['Contacts Elicited'] < HTS_TST_INDEX[
        'Cases Accepted Index Services']

    HTS_TST_INDEX['Level 2 Check: Index_contacts<Index_contacts_pos'] = HTS_TST_INDEX['Contacts Elicited'] < \
                                                                        HTS_TST_INDEX['Index_HTS_TST_POS']

    HTS_TST_INDEX['Level 2 Check: Index_contacts< contacts_ new_pos + contacts_ known_pos'] = HTS_TST_INDEX[
                                                                                                  'Contacts Elicited'] < (
                                                                                                      HTS_TST_INDEX[
                                                                                                          'Index_HTS_TST_POS'] +
                                                                                                      HTS_TST_INDEX[
                                                                                                          'Index_Known_HTS_TST_POS'])

    HTS_TST_INDEX['Level 2 Check: Index_contacts =contacts_ new_pos + contacts_ new_neg + contacts_ known_pos'] = \
        HTS_TST_INDEX['Contacts Elicited'] == (
                HTS_TST_INDEX['Index_HTS_TST'] + HTS_TST_INDEX['Index_Known_HTS_TST_POS'])

    return HTS_TST_INDEX


def run_new_genie(HTS_TST_INDEX, mer_file1, mer_file2, non_tier, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr, mfl):

    HTS_TST_INDEX = run_non_tier(HTS_TST_INDEX, mer_file1, mer_file2, non_tier, mfl)

    second_genie = second_genie[
        (second_genie['indicator'] == 'HTS_INDEX') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'DATIM')]

    HTS_Index_genie = second_genie[second_genie['standardizeddisaggregate'] == '4:Age/Sex/Result']

    Index_HTS_TST = HTS_Index_genie[
        HTS_Index_genie['categoryoptioncomboname'].str.contains('Newly Tested Positives|New Negatives')]

    Index_HTS_TST_POS = HTS_Index_genie[
        HTS_Index_genie['categoryoptioncomboname'].str.contains('Newly Tested Positives')]

    Index_Known_HTS_TST_POS = HTS_Index_genie[
        HTS_Index_genie['categoryoptioncomboname'].str.contains('Known Positives')]

    Index_HTS_TST = Index_HTS_TST.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                              values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    Index_HTS_TST = pd.DataFrame(Index_HTS_TST).reset_index()
    Index_HTS_TST = Index_HTS_TST.rename(columns={'4:Age/Sex/Result': 'Genie_Index_HTS_TST'})

    Index_HTS_TST_POS = Index_HTS_TST_POS.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                                      values=_2ndG_curr_qtr,
                                                      aggfunc='sum')
    Index_HTS_TST_POS = pd.DataFrame(Index_HTS_TST_POS).reset_index()
    Index_HTS_TST_POS = Index_HTS_TST_POS.rename(columns={'4:Age/Sex/Result': 'Genie_Index_HTS_TST_POS'})

    Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.pivot_table(index=['orgunituid'],
                                                                  columns=['standardizeddisaggregate'],
                                                                  values=_2ndG_curr_qtr,
                                                                  aggfunc='sum')
    Index_Known_HTS_TST_POS = pd.DataFrame(Index_Known_HTS_TST_POS).reset_index()
    Index_Known_HTS_TST_POS = Index_Known_HTS_TST_POS.rename(
        columns={'4:Age/Sex/Result': 'Genie_Index_Known_HTS_TST_POS'})

    HTS_Index = pd.merge(HTS_TST_INDEX, Index_HTS_TST, left_on='DATIM UID', right_on='orgunituid', how='left')

    HTS_Index = HTS_Index.drop(columns='orgunituid')

    HTS_Index = pd.merge(HTS_Index, Index_HTS_TST_POS, left_on='DATIM UID', right_on='orgunituid', how='left')
    HTS_Index = HTS_Index.drop(columns='orgunituid')

    HTS_Index = pd.merge(HTS_Index, Index_Known_HTS_TST_POS, left_on='DATIM UID', right_on='orgunituid', how='left')
    HTS_Index = HTS_Index.drop(columns='orgunituid')

    HTS_Index_genie = second_genie.pivot_table(index=['orgunituid'], columns=['standardizeddisaggregate'],
                                               values=_2ndG_curr_qtr,
                                               aggfunc='sum')
    HTS_Index_genie = pd.DataFrame(HTS_Index_genie).reset_index()

    HTS_Index_genie = HTS_Index_genie.rename(
        columns={'1:Age/Sex/IndexCasesOffered': 'Genie_Cases Offered Index Services',
                 '2:Age/Sex/IndexCasesAccepted': 'Genie_Cases Accepted Index Services',
                 '3:Age Aggregated/Sex/Contacts': 'Genie_Contacts Elicited'})

    HTS_Index_genie = HTS_Index_genie.drop(columns=['4:Age/Sex/Result'])

    # merge with first genie
    HTS_TST_INDEX = pd.merge(HTS_Index, HTS_Index_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    # HTS_TST_INDEX = HTS_Index.drop(columns='orgunituid')

    return HTS_TST_INDEX
