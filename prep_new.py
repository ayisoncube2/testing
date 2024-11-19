import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings
warnings.filterwarnings("ignore")

indicator_name = 'PrEP_NEW'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(PrEP_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, PrEP_NEW, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, PrEP_NEW, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        PrEP_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Write Level 1 Check sheet
        level_1_check_df = PrEP_NEW[PrEP_NEW[
                                        'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PrEP_NEW'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_PrEP_NEW', index=False)

        level_1_check_df_agyw = PrEP_NEW[PrEP_NEW[
                                             'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PrEP_NEW_AGYW'] == 'No data reported']
        level_1_check_df_agyw.to_excel(writer, sheet_name='Level 1 Check_PrEP_NEW_AGYW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_NEW_AGYW > PrEP_NEW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP NEW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP NEW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        PrEP_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['MER report 1st submission vs 2nd submission_PrEP_NEW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PrEP_NEW', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['MER report 1st submission vs 2nd submission_PrEP_NEW_AGYW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_PrEP_NEW_AGYW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_NEW_AGYW > PrEP_NEW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP NEW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP NEW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        PrEP_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['MER report 2nd submission vs Import File_PrEP_NEW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 2 vs Import_PrEP_NEW', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['MER report 2nd submission vs Import File_PrEP_NEW_AGYW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 2 vs Import_PrEP_NEW_AGYW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_NEW_AGYW > PrEP_NEW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP NEW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP NEW > PrEP_CT', index=False)

        support_typecheck = PrEP_NEW[PrEP_NEW['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        PrEP_NEW.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['Import File vs Genie_PrEP_NEW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_PrEP_NEW', index=False)

        mer1_vs_mer2 = PrEP_NEW[PrEP_NEW['Import File vs Genie_PrEP_NEW_AGYW'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_PrEP_NEW_AGYW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] == True]
        level_2.to_excel(writer, sheet_name='PrEP_NEW_AGYW > PrEP_NEW', index=False)

        level_2 = PrEP_NEW[PrEP_NEW['PrEP NEW > PrEP_CT'] == True]
        level_2.to_excel(writer, sheet_name='PrEP NEW > PrEP_CT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_prep_new_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        # Genie and MFL Section
        PrEP_NEW = first_genie[
            (first_genie['indicator'] == 'PrEP_NEW') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'DATIM')]

        PrEP_NEW = PrEP_NEW[(PrEP_NEW['standardizeddisaggregate'] == 'Age/Sex')]

        PrEP_NEW = PrEP_NEW.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr, aggfunc='sum')
        PrEP_NEW = pd.DataFrame(PrEP_NEW).reset_index()
        PrEP_NEW = PrEP_NEW.rename(columns={'PrEP_NEW': 'Previous_QTR'})

        # merge with first genie
        PrEP_NEW = pd.merge(mfl, PrEP_NEW, left_on='DATIM UID', right_on='orgunituid', how='left')
        PrEP_NEW = PrEP_NEW.drop(columns='orgunituid')
        PrEP_NEW_AGYW = first_genie[
            (first_genie['indicator'] == 'PrEP_NEW') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'DATIM')]

        PrEP_NEW_AGYW = PrEP_NEW_AGYW[
            (PrEP_NEW_AGYW['sex'] == 'Female') & (PrEP_NEW_AGYW['ageasentered'].isin(['15-19', '20-24']))]

        PrEP_NEW_AGYW = PrEP_NEW_AGYW.pivot_table(index=['orgunituid'], values=_1stG_curr_qtr, aggfunc='sum')
        PrEP_NEW_AGYW = pd.DataFrame(PrEP_NEW_AGYW).reset_index()

        PrEP_NEW_AGYW = PrEP_NEW_AGYW.rename(columns={_1stG_curr_qtr: 'Previous_QTR_PrEP_NEW_AGYW'})
        # merge with first genie
        PrEP_NEW = pd.merge(PrEP_NEW, PrEP_NEW_AGYW, left_on='DATIM UID', right_on='orgunituid', how='left')

        if step == 'MER File 1':
            PrEP_NEW = run_first_mer(PrEP_NEW, mer_file1)

            # step 2 output
            summary_df = PrEP_NEW.groupby('OU3name')[
                ['Previous_QTR', 'Previous_QTR_PrEP_NEW_AGYW', 'MER report 1st submission_PrEP_NEW',
                 'MER report 1st submission_PrEP_NEW_AGYW']].sum().reset_index()

            total_row = summary_df[['Previous_QTR', 'Previous_QTR_PrEP_NEW_AGYW', 'MER report 1st submission_PrEP_NEW',
                                    'MER report 1st submission_PrEP_NEW_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            PrEP_NEW = run_second_mer(PrEP_NEW, mer_file1, mer_file2)

            # step 3 output
            summary_df = PrEP_NEW.groupby('OU3name')[
                ['MER report 1st submission_PrEP_NEW', 'MER report 2nd submission_PrEP_NEW',
                 'MER report 1st submission_PrEP_NEW_AGYW',
                 'MER report 2nd submission_PrEP_NEW_AGYW']].sum().reset_index()

            total_row = summary_df[['MER report 1st submission_PrEP_NEW', 'MER report 2nd submission_PrEP_NEW',
                                    'MER report 1st submission_PrEP_NEW_AGYW',
                                    'MER report 2nd submission_PrEP_NEW_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            PrEP_NEW = run_tier(PrEP_NEW, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_df = PrEP_NEW.groupby('OU3name')[
                ['MER report 1st submission_PrEP_NEW', 'MER report 2nd submission_PrEP_NEW',
                 'MER report 1st submission_PrEP_NEW_AGYW', 'MER report 2nd submission_PrEP_NEW_AGYW',
                 'Import File_PrEP_NEW', 'Import File_PrEP_NEW_AGYW']].sum().reset_index()

            total_row = summary_df[['MER report 1st submission_PrEP_NEW', 'MER report 2nd submission_PrEP_NEW',
                                    'MER report 1st submission_PrEP_NEW_AGYW',
                                    'MER report 2nd submission_PrEP_NEW_AGYW', 'Import File_PrEP_NEW',
                                    'Import File_PrEP_NEW_AGYW']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            PrEP_NEW = run_new_genie(PrEP_NEW, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                     _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['MER report 1st submission_PrEP_NEW', 'MER report 2nd submission_PrEP_NEW',
                            'MER report 1st submission_PrEP_NEW_AGYW', 'MER report 2nd submission_PrEP_NEW_AGYW',
                            'Import File_PrEP_NEW', 'Import File_PrEP_NEW_AGYW', 'Genie_PrEP_NEW',
                            'Genie_PrEP_NEW_AGYW']

            summary_df = PrEP_NEW.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PrEP_NEW, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(PrEP_NEW, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PrEP_NEW'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer_appended = mer_appended[
        (mer_appended['Sex'] == 'Female') & (mer_appended['Coarse Age Group'].isin(['15-19', '20-24']))]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PrEP_NEW_AGYW'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_PrEP_CT'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    PrEP_NEW['PrEP NEW > PrEP_CT'] = PrEP_NEW['MER report 1st submission_PrEP_NEW'] > PrEP_NEW[
        'MER report 1st submission_PrEP_CT']

    PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] = PrEP_NEW['MER report 1st submission_PrEP_NEW_AGYW'] > PrEP_NEW[
        'MER report 1st submission_PrEP_NEW']

    # Track Second Submission: Prp CT
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PrEP_NEW'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_PrEP_NEW'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PrEP_NEW[qtr_data_check] = PrEP_NEW.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    # Track Second Submission PrEP_NEW_AGYW
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_PrEP_NEW_AGYW'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_PrEP_NEW_AGYW'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    PrEP_NEW[qtr_data_check] = PrEP_NEW.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    return PrEP_NEW


def run_second_mer(PrEP_NEW, mer_file1, mer_file2):
    # first run mer 1
    PrEP_NEW = run_first_mer(PrEP_NEW, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='PrEP_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PrEP_NEW'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    kp = pd.read_excel(mer_file2, sheet_name='PrEP_NEW_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_NEW')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer_appended = mer_appended[
        (mer_appended['Sex'] == 'Female') & (mer_appended['Coarse Age Group'].isin(['15-19', '20-24']))]

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PrEP_NEW_AGYW'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    kp = pd.read_excel(mer_file2, sheet_name='PrEP_CT_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='PrEP_CT')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_PrEP_CT'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, mer, left_on='OU5uid', right_on='UID', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns='UID')

    PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] = PrEP_NEW['MER report 2nd submission_PrEP_NEW_AGYW'] > PrEP_NEW[
        'MER report 2nd submission_PrEP_NEW']
    PrEP_NEW['PrEP NEW > PrEP_CT'] = PrEP_NEW['MER report 2nd submission_PrEP_NEW'] > PrEP_NEW[
        'MER report 2nd submission_PrEP_CT']
    PrEP_NEW['MER report 1st submission vs 2nd submission_PrEP_NEW'] = (
            PrEP_NEW['MER report 1st submission_PrEP_NEW'].eq(PrEP_NEW['MER report 2nd submission_PrEP_NEW']) | (
            PrEP_NEW['MER report 1st submission_PrEP_NEW'].isna() & PrEP_NEW[
        'MER report 2nd submission_PrEP_NEW'].isna()))

    PrEP_NEW['MER report 1st submission vs 2nd submission_PrEP_NEW_AGYW'] = (
            PrEP_NEW['MER report 1st submission_PrEP_NEW_AGYW'].eq(
                PrEP_NEW['MER report 2nd submission_PrEP_NEW_AGYW']) | (
                    PrEP_NEW['MER report 1st submission_PrEP_NEW_AGYW'].isna() & PrEP_NEW[
                'MER report 2nd submission_PrEP_NEW_AGYW'].isna()))

    return PrEP_NEW


def run_tier(PrEP_NEW, mer_file1, mer_file2, tier):
    # run the second mer
    PrEP_NEW = run_second_mer(PrEP_NEW, mer_file1, mer_file2)

    PrEP_NEW_tier = tier[tier['dataElement'].str.startswith('PrEP_NEW')]
    PrEP_NEW_tier['dataElement'] = PrEP_NEW_tier['dataElement'].apply(
        lambda x: 'PrEP_NEW' if x.startswith('PrEP_NEW') else x)

    PrEP_NEW_tier = PrEP_NEW_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                              values='value', aggfunc='sum')
    PrEP_NEW_tier = pd.DataFrame(PrEP_NEW_tier).reset_index()

    PrEP_NEW_tier = PrEP_NEW_tier.rename(columns={'PrEP_NEW': 'Import File_PrEP_NEW'})

    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_NEW_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgUnit_uid'])
    PrEP_CT_tier = tier[tier['dataElement'].isin(
        ['PrEP_CT (N, DSD, Age/Sex): Receiving PrEP', 'PrEP_CT (N, TA, Age/Sex): Receiving PrEP'])]

    PrEP_CT_tier['dataElement'] = PrEP_CT_tier['dataElement'].apply(
        lambda x: 'PrEP_CT' if x.startswith('PrEP_CT') else x)

    PrEP_CT_tier = PrEP_CT_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value', aggfunc='sum')

    PrEP_CT_tier = pd.DataFrame(PrEP_CT_tier).reset_index()

    PrEP_CT_tier = PrEP_CT_tier.rename(columns={'PrEP_CT': 'Import File_PrEP_CT'})

    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_CT_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgUnit_uid'])
    PrEP_NEW['PrEP NEW > PrEP_CT'] = PrEP_NEW['Import File_PrEP_NEW'] > PrEP_NEW['Import File_PrEP_CT']
    PrEP_NEW['MER report 2nd submission vs Import File_PrEP_NEW'] = (
                PrEP_NEW['MER report 2nd submission_PrEP_NEW'].eq(PrEP_NEW['Import File_PrEP_NEW']) | (
                    PrEP_NEW['MER report 2nd submission_PrEP_NEW'].isna() & PrEP_NEW['Import File_PrEP_NEW'].isna()))
    PrEP_NEW['Support Type Check'] = (PrEP_NEW['DSD/TA'] == PrEP_NEW['supportType']) | (
                PrEP_NEW['supportType'].isna() | (PrEP_NEW['supportType'] == ''))
    # PrEP_NEW_AGYW
    tier2 = tier[tier['dataElement'].str.startswith('PrEP_NEW')]

    tier2[['Age', 'Gender']] = tier2['categoryOptionComboName'].str.split(',', expand=True).applymap(
        lambda x: x.strip() if isinstance(x, str) else x)

    PrEP_NEW_AGYW_tier = tier2[(tier2['Gender'] == 'Female') & (tier2['Age'].isin(['15-19', '20-24']))]

    PrEP_NEW_AGYW_tier = PrEP_NEW_AGYW_tier.pivot_table(index=['orgUnit_uid'], values='value', aggfunc='sum')
    PrEP_NEW_AGYW_tier = pd.DataFrame(PrEP_NEW_AGYW_tier).reset_index()

    PrEP_NEW_AGYW_tier = PrEP_NEW_AGYW_tier.rename(columns={'value': 'Import File_PrEP_NEW_AGYW'})

    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_NEW_AGYW_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgUnit_uid'])

    PrEP_NEW['MER report 2nd submission vs Import File_PrEP_NEW_AGYW'] = (
                PrEP_NEW['MER report 2nd submission_PrEP_NEW_AGYW'].eq(PrEP_NEW['Import File_PrEP_NEW_AGYW']) | (
                    PrEP_NEW['MER report 2nd submission_PrEP_NEW_AGYW'].isna() & PrEP_NEW[
                'Import File_PrEP_NEW_AGYW'].isna()))
    PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] = PrEP_NEW['Import File_PrEP_NEW_AGYW'] > PrEP_NEW['Import File_PrEP_NEW']
    PrEP_NEW = PrEP_NEW.drop(columns=['orgunituid'])

    return PrEP_NEW


def run_new_genie(PrEP_NEW, mer_file1, mer_file2, tier_df, df, fiscal_year_2ndG, _2ndG_curr_qtr):  # df is new genie
    # call Tier
    PrEP_NEW = run_tier(PrEP_NEW, mer_file1, mer_file2, tier_df)

    PrEP_NEW_genie = df[
        (df['indicator'] == 'PrEP_NEW') & (df['fiscal_year'] == fiscal_year_2ndG) & (df['source_name'] == 'DATIM')]

    PrEP_NEW_genie = PrEP_NEW_genie[(PrEP_NEW_genie['standardizeddisaggregate'] == 'Age/Sex')]

    PrEP_NEW_genie = PrEP_NEW_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                aggfunc='sum')
    PrEP_NEW_genie = pd.DataFrame(PrEP_NEW_genie).reset_index()

    PrEP_NEW_genie = PrEP_NEW_genie.rename(columns={'PrEP_NEW': 'Genie_PrEP_NEW'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_NEW_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgunituid'])

    PrEP_CT_genie = df[
        (df['indicator'] == 'PrEP_CT') & (df['fiscal_year'] == fiscal_year_2ndG) & (df['source_name'] == 'DATIM')]

    PrEP_CT_genie = PrEP_CT_genie[(PrEP_CT_genie['standardizeddisaggregate'] == 'Age/Sex')]

    PrEP_CT_genie = PrEP_CT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                              aggfunc='sum')
    PrEP_CT_genie = pd.DataFrame(PrEP_CT_genie).reset_index()

    PrEP_CT_genie = PrEP_CT_genie.rename(columns={'PrEP_CT': 'Genie_PrEP_CT'})

    # merge with first genie
    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_CT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgunituid'])

    PrEP_NEW['PrEP NEW > PrEP_CT'] = PrEP_NEW['Genie_PrEP_NEW'] > PrEP_NEW['Genie_PrEP_CT']

    PrEP_NEW['Import File vs Genie_PrEP_NEW'] = (PrEP_NEW['Import File_PrEP_NEW'].eq(PrEP_NEW['Genie_PrEP_NEW']) | (
                PrEP_NEW['Import File_PrEP_NEW'].isna() & PrEP_NEW['Genie_PrEP_NEW'].isna()))

    PrEP_NEW_AGYW_genie = df[
        (df['indicator'] == 'PrEP_NEW') & (df['fiscal_year'] == fiscal_year_2ndG) & (df['source_name'] == 'DATIM')]

    PrEP_NEW_AGYW_genie = PrEP_NEW_AGYW_genie[
        (PrEP_NEW_AGYW_genie['sex'] == 'Female') & (PrEP_NEW_AGYW_genie['ageasentered'].isin(['15-19', '20-24']))]

    PrEP_NEW_AGYW = PrEP_NEW_AGYW_genie.pivot_table(index=['orgunituid'], values=_2ndG_curr_qtr, aggfunc='sum')
    PrEP_NEW_AGYW = pd.DataFrame(PrEP_NEW_AGYW).reset_index()

    PrEP_NEW_AGYW = PrEP_NEW_AGYW.rename(columns={_2ndG_curr_qtr: 'Genie_PrEP_NEW_AGYW'})

    PrEP_NEW = pd.merge(PrEP_NEW, PrEP_NEW_AGYW, left_on='DATIM UID', right_on='orgunituid', how='left')
    PrEP_NEW = PrEP_NEW.drop(columns=['orgunituid'])

    PrEP_NEW['PrEP_NEW_AGYW > PrEP_NEW'] = PrEP_NEW['Genie_PrEP_NEW_AGYW'] > PrEP_NEW['Genie_PrEP_NEW']

    PrEP_NEW['Import File vs Genie_PrEP_NEW_AGYW'] = (
                PrEP_NEW['Import File_PrEP_NEW_AGYW'].eq(PrEP_NEW['Genie_PrEP_NEW_AGYW']) | (
                    PrEP_NEW['Import File_PrEP_NEW_AGYW'].isna() & PrEP_NEW['Genie_PrEP_NEW_AGYW'].isna()))

    return PrEP_NEW
