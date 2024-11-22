import streamlit as st
import indicator_handler
from mfl import MFLHandler
from genie import GenieHandler
from non_tier_import_reader import NonTierDataProcessor
from tier_import_reader import TierDataProcessor
from user_inputs import UserInputs
from mer_reader import MerFileReader
from indicator_handler import *
from steps_handler import process_tier_indicator
from non_tier_step_handler import process_non_tier_indicator

# Initialize handlers
mfl_handler = MFLHandler()
genie_handler1 = GenieHandler()
genie_handler2 = GenieHandler()
user_inputs = UserInputs()

mer_reader1 = MerFileReader()
mer_reader2 = MerFileReader()
tier_reader = TierDataProcessor()

# variables
mfl_df = None
genie1_df = None
genie2_df = None

# Define the correct PIN
CORRECT_PIN = "1234"


# Function to check the PIN
def check_pin(user_pin):
    return user_pin == CORRECT_PIN


# Streamlit app
st.title("Welcome to SI MER App")

# Ask for PIN input
input_pin = st.text_input("Enter your PIN:", type="password")

# Check the PIN
if input_pin:
    if check_pin(input_pin):
        st.success("PIN is correct. Access granted!")
        # Main content goes here

        # Sidebar with a button
        page = st.sidebar.selectbox("Choose a page", ["Logic Check", "Monthly"])

        if page == "Logic Check":
            st.header("Logic Check")

            # Display user inputs
            user_inputs.display_inputs()

            mfl_file = st.file_uploader("Upload MFL file", type=["xlsx", "xls"])
            if mfl_file is not None:
                st.success(f"File '{mfl_file.name}' uploaded successfully!")
                mfl_handler.set_file(mfl_file)

                yr = user_inputs.get_fiscal_year()
                qtr = user_inputs.get_qtr()
                sheet_names = mfl_handler.get_sheet_names(yr, qtr)
                mfl_sheet_name = st.selectbox("Select Sheet Name with MFL Data", sheet_names)

                if mfl_sheet_name:
                    mfl_handler.set_sheet_name(mfl_sheet_name)
                    mfl_df = mfl_handler.get_processed_mfl()
                    # Get DataFrame and display
                    mfl_handler.get_df()

            genie_handler1.display_file_uploader("Upload First Genie", key="gene1")

            if genie_handler1.get_file() is not None:
                genie1_df = genie_handler1.get_df()

                non_tier_import_reader = NonTierDataProcessor()
                non_tier_indicators = indicator_handler.get_non_tier_indicators()

                if user_inputs.get_indicator() in non_tier_indicators:
                    process_non_tier_indicator(user_inputs.get_step_output(), mfl_df, genie1_df, user_inputs,
                                               genie_handler2)
                else:
                    process_tier_indicator(user_inputs.get_step_output(), mfl_df, genie1_df, user_inputs, mer_reader1,
                                           mer_reader2, tier_reader, genie_handler2)

        elif page == "Monthly":
            st.header("Monthly Page")
            # First Genie File upload widget
            monthly_path = st.file_uploader("Upload Monthly file", type=["txt"])
            if monthly_path is not None:
                st.write("Monthly file uploaded successfully!")

    else:
        st.error("Incorrect PIN. Access denied.")
else:
    st.info("Please enter the PIN to access the app.")
