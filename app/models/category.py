from app.extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))

    def __repr__(self):
        return f'<Category "{self.title}">'
