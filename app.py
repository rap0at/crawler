from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_keyword(site, keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(site, headers=headers)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외 발생
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 페이지에서 키워드가 포함된 링크를 찾음
        links = soup.find_all('a', href=True)
        results = []
        for link in links:
            if keyword.lower() in link.text.lower():
                results.append({
                    'text': link.text.strip(),
                    'url': link['href']
                })
        
        if results:
            return results
        else:
            return [{"text": "키워드가 포함된 링크가 없습니다.", "url": ""}]
    except Exception as e:
        return [{"text": f"Error accessing {site}: {str(e)}", "url": ""}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    sites = data.get('sites')
    keyword = data.get('keyword')
    
    results = {}
    for site in sites:
        results[site] = search_keyword(site, keyword)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

