import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'SC_ARVDISP'
districts = get_districts()
is_sc_arvdisp_reported = True


# Function to download the Indicator Excel File
def download_excel(SC_ARVDISP, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, SC_ARVDISP, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, SC_ARVDISP, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        SC_ARVDISP.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Write Level 1 Check sheet
        level_1_check_df = SC_ARVDISP[SC_ARVDISP[
                                          'Level 1 Check: sites that had data in previous quarter but no data in current quarter_SC_ARVDISP'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        SC_ARVDISP.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = SC_ARVDISP[SC_ARVDISP['MER report 1st submission vs 2nd submission_SC_ARVDISP'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_SC_ARVDISP', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        SC_ARVDISP.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = SC_ARVDISP[SC_ARVDISP['MER report 1st submission vs 2nd submission_SC_ARVDISP'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_SC_ARVDISP', index=False)

        mer2_vs_import = SC_ARVDISP[SC_ARVDISP['MER report  2nd submission vs Import File_SC_ARVDISP'] == False]
        mer2_vs_import.to_excel(writer, sheet_name='Mer 2 vs Import_SC_ARVDISP', index=False)

        support_typecheck = SC_ARVDISP[SC_ARVDISP['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        SC_ARVDISP.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = SC_ARVDISP[SC_ARVDISP['MER report 1st submission vs 2nd submission_SC_ARVDISP'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_SC_ARVDISP', index=False)

        mer2_vs_import = SC_ARVDISP[SC_ARVDISP['MER report  2nd submission vs Import File_SC_ARVDISP'] == False]
        mer2_vs_import.to_excel(writer, sheet_name='Mer 2 vs Import_SC_ARVDISP', index=False)

        import_vs_genie = SC_ARVDISP[SC_ARVDISP['Import File vs Genie_SC_ARVDISP'] == False]
        import_vs_genie.to_excel(writer, sheet_name='Import vs Genie_SC_ARVDISP', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_sc_arvdisp_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG_semi = user_inputs.get_first_genie_year()
    _1stG_curr_qtr_semi = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        genie = first_genie[
            (first_genie['indicator'] == 'SC_ARVDISP') & (first_genie['fiscal_year'] == fiscal_year_1stG_semi) & (
                        first_genie['source_name'] == 'DATIM')]

        genie = genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr_semi, aggfunc='sum')
        genie = pd.DataFrame(genie).reset_index()
        genie = genie.rename(columns={'SC_ARVDISP': 'Previous_SC_ARVDISP'})

        SC_ARVDISP = pd.merge(mfl, genie, left_on='DATIM UID', right_on='orgunituid', how='left')

        if step == 'MER File 1':

            SC_ARVDISP = run_first_mer(SC_ARVDISP, mer_file1)

            summary_df = SC_ARVDISP.groupby('OU3name')[
                ['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP']].sum().reset_index()

            total_row = summary_df[['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_ARVDISP, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            SC_ARVDISP = run_second_mer(SC_ARVDISP, mer_file1, mer_file2)

            summary_df = SC_ARVDISP.groupby('OU3name')[['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP',
                                                        'MER report 2nd submission_SC_ARVDISP']].sum().reset_index()

            total_row = summary_df[['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP',
                                    'MER report 2nd submission_SC_ARVDISP']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_ARVDISP, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            SC_ARVDISP = run_tier(SC_ARVDISP, mer_file1, mer_file2, tier_df)

            summary_df = SC_ARVDISP.groupby('OU3name')[
                ['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP', 'MER report 2nd submission_SC_ARVDISP',
                 'Import File_SC_ARVDISP']].sum().reset_index()

            total_row = summary_df[
                ['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP', 'MER report 2nd submission_SC_ARVDISP',
                 'Import File_SC_ARVDISP']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_ARVDISP, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            SC_ARVDISP = run_new_genie(SC_ARVDISP, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            summary_df = SC_ARVDISP.groupby('OU3name')[
                ['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP', 'MER report 2nd submission_SC_ARVDISP',
                 'Import File_SC_ARVDISP', 'Genie_SC_ARVDISP']].sum().reset_index()

            total_row = summary_df[
                ['Previous_SC_ARVDISP', 'MER report 1st submission_SC_ARVDISP', 'MER report 2nd submission_SC_ARVDISP',
                 'Import File_SC_ARVDISP', 'Genie_SC_ARVDISP']].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(SC_ARVDISP, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(SC_ARVDISP, mer_file1):
    non_kp = pd.read_excel(mer_file1, sheet_name='ARVDISP')
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer = non_kp.pivot_table(index=['Code'], values='Packs', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Packs': 'MER report 1st submission_SC_ARVDISP'})

    SC_ARVDISP = pd.merge(SC_ARVDISP, mer, left_on='New_OU5 Code', right_on='Code', how='left')
    SC_ARVDISP = SC_ARVDISP.drop(columns=['Code'])

    # Track Second Submission
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_SC_ARVDISP'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_SC_ARVDISP'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    SC_ARVDISP[qtr_data_check] = SC_ARVDISP.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    return SC_ARVDISP


def run_second_mer(SC_ARVDISP, mer_file1, mer_file2):
    # run first mer
    SC_ARVDISP = run_first_mer(SC_ARVDISP, mer_file1)

    non_kp = pd.read_excel(mer_file2, sheet_name='ARVDISP')
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer = non_kp.pivot_table(index=['Code'], values='Packs', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Packs': 'MER report 2nd submission_SC_ARVDISP'})

    SC_ARVDISP = pd.merge(SC_ARVDISP, mer, left_on='New_OU5 Code', right_on='Code', how='left')
    SC_ARVDISP = SC_ARVDISP.drop(columns=['Code'])

    SC_ARVDISP['MER report 1st submission vs 2nd submission_SC_ARVDISP'] = (
                SC_ARVDISP['MER report 1st submission_SC_ARVDISP'].eq(
                    SC_ARVDISP['MER report 2nd submission_SC_ARVDISP']) | (
                            SC_ARVDISP['MER report 1st submission_SC_ARVDISP'].isna() & SC_ARVDISP[
                        'MER report 2nd submission_SC_ARVDISP'].isna()))

    return SC_ARVDISP


def run_tier(SC_ARVDISP, mer_file1, mer_file2, tier):

    SC_ARVDISP = run_second_mer(SC_ARVDISP, mer_file1, mer_file2)

    SC_ARVDISP_tier = tier[tier['dataElement'].str.startswith('SC_ARVDISP')]

    SC_ARVDISP_tier['dataElement'] = SC_ARVDISP_tier['dataElement'].apply(
        lambda x: 'SC_ARVDISP' if x.startswith('SC_ARVDISP') else x)

    SC_ARVDISP_tier = SC_ARVDISP_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                  values='value', aggfunc='sum')

    SC_ARVDISP_tier = pd.DataFrame(SC_ARVDISP_tier).reset_index()

    SC_ARVDISP_tier = SC_ARVDISP_tier.rename(columns={'SC_ARVDISP': 'Import File_SC_ARVDISP'})

    SC_ARVDISP = pd.merge(SC_ARVDISP, SC_ARVDISP_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    SC_ARVDISP = SC_ARVDISP.drop(columns=['orgUnit_uid'])

    SC_ARVDISP['Support Type Check'] = (SC_ARVDISP['DSD/TA'] == SC_ARVDISP['supportType']) | (
                SC_ARVDISP['supportType'].isna() | (SC_ARVDISP['supportType'] == ''))

    SC_ARVDISP['MER report  2nd submission vs Import File_SC_ARVDISP'] = (
                SC_ARVDISP['MER report 2nd submission_SC_ARVDISP'].eq(SC_ARVDISP['Import File_SC_ARVDISP']) | (
                    SC_ARVDISP['MER report 2nd submission_SC_ARVDISP'].isna() & SC_ARVDISP[
                'Import File_SC_ARVDISP'].isna()))

    return SC_ARVDISP


def run_new_genie(SC_ARVDISP, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    SC_ARVDISP = run_tier(SC_ARVDISP, mer_file1, mer_file2, tier_df)

    genie = second_genie[
        (second_genie['indicator'] == 'SC_ARVDISP') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    genie = genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr, aggfunc='sum')
    genie = pd.DataFrame(genie).reset_index()

    genie = genie.rename(columns={'SC_ARVDISP': 'Genie_SC_ARVDISP'})

    # merge with first genie
    SC_ARVDISP = pd.merge(SC_ARVDISP, genie, left_on='DATIM UID', right_on='orgunituid', how='left')

    SC_ARVDISP['Import File vs Genie_SC_ARVDISP'] = (
                SC_ARVDISP['Import File_SC_ARVDISP'].eq(SC_ARVDISP['Genie_SC_ARVDISP']) | (
                    SC_ARVDISP['Import File_SC_ARVDISP'].isna() & SC_ARVDISP['Genie_SC_ARVDISP'].isna()))

    return SC_ARVDISP
