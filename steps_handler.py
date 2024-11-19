import streamlit as st

import indicator_handler
from indicator_handler import process_logic_check
from non_tier_import_reader import NonTierDataProcessor
from template_reader import TierTemplateFileReader


def display_file_uploader(object_reader, label, key):
    """Displays the file uploader for a MER file and returns the uploaded DataFrame."""
    object_reader.display_file_uploader(label, key)
    if object_reader.get_file() is not None:
        df = object_reader.get_df()
        return df
    return None


def process_tier_indicator(step_output, mfl_df, genie_df, user_inputs, mer_reader1, mer_reader2, tier_reader, genie_handler2):
    """Processes the uploaded files based on the step output."""
    tier = None
    temp = None
    non_tier = None

    non_tier_import_reader = NonTierDataProcessor()
    require_non_tier = indicator_handler.get_require_non_tier_indicators()

    if step_output == "MER File 1":
        mer = display_file_uploader(mer_reader1, "Upload First MER file", key="mer")
        if mer is not None:
            # Process the MER file
            process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(), None,
                                None, None, None)

    elif step_output == "MER File 2":
        mer1 = display_file_uploader(mer_reader1, "Upload First MER file", key="mer1")
        if mer1 is not None:
            mer2 = display_file_uploader(mer_reader2, "Upload Second MER file", key="mer2")
            if mer2 is not None and mer2 is not None:
                process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(), mer_reader2.get_file(),
                                    None, None, None)

    elif step_output == "Tier Import":
        mer1 = display_file_uploader(mer_reader1, "Upload First MER file", key="mer3")

        if mer1 is not None:
            mer2 = display_file_uploader(mer_reader2, "Upload Second MER file", key="mer4")
            if mer2 is not None:
                uploaded_file = st.file_uploader("Choose Import Template File", type=["xlsx"])
                if uploaded_file is not None:
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    fileReader = TierTemplateFileReader(uploaded_file)
                    temp = fileReader.get_df()
                    if user_inputs.get_indicator() in require_non_tier:  # dont load tier data for non tiers
                        if user_inputs.get_indicator() in ['TX_NEW', 'PMTCT_EID and HEI_POS']:

                            # tx new requires both tier and non tier for hts
                            tier_reader.display_tier_import_uploader(temp, "Upload Tier Import Excel File", key="tierA")
                            tier = tier_reader.get_df()

                            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                                          "Excel File", key="non tier")
                            non_tier = non_tier_import_reader.get_df()

                            if tier is not None and non_tier is not None:
                                process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(),
                                                    mer_reader2.get_file(),
                                                    tier, None, non_tier)

                        else:
                            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                                          "Excel File", key="non tier")
                            non_tier = non_tier_import_reader.get_df()

                            if user_inputs.get_indicator() in ["HTS_TST_POS", "HTS_TST_INDEX"]:
                                # pass mer 1 and mer 2 for these 2 indicators.
                                # Process MER files and Non Tier Import file
                                process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(), mer_reader2.get_file(),
                                                    None, None, non_tier)
                            else:
                                # other non tiers don't require mer 1 and mer 2 files
                                # Process only Non Tier Import file
                                process_logic_check(mfl_df, genie_df, user_inputs, None, None,
                                                    None, None, non_tier)
                    else:
                        # For Tier Indicators
                        tier_reader.display_tier_import_uploader(temp, "Upload Tier Import Excel File", key="tierA")
                        tier = tier_reader.get_df()
                        if tier is not None:
                            process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(),
                                                mer_reader2.get_file(),
                                                tier, None, None)

    else:
        mer1 = display_file_uploader(mer_reader1, "Upload First MER file", key="mer3")
        if mer1 is not None:
            mer2 = display_file_uploader(mer_reader2, "Upload Second MER file", key="mer4")
            if mer2 is not None:
                uploaded_file = st.file_uploader("Choose Import Template File", type=["xlsx"])
                if uploaded_file is not None:
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    fileReader = TierTemplateFileReader(uploaded_file)
                    temp = fileReader.get_df()

                    if user_inputs.get_indicator() in require_non_tier:  # dont load tier data for non tiers
                        if user_inputs.get_indicator() in ['TX_NEW', 'PMTCT_EID and HEI_POS']:
                            # tx new requires both tier and non tier for hts
                            tier_reader.display_tier_import_uploader(temp, "Upload Tier Import Excel File", key="tierA")
                            tier = tier_reader.get_df()

                            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                                          "Excel File", key="non tier")
                            non_tier = non_tier_import_reader.get_df()

                            if tier is not None and non_tier is not None:
                                genie_handler2.display_file_uploader("Upload Second Genie", key="gene2")

                                if genie_handler2.get_file() is not None:
                                    new_genie_df = genie_handler2.get_df()

                                    # Process MER files and Tier Import file
                                    process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(),
                                                        mer_reader2.get_file(),
                                                        tier, new_genie_df, non_tier)

                        else:  # other non tiers except the TX NEW
                            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                                          "Excel File", key="non tier")
                            non_tier = non_tier_import_reader.get_df()

                            if non_tier is not None:

                                genie_handler2.display_file_uploader("Upload Second Genie", key="gene2")

                                if genie_handler2.get_file() is not None:
                                    new_genie_df = genie_handler2.get_df()

                                    if user_inputs.get_indicator() in ["HTS_TST_POS", "HTS_TST_INDEX"]:
                                        # pass mer 1 and mer 2 for these 2 indicators.
                                        # Process MER files and Non Tier Import file
                                        process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(), mer_reader2.get_file(),
                                                            None, new_genie_df, non_tier)
                                    else:
                                        # other non tiers don't require mer 1 and mer 2 files
                                        # Process only Non Tier Import file
                                        process_logic_check(mfl_df, genie_df, user_inputs, None, None,
                                                            None, new_genie_df, non_tier)

                    else:
                        # For Tier Indicators
                        tier_reader.display_tier_import_uploader(temp, "Upload Tier Import Excel File", key="tierA")
                        tier = tier_reader.get_df()
                        if tier is not None:

                            genie_handler2.display_file_uploader("Upload Second Genie", key="gene2")

                            if genie_handler2.get_file() is not None:
                                new_genie_df = genie_handler2.get_df()

                                process_logic_check(mfl_df, genie_df, user_inputs, mer_reader1.get_file(),
                                                    mer_reader2.get_file(),
                                                    tier, new_genie_df, None)
