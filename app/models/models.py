



class ScrapedData(db.Model):
    __tablename__ = "scraped_data"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    link = Column(String)


class ScrapedCategories(db.Model):
    __tablename__ = "scraped_categories"
    id = Column(Integer, primary_key=True)
    category = Column(String)