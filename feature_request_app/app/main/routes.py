from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from app.models import FeatureRequest
from app.main.forms import FeatureRequestForm


CLIENT_CHOICES = [
    { 'text': "Client A", 'value': 'client_a' },
    { 'text': "Client B", 'value': 'client_b' },
    { 'text': "Client C", 'value': 'client_c' }
]
PRODUCT_AREA_CHOICES = [
    { 'text': "Billing", 'value': 'billing' },
    { 'text': "Claims", 'value': 'claims' },
    { 'text': "Policies", 'value': 'policies' },
    { 'text': "Reports", 'value': 'reports' }
]


@bp.before_app_request
def before_request():
    pass


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = FeatureRequestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.id.data < 1:
                # Insert Mode
                feature_request = FeatureRequest(
                    priority=form.priority.data,
                    title=form.title.data,
                    description=form.description.data,
                    target_date=form.target_date.data,
                    client=form.client.data,
                    product_area=form.product_area.data
                )
                db.session.add(feature_request)
            else:
                # Update mode
                feature_request = FeatureRequest.query.get(form.id.data)
                current_priority = feature_request.priority
                update_priority = True if current_priority != form.priority.data else False

                feature_request.title = form.title.data
                feature_request.description = form.description.data
                feature_request.target_date = form.target_date.data
                feature_request.client = form.client.data
                feature_request.product_area = form.product_area.data

                if update_priority:
                    feature_request.priority = 0  # set temporary priority value

                    # Adjust priority value of affeced records
                    if current_priority < form.priority.data:
                        # small to big
                        priority_adjusted_value = -1
                        feature_requests = FeatureRequest.query \
                            .filter(FeatureRequest.priority > current_priority, FeatureRequest.priority <= form.priority.data) \
                            .order_by(FeatureRequest.priority) \
                            .all()
                    else:
                        # big to small
                        priority_adjusted_value = 1
                        feature_requests = FeatureRequest.query \
                            .filter(FeatureRequest.priority < current_priority, FeatureRequest.priority >= form.priority.data) \
                            .order_by(FeatureRequest.priority.desc()) \
                            .all()

                    for item in feature_requests:
                        item.priority = item.priority + priority_adjusted_value
                        db.session.commit()

                    feature_request.priority = form.priority.data # set the final priority

            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'errors': form.errors})

    # GET method
    data_choices = {
        'clients': CLIENT_CHOICES,
        'product_areas': PRODUCT_AREA_CHOICES
    }
    return render_template('index.html', form=form, data_choices=data_choices)



@bp.route('/feature-requests/<client>', methods=['GET'])
def feature_requests(client):
            # .filter_by(client=client) \
            # .order_by(FeatureRequest.priority) \
    items = FeatureRequest.query \
            .all()
    return jsonify([item.to_dict() for item in items])
