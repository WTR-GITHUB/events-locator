import datetime
import html
import requests
from app.models.models import ScrapeData, Category, City
from app.extensions import db
from lxml import html
from datetime import datetime


def scrape_cities(url):
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="static-filter"]/div[1]/ul/li')
        cities = [div_element.xpath(".//a/text()")[0] for div_element in main_div]
        return cities


def scrape_events(url, city_name, category_title):
    city_id = City.query.filter_by(city_name=city_name).first()
    if city_id is None:
        print(f"City '{city_name}' not found in the database.")
        return

    response = requests.get(url)
    if (
        response.status_code == 200
        and response.url != "https://renginiai.kasvyksta.lt/"
    ):
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="block-list"]/div/div')

        for div_element in main_div:
            title = div_element.xpath(".//div/div[2]/div[1]/a/span/text()")
            print(title)
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
                category = Category.query.filter_by(title=category_title).first()
                if category is None:
                    print(f"Category '{category_title}' not found in the database.")
                    continue

                data = ScrapeData(
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    link=url_to_event,
                    city_id=city_id,
                    city=city_name,
                    category_id=category,
                    category=category,
                )
                # print(title)
                db.session.add(data)
                db.session.commit()
            else:
                continue


def save_category_to_database(category_title):
    existing_category = Category.query.filter_by(title=category_title).first()
    if existing_category is None:
        data = Category(title=category_title)
        db.session.add(data)
        db.session.commit()


def scrape_categories(url):
    response = requests.get(url)
    categories = []
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        main_div = tree.xpath('//*[@id="static-filter"]/div[2]/ul/li')
        for div_element in main_div:
            category = div_element.xpath(".//a/@class")[0]
            categories.append(category)
            save_category_to_database(category)
    return categories


def scrape_and_update():
    ScrapeData.query.delete()
    Category.query.delete()

    url_for_categories_and_cities = "https://renginiai.kasvyksta.lt/"
    scraped_categories = scrape_categories(url_for_categories_and_cities)
    cities_with_events = scrape_cities(url_for_categories_and_cities)
    for city in cities_with_events:
        for category in scraped_categories:
            url = f"https://renginiai.kasvyksta.lt/{city.lower()}/{category}"
            print(url)
            scrape_events(url=url, city_name=city, category_title=category)


if __name__ == "__main__":
    scrape_and_update()
