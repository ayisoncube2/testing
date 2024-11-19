import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'TX_ML'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(TX_ML, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, TX_ML, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, TX_ML, summary_df, step):
    if step == 'MER File 1':
        # Write Main sheet
        TX_ML.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        level_1_check_df = TX_ML[TX_ML[
                                     'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_ML'] == 'No data reported']
        level_1_check_df.to_excel(writer, sheet_name='Level 1 Check_TX_ML', index=False)

        level_2_check_df = TX_ML[TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 <3months > +3months IIT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'MER File 2':
        # Write Main sheet
        TX_ML.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        mer1_vs_mer2 = TX_ML[TX_ML['MER report 1st submission vs 2nd submission_TX_ML'] == False]
        mer1_vs_mer2.to_excel(writer, sheet_name='Mer 1 vs Mer 2_TX_ML', index=False)

        level_2_check_df = TX_ML[TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 <3months > +3months IIT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64  # Exits the function

    elif step == 'Tier Import':
        # Write Main sheet
        TX_ML.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        import_vs_mer2 = TX_ML[TX_ML['MER report 2nd submission vs Import File_TX_ML'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Mer 2_TX_ML', index=False)

        level_2_check_df = TX_ML[TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 <3months >+3months IIT', index=False)

        support_typecheck = TX_ML[TX_ML['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        TX_ML.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        import_vs_mer2 = TX_ML[TX_ML['Import File vs Genie_TX_ML'] == False]
        import_vs_mer2.to_excel(writer, sheet_name='Import vs Genie_TX_ML', index=False)

        level_2_check_df = TX_ML[TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] == True]
        level_2_check_df.to_excel(writer, sheet_name='Level 2 <3months >+3months IIT', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_tx_ml_data(mfl, first_genie, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):

        TX_ML_genie = first_genie[
            (first_genie['indicator'] == 'TX_ML') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]
        TX_ML_genie = TX_ML_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                              aggfunc='sum')
        TX_ML_genie = pd.DataFrame(TX_ML_genie).reset_index()
        TX_ML_genie = TX_ML_genie.rename(columns={'TX_ML': 'Previous_QTR_TX_ML'})

        # merge with first genie
        TX_ML = pd.merge(mfl, TX_ML_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_ML = TX_ML.drop(columns='orgunituid')

        TX_ML_genie = first_genie[
            (first_genie['indicator'] == 'TX_ML') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                        first_genie['source_name'] == 'DATIM')]

        rip = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('Died')]
        tfo = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('Transferred Out')]
        itt_less_3_months = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('3 Months Treatment')]
        itt_3_5_months = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('3-5 Months Treatment')]
        itt_6_plus = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('\(6\+ Months Treatment')]

        sum_rip = rip.groupby('orgunituid')[_1stG_curr_qtr].sum().reset_index()
        sum_rip = sum_rip.rename(columns={_1stG_curr_qtr: 'TX_ML_RIP'})

        sum_tfo = tfo.groupby('orgunituid')[_1stG_curr_qtr].sum().reset_index()
        sum_tfo = sum_tfo.rename(columns={_1stG_curr_qtr: 'TX_ML_TFO'})

        sum_itt_less_3_months = itt_less_3_months.groupby('orgunituid')[_1stG_curr_qtr].sum().reset_index()
        sum_itt_less_3_months = sum_itt_less_3_months.rename(columns={_1stG_curr_qtr: 'TX_ML_IIT_less_3_months'})

        sum_itt_3_5_months = itt_3_5_months.groupby('orgunituid')[_1stG_curr_qtr].sum().reset_index()
        sum_itt_3_5_months = sum_itt_3_5_months.rename(columns={_1stG_curr_qtr: 'TX_ML_IIT_3_5_months'})

        sum_itt_6_plus = itt_6_plus.groupby('orgunituid')[_1stG_curr_qtr].sum().reset_index()
        sum_itt_6_plus = sum_itt_6_plus.rename(columns={_1stG_curr_qtr: 'TX_ML_IIT_6_plus'})

        dfs = [sum_rip, sum_tfo, sum_itt_less_3_months, sum_itt_3_5_months, sum_itt_6_plus]

        sorted_dfs = sorted(dfs, key=lambda x: len(x), reverse=True)

        merged_df = sorted_dfs[0]
        for df in sorted_dfs[1:]:
            merged_df = pd.merge(merged_df, df, on='orgunituid', how='left')

        TX_ML = pd.merge(TX_ML, merged_df, left_on='DATIM UID', right_on='orgunituid', how='left')
        TX_ML = TX_ML.drop(columns=['orgunituid'])

        TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] = TX_ML['TX_ML_IIT_less_3_months'] > TX_ML[
            'TX_ML_IIT_3_5_months']

        if step == 'MER File 1':
            TX_ML = run_first_mer(TX_ML, mer_file1)

            # step 2 output
            summary_cols = ['Previous_QTR_TX_ML', 'MER report 1st submission_TX_ML']

            summary_df = TX_ML.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_ML, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)
            return

        elif step == 'MER File 2':
            TX_ML = run_second_mer(TX_ML, mer_file1, mer_file2)

            # step 3 output
            summary_cols = ['Previous_QTR_TX_ML', 'MER report 1st submission_TX_ML',
                            'MER report 2nd submission_TX_ML']

            summary_df = TX_ML.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_ML, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'Tier Import':
            TX_ML = run_tier(TX_ML, mer_file1, mer_file2, tier_df)

            # step 4 output
            summary_cols = ['Previous_QTR_TX_ML', 'MER report 1st submission_TX_ML',
                            'MER report 2nd submission_TX_ML', 'Import File_TX_ML']

            summary_df = TX_ML.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_ML, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            TX_ML = run_new_genie(TX_ML, mer_file1, mer_file2, tier_df, new_genie_df, fiscal_year_2ndG,
                                   _2ndG_curr_qtr)

            # step 5 output
            summary_cols = ['Previous_QTR_TX_ML', 'MER report 1st submission_TX_ML',
                            'MER report 2nd submission_TX_ML', 'Import File_TX_ML', 'Genie_TX_ML']

            summary_df = TX_ML.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(TX_ML, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_first_mer(TX_ML, mer_file1):
    kp = pd.read_excel(mer_file1, sheet_name='TX_ML_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file1, sheet_name='TX_ML')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 1st submission_TX_ML'})

    # merge with first genie
    TX_ML = pd.merge(TX_ML, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_ML = TX_ML.drop(columns='UID')

    # Track Second Submission: TX_ML
    qtr_data_check = 'Level 1 Check: sites that had data in previous quarter but no data in current quarter_TX_ML'

    def prev_qtr_data_no_current_qtr_check(row):
        if row['MER report 1st submission_TX_ML'] >= 0:
            return "Data Reported"
        else:
            return "No data reported"

    TX_ML[qtr_data_check] = TX_ML.apply(prev_qtr_data_no_current_qtr_check, axis=1)

    return TX_ML


def run_second_mer(TX_ML, mer_file1, mer_file2):
    # run first mer
    TX_ML = run_first_mer(TX_ML, mer_file1)

    kp = pd.read_excel(mer_file2, sheet_name='TX_ML_KP').drop(columns=['KP_Type', 'KP_Location'])
    non_kp = pd.read_excel(mer_file2, sheet_name='TX_ML')

    kp = kp[kp['District'].isin(districts)]
    non_kp = non_kp[non_kp['District'].isin(districts)]

    mer_appended = pd.concat([non_kp, kp], ignore_index=True)

    mer = mer_appended.pivot_table(index=['UID'], values='Total', aggfunc='sum')

    mer = pd.DataFrame(mer).reset_index()

    mer = mer.rename(columns={'Total': 'MER report 2nd submission_TX_ML'})

    # merge with first genie
    TX_ML = pd.merge(TX_ML, mer, left_on='OU5uid', right_on='UID', how='left')
    TX_ML = TX_ML.drop(columns='UID')

    TX_ML['MER report 1st submission vs 2nd submission_TX_ML'] = (
                TX_ML['MER report 1st submission_TX_ML'].eq(TX_ML['MER report 2nd submission_TX_ML']) | (
                    TX_ML['MER report 1st submission_TX_ML'].isna() & TX_ML['MER report 2nd submission_TX_ML'].isna()))

    return TX_ML


def run_tier(TX_ML, mer_file1, mer_file2, tier):
    # run the second mer
    TX_ML = run_second_mer(TX_ML, mer_file1, mer_file2)

    TX_ML_tier = tier[tier['dataElement'].str.startswith('TX_ML')]

    TX_ML_tier['dataElement'] = TX_ML_tier['dataElement'].apply(lambda x: 'TX_ML' if x.startswith('TX_ML') else x)

    TX_ML_tier = TX_ML_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement', values='value',
                                        aggfunc='sum')
    TX_ML_tier = pd.DataFrame(TX_ML_tier).reset_index()

    TX_ML_tier = TX_ML_tier.rename(columns={'TX_ML': 'Import File_TX_ML'})

    TX_ML = pd.merge(TX_ML, TX_ML_tier, left_on='DATIM UID', right_on='orgUnit_uid', how='left')
    TX_ML = TX_ML.drop(columns=['orgUnit_uid'])

    TX_ML['Support Type Check'] = (TX_ML['DSD/TA'] == TX_ML['supportType']) | (
                TX_ML['supportType'].isna() | (TX_ML['supportType'] == ''))

    TX_ML['MER report 2nd submission vs Import File_TX_ML'] = TX_ML['MER report 2nd submission_TX_ML'] == TX_ML[
        'Import File_TX_ML']

    return TX_ML


