import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from lxml import html

Base = declarative_base()


class ScrapedData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    date = Column(DateTime)
    link = Column(String)


engine = create_engine("sqlite:///scraped_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        elements = tree.xpath(
            '//*[@id="block-list"]/div/div[1]/div/div[2]/div[1]/a/span'
        )
        if elements:
            for element in elements:
                print(element.text)
        else:
            print("Element not found")


def save_to_database(title, content):
    data = ScrapedData(title=title, content=content)
    session.add(data)
    session.commit()


if __name__ == "__main__":
    url = "https://renginiai.kasvyksta.lt/vilnius"
    scrape_website(url)
