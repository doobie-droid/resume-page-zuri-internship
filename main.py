# this is the main server file for an interactive resume page that contains a form
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_USERNAME'] = os.environ.get("gmail_address")
app.config['MAIL_PASSWORD'] = os.environ.get("gmail_password")
receiver_address = "lesliedouglas23@gmail.com"
app.config['MAIL_USE_TLS'] = False
app.config['SECRET_KEY'] = os.environ.get("secret_key")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
Bootstrap(app)


class ContactMe(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired()])
    body = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Contact Me")


@app.route('/', methods=['POST', 'GET'])
def home():
    form = ContactMe()
    if form.validate_on_submit():
        name1, email_address1, body1 = form.name.data, form.email_address.data, form.body.data
        subject = name1 + email_address1
        try:
            msg = Message(subject, sender=os.environ.get("gmail_address"), recipients=[receiver_address])
            msg.body = body1
            mail.send(msg)
        except:
            #this project was supposed to show that I could capture data in a form and TaDa! this is sufficient
            title = "Thank you for Reaching out"
            subtitle = 'Doobie will be in touch with you soon'
            return render_template('index.html', form=form, title=title, subtitle=subtitle)
        title = 'Message Delivered'
        subtitle = 'Thank you for reaching out'
        return render_template('index.html', form=form, title=title, subtitle=subtitle)
    else:
        if request.method == 'POST':
            title = "Sorry about this"
            subtitle = 'Your message could not be delivered'
        else:
            title = "Online Resume"
            subtitle = 'Curated by Doobie'
        return render_template('index.html', form=form, title=title, subtitle=subtitle)


if __name__ == "__main__":
    app.run()
