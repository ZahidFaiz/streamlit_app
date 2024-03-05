import streamlit as st

# Add separator lines in the sidebar
separator_style = """
<style>
    .separator {
        margin-top: 10px;
        margin-bottom: 10px;
        border-top: 1px solid #ddd;
    }
</style>
"""
st.sidebar.markdown(separator_style, unsafe_allow_html=True)

# Add sidebar content
st.sidebar.header("Sidebar Title 1")
st.sidebar.write("Sidebar content 1")

# Add separator line
st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Add more sidebar content
st.sidebar.header("Sidebar Title 2")
st.sidebar.write("Sidebar content 2")

# Rest of your Streamlit app code
st.title("Main Content")
st.write("This is the main content of your Streamlit app.")