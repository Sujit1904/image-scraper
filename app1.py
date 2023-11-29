import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import shutil

# Function to scrape and save images
def scrape_and_save_images(name, size, download_path):
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

            # Combine the user-specified download path with the filename
            filename = os.path.join(download_path, f'{i}{ext}')

            with open(filename, 'wb') as file:
                shutil.copyfileobj(data.raw, file)

            i += 1
            image_urls.append(filename)

            if i == size:
                break
        except:
            pass

    response_data = {
        'message': 'Downloaded successfully',
        'image_urls': image_urls,
    }

    return response_data

# Streamlit app
def main():
    st.title('Image Scraper Streamlit App')

    # Get user input for name, size, and download path
    name = st.text_input('Enter search term:')
    size = st.number_input('Enter the number of images:', min_value=1, step=1)
    download_path = st.text_input('Enter the download path:')

    # Call the function with user inputs
    if st.button('Scrape Images'):
        result = scrape_and_save_images(name, size, download_path)
        st.write(result)

if __name__ == '__main__':
    main()
