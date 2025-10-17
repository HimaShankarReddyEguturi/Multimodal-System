import streamlit as st
import os
import tempfile
# Import functions from your separate files
from processing import process_file_to_parts
from database_rag import answer_query_with_context 

st.set_page_config(page_title="Multimodal Data Processor", layout="wide")
st.title("🤖 Multimodal Data Processing System (Gemini RAG)")
st.caption("Processes uploaded files (text, images, PDFs) and answers natural language queries.")

# Initialize session state for storing all processed content
if 'all_parts' not in st.session_state:
    st.session_state.all_parts = []
if 'files_processed' not in st.session_state:
    st.session_state.files_processed = 0

# --- File Upload Section ---
st.header("1. Upload Input Files")
uploaded_files = st.file_uploader(
    "Upload Text (.txt, .md), Documents (.pdf), or Images (.png, .jpg)", 
    accept_multiple_files=True
)

if st.button("Process Files and Build Context"):
    if not uploaded_files:
        st.warning("Please upload files first.")
    else:
        st.session_state.all_parts = []
        st.session_state.files_processed = 0
        
        with st.spinner(f"Processing {len(uploaded_files)} files..."):
            
            # Use temp directory to save uploaded files for processing
            with tempfile.TemporaryDirectory() as tmpdir:
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(tmpdir, uploaded_file.name)
                    # Write the file to the temp directory
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process the saved file
                    parts = process_file_to_parts(file_path)
                    st.session_state.all_parts.extend(parts)
                    st.session_state.files_processed += 1
                    
            st.success(f"Successfully processed {st.session_state.files_processed} files! Context is ready.")
            st.info(f"Total parts generated: {len(st.session_state.all_parts)}")

st.markdown("---")

# --- Query Section ---
st.header("2. Ask a Natural Language Query")
query = st.text_input(
    "Enter your question here:", 
    "What are the key points in the documents I uploaded?"
)

if st.button("Get Answer from Context"):
    if st.session_state.files_processed == 0:
        st.error("Please upload and process files first.")
    elif not query:
        st.error("Please enter a question.")
    else:
        with st.spinner('Generating answer using Gemini...'):
            
            # Pass the user query and all gathered content to the RAG function
            answer = answer_query_with_context(query, st.session_state.all_parts)
            
            st.subheader("🤖 Gemini Response")
            st.markdown(answer)

st.markdown("---")
st.caption(f"Context currently built from {st.session_state.files_processed} files.")