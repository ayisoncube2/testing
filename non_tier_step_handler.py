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


def process_non_tier_indicator(step_output, mfl_df, genie_df, user_inputs, genie_handler2):
    """Processes the uploaded files based on the step output."""
    temp = None
    non_tier = None

    non_tier_import_reader = NonTierDataProcessor()
    # require_non_tier = indicator_handler.get_require_non_tier_indicators()

    if step_output == "Tier Import":
        uploaded_file = st.file_uploader("Upload Import Template File", type=["xlsx"])
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            fileReader = TierTemplateFileReader(uploaded_file)
            temp = fileReader.get_df()

            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                          "Excel File", key="non tier")
            non_tier = non_tier_import_reader.get_df()

            # Process MER files and Tier Import file
            process_logic_check(mfl_df, genie_df, user_inputs, None, None,
                                None, None, non_tier)

    elif step_output == "New Genie":

        uploaded_file = st.file_uploader("Upload Import Template File", type=["xlsx"])
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            fileReader = TierTemplateFileReader(uploaded_file)
            temp = fileReader.get_df()

            non_tier_import_reader.display_non_tier_import_uploader(temp, "Upload Non Tier Import "
                                                                          "Excel File", key="non tier")
            non_tier = non_tier_import_reader.get_df()

            if non_tier is not None:

                genie_handler2.display_file_uploader("Upload Second Genie", key="gene2")

                if genie_handler2.get_file() is not None:
                    new_genie_df = genie_handler2.get_df()

                    # Process MER files and Tier Import file
                    process_logic_check(mfl_df, genie_df, user_inputs, None, None,
                                        None, new_genie_df, non_tier)
    else:
        pass

