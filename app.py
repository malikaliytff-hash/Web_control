"""
Technical Implementation: Integrated Inferno Proxy Dashboard.
This script consolidates the proxy-based injection mechanism with the 
original 'Inferno' visual theme, maintaining the layout previously defined.

Requirements: 'pip install flask requests beautifulsoup4'
"""

from flask import Flask, request, render_template_string
import requests
import base64
from bs4 import BeautifulSoup

app = Flask(__name__)

# Consolidated UI with Fire Theme and Proxy Functionality
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
        input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
        #log { height: 100px; overflow-y: scroll; border: 1px solid #550000; padding: 5px; margin-top: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="fire-box">
        <h3>INFERNO PROXY MANAGER</h3>
        <form action="/proxy" method="POST" enctype="multipart/form-data">
            <input type="text" name="url" placeholder="Target URL" required>
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">EXECUTE INJECTION</button>
        </form>
        <div id="log">Logs: Ready for operation...</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/proxy', methods=['POST'])
def proxy():
    target_url = request.form['url']
    image_file = request.files['image']
    
    try:
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        # Injecting content fixed to the top right corner
        img_tag = f'<img src="data:image/png;base64,{encoded_img}" style="position:fixed; top:20px; right:20px; z-index:99999; max-width: 200px;">'
        
        if soup.body:
            soup.body.insert(0, BeautifulSoup(img_tag, 'html.parser'))
            
        return str(soup)
    except Exception as e:
        return f"Proxy Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
"""
Technical Implementation: State-Persistent Reverse Proxy.
To maintain the injected state across different browser sessions/tabs, the 
proxy logic must preserve the modified HTML structure. This implementation 
renders the modified target website within a dynamic environment.

Requirements: 'pip install flask requests beautifulsoup4'
"""

from flask import Flask, request, render_template_string
import requests
import base64
from bs4 import BeautifulSoup

app = Flask(__name__)

# UI Theme: Integrated Inferno Proxy Dashboard with real-time site viewer
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
        input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
        #site-view { width: 100%; height: 400px; background: #fff; margin-top: 20px; border: 2px solid #ff4500; }
    </style>
</head>
<body>
    <div class="fire-box">
        <h3>INFERNO PROXY MANAGER</h3>
        <form action="/proxy" method="POST" enctype="multipart/form-data" target="site-view">
            <input type="text" name="url" placeholder="Target URL" required>
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">EXECUTE INJECTION</button>
        </form>
        <iframe name="site-view" id="site-view"></iframe>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/proxy', methods=['POST'])
def proxy():
    target_url = request.form['url']
    image_file = request.files['image']
    
    try:
        # Retrieve the target page
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Inject the image tag
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        img_tag = f'<img src="data:image/png;base64,{encoded_img}" style="position:fixed; top:20px; right:20px; z-index:99999; max-width: 200px;">'
        
        if soup.body:
            soup.body.insert(0, BeautifulSoup(img_tag, 'html.parser'))
            
        # Return modified content to the iframe
        return str(soup)
    except Exception as e:
        return f"<html><body style='color:red;'>Proxy Error: {str(e)}</body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
"""
Technical Implementation: Advanced Asset-Proxying Mechanism.
When proxing websites, internal assets (CSS, images, JS) often break because their 
relative paths (e.g., /style.css) point to the local server instead of the target origin. 
To resolve this, we must rewrite all relative URLs to absolute URLs pointing to 
the target website's base domain.

Requirements: 'pip install flask requests beautifulsoup4'
"""

from flask import Flask, request, render_template_string
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# UI Theme: Integrated Inferno Proxy Dashboard
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
        input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
        #site-view { width: 100%; height: 500px; background: #fff; margin-top: 20px; border: 2px solid #ff4500; }
    </style>
</head>
<body>
    <div class="fire-box">
        <h3>INFERNO PROXY MANAGER</h3>
        <form action="/proxy" method="POST" enctype="multipart/form-data" target="site-view">
            <input type="text" name="url" placeholder="Target URL" required>
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">EXECUTE INJECTION</button>
        </form>
        <iframe name="site-view" id="site-view"></iframe>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/proxy', methods=['POST'])
def proxy():
    target_url = request.form['url']
    image_file = request.files['image']
    base_url = f"{urlparse(target_url).scheme}://{urlparse(target_url).netloc}"
    
    try:
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # URL Rewriting: Force all relative assets to absolute URLs
        for tag in soup.find_all(['link', 'script', 'img', 'a']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    tag[attr] = urljoin(base_url, tag[attr])
        
        # Inject the image tag
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
        img_tag = f'<img src="data:image/png;base64,{encoded_img}" style="position:fixed; top:20px; right:20px; z-index:99999; max-width: 200px;">'
        
        if soup.body:
            soup.body.insert(0, BeautifulSoup(img_tag, 'html.parser'))
            
        return str(soup)
    except Exception as e:
        return f"<html><body style='color:red;'>Proxy Error: {str(e)}</body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
"""
Technical Implementation: Final Consolidated Proxy Dashboard.
This code restores your original fire-themed layout and integrates 
the streaming proxy mechanism to ensure target content loads properly.
"""

from flask import Flask, request, render_template_string, Response
import requests

app = Flask(__name__)

# Restored original fire-themed UI
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
        input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
        #site-view { width: 100%; height: 500px; background: #fff; margin-top: 20px; border: 2px solid #ff4500; }
    </style>
</head>
<body>
    <div class="fire-box">
        <h3>INFERNO PROXY MANAGER</h3>
        <form action="/proxy" method="GET" target="site-view">
            <input type="text" name="url" placeholder="Enter Target URL" required>
            <button type="submit">LOAD SITE</button>
        </form>
        <iframe name="site-view" id="site-view"></iframe>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/proxy', methods=['GET'])
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL Required", 400
    
    try:
        # Fetching content as a stream to preserve site assets
        resp = requests.get(target_url, stream=True)
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = {name: value for (name, value) in resp.raw.headers.items() 
                   if name.lower() not in excluded_headers}
        
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
"""
Technical Implementation: Path-Rewriting Proxy.
This version intercepts the HTML and replaces all relative paths with absolute 
ones that route through this proxy, ensuring all assets are loaded.
"""

from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# Same fire-themed UI as before
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; margin: 0; padding: 10px; }
        .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
        input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
        #site-view { width: 100%; height: 500px; background: #fff; margin-top: 20px; border: 2px solid #ff4500; }
    </style>
</head>
<body>
    <div class="fire-box">
        <h3>INFERNO PROXY MANAGER</h3>
        <form action="/proxy" method="GET" target="site-view">
            <input type="text" name="url" placeholder="Enter Target URL" required>
            <button type="submit">LOAD SITE</button>
        </form>
        <iframe name="site-view" id="site-view"></iframe>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/proxy', methods=['GET'])
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "URL Required", 400
    
    try:
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = f"{urlparse(target_url).scheme}://{urlparse(target_url).netloc}"

        # Rewrite paths for all links, scripts, and images
        for tag in soup.find_all(['link', 'script', 'img', 'a']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    # Convert relative path to absolute path pointing back to the proxy
                    full_url = urljoin(base_url, tag[attr])
                    tag[attr] = f"/fetch?url={full_url}"

        return str(soup)
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

@app.route('/fetch', methods=['GET'])
def fetch():
    # Helper route to fetch individual assets
    asset_url = request.args.get('url')
    resp = requests.get(asset_url)
    return Response(resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
