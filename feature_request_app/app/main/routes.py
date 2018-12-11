from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from app.models import FeatureRequest
from app.main.forms import AddUpdateForm


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
    form = AddUpdateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.id.data < 1:
                # Insert Mode
                update_priority = True
                FeatureRequest.adjust_priorities(form.client.data, form.priority.data, 1)
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
                    feature_request.set_priority(form.priority.data)

            db.session.commit()
            return jsonify({'success': True, 'update_priority': update_priority})
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
    items = FeatureRequest.query \
            .filter_by(client=client) \
            .order_by(FeatureRequest.priority) \
            .all()
    return jsonify([item.to_dict() for item in items])


@bp.route('/update-priority', methods=['POST'])
def update_priority():
    client = request.form.get('client')
    priority = int(request.form.get('current_priority'))
    new_priority = int(request.form.get('new_priority'))
    feature_request = FeatureRequest.query.filter_by(client=client, priority=priority).first()
    feature_request.set_priority(new_priority)
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    feature_request = FeatureRequest.query.get(id)
    client = feature_request.client
    priority = feature_request.priority
    db.session.delete(feature_request)
    FeatureRequest.adjust_priorities(client, priority, -1)
    db.session.commit()
    return jsonify({'success': True})


# TODO
# ------------- bug: when adding multiple entries, then try to click one of the created, multiple rows were opened
# ------------- add csrf checking on delete endpoint