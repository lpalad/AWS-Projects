import requests
import base64
import markdown
from bs4 import BeautifulSoup
import boto3
import time
import config

headers = {}
if config.GITHUB_TOKEN:
    headers['Authorization'] = f'token {config.GITHUB_TOKEN}'

def get_repo_contents(repo_name, path=""):
    url = f"https://api.github.com/repos/{config.GITHUB_ORG}/{repo_name}/contents/{path}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def process_markdown_file(repo_name, file_path):
    url = f"https://api.github.com/repos/{config.GITHUB_ORG}/{repo_name}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    content_data = response.json()
    file_content = base64.b64decode(content_data['content']).decode('utf-8')
    
    # Convert markdown to HTML, then extract text
    html = markdown.markdown(file_content)
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    
    return {
        'id': f"{repo_name}#{file_path}",
        'service': repo_name.lower(),
        'title': file_path,
        'content': "\n".join(paragraphs),
        'url': f"https://github.com/{config.GITHUB_ORG}/{repo_name}/blob/master/{file_path}"
    }
