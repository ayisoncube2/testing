import streamlit as st
 
# Set up the page title and layout

st.set_page_config(page_title="File Upload App", layout="centered")
 
# Title and description

st.title("Simple File Upload App")

st.write("Upload your files below and view basic details.")
 
# File uploader

uploaded_file = st.file_uploader("Choose a file", type=None)
 
if uploaded_file:

    st.write("**File Details:**")

    st.write(f"- Name: {uploaded_file.name}")

    st.write(f"- Type: {uploaded_file.type}")

    st.write(f"- Size: {uploaded_file.size / 1024:.2f} KB")
 
    # Display content for specific file types

    if uploaded_file.type == "text/plain":

        st.text_area("Text File Content", uploaded_file.getvalue().decode("utf-8"), height=300)
 
    elif uploaded_file.type == "text/csv":

        import pandas as pd

        df = pd.read_csv(uploaded_file)

        st.write("Preview of CSV File:")

        st.dataframe(df)
 
    elif uploaded_file.type in ["image/png", "image/jpeg"]:

        from PIL import Image

        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Image")
 
    else:

        st.write("File type not supported for preview.")
 
 
