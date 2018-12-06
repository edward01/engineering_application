import datetime
from app import db


class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    client = db.Column(db.String(20), nullable=False, index=True)
    product_area = db.Column(db.String(20), nullable=False, index=True)

    def __repr__(self):
        return '<FeatureRequest {} {}>'.format(self.priority, self.title)


    def to_dict(self):
        data = {
            'id': self.id,
            'priority': self.priority,
            'title': self.title,
            'description': self.description,
            'target_date': self.target_date.strftime('%m/%d/%Y'),
            'client': self.client,
            'product_area': self.product_area,
        }
        return data