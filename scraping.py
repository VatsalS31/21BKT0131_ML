import requests
from bs4 import BeautifulSoup
from db import SessionLocal
from models.document_model import Document

def scrape_news():
    session = SessionLocal()
    response = requests.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", class_="storylink")

    for article in articles:
        title = article.get_text()
        url = article["href"]

        new_doc = Document(title=title, content=url)
        session.add(new_doc)

    session.commit()
    session.close()