def run_new_genie(TX_ML, mer_file1, mer_file2, tier_df, second_genie, fiscal_year_2ndG,
                  _2ndG_curr_qtr):  # df is new genie
    # run tier step
    TX_ML = run_tier(TX_ML, mer_file1, mer_file2, tier_df)

    TX_ML_genie = second_genie[
        (second_genie['indicator'] == 'TX_ML') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]
    TX_ML_genie = TX_ML_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                          aggfunc='sum')
    TX_ML_genie = pd.DataFrame(TX_ML_genie).reset_index()
    TX_ML_genie = TX_ML_genie.rename(columns={'TX_ML': 'Genie_TX_ML'})

    # merge with first genie
    TX_ML = pd.merge(TX_ML, TX_ML_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_ML = TX_ML.drop(columns='orgunituid')

    TX_ML['Import File vs Genie_TX_ML'] = (TX_ML['Import File_TX_ML'].eq(TX_ML['Genie_TX_ML']) | (
                TX_ML['Import File_TX_ML'].isna() & TX_ML['Genie_TX_ML'].isna()))

    # recreate these columns
    # List of columns you want to drop
    columns_to_drop = ['TX_ML_IIT_6_plus', 'TX_ML_TFO', 'TX_ML_IIT_less_3_months', 'TX_ML_RIP', 'TX_ML_IIT_3_5_months']

    # Filter out columns that do not exist in the DataFrame
    existing_columns_to_drop = [col for col in columns_to_drop if col in TX_ML.columns]

    # Drop only the existing columns
    TX_ML = TX_ML.drop(columns=existing_columns_to_drop)

    TX_ML_genie = second_genie[
        (second_genie['indicator'] == 'TX_ML') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                    second_genie['source_name'] == 'DATIM')]

    rip = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('Died')]
    tfo = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('Transferred Out')]
    itt_less_3_months = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('3 Months Treatment')]
    itt_3_5_months = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('3-5 Months Treatment')]
    itt_6_plus = TX_ML_genie[TX_ML_genie['categoryoptioncomboname'].str.contains('\(6\+ Months Treatment')]

    sum_rip = rip.groupby('orgunituid')[_2ndG_curr_qtr].sum().reset_index()
    sum_rip = sum_rip.rename(columns={_2ndG_curr_qtr: 'TX_ML_RIP'})

    sum_tfo = tfo.groupby('orgunituid')[_2ndG_curr_qtr].sum().reset_index()
    sum_tfo = sum_tfo.rename(columns={_2ndG_curr_qtr: 'TX_ML_TFO'})

    sum_itt_less_3_months = itt_less_3_months.groupby('orgunituid')[_2ndG_curr_qtr].sum().reset_index()
    sum_itt_less_3_months = sum_itt_less_3_months.rename(columns={_2ndG_curr_qtr: 'TX_ML_IIT_less_3_months'})

    sum_itt_3_5_months = itt_3_5_months.groupby('orgunituid')[_2ndG_curr_qtr].sum().reset_index()
    sum_itt_3_5_months = sum_itt_3_5_months.rename(columns={_2ndG_curr_qtr: 'TX_ML_IIT_3_5_months'})

    sum_itt_6_plus = itt_6_plus.groupby('orgunituid')[_2ndG_curr_qtr].sum().reset_index()
    sum_itt_6_plus = sum_itt_6_plus.rename(columns={_2ndG_curr_qtr: 'TX_ML_IIT_6_plus'})

    dfs = [sum_rip, sum_tfo, sum_itt_less_3_months, sum_itt_3_5_months, sum_itt_6_plus]

    sorted_dfs = sorted(dfs, key=lambda x: len(x), reverse=True)

    merged_df = sorted_dfs[0]
    for df in sorted_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='orgunituid', how='left')

    TX_ML = pd.merge(TX_ML, merged_df, left_on='DATIM UID', right_on='orgunituid', how='left')
    TX_ML = TX_ML.drop(columns=['orgunituid'])

    TX_ML['Level 2 Check: <3months IIT >+3months IIT "data outlier"'] = TX_ML['TX_ML_IIT_less_3_months'] > TX_ML[
        'TX_ML_IIT_3_5_months']

    return TX_ML