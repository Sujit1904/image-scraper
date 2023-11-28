import streamlit as st
import requests
import bs4
import shutil
import os

# Set page title and favicon with a camera icon
st.set_page_config(
    page_title="Image Scraper",
    page_icon="📷",  # Camera icon
    layout="wide",  # Use wide layout for a better background color display
)

# Define a custom background color
background_color = "#3498db"

# Apply the custom background color using CSS
st.markdown(
    f"""
    <style>
        body {{
            background-color: {background_color};
            margin: 0;
            font-family: 'Arial', sans-serif;
        }}
        .stApp {{
            max-width: 600px;
            margin: 0 auto;
        }}
        .stButton {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }}
        .stButton>button {{
            color: #fff;
            background-color: #2ecc71;  /* Green color for button */
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #27ae60;  /* Darker green on hover */
        }}
        .stTextInput>div>div>input {{
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            background-color: #ecf0f1;  /* Light grey for input field */
        }}
        .stNumberInput>div>div>input {{
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            background-color: #ecf0f1;  /* Light grey for input field */
        }}
        .stError>div {{
            color: #8B0000;
            margin-top: 10px;
            font-size: 18px;
        }}
        .stSuccess>div {{
            color: #008000;
            margin-top: 10px;
            font-size: 18px;
        }}
        #loading-spinner {{
            display: none;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #2ecc71;  /* Green color for spinner */
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
        .stTitle {{
            text-align: center;
            padding: 20px;
            color: #fff;
            font-size: 30px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="stTitle">Image Scraper :mag_right:</div>', unsafe_allow_html=True)
st.markdown("""
    This app allows you to scrape images from Google Images.
    Enter a search term and the number of images you want to download.
""")

# User input fields
name = st.text_input('Search Term:')
size = st.number_input('Number of Images:', min_value=1, step=1)

# Button to trigger image scraping
scrape_button = st.button('Scrape Images')

# Loading spinner
loading_spinner = st.empty()

# List to store downloaded image URLs
image_urls = []

if scrape_button:
    if not name or size <= 0:
        st.error('Invalid input parameters. Please provide a valid search term and a positive number of images.')
    else:
        loading_spinner.text('Downloading images...')
        loading_spinner.markdown('<div id="loading-spinner"></div>', unsafe_allow_html=True)

        # Set the path to save images
        images_path = os.path.join(st._cli.get_main_script_path(), 'images', name)
        os.makedirs(images_path, exist_ok=True)

        GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='
        URL_input = GOOGLE_IMAGE + name
        URLdata = requests.get(URL_input)
        soup = bs4.BeautifulSoup(URLdata.text, "html.parser")
        img = soup.find_all('img')

        i = 0

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
                filename = os.path.join(images_path, f'{i}{ext}')
                with open(filename, 'wb') as file:
                    shutil.copyfileobj(data.raw, file)
                i += 1
                image_urls.append(filename)

                if i == size:
                    break
            except:
                pass

        loading_spinner.empty()  # Clear the loading spinner
        st.success('Downloaded successfully')

# Display the downloaded image URLs
if image_urls:
    st.markdown('### Downloaded Image URLs:')
    st.write(image_urls)
