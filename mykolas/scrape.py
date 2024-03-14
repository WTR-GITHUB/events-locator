import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# Define your data model
class ScrapedData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    date = Column(DateTime)
    link = Column(String)


# Set up your database connection
engine = create_engine("sqlite:///scraped_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Function to scrape data
def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Scraping logic here
        # For example:
        titles = soup.find_all("h1")
        contents = soup.find_all("p")
        for title, content in zip(titles, contents):
            save_to_database(title.text, content.text)
    else:
        print("Failed to fetch the webpage.")


# Function to save data into database
def save_to_database(title, content):
    data = ScrapedData(title=title, content=content)
    session.add(data)
    session.commit()


# Example usage
if __name__ == "__main__":
    url = "https://example.com"
    scrape_website(url)
