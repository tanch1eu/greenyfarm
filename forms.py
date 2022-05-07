from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("Enter your first name", validators=[InputRequired()])
    surname = StringField("Enter your last name", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired(), email()])
    phone = StringField("Your phone number", validators=[InputRequired()])
    submit = SubmitField("Confirm order")

