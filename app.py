import streamlit as st
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- Your original UI string, properly wrapped in triple quotes ---
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
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="url" placeholder="Enter Target URL" required>
            <input type="file" name="image" accept="image/*" required>
            <button type="submit" name="execute">EXECUTE INJECTION</button>
        </form>
    </div>
</body>
</html>
"""

# Render the UI
st.components.v1.html(HTML_UI, height=350)

# Proxy logic
# We capture inputs from the form via streamlit's input methods
target_url = st.text_input("Target URL (for proxy processing)")
uploaded_file = st.file_uploader("Upload Image")

if st.button("EXECUTE INJECTION"):
    if target_url and uploaded_file:
        try:
            response = requests.get(target_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            base_url = f"{urlparse(target_url).scheme}://{urlparse(target_url).netloc}"

            # Asset Rewriting
            for tag in soup.find_all(['link', 'script', 'img', 'a']):
                for attr in ['href', 'src']:
                    if tag.has_attr(attr):
                        tag[attr] = urljoin(base_url, tag[attr])

            # Image Injection
            encoded_img = base64.b64encode(uploaded_file.read()).decode('utf-8')
            img_tag = f'<img src="data:image/png;base64,{encoded_img}" style="position:fixed; top:20px; right:20px; z-index:99999; max-width: 200px;">'
            
            if soup.body:
                soup.body.insert(0, BeautifulSoup(img_tag, 'html.parser'))
                
            # Render result
            st.components.v1.html(str(soup), height=800, scrolling=True)
        except Exception as e:
            st.error(f"Proxy Error: {str(e)}")
    else:
        st.warning("Please enter a URL and upload an image.")
