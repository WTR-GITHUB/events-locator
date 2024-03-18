import requests
from sqlalchemy import create_engine, Column, String, Integer, DateTime, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from lxml import html
from datetime import datetime

Base = declarative_base()


class ScrapedData(Base):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    link = Column(String)


class ScrapedCategories(Base):
    __tablename__ = "scraped_categories"
    id = Column(Integer, primary_key=True)
    category = Column(String)


engine = create_engine("sqlite:///scraped_data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.execute(delete(ScrapedData))
session.execute(delete(ScrapedCategories))
session.commit()


def scrape_events(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="block-list"]/div/div')

        for div_element in main_div:
            title = div_element.xpath(".//div/div[2]/div[1]/a/span/text()")
            locations = div_element.xpath(".//div/div[2]/div[2]/a/text()")
            start_date_info = div_element.xpath(".//div/meta[2]/@content")
            end_date_info = div_element.xpath(".//div/meta[1]/@content")
            url_to_event = (
                div_element.xpath(".//div/meta[2]/@content")[1]
                if len(div_element.xpath(".//div/meta[2]/@content")) > 1
                else None
            )

            if title:
                title = title[0]
                print("Title:", title)
            else:
                print("Title not found")
                continue

            if locations:
                location = locations[0]
                print("Location:", location)
            else:
                print("Location not found")
                continue

            start_date = (
                datetime.strptime(start_date_info[0], "%Y-%m-%d %H:%M:%S")
                if start_date_info
                else None
            )
            end_date = (
                datetime.strptime(end_date_info[0], "%Y-%m-%d %H:%M:%S")
                if end_date_info
                else None
            )

            if start_date:
                print("Start date:", start_date)
            else:
                print("Start date not found")

            if end_date:
                print("End date:", end_date)
            else:
                print("End date not found")

            if url_to_event:
                print("Link:", url_to_event)
            else:
                print("Link not found")

            if title and location and start_date and end_date and url_to_event:
                data = ScrapedData(
                    title=title,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    link=url_to_event,
                )
                session.add(data)
                session.commit()
            else:
                print("Skipping event due to missing information")


def save_category_to_database(category):
    data = ScrapedCategories(category=category)
    session.add(data)
    session.commit()


def scrape_categories(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="static-filter"]/div[2]/ul/li')
        for div_element in main_div:
            category = div_element.xpath(".//a/@class")[0]
            print("Category:", category)
            save_category_to_database(category)


city = "Vilnius"
category = "Koncertas"

if __name__ == "__main__":
    url_for_categories = "https://renginiai.kasvyksta.lt/"
    scrape_categories(url_for_categories)
    url = f"https://renginiai.kasvyksta.lt/{city}/{category}"
    scrape_events(url)
