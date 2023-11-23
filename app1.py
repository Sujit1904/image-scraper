import streamlit as st
import requests
import bs4
import shutil
import os

st.title('Image Scraper')

name = st.text_input('Search Term:', '')
size = st.number_input('Number of Images:', min_value=1, step=1)

if st.button('Scrape Images'):
    if not name or size <= 0:
        st.error('Invalid input parameters')
    else:
        st.info('Please wait...')
        st.write('Downloading images...')

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

        st.success('Downloaded successfully')
        st.write(f'Downloaded Image URLs: {image_urls}')
