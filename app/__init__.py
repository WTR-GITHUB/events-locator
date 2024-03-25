import json
from flask import Flask
from config import Config
from app.extensions import db
from app.models.models import ScrapeData, Category
from app.utility.scrape import scrape_categories, scrape_cities, scrape_events
from flask_apscheduler import APScheduler

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
            scrape_events(url=url, city=city, category=category)

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        from app.models import models

        db.create_all()
        scheduler.add_job(id='Scheduled Task', func=scrape_and_update, trigger='interval', hours=24)

    # Register blueprints here
    from app.routes import bp as main_bp

    app.register_blueprint(main_bp)

    return app


