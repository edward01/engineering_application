import datetime
from app import db


class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, nullable=False)
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


    def set_priority(self, new_priority):
        if self.priority < new_priority:
            # small to big
            priority_adjusted_value = -1
            feature_requests = FeatureRequest.query \
                .filter(FeatureRequest.client == self.client, FeatureRequest.priority > self.priority, FeatureRequest.priority <= new_priority) \
                .order_by(FeatureRequest.priority) \
                .all()
        else:
            # big to small
            priority_adjusted_value = 1
            feature_requests = FeatureRequest.query \
                .filter(FeatureRequest.client == self.client, FeatureRequest.priority < self.priority, FeatureRequest.priority >= new_priority) \
                .order_by(FeatureRequest.priority.desc()) \
                .all()

        for item in feature_requests:
            item.priority = item.priority + priority_adjusted_value

        # set the final priority
        self.priority = new_priority


    @classmethod
    def adjust_priorities(cls, client, starting_priority, incrementor):
        '''
        @incrementor (int): can be 1 or -1
        '''
        feature_requests = FeatureRequest.query \
            .filter(FeatureRequest.client == client, FeatureRequest.priority >= starting_priority) \
            .order_by(FeatureRequest.priority.desc()) \
            .all()
        for item in feature_requests:
            item.priority = item.priority + incrementor