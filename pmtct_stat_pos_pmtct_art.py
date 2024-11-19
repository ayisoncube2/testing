import pandas as pd
import indicator_handler
from districts import get_districts
import streamlit as st
import base64
import io
import warnings

warnings.filterwarnings("ignore")

indicator_name = 'PMTCT_STAT_POS_ART'
districts = get_districts()


# Function to download the Indicator Excel File
def download_excel(PMTCT_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step):
    # Create an Excel file in memory
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    b64 = save_main_sheet(output, writer, PMTCT_STAT_POS_ART, summary_df, step)

    file_path = indicator_handler.get_file_path(fiscal_year_2ndG, _2ndG_curr_qtr, indicator, step)
    href = f'<a download="{file_path}" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">{"Download Logic Check"}</a><br></br>'
    st.markdown(href, unsafe_allow_html=True)


# Function to save the main sheet
def save_main_sheet(output, writer, PMTCT_STAT_POS_ART, summary_df, step):
    if step == 'Tier Import':
        # Write Main sheet
        PMTCT_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        support_typecheck = PMTCT_STAT_POS_ART[PMTCT_STAT_POS_ART['Support Type Check'] == False]
        support_typecheck = support_typecheck[
            ['OU3name', 'OU4name', 'OU5uid', 'OU5name', 'DATIM UID', 'DSD/TA', 'supportType', 'Support Type Check']]
        support_typecheck.to_excel(writer, sheet_name='Support Type Check', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64

    elif step == 'New Genie':
        # Write Main sheet
        PMTCT_STAT_POS_ART.to_excel(writer, sheet_name='Main', index=False)

        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        Import_vs_Genie = PMTCT_STAT_POS_ART[PMTCT_STAT_POS_ART['Import File vs Genie_PMTCT_ART'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_PMTCT_ART', index=False)

        Import_vs_Genie = PMTCT_STAT_POS_ART[PMTCT_STAT_POS_ART['Import File vs Genie_PMTCT_STAT_POS'] == False]
        Import_vs_Genie.to_excel(writer, sheet_name='Import vs Genie_PMTCT_STAT_POS', index=False)

        writer.close()
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return b64
    else:
        st.write("No step was selected")


def process_pmtct_stat_pos_art_data(mfl, first_genie, user_inputs, non_tier, new_genie_df):
    step = user_inputs.get_step_output()
    fiscal_year_1stG = user_inputs.get_first_genie_year()  # select correct year for this semi
    _1stG_curr_qtr = user_inputs.get_first_genie_qtr()  # select correct qtr for this semi
    fiscal_year_2ndG = user_inputs.get_fiscal_year()
    _2ndG_curr_qtr = user_inputs.get_qtr()

    if (first_genie is not None) & (mfl is not None):
        # PMTCT_STAT
        PMTCT_STAT_genie = first_genie[
            (first_genie['indicator'] == 'PMTCT_STAT_POS') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'Derived') &
            (first_genie['standardizeddisaggregate'] == 'Age/Sex/KnownNewResult')]
        PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator',
                                                        values=_1stG_curr_qtr, aggfunc='sum')
        PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()

        PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT_POS': 'Previous_QTR_PMTCT_STAT_POS'})

        # merge with first genie
        PMTCT_STAT_POS_ART = pd.merge(mfl, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid', how='left')
        PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns='orgunituid')

        PMTCT_ART_genie = first_genie[
            (first_genie['indicator'] == 'PMTCT_ART') & (first_genie['fiscal_year'] == fiscal_year_1stG) & (
                    first_genie['source_name'] == 'DATIM')]
        PMTCT_ART_genie = PMTCT_ART_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_1stG_curr_qtr,
                                                      aggfunc='sum')
        PMTCT_ART_genie = pd.DataFrame(PMTCT_ART_genie).reset_index()

        PMTCT_ART_genie = PMTCT_ART_genie.rename(columns={'PMTCT_ART': 'Previous_QTR_PMTCT_ART'})

        # merge with first genie
        PMTCT_STAT_POS_ART = pd.merge(PMTCT_STAT_POS_ART, PMTCT_ART_genie, left_on='DATIM UID', right_on='orgunituid',
                                      how='left')
        PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns='orgunituid')

        PMTCT_STAT_POS_ART['% Linkage'] = ((PMTCT_STAT_POS_ART['Previous_QTR_PMTCT_ART'] / PMTCT_STAT_POS_ART[
            'Previous_QTR_PMTCT_STAT_POS']) * 100).round(2)

        def check_linkage(value):
            if pd.notna(value) and value < 80:
                return "Extremely low HIV testing Linkage"
            elif pd.notna(value) and value > 100:
                return "Data quality issue"
            else:
                return ""

        PMTCT_STAT_POS_ART['Status Check: "Extremely low HIV testing Linkage" <80%, "Data quality issue" >100%'] = \
            PMTCT_STAT_POS_ART['% Linkage'].apply(check_linkage)

        if step == 'Tier Import':
            PMTCT_STAT_POS_ART = run_tier(PMTCT_STAT_POS_ART, non_tier)

            # step 4 output
            summary_cols = [  # 'Previous_QTR_PMTCT_STAT_POS_ART_POS',
                'Previous_QTR_PMTCT_ART',
                # 'Import File_PMTCT_STAT_POS_ART_POS',
                'Import File_PMTCT_ART']

            summary_df = PMTCT_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return

        elif step == 'New Genie':
            PMTCT_STAT_POS_ART = run_new_genie(PMTCT_STAT_POS_ART, non_tier, new_genie_df, fiscal_year_2ndG,
                                               _2ndG_curr_qtr)

            # step 5 output
            summary_cols = [  # 'Previous_QTR_PMTCT_STAT_POS_ART_POS',
                'Previous_QTR_PMTCT_ART',
                # 'Import File_PMTCT_STAT_POS_ART_POS',
                'Import File_PMTCT_ART',
                'Genie_PMTCT_ART',
                'Genie_PMTCT_STAT_POS'
            ]

            summary_df = PMTCT_STAT_POS_ART.groupby('OU3name')[summary_cols].sum().reset_index()

            total_row = summary_df[summary_cols].sum().tolist()
            total_row.insert(0, 'Total')
            summary_df.loc[len(summary_df)] = total_row

            # Button to trigger download
            download_excel(PMTCT_STAT_POS_ART, summary_df, fiscal_year_2ndG, _2ndG_curr_qtr, indicator_name, step)

            return
        else:
            st.write("No step was selected")


