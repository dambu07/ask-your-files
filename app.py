import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io
import tempfile
import fitz  
import time

load_dotenv()

genai.configure(api_key=os.getenv('Gemini_Api_Key'))

def find_img(prompt, image_data):
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    try:
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data 
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return "Error processing image: {}".format(e)
    
st.set_page_config(page_title="Text Extractor", page_icon="⚖️")

def input_img_setup(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            with tempfile.TemporaryDirectory() as temp_folder:
                images = []
                pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page_number in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_number)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    images.append(img)
            return images  # Return list of images for all pages
        else:
            return [uploaded_file.getvalue()]  # Return single image as a list
    else:
        raise FileNotFoundError("No File Uploaded")

###--- Title ---###
# Use st.markdown with HTML content
st.markdown("""
    <h1 style='text-align: center;'> 
        <span style='color: #F81F6F;'>Notes Extractor and Text Generator</span>
    </h1>
""", unsafe_allow_html=True)

# Again, use st.markdown for second header
st.markdown("""
    <h4 style='text-align: center;'>
        <span style='color: #f5f8fc;'>Upload Image or PDF</span>
        <span style='color: #f5f8fc;'>of your notes</span>
    </h4>
""", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Choose files", type=["jpg", "jpeg", "png", "webp", "pdf"], accept_multiple_files=True)
if uploaded_files:
    all_responses = []
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.type != "application/pdf":
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
            else:
                images = input_img_setup(uploaded_file)
                for idx, img in enumerate(images):
                    st.image(img, caption=f"Page {idx + 1} of {uploaded_file.name}", use_column_width=True)
        except Exception as e:
            st.error(f"Error processing file {uploaded_file.name}: {e}")

    imp = st.text_input("Chat with document")

    if imp:
        for uploaded_file in uploaded_files:
            if uploaded_file is None:
                st.error("Please upload a file before submitting.")
            else:
                image_data = input_img_setup(uploaded_file)
                with st.spinner('Just a moment...'):
                    time.sleep(15)
                prompt = imp
                for img in image_data:
                    response = find_img(prompt, img)
                    all_responses.append(response)

        st.header("The responses are: ")
        for response in all_responses:
            st.subheader("Here's what we found")
            st.write(response)
            st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

    # Other buttons and functionality remain the same
    res = st.button("Summarize It")
    submit = st.button("Extract Text")
    submit1 = st.button("Raise Questions")

    # Define your prompts
    prompt1 = "Summarize the extracted text from the uploaded file, image or document in a concise manner, highlighting the key points and main ideas. Ensure the summary is clear and easy to understand."
    prompt2 = "Extract the text from the uploaded file, image or document. Once the extraction is complete, provide a list of the topics mentioned in the file along with one-line descriptions for each in bullet format. After that, ask if I would like to convert the extracted text into another language. "
    prompt3 = "Analyze the extracted text from the uploaded file, image or document and generate a list of relevant questions based on the content. The questions should cover key concepts, important details, and any critical thinking prompts related to the material."


    # Handle button clicks
    if submit1:
        for uploaded_file in uploaded_files:
            if uploaded_file is None:
                st.error("Please upload a file before submitting.")
            else:
                image_data = input_img_setup(uploaded_file)
                with st.spinner('Just a moment...'):
                    time.sleep(15)
                for img in image_data:
                    response = find_img(prompt3, img)
                    st.header("The response is: ")
                    st.subheader("Here's what we found")
                    st.write(response)
                    st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

    if res:
        for uploaded_file in uploaded_files:
            if uploaded_file is None:
                st.error("Please upload a file before submitting.")
            else:
                image_data = input_img_setup(uploaded_file)
                with st.spinner('Just a moment...'):
                    time.sleep(15)
                for img in image_data:
                    response = find_img(prompt2, img)
                    st.header("The response is: ")
                    st.subheader("Here's what we found")
                    st.write(response)
                    st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

    if submit:
        for uploaded_file in uploaded_files:
            if uploaded_file is None:
                st.error("Please upload a file before submitting.")
            else:
                image_data = input_img_setup(uploaded_file)
                with st.spinner('Just a moment...'):
                    time.sleep(15)
                for img in image_data:
                    response = find_img(prompt1, img)
                    st.header("The response is: ")
                    st.subheader("Here's what we found")
                    st.write(response)
                    st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

footer = """
<style>
a:link, a:visited {
    color: #FFFFFF;
    background-color: transparent;
    text-decoration: underline;
}
a:hover, a:active {
    color: #7AE7C7;
    background-color: transparent;
    text-decoration: underline;
}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: ##F5BF03;
    text-align: center;
}
</style>
<div class="footer">
    <h8 style='text-align: center;'>
        <span style='color: #f5f8fc;'>Developed by </span> 
        <span style='color: #F81F6F;'> Raavi </span>
    </h8>
</div>
"""

# Now, you can use this string in Streamlit's markdown
import streamlit as st
st.markdown(footer, unsafe_allow_html=True)


#----------------------Hide Streamlit footer----------------------------
hide_st_style = """
<style>
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
#--------------------------------------------------------------------
