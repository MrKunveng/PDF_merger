import streamlit as st
import os
from PyPDF2 import PdfMerger
import tempfile

st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="centered"
)

def merge_pdfs(pdf_files):
    try:
        # Create a PdfMerger object
        merger = PdfMerger()
        
        if not pdf_files:
            st.error("Please upload PDF files!")
            return None
        
        # Create a temporary directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files to temporary directory and merge
            for pdf in pdf_files:
                temp_path = os.path.join(temp_dir, pdf.name)
                with open(temp_path, 'wb') as f:
                    f.write(pdf.getbuffer())
                merger.append(temp_path)
            
            # Create merged PDF in memory
            merged_pdf_path = os.path.join(temp_dir, "merged.pdf")
            merger.write(merged_pdf_path)
            
            # Read the merged PDF for download
            with open(merged_pdf_path, 'rb') as f:
                merged_pdf = f.read()
            
        merger.close()
        return merged_pdf
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
    finally:
        if 'merger' in locals():
            merger.close()

def main():
    st.title("📄 PDF Merger")
    st.write("Upload multiple PDF files to merge them into a single PDF.")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload PDF files", 
        type="pdf",
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} files:")
        for file in uploaded_files:
            st.write(f"- {file.name}")
        
        if st.button("Merge PDFs"):
            with st.spinner("Merging PDFs..."):
                merged_pdf = merge_pdfs(uploaded_files)
                
                if merged_pdf:
                    st.success("PDFs merged successfully!")
                    st.download_button(
                        label="Download Merged PDF",
                        data=merged_pdf,
                        file_name="merged_pdf.pdf",
                        mime="application/pdf"
                    )

if __name__ == "__main__":
    main() 