from app.extensions import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    latitude = db.Column(db.DECIMAL(8, 6))
    longitude = db.Column(db.DECIMAL(9, 6))

  
    def __repr__(self):
        return f'<City "{self.title}">'



