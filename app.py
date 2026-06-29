import streamlit as st
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Wide layout configuration
st.set_page_config(layout="wide")

# CSS stored in a safe string variable to prevent SyntaxErrors
CSS_STYLE = """
<style>
    body { background: #1a0000; color: #ff4500; font-family: 'Courier New', monospace; }
    .fire-box { border: 2px solid #ff4500; padding: 15px; box-shadow: 0 0 20px #ff0000; }
    input { width: 100%; box-sizing: border-box; background: #330000; color: #ffaa00; border: 1px solid #ff4500; padding: 10px; margin-top: 10px; }
    button { width: 100%; padding: 10px; background: #ff4500; border: none; margin-top: 10px; color: #000; font-weight: bold; }
</style>
"""

st.markdown(CSS_STYLE, unsafe_allow_html=True)
st.subheader("🔥 INFERNO PROXY MANAGER")

# User Inputs
target_url = st.text_input("Target URL")
image_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

if st.button("EXECUTE INJECTION"):
    if target_url and image_file:
        try:
            # 1. Fetch Target
            response = requests.get(target_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            base_url = f"{urlparse(target_url).scheme}://{urlparse(target_url).netloc}"

            # 2. Asset & Link Rewriting
            for tag in soup.find_all(['link', 'script', 'img', 'a']):
                if tag.name == 'a' and tag.has_attr('href'):
                    tag['target'] = '_self'
                for attr in ['href', 'src']:
                    if tag.has_attr(attr):
                        tag[attr] = urljoin(base_url, tag[attr])

            # 3. Image Injection
            encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
            img_tag = f'<img src="data:image/png;base64,{encoded_img}" style="position:fixed; top:20px; right:20px; z-index:99999; max-width: 200px;">'
            
            if soup.body:
                soup.body.insert(0, BeautifulSoup(img_tag, 'html.parser'))
            
            # 4. Rendering (Using compliant st.markdown)
            st.markdown(str(soup), unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Proxy Error: {str(e)}")
    else:
        st.warning("Please provide both a URL and an image.")
