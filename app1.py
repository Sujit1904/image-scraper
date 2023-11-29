import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import zipfile
from io import BytesIO
import base64
import shutil

# Function to scrape and save images
def scrape_and_save_images(name, size):
    GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='

    URL_input = GOOGLE_IMAGE + name
    st.write('Fetching from URL:', URL_input)

    URLdata = requests.get(URL_input)
    soup = BeautifulSoup(URLdata.text, "html.parser")
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

            # Create a BytesIO object to store the image data
            img_bytes = BytesIO(data.content)

            # Append the BytesIO object to the list
            image_urls.append((f'{i}{ext}', img_bytes))
            
            i += 1

            if i == size:
                break
        except:
            pass

    return image_urls

# Streamlit app
def main():
    st.title('Image Scraper Streamlit App')

    # Get user input for name and size
    name = st.text_input('Enter Image:')
    size = st.number_input('Enter the number of images:', min_value=1, step=1)

    # Call the function with user inputs
    if st.button('Scrape Images'):
        image_data = scrape_and_save_images(name, size)

        # Create a zip file containing the images
        with zipfile.ZipFile('images.zip', 'w') as zipf:
            for img_name, img_bytes in image_data:
                zipf.writestr(img_name, img_bytes.getvalue())

        # Display a download button for the zip file
        st.download_button(
            label='Download Images',
            data=zipf.read('images.zip'),
            file_name='images.zip',
            mime='application/zip',
        )

if __name__ == '__main__':
    main()
