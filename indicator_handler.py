from hts_self import process_hts_self_data
from hts_tst_index import process_hts_tst_index_data
from hts_tst_pos import process_hts_tst_pos_data
from pmtct_eid_and_hei_pos import process_pmtct_eid_hei_pos_data
from pmtct_stat import process_pmtct_stat_data
from pmtct_stat_pos_pmtct_art import process_pmtct_stat_pos_art_data
from prep_ct import process_prep_ct_data
import streamlit as st
from datetime import datetime
from prep_new import process_prep_new_data
from qaurter_handler import get_fy_qtr_suffix
import warnings

from sc_arvdisp import process_sc_arvdisp_data
from sc_curr import process_sc_curr_data
from tb_prev import process_tb_prev_data
from tb_stat import process_tb_stat_data
from tb_stat_pos import process_tb_stat_pos_data
from tx_curr import process_tx_curr_data
from tx_ml import process_tx_ml_data
from tx_new import process_tx_new_data
from tx_pvls import process_tx_pvls_data
from tx_rtt import process_tx_rtt_data
from tx_tb import process_tx_tb_data

warnings.filterwarnings("ignore")


def get_indicators():
    indicator_ls = ["HTS_SELF", "HTS_TST_POS", "HTS_TST_INDEX", "PrEP_NEW", "PrEP_CT",
                    "PMTCT_EID and HEI_POS", "PMTCT_STAT", "PMTCT_STAT_POS vs PMTCT_ART",
                    "SC_CURR", "SC_ARVDISP", "TX_CURR", "TX_ML", "TX_NEW", "TX_RTT", "TX_PVLS",
                    "TB_PREV", "TB_STAT", "TB_STAT_POS and ART", "TX_TB"]
    return indicator_ls


def get_file_path(fy, qtr, indicator_name, step):
    today = datetime.now().strftime("%d-%B-%Y_%H_%M_%S")
    file_path = indicator_name + '_FY' + get_fy_qtr_suffix(fy, qtr) + '_' + today + '_Step ' + step + '.xlsx'
    return file_path


def get_require_non_tier_indicators():
    indicator_ls = ["HTS_SELF", "HTS_TST_POS", "HTS_TST_INDEX", "PMTCT_EID and HEI_POS",
                    "PMTCT_STAT", "PMTCT_STAT_POS vs PMTCT_ART", "SC_CURR", "TX_NEW"]
    return indicator_ls


def get_non_tier_indicators():
    non_tier_indicators = ["HTS_SELF",  # "HTS_TST_POS", "HTS_TST_INDEX",
                           "PMTCT_STAT", "PMTCT_STAT_POS vs PMTCT_ART",
                           "SC_CURR"]
    # "HTS_TST and POS", "HTS_TST_INDEX" are non tiers - but they require MER files

    return non_tier_indicators


def process_logic_check(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df, non_tier):
    indicator_name = user_inputs.get_indicator()
    if indicator_name == 'PrEP_CT':
        process_prep_ct_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'PrEP_NEW':
        process_prep_new_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TX_RTT':
        process_tx_rtt_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TX_ML':
        process_tx_ml_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TX_PVLS':
        process_tx_pvls_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TX_NEW':  # require both tier and non tier files
        process_tx_new_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df, non_tier)
    elif indicator_name == 'TX_CURR':
        process_tx_curr_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
        # process_tx_tb_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'SC_ARVDISP':
        process_sc_arvdisp_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TB_STAT':
        process_tb_stat_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == 'TB_STAT_POS and ART':
        process_tb_stat_pos_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == "TB_PREV":
        process_tb_prev_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    elif indicator_name == "PMTCT_EID and HEI_POS":  # require both tier and non tier files
        process_pmtct_eid_hei_pos_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df,
                                       non_tier)
    elif indicator_name == "TX_TB":  # require both tier and non tier files
        process_tx_tb_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, tier_df, new_genie_df)
    # Non Tiers
    elif indicator_name == 'SC_CURR':
        process_sc_curr_data(mfl_df, genie_df, user_inputs, non_tier, new_genie_df)
    elif indicator_name == 'PMTCT_STAT':
        process_pmtct_stat_data(mfl_df, genie_df, user_inputs, non_tier, new_genie_df)
    elif indicator_name == 'PMTCT_STAT_POS vs PMTCT_ART':
        process_pmtct_stat_pos_art_data(mfl_df, genie_df, user_inputs, non_tier, new_genie_df)
    elif indicator_name == 'HTS_SELF':
        process_hts_self_data(mfl_df, genie_df, user_inputs, non_tier, new_genie_df)
    elif indicator_name == 'HTS_TST_POS':
        process_hts_tst_pos_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, non_tier, new_genie_df)
    elif indicator_name == 'HTS_TST_INDEX':
        process_hts_tst_index_data(mfl_df, genie_df, user_inputs, mer_file1, mer_file2, non_tier, new_genie_df)
    else:
        res = "Sorry, " + indicator_name + " is still under development"
        st.write(res)
