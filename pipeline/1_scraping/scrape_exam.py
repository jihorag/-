import requests
from bs4 import BeautifulSoup
import json

url = 'https://cbtbank.kr/exam/cem20250405'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

questions = soup.find_all(class_='card') # Wait, I don't know the exact class yet. Let's just find the first few questions or print the structure.

# Let's save the HTML to a file so we can view its structure
with open('exam_raw.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
