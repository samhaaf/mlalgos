from src import db

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), index=True, unique=True)
    body = db.Column(db.String(5000), index=True, unique=False)
    tex = db.Column(db.String(5000), index=True, unique=False)

    def __repr__(self):
        return '<Page %r>' % self.url


# class LaTeX(db.Model):
    # formula = db.Column(db.)