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
    model = genai.GenerativeModel('gemini-pro-vision')
    try:
        
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data 
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return "Error processing image: {}".format(e)


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
            
            image = images[0]
            
            with io.BytesIO() as output:
                image.save(output, format="JPEG")
                return output.getvalue()
        else:
            
            return uploaded_file.getvalue()
    else:
        raise FileNotFoundError("No File Uploaded")

st.title(":red[SmartScript] ")
st.header("Upload image or pdf of your notes")
uploaded_file = st.file_uploader(type=["jpg", "jpeg", "png", "webp","pdf"], label="")

if uploaded_file is not None:
    try:
        if uploaded_file.type != "application/pdf":
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing file: {e}")

imp = st.text_input("Chat with document")

if imp:
    if uploaded_file is None:
        st.error("Please upload a file before submitting.")
    else:
        image_data = input_img_setup(uploaded_file)
        with st.spinner('Just a moment...'):
          time.sleep(15)
        prompt = imp
        response = find_img(prompt, image_data)
        st.header("The response is: ")
        st.subheader("Here's what we found")
        st.write(response)
        st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

 # Other buttons and functionality remain the same
    res = st.button("Summarize It")
    submit = st.button("Extract Text")
    submit1 = st.button("Raise Questions")

    # Define your prompts
    prompt1 = """
        Summarize the extracted text from the uploaded file, image or document in a concise manner, highlighting the key points and main ideas. Ensure the summary is clear and easy to understand.
        """
    prompt2 = """
        Extract the text from the uploaded file, image or document. Once the extraction is complete, provide a list of the topics mentioned in the file along with one-line descriptions for each in bullet format. After that, ask if I would like to convert the extracted text into another language.
        """
    prompt3 = """
        Analyze the extracted text from the uploaded file, image or document and generate a list of relevant questions based on the content. The questions should cover key concepts, important details, and any critical thinking prompts related to the material.
        """

    
if submit1:
    if uploaded_file is None:
        st.error("Please upload a file before submitting.")
    else:
        image_data = input_img_setup(uploaded_file)
        with st.spinner('Just a moment...'):
          time.sleep(15)
        response = find_img(prompt3, image_data)
        st.header("The response is: ")
        st.subheader("Here's what we found")

        st.write(response)
        st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

if res:
    if uploaded_file is None:
        st.error("Please upload a file before submitting.")
    else:
        image_data = input_img_setup(uploaded_file)
        with st.spinner('Just a moment...'):
          time.sleep(15)
        response = find_img(prompt2, image_data)
        st.header("The response is: ")
        st.subheader("Here's what we found")
        st.write(response)
        st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

if submit:
    if uploaded_file is None:
        st.error("Please upload a file before submitting.")
    else:
        image_data = input_img_setup(uploaded_file)
        with st.spinner('Just a moment...'):
          time.sleep(15)
        response = find_img(prompt1, image_data)
        st.header("The response is: ")
        st.subheader("Here's what we found")
        st.write(response)
        st.info("Information provided may be inaccurate. Kindly consider double-checking the responses.")

        #--------------------------------------------------------------------
    hide_st_style = """
        <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
       </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
