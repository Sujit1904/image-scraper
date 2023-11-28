import streamlit as st
import requests
import bs4
import shutil
import os

# Set page title and favicon
st.set_page_config(
    page_title="Image Scraper",
    page_icon=":camera:",
    layout="centered", 
)
# Apply the custom background color using CSS
st.markdown(
    f"""
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(45deg, #3498db, #8e44ad);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .stApp {{
            max-width: 600px;
            max-height:700px;
            margin: 0 auto;
        }}
        .stButton {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }}
        .stButton>button {{
           background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }}
        .stButton>button:hover {{
            background-color: #0056b3;
        }}
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {{
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            background-color: #ecf0f1;
        }}
        .stError>div,
        .stSuccess>div {{
            color: #fff;
            margin-top: 10px;
            font-size: 18px;
        }}
        #loading-spinner {{
            display: none;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #2ecc71;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title('Image Scraper :mag_right:')
st.markdown("""Scrape images from Google Images !!!""")

# User input fields
name = st.text_input('Search Images:')
size = st.number_input('Number of Images:', min_value=1, step=1)

# Button to trigger image scraping
scrape_button = st.button('Scrape Images')

# Loading spinner
loading_spinner = st.empty()

if scrape_button:
    if not name or size <= 0:
        st.error('Invalid input parameters. Please provide a valid search term and a positive number of images.')
    else:
        loading_spinner.text('Downloading images...')
        loading_spinner.markdown('<div id="loading-spinner"></div>', unsafe_allow_html=True)

        GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='
        URL_input = GOOGLE_IMAGE + name
        URLdata = requests.get(URL_input)
        soup = bs4.BeautifulSoup(URLdata.text, "html.parser")
        img = soup.find_all('img')

        i = 0
        image_urls = []

        for link in img:
            try:
                images = link.get('src')
                ext = images[images.rindex('.'):]
                if ext.startswith('.png'):
                    ext = '.png'
                elif ext.startswith('.jpg'):
                    ext = '.jpg'
                elif ext.startswith('.jfif'):
                    ext = '.jfif'
                elif ext.startswith('.com'):
                    ext = '.jpg'
                elif ext.startswith('.svg'):
                    ext = '.svg'
                data = requests.get(images, stream=True)
                newpath = f'./images/{name}/'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                filename = newpath + str(i) + ext
                with open(filename, 'wb') as file:
                    shutil.copyfileobj(data.raw, file)
                i += 1
                image_urls.append(filename)

                if i == size:
                    break
            except:
                pass

        loading_spinner.empty()
        st.success('Downloaded successfully')