def run_tier(PMTCT_STAT_POS_ART, non_tier):
    PMTCT_STAT_P_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_STAT')]

    PMTCT_STAT_P_tier = PMTCT_STAT_P_tier[PMTCT_STAT_P_tier['categoryOptionComboName'].str.contains('Positive')]
    # PMTCT_STAT_P_tier = PMTCT_STAT_P_tier[~PMTCT_STAT_P_tier['categoryOptionComboName'].str.contains('Known
    # Positives')]
    PMTCT_STAT_P_tier['dataElement'] = 'PMTCT_STAT_POS'

    PMTCT_STAT_P_tier = PMTCT_STAT_P_tier.pivot_table(index=['orgUnit_uid', 'supportType'], columns='dataElement',
                                                      values='value', aggfunc='sum')

    PMTCT_STAT_P_tier = pd.DataFrame(PMTCT_STAT_P_tier).reset_index()

    PMTCT_STAT_P_tier = PMTCT_STAT_P_tier.rename(columns={'PMTCT_STAT_POS': 'Import File_PMTCT_STAT_POS'})

    PMTCT_STAT_POS_ART = pd.merge(PMTCT_STAT_POS_ART, PMTCT_STAT_P_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                  how='left')
    PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns=['orgUnit_uid'])

    PMTCT_ART_tier = non_tier[non_tier['dataElement'].str.startswith('PMTCT_ART')]
    PMTCT_ART_tier['dataElement'] = 'PMTCT_ART'

    PMTCT_ART_tier = PMTCT_ART_tier.pivot_table(index=['orgUnit_uid'], columns='dataElement', values='value',
                                                aggfunc='sum')

    PMTCT_ART_tier = pd.DataFrame(PMTCT_ART_tier).reset_index()

    PMTCT_ART_tier = PMTCT_ART_tier.rename(columns={'PMTCT_ART': 'Import File_PMTCT_ART'})

    PMTCT_STAT_POS_ART = pd.merge(PMTCT_STAT_POS_ART, PMTCT_ART_tier, left_on='DATIM UID', right_on='orgUnit_uid',
                                  how='left')
    PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns=['orgUnit_uid'])

    PMTCT_STAT_POS_ART['% Linkage'] = ((PMTCT_STAT_POS_ART['Import File_PMTCT_ART'] / PMTCT_STAT_POS_ART[
        'Import File_PMTCT_STAT_POS']) * 100).round(2)

    def check_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low HIV testing Linkage"
        elif pd.notna(value) and value > 100:
            return "Data quality issue"
        else:
            return ""

    PMTCT_STAT_POS_ART['Status Check: "Extremely low HIV testing Linkage" <80%, "Data quality issue" >100%'] = \
        PMTCT_STAT_POS_ART['% Linkage'].apply(check_linkage)

    PMTCT_STAT_POS_ART['Support Type Check'] = (PMTCT_STAT_POS_ART['DSD/TA'] == PMTCT_STAT_POS_ART['supportType']) | (
            PMTCT_STAT_POS_ART['supportType'].isna() | (PMTCT_STAT_POS_ART['supportType'] == ''))

    return PMTCT_STAT_POS_ART


