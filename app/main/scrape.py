import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from lxml import html
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scraped_data.db"
db = SQLAlchemy(app)


class ScrapedData(db.Model):
    __tablename__ = "scraped_data"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    location = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    link = db.Column(db.String)


class ScrapedCategories(db.Model):
    __tablename__ = "scraped_categories"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)


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
            else:
                continue

            if locations:
                location = locations[0]
            else:
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

            if title and location and start_date and end_date and url_to_event:
                data = ScrapedData(
                    title=title,
                    location=location,
                    start_date=start_date,
                    end_date=end_date,
                    link=url_to_event,
                )
                db.session.add(data)
                db.session.commit()
            else:
                continue


def save_category_to_database(category):
    data = ScrapedCategories(category=category)
    db.session.add(data)
    db.session.commit()


def scrape_categories(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="static-filter"]/div[2]/ul/li')
        for div_element in main_div:
            category = div_element.xpath(".//a/@class")[0]
            save_category_to_database(category)


city = "Vilnius"
category = "Koncertas"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        ScrapedData.query.delete()
        ScrapedCategories.query.delete()

        url_for_categories = "https://renginiai.kasvyksta.lt/"
        scrape_categories(url_for_categories)
        url = f"https://renginiai.kasvyksta.lt/{city}/{category}"
        scrape_events(url)
