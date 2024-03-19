from app.extensions import db


class ScrapeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    start_date = db.Column(db.String(12))
    end_date = db.Column(db.String(12))
    link = db.Column(db.String(100))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("City", cascade="all, delete", passive_deletes=True)
    category_id = db.Column(db.Integer, db.ForeignKey("catogory.id"))
    category = db.relationship("Category", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f'<Event title "{self.title}">'