def run_new_genie(PMTCT_STAT_POS_ART, non_tier, second_genie, fiscal_year_2ndG, _2ndG_curr_qtr):
    # run tier step
    PMTCT_STAT_POS_ART = run_tier(PMTCT_STAT_POS_ART, non_tier)

    # PMTCT_STAT
    PMTCT_STAT_genie = second_genie[
        (second_genie['indicator'] == 'PMTCT_STAT_POS') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'Derived') &
        (second_genie['standardizeddisaggregate'] == 'Age/Sex/KnownNewResult')]
    PMTCT_STAT_genie = PMTCT_STAT_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                    aggfunc='sum')
    PMTCT_STAT_genie = pd.DataFrame(PMTCT_STAT_genie).reset_index()

    PMTCT_STAT_genie = PMTCT_STAT_genie.rename(columns={'PMTCT_STAT_POS': 'Genie_PMTCT_STAT_POS'})

    # merge with first genie
    PMTCT_STAT_POS_ART = pd.merge(PMTCT_STAT_POS_ART, PMTCT_STAT_genie, left_on='DATIM UID', right_on='orgunituid',
                                  how='left')
    PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns='orgunituid')

    PMTCT_STAT_POS_ART['Import File vs Genie_PMTCT_STAT_POS'] = (
            PMTCT_STAT_POS_ART['Import File_PMTCT_STAT_POS'].eq(PMTCT_STAT_POS_ART['Genie_PMTCT_STAT_POS']) | (
            PMTCT_STAT_POS_ART['Import File_PMTCT_STAT_POS'].isna() & PMTCT_STAT_POS_ART[
        'Genie_PMTCT_STAT_POS'].isna()))

    PMTCT_ART_genie = second_genie[
        (second_genie['indicator'] == 'PMTCT_ART') & (second_genie['fiscal_year'] == fiscal_year_2ndG) & (
                second_genie['source_name'] == 'DATIM')]
    PMTCT_ART_genie = PMTCT_ART_genie.pivot_table(index=['orgunituid'], columns='indicator', values=_2ndG_curr_qtr,
                                                  aggfunc='sum')
    PMTCT_ART_genie = pd.DataFrame(PMTCT_ART_genie).reset_index()

    PMTCT_ART_genie = PMTCT_ART_genie.rename(columns={'PMTCT_ART': 'Genie_PMTCT_ART'})

    # merge with first genie
    PMTCT_STAT_POS_ART = pd.merge(PMTCT_STAT_POS_ART, PMTCT_ART_genie, left_on='DATIM UID', right_on='orgunituid',
                                  how='left')
    PMTCT_STAT_POS_ART = PMTCT_STAT_POS_ART.drop(columns='orgunituid')

    PMTCT_STAT_POS_ART['Import File vs Genie_PMTCT_ART'] = (
            PMTCT_STAT_POS_ART['Import File_PMTCT_ART'].eq(PMTCT_STAT_POS_ART['Genie_PMTCT_ART']) | (
            PMTCT_STAT_POS_ART['Import File_PMTCT_ART'].isna() & PMTCT_STAT_POS_ART['Genie_PMTCT_ART'].isna()))

    PMTCT_STAT_POS_ART['% Linkage'] = (
            (PMTCT_STAT_POS_ART['Genie_PMTCT_ART'] / PMTCT_STAT_POS_ART['Genie_PMTCT_STAT_POS']) * 100).round(2)

    def check_linkage(value):
        if pd.notna(value) and value < 80:
            return "Extremely low HIV testing Linkage"
        elif pd.notna(value) and value > 100:
            return "Data quality issue"
        else:
            return ""

    PMTCT_STAT_POS_ART['Status Check: "Extremely low HIV testing Linkage" <80%, "Data quality issue" >100%'] = \
        PMTCT_STAT_POS_ART['% Linkage'].apply(check_linkage)

    return PMTCT_STAT_POS_ART
