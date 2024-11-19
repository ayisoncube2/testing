# Set up the page title and layout
st.set_page_config(page_title="Hosting App", layout="wide")
 
# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Upload", "About"])
 
if menu == "Home":
    st.title("Welcome to the Hosting App")
    st.write(
        """
        This is a simple app for hosting and sharing content. Use the navigation menu to:
        - Upload files
        - View your content
        - Learn more about the app
        """
    )
    st.image("https://via.placeholder.com/600x300.png", caption="Hosting App", use_column_width=True)
 
elif menu == "Upload":
    st.title("Upload Your Files")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "png", "jpg", "pdf"])
    if uploaded_file:
        st.write("File Uploaded Successfully!")
        st.write(f"File Name: {uploaded_file.name}")
        if uploaded_file.type == "text/plain":
            st.text_area("File Content", uploaded_file.getvalue().decode("utf-8"), height=300)
        elif uploaded_file.type == "text/csv":
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
        elif uploaded_file.type in ["image/png", "image/jpeg"]:
            from PIL import Image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}")
        elif uploaded_file.type == "application/pdf":
            st.write("PDF preview is not available in this app yet.")
elif menu == "About":
    st.title("About This App")
    st.write(
        """
        This hosting app is built using Streamlit, a Python library for creating beautiful web apps.
        Features:
        - Upload and display files
        - Host content and interact with users
        Created with ❤️ using Python and Streamlit.
        """
    )
    st.image("https://via.placeholder.com/400x200.png", caption="Streamlit App", use_column_width=True)
 
