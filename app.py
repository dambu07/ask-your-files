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

res = st.button("Explore Topics")
submit = st.button("Generate Questionnaire")
submit1 = st.button("Collect Formulas")

prompt1 = """
    Make a short quiz out of the image along with their answers including short explanation and formulas
    """

prompt2 = """
    List out the topics in the image and write one line descriptions for them in bullet format. After completing, provide study material websites for reference for the listed topics
    """
prompt3 = """ 
    List out only the formulas in the image without any explanation or any description
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


footer="""<style>
a:link , a:visited{
color: #FFFFFF;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: #7AE7C7;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color:transparent;
color: ##F5BF03;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by SmartScripters </p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)