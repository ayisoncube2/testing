import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings
warnings.filterwarnings("ignore")

indicator_name = 'PrEP_CT'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(PrEP_CT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, PrEP_CT, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)

    # Provide download link with automatic download
    # href = (f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" '
    #         f'download="{file_path}">Export Excel File</a>')

    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, PrEP_CT, summary_df, step):
    if step == 'MER File 1':
        PrEP_CT.to_excel(writer, sheet_name='Main', index=False)

        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = PrEP_CT[PrEP_CT[
                                       ('Level 1 Check: sites that had data in previous quarter but no data in '
                                        'current quarter_PrEP_CT')] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_PrEP_CT', index=False)

        level_1_check_df_agyw = PrEP_CT[PrEP_CT[
                                            ('Level 1 Check: sites that had data in previous quarter but no data '
                                             'in current quarter_PrEP_CT_AGYW')] == 'No data reported']
        level_1_check_df_agyw.to_excel(writer, sheet_name='Level 1 Check_PrEP_CT_AGYW', index=False)

        level_2 = PrEP_CT[PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_CT_AGYW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        PrEP_CT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = PrEP_CT[PrEP_CT['MER report 1st submission vs 2nd submission_PrEP_CT'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PrEP_CT', index=False)

        mer1_vs_mer2 = PrEP_CT[PrEP_CT['MER report 1st submission vs 2nd submission_PrEP_CT_AGYW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PrEP_CT_AGYW', index=False)

        level_2 = PrEP_CT[PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_CT_AGYW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Create Excel writer object
        # Write Main sheet
        PrEP_CT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_mer2 = PrEP_CT[PrEP_CT['MER report 2nd submission vs Import File_PrEP_CT'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Mer 2 vs Import_PrEP_CT', index=False)

        imp_vs_mer2 = PrEP_CT[PrEP_CT['MER report 2nd submission vs Import File_PrEP_CT_AGYW'] == False]
        imp_vs_mer2.to_excel(writer, sheet_name='Mer 2 vs Import_PrEP_CT_AGYW', index=False)

        level_2 = PrEP_CT[PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_CT_AGYW > PrEP_CT', index=False)

        support_typecheck = PrEP_CT[PrEP_CT['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        PrEP_CT.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        imp_vs_genie = PrEP_CT[PrEP_CT['Import File vs Genie_PrEP_CT'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_PrEP_CT', index=False)

        imp_vs_genie = PrEP_CT[PrEP_CT['Import File vs Genie_PrEP_CT_AGYW'] == False]
        imp_vs_genie.to_excel(writer, sheet_name='Import vs Genie_PrEP_CT_AGYW', index=False)

        level_2 = PrEP_CT[PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_CT_AGYW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_prep_ct_data(mfl, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    # districts = get_districts()
    fiscal_year_1stg = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (genie_df is not None) & (mfl is not None):
        # Process Genie data for PrEP_CT
        PrEP_CT = genie_df[(genie_df['indicator'] == 'PrEP_CT') &
                           (genie_df['fiscal_year'] == fiscal_year_1stg) &
                           (genie_df['source_name'] == 'DATIM')]

        PrEP_CT = PrEP_CT[(PrEP_CT['standardizeddisaggregate'] == 'Age/Sex')]
        PrEP_CT = PrEP_CT.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr, aggfunc='sum')
        PrEP_CT = pd.DataFrame(PrEP_CT).reset_index()
        PrEP_CT = PrEP_CT.rename(columns={'PrEP_CT': 'Previous_QTR'})

        # Merge MFL and Genie data
        PrEP_CT = pd.merge(mfl, PrEP_CT, left_on='DATIM UID', right_on='orgunituid', how='left')
        PrEP_CT = PrEP_CT.drop(columns='orgunituid')

        # Process Genie data for AGYW
        PrEP_CT_AGYW = genie_df[(genie_df['indicator'] == 'PrEP_CT') &
                                (genie_df['fiscal_year'] == fiscal_year_1stg) &
                                (genie_df['source_name'] == 'DATIM') &
                                (genie_df['sex'] == 'Female') &
                                (genie_df['ageasentered'].isin(['15-19', '20-24']))]

        PrEP_CT_AGYW = PrEP_CT_AGYW.pivot_table(index=['orgunituid'], values=_1stG_curr_qtr, aggfunc='sum')
        PrEP_CT_AGYW = pd.DataFrame(PrEP_CT_AGYW).reset_index()
        PrEP_CT_AGYW = PrEP_CT_AGYW.rename(columns={_1stG_curr_qtr: 'Previous_QTR_PrEP_CT_AGYW'})

        # Merge with main PrEP_CT
        PrEP_CT = pd.merge(PrEP_CT, PrEP_CT_AGYW, left_on='DATIM UID', right_on='orgunituid', how='left')

        if step == 'MER File 1':
            PrEP_CT = run_first_mer(PrEP_CT, mer_file1)

            # Create summary
            summary_df = PrEP_CT.groupby('OU3name')[
                ['Previous_QTR', 'Previous_QTR_PrEP_CT_AGYW', 'MER report 1st submission_PrEP_CT',
                 'MER report 1st submission_PrEP_CT_AGYW']].sum().reset_index()

            total_row = summary_df[
                ['Previous_QTR', 'Previous_QTR_PrEP_CT_AGYW', 'MER report 1st submission_PrEP_CT',
                 'MER report 1st submission_PrEP_CT_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_CT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'MER File 2':
            PrEP_CT = run_second_mer(PrEP_CT, mer_file1, mer_file2)

            summary_df = PrEP_CT.groupby('OU3name')[
                ['MER report 1st submission_PrEP_CT', 'MER report 2nd submission_PrEP_CT',
                 'MER report 1st submission_PrEP_CT_AGYW',
                 'MER report 2nd submission_PrEP_CT_AGYW']].sum().reset_index()

            total_row = summary_df[['MER report 1st submission_PrEP_CT', 'MER report 2nd submission_PrEP_CT',
                                    'MER report 1st submission_PrEP_CT_AGYW',
                                    'MER report 2nd submission_PrEP_CT_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_CT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            PrEP_CT = run_tier(PrEP_CT, mer_file1, mer_file2, tier_df)

            # Summary part
            summary_df = PrEP_CT.groupby('OU3name')[
                ['MER report 1st submission_PrEP_CT', 'MER report 2nd submission_PrEP_CT',
                 'MER report 1st submission_PrEP_CT_AGYW', 'MER report 2nd submission_PrEP_CT_AGYW',
                 'Import File_PrEP_CT', 'Import File_PrEP_CT_AGYW']].sum().reset_index()

            total_row = summary_df[['MER report 1st submission_PrEP_CT', 'MER report 2nd submission_PrEP_CT',
                                    'MER report 1st submission_PrEP_CT_AGYW', 'MER report 2nd submission_PrEP_CT_AGYW',
                                    'Import File_PrEP_CT', 'Import File_PrEP_CT_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_CT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            PrEP_CT = run_new_genie(PrEP_CT, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                    _2ndG_curr_qtr)

            # summary part
            summary_cols = ['MER report 1st submission_PrEP_CT', 'MER report 2nd submission_PrEP_CT',
                            'MER report 1st submission_PrEP_CT_AGYW', 'MER report 2nd submission_PrEP_CT_AGYW',
                            'Import File_PrEP_CT', 'Import File_PrEP_CT_AGYW', 'Genie_PrEP_CT', 'Genie_PrEP_CT_AGYW']

            summary_df = PrEP_CT.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_CT, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(PrEP_CT, mer_file1):
    # Process MER data for PrEP_CT
    kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]
    mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()
    mer = mer.rename(columns={'Total': 'MER report 1st submission_PrEP_CT'})

    # Merge with main PrEP_CT
    PrEP_CT = pd.merge(PrEP_CT, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_CT = PrEP_CT.drop(columns='UID')

    # Process MER data for AGYW
    kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT')
    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]
    mer_appended = pd.concat([non_kp, kp], ignore_index=True)
    mer_appended = mer_appended[(mer_appended['Sex'] == 'Female') &
                                (mer_appended['FineAgeGroup'].isin(['15-19', '20-24']))]
    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')
    mer = pd.DataFrame(mer).reset_index()
    mer = mer.rename(columns={'Total': 'MER report 1st submission_PrEP_CT_AGYW'})

    # Merge with main PrEP_CT
    PrEP_CT = pd.merge(PrEP_CT, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_CT = PrEP_CT.drop(columns='UID')

    # Additional calculations
    PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] = PrEP_CT['MER report 1st submission_PrEP_CT_AGYW'] > PrEP_CT[
        'MER report 1st submission_PrEP_CT']

    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PrEP_CT'
    PrEP_CT[qtr_data_check] = PrEP_CT.apply(
        lambda row: "Data Reported" if row[
                                           'MER report 1st submission_PrEP_CT'] >= 0 else "No data reported",
        axis=1)

    qtr_data_check_agyw = ('Level 1 Check: sites that had data in previous quarter but no data in current '
                           'quarter_PrEP_CT_AGYW')

    PrEP_CT[qtr_data_check_agyw] = PrEP_CT.apply(
        lambda row: "Data Reported" if row[
                                           'MER report 1st submission_PrEP_CT_AGYW'] >= 0 else "No data reported",
        axis=1)

    return PrEP_CT


def run_second_mer(PrEP_CT, mer_file1, mer_file2):
    # first run mer 1
    PrEP_CT = run_first_mer(PrEP_CT, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='PrEP_CT')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PrEP_CT'})
    # print(mer['MER report 2nd submission_PrEP_CT'].sum())

    # merge with first genie
    PrEP_CT = pd.merge(PrEP_CT, mer, left_on='OU5uid', right_on='UID', how='left')

    PrEP_CT = PrEP_CT.drop(columns='UID')
    # PrEP_CT.head(2)

    kp = pd.read_excel(mer_file2, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='PrEP_CT')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer_appended = mer_appended[
        (mer_appended['Sex'] == 'Female') & (mer_appended['FineAgeGroup'].isin(['15-19', '20-24']))]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PrEP_CT_AGYW'})

    # merge with first genie
    PrEP_CT = pd.merge(PrEP_CT, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_CT = PrEP_CT.drop(columns='UID')
    # PrEP_CT.head(2)

    PrEP_CT['MER report 1st submission vs 2nd submission_PrEP_CT'] = (
            PrEP_CT['MER report 1st submission_PrEP_CT'].eq(
                PrEP_CT['MER report 2nd submission_PrEP_CT']) | (
                    PrEP_CT['MER report 1st submission_PrEP_CT'].isna() &
                    PrEP_CT['MER report 2nd submission_PrEP_CT'].isna()))

    PrEP_CT['MER report 1st submission vs 2nd submission_PrEP_CT_AGYW'] = (
            PrEP_CT['MER report 1st submission_PrEP_CT_AGYW'].eq(
                PrEP_CT['MER report 2nd submission_PrEP_CT_AGYW']) | (
                    PrEP_CT['MER report 1st submission_PrEP_CT_AGYW'].isna() &
                    PrEP_CT['MER report 2nd submission_PrEP_CT_AGYW'].isna()))

    PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] = (PrEP_CT['MER report 2nd submission_PrEP_CT_AGYW'] >
                                         PrEP_CT['MER report 2nd submission_PrEP_CT'])

    return PrEP_CT


def run_tier(PrEP_CT, mer_file1, mer_file2, tier_df):
    # run the second mer
    PrEP_CT = run_second_mer(PrEP_CT, mer_file1, mer_file2)

    PrEP_CT_tier = tier_df[tier_df['dataElement'].isin(
        ['PrEP_CT (N, DSD, Age/Sex): Receiving PrEP', 'PrEP_CT (N, TA, Age/Sex): Receiving PrEP'])]

    PrEP_CT_tier['dataElement'] = PrEP_CT_tier['dataElement'].apply(
        lambda x: 'PrEP_CT' if x.startswith('PrEP_CT') else x)

    PrEP_CT_tier = PrEP_CT_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                            values='value', aggfunc='sum')

    PrEP_CT_tier = pd.DataFrame(PrEP_CT_tier).reset_index()

    PrEP_CT_tier = PrEP_CT_tier.rename(columns={'PrEP_CT': 'Import File_PrEP_CT'})

    PrEP_CT = pd.merge(PrEP_CT, PrEP_CT_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PrEP_CT = PrEP_CT.drop(columns=['orgUnit_uid'])

    PrEP_CT['Support Type Check'] = (PrEP_CT['DSD/TA'] == PrEP_CT['supportType']) | (
            PrEP_CT['supportType'].isna() | (PrEP_CT['supportType'] == ''))

    PrEP_CT['MER report 2nd submission vs Import File_PrEP_CT'] = (
            PrEP_CT['MER report 2nd submission_PrEP_CT'].eq(PrEP_CT['Import File_PrEP_CT']) | (
            PrEP_CT['MER report 2nd submission_PrEP_CT'].isna() & PrEP_CT[
        'Import File_PrEP_CT'].isna()))

    # PrEP_CT_AGYW
    tier2 = tier_df[tier_df['dataElement'].isin(
        ['PrEP_CT (N, DSD, Age/Sex): Receiving PrEP', 'PrEP_CT (N, TA, Age/Sex): Receiving PrEP'])]

    tier2[['Age', 'Gender']] = tier2['categoryOptionComboName'].str.split(',', expand=True).applymap(
        lambda x: x.strip() if isinstance(x, str) else x)

    PrEP_CT_AGYW_tier = tier2[(tier2['Gender'] == 'Female') & (tier2['Age'].isin(['15-19', '20-24']))]

    PrEP_CT_AGYW_tier = PrEP_CT_AGYW_tier.pivot_table(index=['orgUnit_uid'], values='value', aggfunc='sum')
    PrEP_CT_AGYW_tier = pd.DataFrame(PrEP_CT_AGYW_tier).reset_index()

    PrEP_CT_AGYW_tier = PrEP_CT_AGYW_tier.rename(columns={'value': 'Import File_PrEP_CT_AGYW'})

    PrEP_CT = pd.merge(PrEP_CT, PrEP_CT_AGYW_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PrEP_CT = PrEP_CT.drop(columns=['orgUnit_uid'])

    PrEP_CT['MER report 2nd submission vs Import File_PrEP_CT_AGYW'] = (
            PrEP_CT['MER report 2nd submission_PrEP_CT_AGYW'].eq(PrEP_CT['Import File_PrEP_CT_AGYW']) | (
            PrEP_CT['MER report 2nd submission_PrEP_CT_AGYW'].isna() & PrEP_CT[
        'Import File_PrEP_CT_AGYW'].isna()))

    PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] = PrEP_CT['Import File_PrEP_CT_AGYW'] > PrEP_CT['Import File_PrEP_CT']

    return PrEP_CT


def run_new_genie(PrEP_CT, mer_file1, mer_file2, tier_df, df, fiscal_year_2ndG, _2ndG_curr_qtr):  # df is new genie
    # call Tier
    PrEP_CT = run_tier(PrEP_CT, mer_file1, mer_file2, tier_df)

    PrEP_CT_genie = df[
        (df['indicator'] == 'PrEP_CT') & (df['fiscal_year'] == fiscal_year_2ndG) & (df['source_name'] == 'DATIM')]

    PrEP_CT_genie = PrEP_CT_genie[(PrEP_CT_genie['standardizeddisaggregate'] == 'Age/Sex')]

    PrEP_CT_genie = PrEP_CT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    PrEP_CT_genie = pd.DataFrame(PrEP_CT_genie).reset_index()

    print(PrEP_CT_genie['PrEP_CT'].sum())
    PrEP_CT_genie = PrEP_CT_genie.rename(columns={'PrEP_CT': 'Genie_PrEP_CT'})

    # merge with first genie
    PrEP_CT = pd.merge(PrEP_CT, PrEP_CT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')

    PrEP_CT['Import File vs Genie_PrEP_CT'] = (PrEP_CT['Import File_PrEP_CT'].eq(PrEP_CT['Genie_PrEP_CT']) | (
            PrEP_CT['Import File_PrEP_CT'].isna() & PrEP_CT['Genie_PrEP_CT'].isna()))

    PrEP_CT_AGYW_genie = df[
        (df['indicator'] == 'PrEP_CT') & (df['fiscal_year'] == fiscal_year_2ndG) & (df['source_name'] == 'DATIM')]

    PrEP_CT_AGYW_genie = PrEP_CT_AGYW_genie[
        (PrEP_CT_AGYW_genie['sex'] == 'Female') & (PrEP_CT_AGYW_genie['ageasentered'].isin(['15-19', '20-24']))]
    print(PrEP_CT_AGYW_genie.shape)

    PrEP_CT_AGYW = PrEP_CT_AGYW_genie.pivot_table(index=['orgunituid'], values=_2ndG_curr_qtr, aggfunc='sum')
    PrEP_CT_AGYW = pd.DataFrame(PrEP_CT_AGYW).reset_index()

    PrEP_CT_AGYW = PrEP_CT_AGYW.rename(columns={_2ndG_curr_qtr: 'Genie_PrEP_CT_AGYW'})

    PrEP_CT = pd.merge(PrEP_CT, PrEP_CT_AGYW, left_on='DATIM UID', right_on='orgunituid', how='left')

    PrEP_CT['Import File vs Genie_PrEP_CT_AGYW'] = (
            PrEP_CT['Import File_PrEP_CT_AGYW'].eq(PrEP_CT['Genie_PrEP_CT_AGYW']) | (
            PrEP_CT['Import File_PrEP_CT_AGYW'].isna() & PrEP_CT['Genie_PrEP_CT_AGYW'].isna()))

    PrEP_CT['PrEP_CT_AGYW > PrEP_CT'] = PrEP_CT['Genie_PrEP_CT_AGYW'] > PrEP_CT['Genie_PrEP_CT']

    return PrEP_CT
