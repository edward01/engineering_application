from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, AnyOf


class FeatureRequestForm(FlaskForm):
    id = IntegerField('id')
    priority = IntegerField('Priority', validators=[DataRequired()])
    # priority = StringField('Priority', validators=[DataRequired(),
    #             AnyOf(['highest', 'lowest'])])
    title = StringField('Title', validators=[Length(min=3, max=50)])
    description = TextAreaField('Description', validators=[Length(min=5)])
    target_date = DateField('Target Date', validators=[DataRequired()], format='%m/%d/%Y')
    client = StringField('Client', validators=[DataRequired(),
                AnyOf(['client_a', 'client_b', 'client_c'])])
    product_area = StringField('Product Area', validators=[DataRequired(),
                AnyOf(['billing', 'claims', 'policies', 'reports'])])

    # client = SelectField('Client', choices=[
    #                         ('client_a', 'Client A'),
    #                         ('client_b', 'Client B'),
    #                         ('client_c', 'Client C')
    #                     ], validators=[DataRequired()])
    # product_area = SelectField('Product Area', choices=[
    #                                 ('billing', 'Billing'),
    #                                 ('claims', 'Claims'),
    #                                 ('policies', 'Policies'),
    #                                 ('reports', 'Reports'),
    #                             ], validators=[DataRequired()])

    # def __init__(self, original_username, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.original_username = original_username

    # def validate_username(self, username):
    #     if username.data != self.original_username:
    #         user = User.query.filter_by(username=self.username.data).first()
    #         if user is not None:
    #             raise ValidationError(_('Please use a different username.'))
