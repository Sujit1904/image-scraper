from flask import Flask, render_template, request, jsonify
import bs4
import requests
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

    try:
        URLdata = requests.get(URL_input)
        URLdata.raise_for_status()  # Check for HTTP errors
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
                download_path = os.path.join('static', 'images', name, f'{i}{ext}')  
                i += 1
                image_urls.append(download_path)
                os.makedirs(os.path.dirname(download_path), exist_ok=True)
                with open(download_path, 'wb') as file:
                    for chunk in data.iter_content(chunk_size=1024):
                        file.write(chunk)

                if i == size:
                    break
            except Exception as e:
                print(f"Error: {e}")

        response_data = {
            'message': 'Downloaded successfully',
            'image_urls': image_urls,
        }

        return jsonify(response_data)

    except requests.RequestException as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
