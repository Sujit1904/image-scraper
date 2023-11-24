from flask import Flask, render_template, request, jsonify
import bs4
import requests
import shutil
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape_images', methods=['POST'])
def scrape_images():
    data = request.get_json()
    name = data.get('name', '')
    size = int(data.get('size', 0))

    if not name or size <= 0:
        return jsonify({'error': 'Invalid input parameters'})

    GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='

    URL_input = GOOGLE_IMAGE + name
    print('Fetching from URL:', URL_input)

    URLdata = requests.get(URL_input)
    soup = bs4.BeautifulSoup(URLdata.text, "html.parser")
    img = soup.find_all('img')
    i = 0
    print('Please wait...')
    
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

    response_data = {
        'message': 'Downloaded successfully',
    }

    return jsonify(response_data)
 
if __name__ == '__main__':
    app.run(host="https://image-scraper.streamlit.app",port=5748)
